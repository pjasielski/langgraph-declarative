"""langgraph-declarative: YAML-defined LangGraph workflows."""

from __future__ import annotations

from pathlib import Path

from langgraph.graph.state import CompiledStateGraph

from langgraph_declarative.builder import GraphBuilder
from langgraph_declarative.loader import Loader, YamlLoader
from langgraph_declarative.loaders import SQLiteLoader, build_graph_from_db
from langgraph_declarative.registry import Registry
from langgraph_declarative.schema import export_json_schema


def build_graph(
    path: str | Path,
    registry: Registry,
    state_class: type | None = None,
) -> CompiledStateGraph:
    """One-line graph compilation from a YAML file + registry.

    Args:
        path: Path to the YAML workflow definition.
        registry: Registry containing the node/router functions.
        state_class: State annotation for the graph. Defaults to
            ``MessagesState``. Ignored when the YAML declares ``state:``.

    Returns:
        A compiled LangGraph ``CompiledStateGraph`` ready for ``.invoke()``.
    """
    builder = GraphBuilder(registry=registry, state_class=state_class)
    return builder.build_from_file(path)


def draw_mermaid(
    path: str | Path,
    registry: Registry,
    state_class: type | None = None,
    output_path: str | Path | None = None,
) -> str:
    """Compile a YAML workflow and return its Mermaid diagram source.

    Args:
        path: Path to the YAML workflow definition.
        registry: Registry containing the node/router functions.
        state_class: State annotation for the graph (optional).
        output_path: If given, also write the diagram to this file
            (``.md`` gets a fenced code block, anything else raw Mermaid).
    """
    from langgraph_declarative.builder import _render_mermaid

    compiled = build_graph(path, registry, state_class=state_class)
    return _render_mermaid(compiled, output_path)


__all__ = [
    "Registry",
    "GraphBuilder",
    "Loader",
    "YamlLoader",
    "SQLiteLoader",
    "build_graph",
    "build_graph_from_db",
    "draw_mermaid",
    "export_json_schema",
]
