"""Tests for subgraph composition (task-018)."""

from __future__ import annotations

from pathlib import Path

import pytest
from langgraph.graph.state import CompiledStateGraph

from langgraph_declarative import Registry, build_graph
from langgraph_declarative.errors import ConfigValidationError

FIXTURES = Path(__file__).parent / "fixtures"


def _registry() -> Registry:
    reg = Registry()

    @reg.node("intro_fn")
    def intro_fn(state):
        return {"messages": [{"role": "assistant", "content": "intro"}]}

    @reg.node("child_step_fn")
    def child_step_fn(state):
        return {"messages": [{"role": "assistant", "content": "child"}]}

    @reg.node("outro_fn")
    def outro_fn(state):
        return {"messages": [{"role": "assistant", "content": "outro"}]}

    return reg


class TestBasicSubgraph:
    def test_parent_with_subgraph_builds(self):
        graph = build_graph(FIXTURES / "subgraph_parent.yaml", _registry())
        assert isinstance(graph, CompiledStateGraph)
        assert "child" in graph.nodes

    def test_subgraph_executes_in_parent_flow(self):
        graph = build_graph(FIXTURES / "subgraph_parent.yaml", _registry())
        result = graph.invoke({"messages": []})
        contents = [m.content for m in result["messages"]]
        assert contents == ["intro", "child", "outro"]

    def test_child_declares_own_state(self):
        """subgraph_child.yaml has its own state: section (v1.1 feature)."""
        reg = Registry()

        @reg.node("child_step_fn")
        def child_step_fn(state):
            return {"messages": [{"role": "assistant", "content": "solo-child"}]}

        graph = build_graph(FIXTURES / "subgraph_child.yaml", reg)
        result = graph.invoke({"messages": []})
        assert result["messages"][-1].content == "solo-child"


class TestNestedSubgraphs:
    def test_two_levels(self, tmp_path):
        (tmp_path / "level2.yaml").write_text(
            "nodes:\n"
            "  - name: deep\n"
            "    function: deep_fn\n"
            "edges:\n"
            "  - {source: START, target: deep}\n"
            "  - {source: deep, target: END}\n",
            encoding="utf-8",
        )
        (tmp_path / "level1.yaml").write_text(
            "nodes:\n"
            "  - name: mid\n"
            "    subgraph: level2.yaml\n"
            "edges:\n"
            "  - {source: START, target: mid}\n"
            "  - {source: mid, target: END}\n",
            encoding="utf-8",
        )
        (tmp_path / "root.yaml").write_text(
            "nodes:\n"
            "  - name: top\n"
            "    subgraph: level1.yaml\n"
            "edges:\n"
            "  - {source: START, target: top}\n"
            "  - {source: top, target: END}\n",
            encoding="utf-8",
        )
        reg = Registry()

        @reg.node("deep_fn")
        def deep_fn(state):
            return {"messages": [{"role": "assistant", "content": "deep"}]}

        graph = build_graph(tmp_path / "root.yaml", reg)
        result = graph.invoke({"messages": []})
        assert result["messages"][-1].content == "deep"


class TestCircularDetection:
    def test_self_reference_rejected(self, tmp_path):
        (tmp_path / "loop.yaml").write_text(
            "nodes:\n"
            "  - name: me\n"
            "    subgraph: loop.yaml\n"
            "edges:\n"
            "  - {source: START, target: me}\n"
            "  - {source: me, target: END}\n",
            encoding="utf-8",
        )
        with pytest.raises(ConfigValidationError, match="Circular subgraph"):
            build_graph(tmp_path / "loop.yaml", Registry())

    def test_mutual_reference_rejected(self, tmp_path):
        for a, b in (("a", "b"), ("b", "a")):
            (tmp_path / f"{a}.yaml").write_text(
                f"nodes:\n"
                f"  - name: jump\n"
                f"    subgraph: {b}.yaml\n"
                f"edges:\n"
                f"  - {{source: START, target: jump}}\n"
                f"  - {{source: jump, target: END}}\n",
                encoding="utf-8",
            )
        with pytest.raises(ConfigValidationError, match="Circular subgraph"):
            build_graph(tmp_path / "a.yaml", Registry())


class TestSubgraphSchema:
    def test_function_and_subgraph_mutually_exclusive(self):
        from langgraph_declarative.schema import validate_config

        raw = {
            "nodes": [{"name": "x", "function": "f", "subgraph": "y.yaml"}],
            "edges": [{"source": "START", "target": "x"}],
        }
        with pytest.raises(ConfigValidationError, match="both 'function' and 'subgraph'"):
            validate_config(raw)
