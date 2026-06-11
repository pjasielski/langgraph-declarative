"""Tests for cross-file node references (task-023)."""

from __future__ import annotations

from pathlib import Path

import pytest
from langgraph.graph.state import CompiledStateGraph

from langgraph_declarative import Registry, build_graph
from langgraph_declarative.errors import ConfigValidationError

FIXTURES = Path(__file__).parent / "fixtures"


def _registry() -> Registry:
    reg = Registry()

    @reg.node("process")
    def process(state):
        return {"messages": [{"role": "assistant", "content": "processed"}]}

    @reg.node("handle_error")
    def handle_error(state):
        return {"messages": [{"role": "assistant", "content": "handled"}]}

    @reg.node("retry_fn")
    def retry_fn(state):
        return {"messages": [{"role": "assistant", "content": "retried"}]}

    return reg


class TestBasicImport:
    def test_imported_node_usable_in_edges(self):
        graph = build_graph(FIXTURES / "importing_workflow.yaml", _registry())
        assert isinstance(graph, CompiledStateGraph)
        assert "error_handler" in graph.nodes

    def test_executes_through_imported_node(self):
        graph = build_graph(FIXTURES / "importing_workflow.yaml", _registry())
        result = graph.invoke({"messages": []})
        contents = [m.content for m in result["messages"]]
        assert contents == ["processed", "handled"]

    def test_unselected_nodes_not_imported(self):
        graph = build_graph(FIXTURES / "importing_workflow.yaml", _registry())
        assert "retry_node" not in graph.nodes


class TestMultiFileChain:
    def test_imports_resolve_recursively(self, tmp_path):
        (tmp_path / "base.yaml").write_text(
            "nodes:\n  - {name: base_node, function: process}\n",
            encoding="utf-8",
        )
        (tmp_path / "mid.yaml").write_text(
            "imports:\n"
            "  - file: base.yaml\n"
            "nodes:\n  - {name: mid_node, function: handle_error}\n",
            encoding="utf-8",
        )
        (tmp_path / "top.yaml").write_text(
            "imports:\n"
            "  - file: mid.yaml\n"
            "nodes:\n  - {name: top_node, function: retry_fn}\n"
            "edges:\n"
            "  - {source: START, target: top_node}\n"
            "  - {source: top_node, target: mid_node}\n"
            "  - {source: mid_node, target: base_node}\n"
            "  - {source: base_node, target: END}\n",
            encoding="utf-8",
        )
        graph = build_graph(tmp_path / "top.yaml", _registry())
        result = graph.invoke({"messages": []})
        contents = [m.content for m in result["messages"]]
        assert contents == ["retried", "handled", "processed"]


class TestImportErrors:
    def test_circular_import_rejected(self, tmp_path):
        for a, b in (("x", "y"), ("y", "x")):
            (tmp_path / f"{a}.yaml").write_text(
                f"imports:\n"
                f"  - file: {b}.yaml\n"
                f"nodes:\n  - {{name: {a}_node, function: process}}\n"
                f"edges:\n"
                f"  - {{source: START, target: {a}_node}}\n"
                f"  - {{source: {a}_node, target: END}}\n",
                encoding="utf-8",
            )
        with pytest.raises(ConfigValidationError, match="Circular import"):
            build_graph(tmp_path / "x.yaml", _registry())

    def test_name_collision_rejected(self, tmp_path):
        (tmp_path / "shared.yaml").write_text(
            "nodes:\n  - {name: my_node, function: process}\n",
            encoding="utf-8",
        )
        (tmp_path / "main.yaml").write_text(
            "imports:\n"
            "  - file: shared.yaml\n"
            "nodes:\n  - {name: my_node, function: process}\n"
            "edges:\n"
            "  - {source: START, target: my_node}\n"
            "  - {source: my_node, target: END}\n",
            encoding="utf-8",
        )
        with pytest.raises(ConfigValidationError, match="collides"):
            build_graph(tmp_path / "main.yaml", _registry())

    def test_unknown_imported_node_rejected(self, tmp_path):
        (tmp_path / "shared.yaml").write_text(
            "nodes:\n  - {name: real_node, function: process}\n",
            encoding="utf-8",
        )
        (tmp_path / "main.yaml").write_text(
            "imports:\n"
            "  - file: shared.yaml\n"
            "    nodes: [ghost_node]\n"
            "nodes:\n  - {name: my_node, function: process}\n"
            "edges:\n"
            "  - {source: START, target: my_node}\n"
            "  - {source: my_node, target: END}\n",
            encoding="utf-8",
        )
        with pytest.raises(ConfigValidationError, match="'ghost_node' not found"):
            build_graph(tmp_path / "main.yaml", _registry())
