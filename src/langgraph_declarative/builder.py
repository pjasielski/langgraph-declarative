"""GraphBuilder — compiles validated config + registry into a LangGraph CompiledStateGraph."""

from __future__ import annotations

from pathlib import Path

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from langgraph_declarative.loader import load_yaml
from langgraph_declarative.registry import Registry
from langgraph_declarative.schema import EdgeConfig, GraphConfig, NodeConfig, cross_validate, validate_config


# Sentinel mapping: YAML string → LangGraph constant
_SENTINELS = {"START": START, "END": END}


def _default_state_class():
    """Import MessagesState lazily to avoid hard failure if langgraph version varies."""
    from langgraph.graph import MessagesState
    return MessagesState


class GraphBuilder:
    """Build and compile a ``StateGraph`` from a validated ``GraphConfig``.

    Args:
        registry: The node/router registry to resolve function references against.
        state_class: The state annotation for the graph. Defaults to ``MessagesState``.
    """

    def __init__(self, registry: Registry, state_class: type | None = None) -> None:
        self.registry = registry
        self.state_class = state_class or _default_state_class()

    def build(self, config: GraphConfig) -> CompiledStateGraph:
        """Build and compile a StateGraph from a validated config."""
        cross_validate(config, self.registry)

        graph = StateGraph(self.state_class)
        self._add_nodes(graph, config.nodes)
        self._add_edges(graph, config.edges)
        return graph.compile()

    def build_from_file(self, path: str | Path) -> CompiledStateGraph:
        """Load YAML, validate, cross-validate, and build. Full pipeline."""
        raw = load_yaml(path)
        config = validate_config(raw)
        return self.build(config)

    def _add_nodes(self, graph: StateGraph, nodes: list[NodeConfig]) -> None:
        """Register all node functions on the graph."""
        for node in nodes:
            fn = self.registry.get_node(node.function)
            graph.add_node(node.name, fn)

    def _add_edges(self, graph: StateGraph, edges: list[EdgeConfig]) -> None:
        """Wire all edges on the graph."""
        for edge in edges:
            source = self._resolve_sentinel(edge.source)

            if edge.path is not None:
                # Conditional edge (mapped or dynamic)
                router_fn = self.registry.get_router(edge.path)
                if edge.targets is not None:
                    # Mapped routing: path_map provided
                    path_map = {
                        k: self._resolve_sentinel(v)
                        for k, v in edge.targets.items()
                    }
                    graph.add_conditional_edges(source, router_fn, path_map)
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

    def _resolve_sentinel(self, name: str) -> str:
        """Map "START"/"END" strings to LangGraph constants, pass others through."""
        return _SENTINELS.get(name, name)
