"""GraphBuilder — compiles validated config + registry into a LangGraph CompiledStateGraph."""

from __future__ import annotations

import functools
import importlib
import inspect
import warnings
from pathlib import Path
from typing import Callable

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from langgraph_declarative.errors import ConfigValidationError, ToolNotFoundError
from langgraph_declarative.llm_factory import create_llm, merge_llm_config
from langgraph_declarative.loader import load_yaml
from langgraph_declarative.registry import Registry
from langgraph_declarative.schema import (
    EdgeConfig,
    GraphConfig,
    LLMConfig,
    NodeConfig,
    cross_validate,
    validate_config,
)
from langgraph_declarative.state_factory import build_state_class


# Sentinel mapping: YAML string → LangGraph constant
_SENTINELS = {"START": START, "END": END}

# Reserved key in match-routing targets used as fallback.
_MATCH_DEFAULT_KEY = "default"


def _default_state_class():
    """Import MessagesState lazily to avoid hard failure if langgraph version varies."""
    from langgraph.graph import MessagesState
    return MessagesState


class GraphBuilder:
    """Build and compile a ``StateGraph`` from a validated ``GraphConfig``.

    Args:
        registry: The node/router registry to resolve function references against.
        state_class: The state annotation for the graph. Defaults to
            ``MessagesState``. Ignored (with a warning) when the YAML declares
            its own ``state:`` section.
    """

    def __init__(self, registry: Registry, state_class: type | None = None) -> None:
        self.registry = registry
        self._explicit_state = state_class is not None
        self.state_class = state_class or _default_state_class()

    # -- public API --

    def build(self, config: GraphConfig) -> CompiledStateGraph:
        """Build and compile a StateGraph from a validated config."""
        return self._build(config, base_dir=Path.cwd(), visiting=())

    def build_from_file(self, path: str | Path) -> CompiledStateGraph:
        """Load YAML, validate, cross-validate, and build. Full pipeline."""
        return self._build_from_file(Path(path), visiting=())

    def draw_mermaid(
        self, config: GraphConfig, output_path: str | Path | None = None
    ) -> str:
        """Compile the config and return its Mermaid diagram source.

        Args:
            config: A validated graph configuration.
            output_path: If given, also write the diagram to this file
                (``.md`` gets a fenced code block, anything else raw Mermaid).
        """
        compiled = self.build(config)
        return _render_mermaid(compiled, output_path)

    # -- pipeline internals --

    def _build_from_file(
        self, path: Path, visiting: tuple[Path, ...]
    ) -> CompiledStateGraph:
        resolved = path.resolve()
        if resolved in visiting:
            chain = " -> ".join(p.name for p in (*visiting, resolved))
            raise ConfigValidationError(f"Circular subgraph reference: {chain}")
        raw = load_yaml(resolved)
        config = validate_config(raw)
        return self._build(config, resolved.parent, (*visiting, resolved))

    def _build(
        self, config: GraphConfig, base_dir: Path, visiting: tuple[Path, ...]
    ) -> CompiledStateGraph:
        config = _resolve_imports(config, base_dir)
        cross_validate(config, self.registry)

        graph = StateGraph(self._resolve_state_class(config))
        self._add_nodes(graph, config, base_dir, visiting)
        self._add_edges(graph, config.edges)
        return graph.compile()

    def _resolve_state_class(self, config: GraphConfig) -> type:
        """YAML ``state:`` wins over the constructor's state_class (with warning)."""
        if config.state is None:
            return self.state_class
        if self._explicit_state:
            warnings.warn(
                "YAML 'state:' section overrides the state_class parameter "
                "passed to GraphBuilder — the parameter is ignored.",
                UserWarning,
                stacklevel=4,
            )
        return build_state_class(config.state)

    # -- nodes --

    def _add_nodes(
        self,
        graph: StateGraph,
        config: GraphConfig,
        base_dir: Path,
        visiting: tuple[Path, ...],
    ) -> None:
        """Register all node functions (or compiled subgraphs) on the graph."""
        for node in config.nodes:
            if node.subgraph is not None:
                compiled = self._build_from_file(base_dir / node.subgraph, visiting)
                graph.add_node(node.name, compiled)
            else:
                fn = self.registry.get_node(node.function)
                fn = self._wire_llm_and_tools(fn, node, config.llm)
                graph.add_node(node.name, fn)

    def _wire_llm_and_tools(
        self, fn: Callable, node: NodeConfig, graph_llm: LLMConfig | None
    ) -> Callable:
        """Inject a configured LLM (with tools bound) into functions that opt in.

        Opt-in contract: the node function accepts an ``llm`` keyword parameter.
        A graph-level default is applied silently only to opting-in functions;
        a node-level ``llm:`` or ``tools:`` on a non-opting function is an error.
        """
        effective = merge_llm_config(graph_llm, node.llm)
        accepts_llm = "llm" in inspect.signature(fn).parameters

        if node.tools and effective is None:
            raise ConfigValidationError(
                f"Node '{node.name}' declares 'tools' but has no llm config "
                "(node-level or graph-level) to bind them to."
            )
        if not accepts_llm:
            if node.llm is not None or node.tools:
                raise ConfigValidationError(
                    f"Node '{node.name}' has llm/tools config but function "
                    f"'{node.function}' does not accept an 'llm' parameter. "
                    "Add 'llm=None' to the function signature to opt in."
                )
            return fn
        if effective is None:
            return fn

        llm = create_llm(effective)
        if node.tools:
            tools = [self._resolve_tool(name) for name in node.tools]
            llm = llm.bind_tools(tools)
        return functools.partial(fn, llm=llm)

    def _resolve_tool(self, name: str):
        """Resolve a tool by registry name or ``module.path:attr`` import path."""
        if ":" in name:
            module_name, attr = name.split(":", 1)
            try:
                module = importlib.import_module(module_name)
            except ImportError as exc:
                raise ToolNotFoundError(
                    f"Cannot import tool module '{module_name}': {exc}"
                ) from None
            try:
                return getattr(module, attr)
            except AttributeError:
                raise ToolNotFoundError(
                    f"Module '{module_name}' has no attribute '{attr}'"
                ) from None
        return self.registry.get_tool(name)

    # -- edges --

    def _add_edges(self, graph: StateGraph, edges: list[EdgeConfig]) -> None:
        """Wire all edges on the graph."""
        for edge in edges:
            source = self._resolve_sentinel(edge.source)

            if edge.match is not None:
                # Match routing: synthetic router from state-field lookup
                path_map = {
                    k: self._resolve_sentinel(v) for k, v in edge.targets.items()
                }
                router = _make_match_router(edge.match, set(edge.targets.keys()))
                graph.add_conditional_edges(source, router, path_map)
            elif edge.path is not None:
                # Conditional edge (mapped or dynamic)
                router_fn = self.registry.get_router(edge.path)
                if edge.targets is not None:
                    # Mapped routing: path_map provided
                    path_map = {
                        k: self._resolve_sentinel(v)
                        for k, v in edge.targets.items()
                    }
                    wrapped = self._wrap_mapped_router(
                        router_fn, edge.path, set(edge.targets.keys())
                    )
                    graph.add_conditional_edges(source, wrapped, path_map)
                else:
                    # Dynamic routing (Send): no path_map
                    graph.add_conditional_edges(source, router_fn)
            elif isinstance(edge.target, list):
                # Fan-out: multiple targets
                for t in edge.target:
                    graph.add_edge(source, self._resolve_sentinel(t))
            else:
                # Simple edge
                graph.add_edge(source, self._resolve_sentinel(edge.target))

    def _wrap_mapped_router(
        self, router_fn: Callable, router_name: str, allowed_keys: set[str]
    ) -> Callable:
        """Wrap a router function to validate its return value against allowed keys."""
        def _validated_router(state):
            result = router_fn(state)
            if not isinstance(result, str):
                raise ConfigValidationError(
                    f"Router '{router_name}' returned {type(result).__name__}, "
                    f"expected str. Mapped routing requires a string key."
                )
            if result not in allowed_keys:
                sorted_keys = ", ".join(f"'{k}'" for k in sorted(allowed_keys))
                raise ConfigValidationError(
                    f"Router '{router_name}' returned unmapped key '{result}'. "
                    f"Allowed keys: {sorted_keys}."
                )
            return result
        return _validated_router

    def _resolve_sentinel(self, name: str) -> str:
        """Map "START"/"END" strings to LangGraph constants, pass others through."""
        return _SENTINELS.get(name, name)


