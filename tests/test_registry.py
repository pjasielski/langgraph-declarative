"""Tests for the Registry module."""

import pytest

from langgraph_declarative.errors import NodeNotFoundError, RouterNotFoundError
from langgraph_declarative.registry import Registry


@pytest.fixture
def registry():
    return Registry()


# --- Node registration ---


class TestNodeRegistration:
    def test_register_and_retrieve(self, registry):
        @registry.node("greet")
        def greet(state):
            return {"messages": ["hi"]}

        assert registry.get_node("greet") is greet

    def test_decorator_returns_original_function(self, registry):
        def my_fn(state):
            return {}

        result = registry.node("my_fn")(my_fn)
        assert result is my_fn

    def test_duplicate_name_raises(self, registry):
        @registry.node("dup")
        def fn1(state):
            return {}

        with pytest.raises(ValueError, match="Duplicate node name: 'dup'"):

            @registry.node("dup")
            def fn2(state):
                return {}

    def test_missing_node_raises_with_suggestion(self, registry):
        @registry.node("process_input")
        def process_input(state):
            return {}

        with pytest.raises(NodeNotFoundError, match="Did you mean"):
            registry.get_node("procss_input")

    def test_missing_node_raises_when_empty(self, registry):
        with pytest.raises(NodeNotFoundError, match="not found"):
            registry.get_node("anything")

    def test_list_nodes(self, registry):
        @registry.node("a")
        def fn_a(state):
            return {}

        @registry.node("b")
        def fn_b(state):
            return {}

        assert set(registry.list_nodes()) == {"a", "b"}


# --- Router registration ---


class TestRouterRegistration:
    def test_register_and_retrieve(self, registry):
        @registry.router("route_it")
        def route_it(state):
            return "branch_a"

        assert registry.get_router("route_it") is route_it

    def test_decorator_returns_original_function(self, registry):
        def my_router(state):
            return "x"

        result = registry.router("my_router")(my_router)
        assert result is my_router

    def test_duplicate_name_raises(self, registry):
        @registry.router("dup")
        def fn1(state):
            return "a"

        with pytest.raises(ValueError, match="Duplicate router name: 'dup'"):

            @registry.router("dup")
            def fn2(state):
                return "b"

    def test_missing_router_raises_with_suggestion(self, registry):
        @registry.router("classify_intent")
        def classify_intent(state):
            return "a"

        with pytest.raises(RouterNotFoundError, match="Did you mean"):
            registry.get_router("clasify_intent")

    def test_list_routers(self, registry):
        @registry.router("r1")
        def r1(state):
            return "x"

        assert registry.list_routers() == ["r1"]


# --- Namespace isolation ---


class TestNamespaceIsolation:
    def test_same_name_in_both_namespaces(self, registry):
        @registry.node("process")
        def process_node(state):
            return {}

        @registry.router("process")
        def process_router(state):
            return "x"

        assert registry.get_node("process") is process_node
        assert registry.get_router("process") is process_router

    def test_node_lookup_does_not_find_router(self, registry):
        @registry.router("only_router")
        def only_router(state):
            return "x"

        with pytest.raises(NodeNotFoundError):
            registry.get_node("only_router")

    def test_router_lookup_does_not_find_node(self, registry):
        @registry.node("only_node")
        def only_node(state):
            return {}

        with pytest.raises(RouterNotFoundError):
            registry.get_router("only_node")
