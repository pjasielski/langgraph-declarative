"""Tests for match: routing syntax (task-017)."""

from __future__ import annotations

from pathlib import Path

import pytest

from langgraph_declarative import GraphBuilder, Registry, build_graph
from langgraph_declarative.builder import _make_match_router
from langgraph_declarative.errors import ConfigValidationError
from langgraph_declarative.schema import validate_config

FIXTURES = Path(__file__).parent / "fixtures"


def _registry(category: str) -> Registry:
    reg = Registry()

    @reg.node("classify")
    def classify(state):
        return {"category": category}

    for name in ("billing", "tech", "general"):
        def _make(label):
            def fn(state):
                return {"messages": [{"role": "assistant", "content": label}]}
            return fn

        reg._nodes[name] = _make(name)

    return reg


class TestMatchRouting:
    def test_basic_matching(self):
        graph = build_graph(FIXTURES / "match_routing.yaml", _registry("billing"))
        result = graph.invoke({"messages": [], "category": ""})
        assert result["messages"][-1].content == "billing"

    def test_second_branch(self):
        graph = build_graph(FIXTURES / "match_routing.yaml", _registry("technical"))
        result = graph.invoke({"messages": [], "category": ""})
        assert result["messages"][-1].content == "tech"

    def test_default_fallback(self):
        graph = build_graph(FIXTURES / "match_routing.yaml", _registry("unknown"))
        result = graph.invoke({"messages": [], "category": ""})
        assert result["messages"][-1].content == "general"

    def test_value_not_found_no_default_raises(self):
        router = _make_match_router("category", {"billing", "technical"})
        with pytest.raises(ConfigValidationError, match="no 'default' key"):
            router({"category": "unknown"})

    def test_missing_state_field_raises(self):
        router = _make_match_router("category", {"billing", "default"})
        with pytest.raises(ConfigValidationError, match="no field 'category'"):
            router({"other": 1})

    def test_nested_dot_access(self):
        router = _make_match_router("result.status", {"ok", "fail"})
        assert router({"result": {"status": "ok"}}) == "ok"

    def test_nested_attribute_access(self):
        class Result:
            status = "fail"

        router = _make_match_router("result.status", {"ok", "fail"})
        assert router({"result": Result()}) == "fail"

    def test_non_string_value_stringified(self):
        router = _make_match_router("flag", {"True", "False"})
        assert router({"flag": True}) == "True"


class TestMatchSchema:
    BASE = {
        "nodes": [{"name": "a", "function": "f"}, {"name": "b", "function": "g"}],
    }

    def test_match_without_targets_rejected(self):
        raw = {
            **self.BASE,
            "edges": [{"source": "a", "match": "category"}],
        }
        with pytest.raises(ConfigValidationError, match="'match' without 'targets'"):
            validate_config(raw)

    def test_match_and_path_mutually_exclusive(self):
        raw = {
            **self.BASE,
            "edges": [
                {
                    "source": "a",
                    "match": "x",
                    "path": "router",
                    "targets": {"k": "b"},
                }
            ],
        }
        with pytest.raises(ConfigValidationError, match="mutually exclusive"):
            validate_config(raw)

    def test_match_and_target_mutually_exclusive(self):
        raw = {
            **self.BASE,
            "edges": [
                {"source": "a", "match": "x", "target": "b", "targets": {"k": "b"}}
            ],
        }
        with pytest.raises(ConfigValidationError, match="mutually exclusive"):
            validate_config(raw)

    def test_match_targets_checked_against_nodes(self):
        reg = Registry()

        @reg.node("f")
        def f(state):
            return {}

        @reg.node("g")
        def g(state):
            return {}

        raw = {
            **self.BASE,
            "edges": [
                {"source": "a", "match": "x", "targets": {"k": "nonexistent"}}
            ],
        }
        config = validate_config(raw)
        with pytest.raises(ConfigValidationError, match="'nonexistent' not found"):
            GraphBuilder(reg).build(config)
