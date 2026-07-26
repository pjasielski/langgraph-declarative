"""Tests for auto-Mermaid generation (task-015)."""

from __future__ import annotations

from pathlib import Path

from langgraph_declarative import GraphBuilder, Registry, draw_mermaid
from langgraph_declarative.schema import validate_config

FIXTURES = Path(__file__).parent / "fixtures"


def _registry() -> Registry:
    reg = Registry()

    @reg.node("greet")
    def greet(state):
        return {"messages": []}

    @reg.node("respond")
    def respond(state):
        return {"messages": []}

    return reg


class TestDrawMermaid:
    def test_returns_mermaid_with_node_names(self):
        mermaid = draw_mermaid(FIXTURES / "simple.yaml", _registry())
        assert "graph TD" in mermaid or "flowchart" in mermaid
        assert "greeter" in mermaid
        assert "responder" in mermaid

    def test_edge_structure_matches_yaml(self):
        mermaid = draw_mermaid(FIXTURES / "simple.yaml", _registry())
        # simple.yaml: START -> greeter -> responder -> END
        assert "greeter --> responder" in mermaid.replace("\t", "")

    def test_writes_raw_mmd_file(self, tmp_path):
        out = tmp_path / "graph.mmd"
        mermaid = draw_mermaid(FIXTURES / "simple.yaml", _registry(), output_path=out)
        assert out.read_text(encoding="utf-8") == mermaid

    def test_writes_fenced_md_file(self, tmp_path):
        out = tmp_path / "graph.md"
        mermaid = draw_mermaid(FIXTURES / "simple.yaml", _registry(), output_path=out)
        content = out.read_text(encoding="utf-8")
        assert content.startswith("```mermaid\n")
        assert mermaid in content
        assert content.rstrip().endswith("```")

    def test_builder_method(self):
        raw = {
            "nodes": [{"name": "solo", "function": "greet"}],
            "edges": [
                {"source": "START", "target": "solo"},
                {"source": "solo", "target": "END"},
            ],
        }
        builder = GraphBuilder(_registry())
        mermaid = builder.draw_mermaid(validate_config(raw))
        assert "solo" in mermaid
