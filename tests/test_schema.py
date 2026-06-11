"""Tests for the Schema module."""

import pytest

from langgraph_declarative.errors import (
    ConfigValidationError,
    NodeNotFoundError,
    RouterNotFoundError,
)
from langgraph_declarative.registry import Registry
from langgraph_declarative.schema import GraphConfig, cross_validate, validate_config


# --- Fixtures ---


@pytest.fixture
def valid_raw():
    """Minimal valid config dict."""
    return {
        "nodes": [
            {"name": "greet", "function": "greet_fn"},
            {"name": "respond", "function": "respond_fn"},
        ],
        "edges": [
            {"source": "START", "target": "greet"},
            {"source": "greet", "target": "respond"},
            {"source": "respond", "target": "END"},
        ],
    }


@pytest.fixture
def registry_with_fns():
    """Registry pre-loaded with functions matching valid_raw."""
    reg = Registry()

    @reg.node("greet_fn")
    def greet_fn(state):
        return {}

    @reg.node("respond_fn")
    def respond_fn(state):
        return {}

    return reg


# --- validate_config ---


class TestValidateConfig:
    def test_valid_config_parses(self, valid_raw):
        config = validate_config(valid_raw)
        assert len(config.nodes) == 2
        assert len(config.edges) == 3

    def test_fan_out_target(self):
        raw = {
            "nodes": [
                {"name": "a", "function": "fn_a"},
                {"name": "b", "function": "fn_b"},
                {"name": "c", "function": "fn_c"},
            ],
            "edges": [{"source": "START", "target": ["a", "b", "c"]}],
        }
        config = validate_config(raw)
        assert config.edges[0].target == ["a", "b", "c"]

    def test_conditional_edge(self):
        raw = {
            "nodes": [{"name": "a", "function": "fn_a"}],
            "edges": [
                {
                    "source": "a",
                    "path": "my_router",
                    "targets": {"yes": "a", "no": "END"},
                }
            ],
        }
        config = validate_config(raw)
        assert config.edges[0].path == "my_router"
        assert config.edges[0].targets == {"yes": "a", "no": "END"}

    def test_dynamic_routing_no_targets(self):
        raw = {
            "nodes": [{"name": "a", "function": "fn_a"}],
            "edges": [{"source": "a", "path": "my_router"}],
        }
        config = validate_config(raw)
        assert config.edges[0].path == "my_router"
        assert config.edges[0].targets is None

    def test_missing_target_and_path_raises(self):
        raw = {
            "nodes": [{"name": "a", "function": "fn_a"}],
            "edges": [{"source": "a"}],
        }
        with pytest.raises(ConfigValidationError, match="neither 'target' nor 'path'"):
            validate_config(raw)

    def test_both_target_and_path_raises(self):
        raw = {
            "nodes": [{"name": "a", "function": "fn_a"}],
            "edges": [{"source": "a", "target": "a", "path": "router"}],
        }
        with pytest.raises(ConfigValidationError, match="both 'target' and 'path'"):
            validate_config(raw)

    def test_targets_without_path_raises(self):
        raw = {
            "nodes": [{"name": "a", "function": "fn_a"}],
            "edges": [
                {"source": "a", "target": "a", "targets": {"x": "a"}}
            ],
        }
        with pytest.raises(ConfigValidationError, match="'targets' without 'path'"):
            validate_config(raw)

    def test_targets_without_path_no_target_raises(self):
        raw = {
            "nodes": [{"name": "a", "function": "fn_a"}],
            "edges": [{"source": "a", "targets": {"x": "a"}}],
        }
        with pytest.raises(ConfigValidationError, match="neither 'target' nor 'path'"):
            validate_config(raw)

    def test_empty_targets_raises(self):
        raw = {
            "nodes": [{"name": "a", "function": "fn_a"}],
            "edges": [{"source": "a", "path": "my_router", "targets": {}}],
        }
        with pytest.raises(ConfigValidationError, match="empty 'targets' map"):
            validate_config(raw)

    def test_duplicate_node_names_raises(self):
        raw = {
            "nodes": [
                {"name": "dup", "function": "fn_a"},
                {"name": "dup", "function": "fn_b"},
            ],
            "edges": [{"source": "START", "target": "dup"}],
        }
        with pytest.raises(ConfigValidationError, match="Duplicate node name: 'dup'"):
            validate_config(raw)

    def test_extra_unknown_fields_are_ignored(self):
        raw = {
            "nodes": [{"name": "a", "function": "fn_a", "description": "extra field"}],
            "edges": [{"source": "START", "target": "a", "label": "also extra"}],
            "metadata": {"version": "1.0"},
        }
        config = validate_config(raw)
        assert len(config.nodes) == 1
        assert len(config.edges) == 1

    def test_nodes_only_no_edges_raises(self):
        raw = {
            "nodes": [{"name": "a", "function": "fn_a"}],
        }
        with pytest.raises(ConfigValidationError):
            validate_config(raw)

    def test_edges_only_no_nodes_raises(self):
        raw = {
            "edges": [{"source": "START", "target": "END"}],
        }
        with pytest.raises(ConfigValidationError):
            validate_config(raw)


