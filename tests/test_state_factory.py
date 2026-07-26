"""Tests for YAML state declaration (task-014)."""

from __future__ import annotations

import operator
from pathlib import Path
from typing import Annotated, get_args, get_origin

import pytest
from langgraph.graph import MessagesState, add_messages
from langgraph.graph.state import CompiledStateGraph

from langgraph_declarative import GraphBuilder, Registry, build_graph
from langgraph_declarative.errors import ConfigValidationError
from langgraph_declarative.schema import validate_config
from langgraph_declarative.state_factory import StateFieldConfig, build_state_class

FIXTURES = Path(__file__).parent / "fixtures"


def _fields(*specs: dict) -> list[StateFieldConfig]:
    return [StateFieldConfig(**s) for s in specs]


class TestBuildStateClass:
    def test_plain_field_types(self):
        cls = build_state_class(
            _fields(
                {"name": "summary", "type": "str"},
                {"name": "count", "type": "int"},
                {"name": "score", "type": "float"},
                {"name": "done", "type": "bool"},
                {"name": "items", "type": "list"},
                {"name": "meta", "type": "dict"},
            )
        )
        ann = cls.__annotations__
        assert ann["summary"] is str
        assert ann["count"] is int
        assert ann["score"] is float
        assert ann["done"] is bool
        assert ann["items"] is list
        assert ann["meta"] is dict

    def test_parameterized_list_types(self):
        cls = build_state_class(
            _fields(
                {"name": "tags", "type": "list[str]"},
                {"name": "records", "type": "list[dict]"},
            )
        )
        assert cls.__annotations__["tags"] == list[str]
        assert cls.__annotations__["records"] == list[dict]

    def test_add_messages_reducer(self):
        cls = build_state_class(
            _fields({"name": "messages", "type": "list", "reducer": "add_messages"})
        )
        ann = cls.__annotations__["messages"]
        assert get_origin(ann) is Annotated
        assert get_args(ann)[1] is add_messages

    def test_append_reducer_is_operator_add(self):
        cls = build_state_class(
            _fields({"name": "steps", "type": "list[str]", "reducer": "append"})
        )
        ann = cls.__annotations__["steps"]
        assert get_args(ann)[1] is operator.add

    def test_replace_reducer_has_no_annotation(self):
        cls = build_state_class(
            _fields({"name": "summary", "type": "str", "reducer": "replace"})
        )
        assert cls.__annotations__["summary"] is str

    def test_defaults_stored(self):
        cls = build_state_class(
            _fields({"name": "summary", "type": "str", "default": "n/a"})
        )
        assert cls.__field_defaults__ == {"summary": "n/a"}


class TestInvalidConfigs:
    def test_invalid_type_suggests(self):
        with pytest.raises(ValueError, match="state type 'string' not found"):
            StateFieldConfig(name="x", type="string")

    def test_invalid_reducer_suggests(self):
        with pytest.raises(ValueError, match="reducer 'apend' not found.*append"):
            StateFieldConfig(name="x", type="list", reducer="apend")

    def test_duplicate_state_field_names_rejected(self):
        raw = {
            "state": [
                {"name": "x", "type": "str"},
                {"name": "x", "type": "int"},
            ],
            "nodes": [{"name": "a", "function": "f"}],
            "edges": [{"source": "START", "target": "a"}],
        }
        with pytest.raises(ConfigValidationError, match="Duplicate state field"):
            validate_config(raw)


class TestIntegration:
    def _registry(self) -> Registry:
        reg = Registry()

        @reg.node("summarize_fn")
        def summarize_fn(state):
            return {
                "summary": "short",
                "steps": ["summarize"],
                "counter": 1,
                "messages": [{"role": "assistant", "content": "summarized"}],
            }

        @reg.node("finish_fn")
        def finish_fn(state):
            return {"steps": ["finish"]}

        return reg

    def test_yaml_state_builds_and_runs(self):
        graph = build_graph(FIXTURES / "state_declaration.yaml", self._registry())
        assert isinstance(graph, CompiledStateGraph)
        result = graph.invoke(
            {"messages": [], "summary": "", "steps": ["init"], "counter": 0}
        )
        assert result["summary"] == "short"
        # append reducer accumulates across nodes
        assert result["steps"] == ["init", "summarize", "finish"]
        # replace semantics for plain fields
        assert result["counter"] == 1
        # add_messages reducer produced message objects
        assert len(result["messages"]) == 1

    def test_state_class_param_ignored_with_warning(self):
        with pytest.warns(UserWarning, match="overrides the state_class"):
            graph = build_graph(
                FIXTURES / "state_declaration.yaml",
                self._registry(),
                state_class=MessagesState,
            )
        assert isinstance(graph, CompiledStateGraph)

    def test_no_state_section_is_backwards_compatible(self):
        reg = Registry()

        @reg.node("greet")
        def greet(state):
            return {"messages": [{"role": "assistant", "content": "hello"}]}

        @reg.node("respond")
        def respond(state):
            return {"messages": [{"role": "assistant", "content": "bye"}]}

        builder = GraphBuilder(reg)
        graph = builder.build_from_file(FIXTURES / "simple.yaml")
        assert builder.state_class is MessagesState
        assert isinstance(graph, CompiledStateGraph)
