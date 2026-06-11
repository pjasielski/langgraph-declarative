"""Tests for per-node LLM configuration (task-020)."""

from __future__ import annotations

from pathlib import Path

import pytest

from langgraph_declarative import Registry, build_graph
from langgraph_declarative import llm_factory
from langgraph_declarative.errors import ConfigValidationError, DeclarativeError
from langgraph_declarative.llm_factory import create_llm, merge_llm_config
from langgraph_declarative.schema import LLMConfig

FIXTURES = Path(__file__).parent / "fixtures"


class FakeLLM:
    """Minimal stand-in for a LangChain chat model."""

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


class TestLLMConfigParsing:
    def test_merge_node_overrides_graph_default(self):
        base = LLMConfig(provider="fake", model="fake-default", temperature=0.7)
        override = LLMConfig(model="fake-mini", temperature=0)
        merged = merge_llm_config(base, override)
        assert merged.provider == "fake"
        assert merged.model == "fake-mini"
        assert merged.temperature == 0

    def test_merge_none_cases(self):
        cfg = LLMConfig(provider="fake", model="m")
        assert merge_llm_config(None, None) is None
        assert merge_llm_config(cfg, None) is cfg
        assert merge_llm_config(None, cfg) is cfg

    def test_missing_provider_error(self):
        with pytest.raises(ConfigValidationError, match="missing 'provider'"):
            create_llm(LLMConfig(model="m"))

    def test_missing_model_error(self):
        with pytest.raises(ConfigValidationError, match="missing 'model'"):
            create_llm(LLMConfig(provider="openai"))

    def test_unknown_provider_error(self):
        with pytest.raises(ConfigValidationError, match="Unknown llm provider 'zzz'"):
            create_llm(LLMConfig(provider="zzz", model="m"))

    def test_missing_provider_package_hint(self):
        # langchain_openai is not installed in the test environment
        with pytest.raises(DeclarativeError, match="pip install langchain-openai"):
            create_llm(LLMConfig(provider="openai", model="gpt-4o"))


class TestLLMInjection:
    def _registry(self, captured: dict) -> Registry:
        reg = Registry()

        @reg.node("chat_node")
        def chat_node(state, llm=None):
            captured["chat_llm"] = llm
            return {"messages": [{"role": "assistant", "content": "chat"}]}

        @reg.node("summarize_node")
        def summarize_node(state, llm=None):
            captured["summary_llm"] = llm
            return {"messages": [{"role": "assistant", "content": "summary"}]}

        return reg

    def test_graph_default_and_node_override(self, fake_provider):
        captured: dict = {}
        graph = build_graph(FIXTURES / "llm_workflow.yaml", self._registry(captured))
        graph.invoke({"messages": []})

        # chatter gets the graph-level default
        assert captured["chat_llm"].config.model == "fake-default"
        assert captured["chat_llm"].config.temperature == 0.7
        # summarizer overrides model + temperature, inherits provider
        assert captured["summary_llm"].config.model == "fake-mini"
        assert captured["summary_llm"].config.temperature == 0
        assert captured["summary_llm"].config.provider == "fake"

    def test_node_llm_without_param_is_error(self, fake_provider):
        reg = Registry()

        @reg.node("plain")
        def plain(state):
            return {}

        raw = {
            "nodes": [
                {
                    "name": "n",
                    "function": "plain",
                    "llm": {"provider": "fake", "model": "m"},
                }
            ],
            "edges": [
                {"source": "START", "target": "n"},
                {"source": "n", "target": "END"},
            ],
        }
        from langgraph_declarative import GraphBuilder
        from langgraph_declarative.schema import validate_config

        with pytest.raises(ConfigValidationError, match="does not accept an 'llm'"):
            GraphBuilder(reg).build(validate_config(raw))

    def test_graph_default_skips_non_opting_functions(self, fake_provider):
        """A graph-level llm: must not break nodes without an llm param."""
        reg = Registry()

        @reg.node("plain")
        def plain(state):
            return {"messages": [{"role": "assistant", "content": "ok"}]}

        raw = {
            "llm": {"provider": "fake", "model": "m"},
            "nodes": [{"name": "n", "function": "plain"}],
            "edges": [
                {"source": "START", "target": "n"},
                {"source": "n", "target": "END"},
            ],
        }
        from langgraph_declarative import GraphBuilder
        from langgraph_declarative.schema import validate_config

        graph = GraphBuilder(reg).build(validate_config(raw))
        result = graph.invoke({"messages": []})
        assert result["messages"][-1].content == "ok"