# --- cross_validate ---


class TestCrossValidate:
    def test_valid_config_passes(self, valid_raw, registry_with_fns):
        config = validate_config(valid_raw)
        cross_validate(config, registry_with_fns)  # should not raise

    def test_missing_node_function_raises(self, registry_with_fns):
        raw = {
            "nodes": [{"name": "a", "function": "nonexistent_fn"}],
            "edges": [{"source": "START", "target": "a"}],
        }
        config = validate_config(raw)
        with pytest.raises(NodeNotFoundError, match="not found"):
            cross_validate(config, registry_with_fns)

    def test_missing_router_raises(self, registry_with_fns):
        raw = {
            "nodes": [{"name": "a", "function": "greet_fn"}],
            "edges": [{"source": "a", "path": "nonexistent_router"}],
        }
        config = validate_config(raw)
        with pytest.raises(RouterNotFoundError, match="not found"):
            cross_validate(config, registry_with_fns)

    def test_edge_source_references_undefined_node(self, registry_with_fns):
        raw = {
            "nodes": [{"name": "a", "function": "greet_fn"}],
            "edges": [
                {"source": "START", "target": "a"},
                {"source": "undefined_node", "target": "END"},
            ],
        }
        config = validate_config(raw)
        with pytest.raises(ConfigValidationError, match="not found"):
            cross_validate(config, registry_with_fns)

    def test_edge_target_references_undefined_node(self, registry_with_fns):
        raw = {
            "nodes": [{"name": "a", "function": "greet_fn"}],
            "edges": [{"source": "START", "target": "undefined_node"}],
        }
        config = validate_config(raw)
        with pytest.raises(ConfigValidationError, match="not found"):
            cross_validate(config, registry_with_fns)

    def test_fan_out_target_references_undefined_node(self, registry_with_fns):
        raw = {
            "nodes": [{"name": "a", "function": "greet_fn"}],
            "edges": [{"source": "START", "target": ["a", "nonexistent"]}],
        }
        config = validate_config(raw)
        with pytest.raises(ConfigValidationError, match="not found"):
            cross_validate(config, registry_with_fns)

    def test_conditional_targets_reference_undefined_node(self):
        reg = Registry()

        @reg.node("fn_a")
        def fn_a(state):
            return {}

        @reg.router("my_router")
        def my_router(state):
            return "yes"

        raw = {
            "nodes": [{"name": "a", "function": "fn_a"}],
            "edges": [
                {
                    "source": "a",
                    "path": "my_router",
                    "targets": {"yes": "a", "no": "ghost_node"},
                }
            ],
        }
        config = validate_config(raw)
        with pytest.raises(ConfigValidationError, match="not found"):
            cross_validate(config, reg)

    def test_start_and_end_are_valid_references(self, registry_with_fns):
        raw = {
            "nodes": [{"name": "greet", "function": "greet_fn"}],
            "edges": [
                {"source": "START", "target": "greet"},
                {"source": "greet", "target": "END"},
            ],
        }
        config = validate_config(raw)
        cross_validate(config, registry_with_fns)  # should not raise

    def test_missing_function_suggests_similar(self):
        reg = Registry()

        @reg.node("process_input")
        def process_input(state):
            return {}

        raw = {
            "nodes": [{"name": "a", "function": "procss_input"}],
            "edges": [{"source": "START", "target": "a"}],
        }
        config = validate_config(raw)
        with pytest.raises(NodeNotFoundError, match="Did you mean"):
            cross_validate(config, reg)
