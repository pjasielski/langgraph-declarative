"""Pydantic models for YAML config validation and cross-reference checking."""

from __future__ import annotations

from pydantic import BaseModel, model_validator

from langgraph_declarative.errors import (
    ConfigValidationError,
    NodeNotFoundError,
    RouterNotFoundError,
    format_not_found,
)

# Sentinel names that are always valid in edge source/target fields.
_SENTINELS = {"START", "END"}


class NodeConfig(BaseModel):
    """A single node declaration: name + registered function reference."""

    name: str
    function: str


class EdgeConfig(BaseModel):
    """A single edge declaration with validation rules.

    Exactly one of ``target`` or ``path`` must be provided.
    ``targets`` (the path_map) is only valid together with ``path``.
    """

    source: str
    target: str | list[str] | None = None
    path: str | None = None
    targets: dict[str, str] | None = None

    @model_validator(mode="after")
    def _validate_edge_fields(self) -> "EdgeConfig":
        has_target = self.target is not None
        has_path = self.path is not None

        if not has_target and not has_path:
            raise ValueError(
                f"Edge from '{self.source}' has neither 'target' nor 'path'"
            )
        if has_target and has_path:
            raise ValueError(
                f"Edge from '{self.source}' has both 'target' and 'path' "
                "-- use one or the other"
            )
        if self.targets is not None and not has_path:
            raise ValueError(
                f"Edge from '{self.source}' has 'targets' without 'path'"
            )
        return self


class GraphConfig(BaseModel):
    """Top-level validated graph configuration."""

    nodes: list[NodeConfig]
    edges: list[EdgeConfig]

    @model_validator(mode="after")
    def _validate_unique_node_names(self) -> "GraphConfig":
        seen: set[str] = set()
        for node in self.nodes:
            if node.name in seen:
                raise ValueError(f"Duplicate node name: '{node.name}'")
            seen.add(node.name)
        return self


def validate_config(raw: dict) -> GraphConfig:
    """Parse a raw dict into a validated ``GraphConfig``.

    Raises ``ConfigValidationError`` on any structural problem.
    """
    try:
        return GraphConfig.model_validate(raw)
    except Exception as exc:
        raise ConfigValidationError(str(exc)) from exc


def cross_validate(config: GraphConfig, registry: "Registry") -> None:  # noqa: F821
    """Check that all function/path refs exist in the registry and that
    edge sources/targets reference defined nodes or START/END.

    Raises ``NodeNotFoundError`` or ``RouterNotFoundError`` with suggestions.
    """
    from langgraph_declarative.registry import Registry  # deferred to avoid circular

    node_names = {n.name for n in config.nodes}
    valid_names = node_names | _SENTINELS

    # Check node function references
    for node in config.nodes:
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
