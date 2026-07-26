"""Tests for the database-driven graph source (task-021)."""

from __future__ import annotations

import pytest
from langgraph.graph.state import CompiledStateGraph

from langgraph_declarative import (
    Loader,
    Registry,
    SQLiteLoader,
    YamlLoader,
    build_graph_from_db,
)
from langgraph_declarative.errors import ConfigLoadError

SIMPLE_DEF = {
    "nodes": [{"name": "greeter", "function": "greet"}],
    "edges": [
        {"source": "START", "target": "greeter"},
        {"source": "greeter", "target": "END"},
    ],
}


def _registry() -> Registry:
    reg = Registry()

    @reg.node("greet")
    def greet(state):
        return {"messages": [{"role": "assistant", "content": "hello-from-db"}]}

    return reg


class TestLoaderProtocol:
    def test_implementations_satisfy_protocol(self, tmp_path):
        assert isinstance(YamlLoader(), Loader)
        assert isinstance(SQLiteLoader(tmp_path / "g.db"), Loader)


class TestSQLiteLoader:
    def test_save_and_load_roundtrip(self, tmp_path):
        loader = SQLiteLoader(tmp_path / "g.db")
        loader.save("flow", SIMPLE_DEF)
        assert loader.load("flow") == SIMPLE_DEF

    def test_load_accepts_raw_yaml_text(self, tmp_path):
        loader = SQLiteLoader(tmp_path / "g.db")
        loader.save("flow", "nodes:\n  - {name: a, function: f}\nedges: []\n")
        assert loader.load("flow")["nodes"][0]["name"] == "a"

    def test_missing_source_error(self, tmp_path):
        loader = SQLiteLoader(tmp_path / "g.db")
        with pytest.raises(ConfigLoadError, match="'nope' not found"):
            loader.load("nope")

    def test_version_tracking(self, tmp_path):
        loader = SQLiteLoader(tmp_path / "g.db")
        v1 = dict(SIMPLE_DEF)
        v2 = {**SIMPLE_DEF, "llm": {"provider": "openai", "model": "gpt-4o"}}
        assert loader.save("flow", v1) == 1
        assert loader.save("flow", v2) == 2
        assert loader.versions("flow") == [1, 2]
        assert loader.load("flow") == v2          # latest by default
        assert loader.load("flow@1") == v1        # explicit version

    def test_missing_version_error(self, tmp_path):
        loader = SQLiteLoader(tmp_path / "g.db")
        loader.save("flow", SIMPLE_DEF)
        with pytest.raises(ConfigLoadError, match="'flow@9' not found"):
            loader.load("flow@9")

    def test_invalid_version_error(self, tmp_path):
        loader = SQLiteLoader(tmp_path / "g.db")
        with pytest.raises(ConfigLoadError, match="Invalid version"):
            loader.load("flow@two")


class TestBuildGraphFromDb:
    def test_end_to_end(self, tmp_path):
        db = tmp_path / "g.db"
        SQLiteLoader(db).save("flow", SIMPLE_DEF)
        graph = build_graph_from_db("flow", _registry(), db)
        assert isinstance(graph, CompiledStateGraph)
        result = graph.invoke({"messages": []})
        assert result["messages"][-1].content == "hello-from-db"