# -- match routing (module-level: no builder state needed) --


def _make_match_router(field: str, allowed_keys: set[str]) -> Callable:
    """Create a router that reads ``state.<field>`` and returns it as a route key.

    No ``eval()`` — pure dict/attribute access. Supports one level of
    dot-notation nesting (``result.status``). Falls back to the ``default``
    target key when the value has no explicit mapping.
    """
    parts = field.split(".")

    def _match_router(state):
        value = state
        for part in parts:
            if isinstance(value, dict):
                if part not in value:
                    raise ConfigValidationError(
                        f"match: state has no field '{part}' "
                        f"(while resolving '{field}')"
                    )
                value = value[part]
            else:
                if not hasattr(value, part):
                    raise ConfigValidationError(
                        f"match: state has no field '{part}' "
                        f"(while resolving '{field}')"
                    )
                value = getattr(value, part)

        key = value if isinstance(value, str) else str(value)
        if key in allowed_keys:
            return key
        if _MATCH_DEFAULT_KEY in allowed_keys:
            return _MATCH_DEFAULT_KEY
        sorted_keys = ", ".join(f"'{k}'" for k in sorted(allowed_keys))
        raise ConfigValidationError(
            f"match: value '{key}' from state field '{field}' not found in "
            f"targets and no 'default' key provided. Allowed keys: {sorted_keys}."
        )

    return _match_router


