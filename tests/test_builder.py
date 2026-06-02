"""Tests for the Builder module."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, TypedDict

import operator

import pytest
from langgraph.graph import MessagesState, END, START
from langgraph.graph.state import CompiledStateGraph

from langgraph_declarative.builder import GraphBuilder
from langgraph_declarative.errors import ConfigValidationError, NodeNotFoundError
from langgraph_declarative.registry import Registry
from langgraph_declarative.schema import validate_config

FIXTURES = Path(__file__).parent / "fixtures"


# --- Helpers ---


def _make_simple_registry() -> Registry:
    """Registry matching simple.yaml."""
    reg = Registry()

    @reg.node("greet")
    def greet(state):
        return {"messages": [{"role": "assistant", "content": "hello"}]}

    @reg.node("respond")
    def respond(state):
        return {"messages": [{"role": "assistant", "content": "goodbye"}]}

    return reg


def _make_fan_out_registry() -> Registry:
    """Registry matching fan_out.yaml."""
    reg = Registry()

    @reg.node("split")
    def split(state):
        return {"messages": [{"role": "assistant", "content": "splitting"}]}

    @reg.node("process_a")
    def process_a(state):
        return {"messages": [{"role": "assistant", "content": "a"}]}

    @reg.node("process_b")
    def process_b(state):
        return {"messages": [{"role": "assistant", "content": "b"}]}

    @reg.node("join")
    def join(state):
        return {"messages": [{"role": "assistant", "content": "joined"}]}

    return reg


# --- Simple linear graph ---


class TestSimpleGraph:
    def test_build_from_file(self):
        reg = _make_simple_registry()
        builder = GraphBuilder(reg)
        graph = builder.build_from_file(FIXTURES / "simple.yaml")
        assert isinstance(graph, CompiledStateGraph)

    def test_build_from_config(self):
        reg = _make_simple_registry()
        raw = {
            "nodes": [
                {"name": "greeter", "function": "greet"},
                {"name": "responder", "function": "respond"},
            ],
            "edges": [
                {"source": "START", "target": "greeter"},
                {"source": "greeter", "target": "responder"},
                {"source": "responder", "target": "END"},
            ],
        }
        config = validate_config(raw)
        builder = GraphBuilder(reg)
        graph = builder.build(config)
        assert isinstance(graph, CompiledStateGraph)

    def test_compiled_graph_has_nodes(self):
        reg = _make_simple_registry()
        builder = GraphBuilder(reg)
        graph = builder.build_from_file(FIXTURES / "simple.yaml")
        # CompiledStateGraph should have the registered nodes
        node_names = set(graph.nodes.keys())
        assert "greeter" in node_names
        assert "responder" in node_names


# --- Fan-out graph ---


class TestFanOutGraph:
    def test_build_fan_out(self):
        reg = _make_fan_out_registry()
        builder = GraphBuilder(reg)
        graph = builder.build_from_file(FIXTURES / "fan_out.yaml")
        assert isinstance(graph, CompiledStateGraph)
        node_names = set(graph.nodes.keys())
        assert "branch_a" in node_names
        assert "branch_b" in node_names


# --- Conditional routing graph ---


class TestConditionalGraph:
    def test_build_conditional(self):
        reg = Registry()

        @reg.node("classify")
        def classify(state):
            return {"messages": [{"role": "assistant", "content": "classified"}]}

        @reg.node("positive")
        def positive(state):
            return {"messages": [{"role": "assistant", "content": "pos"}]}

        @reg.node("negative")
        def negative(state):
            return {"messages": [{"role": "assistant", "content": "neg"}]}

        @reg.router("sentiment_router")
        def sentiment_router(state):
            return "positive"

        builder = GraphBuilder(reg)
        graph = builder.build_from_file(FIXTURES / "conditional.yaml")
        assert isinstance(graph, CompiledStateGraph)
        assert "classifier" in graph.nodes
        assert "handle_positive" in graph.nodes
        assert "handle_negative" in graph.nodes


# --- Dynamic routing graph ---


class TestDynamicRoutingGraph:
    def test_build_dynamic(self):
        reg = Registry()

        @reg.node("dispatch")
        def dispatch(state):
            return {"messages": [{"role": "assistant", "content": "dispatched"}]}

        @reg.node("work")
        def work(state):
            return {"messages": [{"role": "assistant", "content": "done"}]}

        @reg.router("dynamic_router")
        def dynamic_router(state):
            return "worker"

        builder = GraphBuilder(reg)
        graph = builder.build_from_file(FIXTURES / "dynamic_routing.yaml")
        assert isinstance(graph, CompiledStateGraph)
        assert "dispatcher" in graph.nodes
        assert "worker" in graph.nodes


# --- Error cases ---


class TestBuilderErrors:
    def test_missing_function_ref_raises(self):
        reg = Registry()  # empty registry
        raw = {
            "nodes": [{"name": "a", "function": "nonexistent"}],
            "edges": [{"source": "START", "target": "a"}],
        }
        config = validate_config(raw)
        builder = GraphBuilder(reg)
        with pytest.raises(NodeNotFoundError):
            builder.build(config)


# --- Custom state class ---


class TestCustomStateClass:
    def test_custom_state_class_used(self):
        class MyState(TypedDict):
            count: Annotated[int, operator.add]

        reg = Registry()

        @reg.node("inc")
        def inc(state):
            return {"count": 1}

        raw = {
            "nodes": [{"name": "counter", "function": "inc"}],
            "edges": [
                {"source": "START", "target": "counter"},
                {"source": "counter", "target": "END"},
            ],
        }
        config = validate_config(raw)
        builder = GraphBuilder(reg, state_class=MyState)
        graph = builder.build(config)
        assert isinstance(graph, CompiledStateGraph)

    def test_default_state_is_messages_state(self):
        builder = GraphBuilder(Registry())
        assert builder.state_class is MessagesState


# --- Mapped routing validation ---


class TestMappedRoutingValidation:
    def _build_conditional_graph(self, router_fn):
        """Helper: build a graph with a mapped conditional edge using the given router."""
        reg = Registry()

        @reg.node("classify")
        def classify(state):
            return {"messages": [{"role": "assistant", "content": "classified"}]}

        @reg.node("positive")
        def positive(state):
            return {"messages": [{"role": "assistant", "content": "pos"}]}

        @reg.node("negative")
        def negative(state):
            return {"messages": [{"role": "assistant", "content": "neg"}]}

        reg._routers["test_router"] = router_fn

        raw = {
            "nodes": [
                {"name": "classifier", "function": "classify"},
                {"name": "handle_pos", "function": "positive"},
                {"name": "handle_neg", "function": "negative"},
            ],
            "edges": [
                {"source": "START", "target": "classifier"},
                {
                    "source": "classifier",
                    "path": "test_router",
                    "targets": {"pos": "handle_pos", "neg": "handle_neg"},
                },
                {"source": "handle_pos", "target": "END"},
                {"source": "handle_neg", "target": "END"},
            ],
        }
        config = validate_config(raw)
        builder = GraphBuilder(reg)
        return builder.build(config)

    def test_unmapped_key_raises(self):
        def bad_router(state):
            return "unknown_key"

        graph = self._build_conditional_graph(bad_router)
        with pytest.raises(ConfigValidationError, match="unmapped key 'unknown_key'"):
            graph.invoke({"messages": [{"role": "user", "content": "hi"}]})

    def test_non_string_return_raises(self):
        def bad_router(state):
            return ["pos", "neg"]

        graph = self._build_conditional_graph(bad_router)
        with pytest.raises(ConfigValidationError, match="returned list, expected str"):
            graph.invoke({"messages": [{"role": "user", "content": "hi"}]})

    def test_valid_mapped_key_works(self):
        def good_router(state):
            return "pos"

        graph = self._build_conditional_graph(good_router)
        result = graph.invoke({"messages": [{"role": "user", "content": "hi"}]})
        contents = [m.content for m in result["messages"]]
        assert "pos" in contents
