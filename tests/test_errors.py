"""Tests for the errors module."""

import pytest

from langgraph_declarative.errors import (
    ConfigLoadError,
    ConfigValidationError,
    DeclarativeError,
    NodeNotFoundError,
    RouterNotFoundError,
    format_not_found,
    suggest_similar,
)


# --- Exception hierarchy ---


class TestExceptionHierarchy:
    """All custom exceptions inherit from DeclarativeError."""

    @pytest.mark.parametrize(
        "exc_class",
        [ConfigLoadError, ConfigValidationError, NodeNotFoundError, RouterNotFoundError],
    )
    def test_subclass_of_declarative_error(self, exc_class):
        assert issubclass(exc_class, DeclarativeError)

    @pytest.mark.parametrize(
        "exc_class",
        [ConfigLoadError, ConfigValidationError, NodeNotFoundError, RouterNotFoundError],
    )
    def test_isinstance_check(self, exc_class):
        exc = exc_class("test message")
        assert isinstance(exc, DeclarativeError)
        assert isinstance(exc, Exception)

    def test_declarative_error_is_exception(self):
        assert issubclass(DeclarativeError, Exception)


# --- suggest_similar ---


class TestSuggestSimilar:
    def test_returns_close_matches(self):
        available = ["process_input", "process_output", "classify"]
        result = suggest_similar("process_inut", available)
        assert "process_input" in result

    def test_returns_empty_for_no_match(self):
        available = ["alpha", "beta", "gamma"]
        result = suggest_similar("zzzzz", available)
        assert result == []

    def test_returns_empty_for_empty_available(self):
        result = suggest_similar("anything", [])
        assert result == []

    def test_respects_n_parameter(self):
        available = ["aaa", "aab", "aac", "aad"]
        result = suggest_similar("aaa", available, n=2)
        assert len(result) <= 2

    def test_exact_match_is_included(self):
        available = ["foo", "bar", "baz"]
        result = suggest_similar("foo", available)
        assert "foo" in result


# --- format_not_found ---


class TestFormatNotFound:
    def test_includes_kind_and_name(self):
        msg = format_not_found("node", "my_node", [])
        assert "node" in msg
        assert "'my_node'" in msg

    def test_includes_suggestions_when_available(self):
        msg = format_not_found("node", "procss_input", ["process_input", "process_output"])
        assert "Did you mean" in msg
        assert "'process_input'" in msg

    def test_lists_available_when_no_close_match(self):
        msg = format_not_found("router", "zzzzz", ["alpha", "beta"])
        assert "Available routers" in msg
        assert "'alpha'" in msg
        assert "'beta'" in msg

    def test_no_suggestions_when_available_empty(self):
        msg = format_not_found("node", "anything", [])
        assert "not found" in msg
        assert "Did you mean" not in msg
        assert "Available" not in msg

    def test_available_names_sorted(self):
        msg = format_not_found("router", "zzzzz", ["gamma", "alpha", "beta"])
        # Available list should be sorted
        alpha_pos = msg.index("'alpha'")
        beta_pos = msg.index("'beta'")
        gamma_pos = msg.index("'gamma'")
        assert alpha_pos < beta_pos < gamma_pos
