"""Tests for tool configuration in YAML (task-019)."""

from __future__ import annotations

from pathlib import Path

import pytest

from langgraph_declarative import GraphBuilder, Registry, build_graph
from langgraph_declarative import llm_factory
from langgraph_declarative.errors import ConfigValidationError, ToolNotFoundError
from langgraph_declarative.schema import LLMConfig, validate_config

FIXTURES = Path(__file__).parent / "fixtures"


class FakeLLM:
    def __init__(self, config: LLMConfig):
        self.config = config
        self.tools = None

    def bind_tools(self, tools):
        bound = FakeLLM(self.config)
        bound.tools = list(tools)
        return bound


@pytest.fixture
def fake_provider(monkeypatch):
    monkeypatch.setitem(llm_factory._PROVIDERS, "fake", FakeLLM)


def _registry(captured: dict) -> Registry:
    reg = Registry()

    @reg.node("chat_node")
    def chat_node(state, llm=None):
        captured["llm"] = llm
        return {"messages": [{"role": "assistant", "content": "done"}]}

    @reg.tool("search_web")
    def search_web(query: str) -> str:
        """Search the web."""
        return "results"

    @reg.tool("calculator")
    def calculator(expression: str) -> str:
        """Evaluate math."""
        return "42"

    return reg


class TestToolBinding:
    def test_tools_bound_to_node_llm(self, fake_provider):
        captured: dict = {}
        reg = _registry(captured)
        graph = build_graph(FIXTURES / "tools_workflow.yaml", reg)
        graph.invoke({"messages": []})

        llm = captured["llm"]
        assert llm.tools is not None
        assert [t.__name__ for t in llm.tools] == ["search_web", "calculator"]

    def test_import_path_tool_resolution(self, fake_provider):
        captured: dict = {}
        reg = _registry(captured)
        raw = {
            "llm": {"provider": "fake", "model": "m"},
            "nodes": [
                {
                    "name": "agent",
                    "function": "chat_node",
                    "tools": ["json:dumps"],
                }
            ],
            "edges": [
                {"source": "START", "target": "agent"},
                {"source": "agent", "target": "END"},
            ],
        }
        graph = GraphBuilder(reg).build(validate_config(raw))
        graph.invoke({"messages": []})
        import json

        assert captured["llm"].tools == [json.dumps]


class TestToolErrors:
    def _raw(self, tools: list[str]) -> dict:
        return {
            "llm": {"provider": "fake", "model": "m"},
            "nodes": [{"name": "agent", "function": "chat_node", "tools": tools}],
            "edges": [
                {"source": "START", "target": "agent"},
                {"source": "agent", "target": "END"},
            ],
        }

    def test_missing_tool_suggests(self, fake_provider):
        reg = _registry({})
        with pytest.raises(ToolNotFoundError, match="Did you mean: 'calculator'"):
            GraphBuilder(reg).build(validate_config(self._raw(["calculatr"])))

    def test_bad_import_path_module(self, fake_provider):
        reg = _registry({})
        with pytest.raises(ToolNotFoundError, match="Cannot import tool module"):
            GraphBuilder(reg).build(validate_config(self._raw(["no_such_mod:fn"])))

    def test_bad_import_path_attr(self, fake_provider):
        reg = _registry({})
        with pytest.raises(ToolNotFoundError, match="no attribute 'nope'"):
            GraphBuilder(reg).build(validate_config(self._raw(["json:nope"])))

    def test_tools_without_llm_config_error(self):
        reg = _registry({})
        raw = self._raw(["calculator"])
        del raw["llm"]
        with pytest.raises(ConfigValidationError, match="no llm config"):
            GraphBuilder(reg).build(validate_config(raw))
