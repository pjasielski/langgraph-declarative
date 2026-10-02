"""Pydantic models for YAML config validation and cross-reference checking."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError, model_validator

from langgraph_declarative._base import StrictModel
from langgraph_declarative.errors import (
    ConfigValidationError,
    NodeNotFoundError,
    RouterNotFoundError,
    format_not_found,
    suggest_similar,
)
from langgraph_declarative.state_factory import StateFieldConfig

# Sentinel names that are always valid in edge source/target fields.
_SENTINELS = {"START", "END"}


class LLMConfig(StrictModel):
    """LLM parameters, usable at graph level (default) or per node (override)."""

    provider: str | None = None
    model: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None


class NodeConfig(StrictModel):
    """A single node declaration.

    Exactly one of ``function`` (registered function reference) or
    ``subgraph`` (path to another YAML workflow file) must be provided.
    """

    name: str
    description: str | None = None
    function: str | None = None
    subgraph: str | None = None
    llm: LLMConfig | None = None
    tools: list[str] | None = None
    destinations: list[str] | None = None

    @model_validator(mode="after")
    def _validate_node_fields(self) -> "NodeConfig":
        if self.function is None and self.subgraph is None:
            raise ValueError(
                f"Node '{self.name}' has neither 'function' nor 'subgraph'"
            )
        if self.function is not None and self.subgraph is not None:
            raise ValueError(
                f"Node '{self.name}' has both 'function' and 'subgraph' "
                "-- use one or the other"
            )
        if self.subgraph is not None and (self.llm or self.tools):
            raise ValueError(
                f"Node '{self.name}' is a subgraph and cannot have 'llm' or "
                "'tools' -- configure them inside the subgraph file"
            )
        return self


class EdgeConfig(StrictModel):
    """A single edge declaration with validation rules.

    Exactly one of ``target``, ``path``, or ``match`` must be provided.
    ``targets`` (the path_map) is required with ``match`` and optional
    with ``path``.
    """

    source: str
    description: str | None = None
    target: str | list[str] | None = None
    path: str | None = None
    match: str | None = None
    targets: dict[str, str] | None = None

    @model_validator(mode="after")
    def _validate_edge_fields(self) -> "EdgeConfig":
        provided = [
            name
            for name, value in (
                ("target", self.target),
                ("path", self.path),
                ("match", self.match),
            )
            if value is not None
        ]
        if len(provided) == 0:
            raise ValueError(
                f"Edge from '{self.source}' has none of 'target', 'path', "
                "or 'match'"
            )
        if len(provided) > 1:
            joined = " and ".join(f"'{p}'" for p in provided)
            raise ValueError(
                f"Edge from '{self.source}' has {joined} -- they are "
                "mutually exclusive"
            )
        if self.targets is not None and self.path is None and self.match is None:
            raise ValueError(
                f"Edge from '{self.source}' has 'targets' without 'path' or 'match'"
            )
        if self.match is not None and self.targets is None:
            raise ValueError(
                f"Edge from '{self.source}' has 'match' without 'targets' — "
                "match routing requires a targets map"
            )
        if self.targets is not None and len(self.targets) == 0:
            raise ValueError(
                f"Edge from '{self.source}' has empty 'targets' map — "
                "provide at least one routing key"
            )
        return self


class ImportConfig(StrictModel):
    """A cross-file import: pull node definitions from another YAML file."""

    file: str
    nodes: list[str] | None = None  # None = import all nodes from the file


class GraphConfig(StrictModel):
    """Top-level validated graph configuration."""

    description: str | None = None
    nodes: list[NodeConfig]
    edges: list[EdgeConfig] = []
    state: list[StateFieldConfig] | None = None
    llm: LLMConfig | None = None
    imports: list[ImportConfig] | None = None
    interrupt_before: list[str] | None = None
    interrupt_after: list[str] | None = None

    @model_validator(mode="after")
    def _validate_unique_names(self) -> "GraphConfig":
        seen: set[str] = set()
        for node in self.nodes:
            if node.name in seen:
                raise ValueError(f"Duplicate node name: '{node.name}'")
            seen.add(node.name)
        if self.state is not None:
            seen_fields: set[str] = set()
            for field in self.state:
                if field.name in seen_fields:
                    raise ValueError(f"Duplicate state field name: '{field.name}'")
                seen_fields.add(field.name)
        return self


def validate_config(raw: dict) -> GraphConfig:
    """Parse a raw dict into a validated ``GraphConfig``.

    Raises ``ConfigValidationError`` on any structural problem. Unknown keys
    are reported by name and location, with a closest-match suggestion.
    """
    try:
        return GraphConfig.model_validate(raw)
    except ValidationError as exc:
        raise ConfigValidationError(_format_validation_error(exc, raw)) from exc
    except Exception as exc:
        raise ConfigValidationError(str(exc)) from exc


# Which model owns the keys at a location (list indices stripped from the path).
_MODEL_AT: dict[tuple[str, ...], type[StrictModel]] = {
    (): GraphConfig,
    ("nodes",): NodeConfig,
    ("nodes", "llm"): LLMConfig,
    ("edges",): EdgeConfig,
    ("state",): StateFieldConfig,
    ("llm",): LLMConfig,
    ("imports",): ImportConfig,
}


def _format_validation_error(exc: ValidationError, raw: object) -> str:
    """Render unknown-key errors readably; keep Pydantic's text for the rest."""
    errors = exc.errors()
    unknown = [e for e in errors if e["type"] == "extra_forbidden"]
    if not unknown:
        return str(exc)

    lines = []
    for err in unknown:
        *parent, key = err["loc"]
        model = _MODEL_AT.get(tuple(p for p in parent if isinstance(p, str)))
        line = f"Unknown key '{key}' at {_describe_location(parent, raw)}."
        if model is not None:
            allowed = list(model.model_fields)
            suggestions = suggest_similar(str(key), allowed, n=1)
            if suggestions:
                line += f" Did you mean '{suggestions[0]}'?"
            else:
                line += f" Allowed keys: {', '.join(allowed)}."
        lines.append(line)

    for err in errors:
        if err["type"] != "extra_forbidden":
            where = _describe_location(list(err["loc"]), raw)
            lines.append(f"{where}: {err['msg']}")
    return "\n".join(lines)


