"""langgraph-declarative: YAML-defined LangGraph workflows."""

from __future__ import annotations

from pathlib import Path

from langgraph.graph.state import CompiledStateGraph

from langgraph_declarative.builder import GraphBuilder
from langgraph_declarative.registry import Registry


def build_graph(
    path: str | Path,
    registry: Registry,
    state_class: type | None = None,
) -> CompiledStateGraph:
    """One-line graph compilation from a YAML file + registry.

    Args:
        path: Path to the YAML workflow definition.
        registry: Registry containing the node/router functions.
        state_class: State annotation for the graph. Defaults to ``MessagesState``.

    Returns:
        A compiled LangGraph ``CompiledStateGraph`` ready for ``.invoke()``.
    """
    builder = GraphBuilder(registry=registry, state_class=state_class)
    return builder.build_from_file(path)


__all__ = ["Registry", "GraphBuilder", "build_graph"]