# -- cross-file imports (task-023) --


def _resolve_imports(
    config: GraphConfig, base_dir: Path, chain: tuple[Path, ...] = ()
) -> GraphConfig:
    """Merge node definitions from imported YAML files into *config*.

    Imports are resolved recursively (imported files may import too), relative
    to the importing file. Circular imports and name collisions raise
    ``ConfigValidationError``.
    """
    if not config.imports:
        return config

    merged_nodes = list(config.nodes)
    existing = {n.name for n in merged_nodes}

    for imp in config.imports:
        resolved = (base_dir / imp.file).resolve()
        if resolved in chain:
            cycle = " -> ".join(p.name for p in (*chain, resolved))
            raise ConfigValidationError(f"Circular import: {cycle}")

        raw = load_yaml(resolved)
        imported = validate_config(raw)
        imported = _resolve_imports(imported, resolved.parent, (*chain, resolved))

        available = {n.name: n for n in imported.nodes}
        wanted = imp.nodes if imp.nodes is not None else list(available)
        for name in wanted:
            if name not in available:
                from langgraph_declarative.errors import format_not_found

                raise ConfigValidationError(
                    f"Import from '{imp.file}': "
                    + format_not_found("node", name, list(available))
                )
            if name in existing:
                raise ConfigValidationError(
                    f"Import from '{imp.file}': node name '{name}' collides "
                    "with an existing node"
                )
            merged_nodes.append(available[name])
            existing.add(name)

    return config.model_copy(update={"nodes": merged_nodes, "imports": None})


# -- mermaid rendering (task-015) --


def _render_mermaid(
    compiled: CompiledStateGraph, output_path: str | Path | None
) -> str:
    """Extract Mermaid source from a compiled graph, optionally writing a file."""
    mermaid = compiled.get_graph().draw_mermaid()
    if output_path is not None:
        path = Path(output_path)
        if path.suffix == ".md":
            path.write_text(f"```mermaid\n{mermaid}\n```\n", encoding="utf-8")
        else:
            path.write_text(mermaid, encoding="utf-8")
    return mermaid