def _describe_location(loc: list, raw: object) -> str:
    """``['nodes', 2]`` → ``nodes[2] (node 'approval')``; ``[]`` → ``top level``."""
    if not loc:
        return "top level"
    text = ""
    node = raw
    for part in loc:
        text += f"[{part}]" if isinstance(part, int) else (
            f".{part}" if text else str(part)
        )
        try:
            node = node[part]  # type: ignore[index]
        except (KeyError, IndexError, TypeError):
            node = None
    if isinstance(node, dict) and isinstance(node.get("name"), str):
        text += f" ('{node['name']}')"
    elif isinstance(node, dict) and isinstance(node.get("source"), str):
        text += f" (edge from '{node['source']}')"
    return text


def export_json_schema(output_path: str | Path | None = None) -> dict:
    """Return the JSON Schema for workflow YAML files (derived from GraphConfig).

    IDEs can use it via a modeline comment in the YAML file:
    ``# yaml-language-server: $schema=path/to/workflow.schema.json``

    Args:
        output_path: If given, also write the schema as JSON to this path.
    """
    schema = GraphConfig.model_json_schema()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["title"] = "langgraph-declarative workflow"
    if output_path is not None:
        Path(output_path).write_text(
            json.dumps(schema, indent=2) + "\n", encoding="utf-8"
        )
    return schema


def cross_validate(config: GraphConfig, registry: "Registry") -> None:  # noqa: F821
    """Check that all function/path refs exist in the registry and that
    edge sources/targets reference defined nodes or START/END.

    Raises ``NodeNotFoundError`` or ``RouterNotFoundError`` with suggestions.
    """
    from langgraph_declarative.registry import Registry  # deferred to avoid circular

    node_names = {n.name for n in config.nodes}
    valid_names = node_names | _SENTINELS

    # Check node function references (subgraph nodes resolve to files, not registry)
    for node in config.nodes:
        if node.function is None:
            continue
        try:
            registry.get_node(node.function)
        except NodeNotFoundError:
            raise NodeNotFoundError(
                format_not_found("node", node.function, registry.list_nodes())
            ) from None

    # Check router (path) references
    for edge in config.edges:
        if edge.path is not None:
            try:
                registry.get_router(edge.path)
            except RouterNotFoundError:
                raise RouterNotFoundError(
                    format_not_found("router", edge.path, registry.list_routers())
                ) from None

    # Check edge source/target references against defined nodes
    for edge in config.edges:
        if edge.source not in valid_names:
            raise ConfigValidationError(
                format_not_found("node", edge.source, sorted(node_names))
            )

        if isinstance(edge.target, list):
            for t in edge.target:
                if t not in valid_names:
                    raise ConfigValidationError(
                        format_not_found("node", t, sorted(node_names))
                    )
        elif edge.target is not None and edge.target not in valid_names:
            raise ConfigValidationError(
                format_not_found("node", edge.target, sorted(node_names))
            )

        if edge.targets is not None:
            for t in edge.targets.values():
                if t not in valid_names:
                    raise ConfigValidationError(
                        format_not_found("node", t, sorted(node_names))
                    )

    # Check Command(goto=...) destinations reference defined nodes or END
    for node in config.nodes:
        if not node.destinations:
            continue
        for dest in node.destinations:
            if dest not in valid_names:
                raise ConfigValidationError(
                    f"Node '{node.name}' destination: "
                    + format_not_found("node", dest, sorted(node_names))
                )

    # Check static interrupt points reference defined nodes.
    # These are top-level compile() arguments, so a node inside a subgraph file
    # is not addressable here — validation stays scoped to this file's nodes.
    for field_name in ("interrupt_before", "interrupt_after"):
        for name in getattr(config, field_name) or []:
            if name not in node_names:
                raise ConfigValidationError(
                    f"{field_name}: " + format_not_found(
                        "node", name, sorted(node_names)
                    )
                )
