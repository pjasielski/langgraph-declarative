"""End-to-end integration tests — YAML -> build_graph -> invoke -> verify."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, TypedDict

import operator

import pytest
from langgraph.types import Send

from langgraph_declarative import Registry, build_graph

FIXTURES = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# State classes for non-MessagesState tests
# ---------------------------------------------------------------------------


class CounterState(TypedDict):
    values: Annotated[list[str], operator.add]


# ---------------------------------------------------------------------------
# Simple linear graph
# ---------------------------------------------------------------------------


class TestSimpleLinear:
    """START -> greeter -> responder -> END"""

    def test_invoke_produces_messages(self):
        reg = Registry()

        @reg.node("greet")
        def greet(state):
            return {"values": ["hello"]}

        @reg.node("respond")
        def respond(state):
            return {"values": ["goodbye"]}

        graph = build_graph(FIXTURES / "simple.yaml", reg, state_class=CounterState)
        result = graph.invoke({"values": []})
        assert result["values"] == ["hello", "goodbye"]


# ---------------------------------------------------------------------------
# Fan-out graph
# ---------------------------------------------------------------------------


class TestFanOut:
    """START -> splitter -> [branch_a, branch_b] -> joiner -> END"""

    def test_parallel_branches_both_execute(self):
        reg = Registry()

        @reg.node("split")
        def split(state):
            return {"values": ["split"]}

        @reg.node("process_a")
        def process_a(state):
            return {"values": ["a"]}

        @reg.node("process_b")
        def process_b(state):
            return {"values": ["b"]}

        @reg.node("join")
        def join(state):
            return {"values": ["joined"]}

        graph = build_graph(FIXTURES / "fan_out.yaml", reg, state_class=CounterState)
        result = graph.invoke({"values": []})
        # split runs first, then a and b in parallel, then join
        assert "split" in result["values"]
        assert "a" in result["values"]
        assert "b" in result["values"]
        assert "joined" in result["values"]
        assert result["values"][0] == "split"
        assert result["values"][-1] == "joined"


# ---------------------------------------------------------------------------
# Conditional routing (mapped)
# ---------------------------------------------------------------------------


class TestConditionalRouting:
    """START -> classifier -> (sentiment_router) -> handle_positive|handle_negative -> END"""

    def _build(self, router_return: str):
        reg = Registry()

        @reg.node("classify")
        def classify(state):
            return {"values": ["classified"]}

        @reg.node("positive")
        def positive(state):
            return {"values": ["pos_handled"]}

        @reg.node("negative")
        def negative(state):
            return {"values": ["neg_handled"]}

        @reg.router("sentiment_router")
        def sentiment_router(state):
            return router_return

        return build_graph(FIXTURES / "conditional.yaml", reg, state_class=CounterState)

    def test_positive_path(self):
        graph = self._build("positive")
        result = graph.invoke({"values": []})
        assert "classified" in result["values"]
        assert "pos_handled" in result["values"]
        assert "neg_handled" not in result["values"]

    def test_negative_path(self):
        graph = self._build("negative")
        result = graph.invoke({"values": []})
        assert "classified" in result["values"]
        assert "neg_handled" in result["values"]
        assert "pos_handled" not in result["values"]


# ---------------------------------------------------------------------------
# Dynamic routing (Send)
# ---------------------------------------------------------------------------


class TestDynamicRouting:
    """START -> dispatcher -> (dynamic_router returns Send) -> worker(s) -> END"""

    def test_send_based_fanout(self):
        reg = Registry()

        @reg.node("dispatch")
        def dispatch(state):
            return {"values": ["dispatched"]}

        @reg.node("work")
        def work(state):
            return {"values": [f"work_{state['values'][-1]}"]}

        @reg.router("dynamic_router")
        def dynamic_router(state):
            # Send two parallel invocations to "worker" with different state
            return [
                Send("worker", {"values": ["task_1"]}),
                Send("worker", {"values": ["task_2"]}),
            ]

        graph = build_graph(
            FIXTURES / "dynamic_routing.yaml", reg, state_class=CounterState
        )
        result = graph.invoke({"values": []})
        assert "dispatched" in result["values"]
        # Both Send invocations should have run
        assert "work_task_1" in result["values"]
        assert "work_task_2" in result["values"]


# ---------------------------------------------------------------------------
# Full-featured graph (combines fan-out + conditional)
# ---------------------------------------------------------------------------


class TestFullFeatured:
    """START -> entry -> [branch_a, branch_b] -> merger -> (yes_no_router) -> final_yes|final_no -> END"""

    def test_full_featured_yes_path(self):
        reg = Registry()

        @reg.node("entry_fn")
        def entry_fn(state):
            return {"values": ["entry"]}

        @reg.node("branch_a_fn")
        def branch_a_fn(state):
            return {"values": ["a"]}

        @reg.node("branch_b_fn")
        def branch_b_fn(state):
            return {"values": ["b"]}

        @reg.node("merger_fn")
        def merger_fn(state):
            return {"values": ["merged"]}

        @reg.node("final_yes_fn")
        def final_yes_fn(state):
            return {"values": ["YES"]}

        @reg.node("final_no_fn")
        def final_no_fn(state):
            return {"values": ["NO"]}

        @reg.router("yes_no_router")
        def yes_no_router(state):
            return "yes"

        graph = build_graph(
            FIXTURES / "full_featured.yaml", reg, state_class=CounterState
        )
        result = graph.invoke({"values": []})
        assert "entry" in result["values"]
        assert "a" in result["values"]
        assert "b" in result["values"]
        assert "merged" in result["values"]
        assert "YES" in result["values"]
        assert "NO" not in result["values"]


# ---------------------------------------------------------------------------
# build_graph convenience function
# ---------------------------------------------------------------------------


class TestBuildGraphConvenience:
    def test_import_from_package(self):
        """Public API is importable from the top-level package."""
        from langgraph_declarative import Registry, GraphBuilder, build_graph

        assert callable(build_graph)
        assert callable(Registry)
        assert callable(GraphBuilder)
