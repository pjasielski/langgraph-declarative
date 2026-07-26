"""Custom exceptions and typo-suggestion helpers for langgraph-declarative."""

from __future__ import annotations

import difflib


class DeclarativeError(Exception):
    """Base exception for all langgraph-declarative errors."""


class ConfigLoadError(DeclarativeError):
    """YAML file loading failed (file not found, parse error, etc.)."""


class ConfigValidationError(DeclarativeError):
    """YAML structure is invalid (schema validation failure)."""


class NodeNotFoundError(DeclarativeError):
    """Node name not found in the registry."""


class RouterNotFoundError(DeclarativeError):
    """Router name not found in the registry."""


class ToolNotFoundError(DeclarativeError):
    """Tool name not found in the registry or via import path."""


def suggest_similar(name: str, available: list[str], n: int = 3) -> list[str]:
    """Return up to *n* close matches for *name* from *available* names.

    Uses ``difflib.get_close_matches`` with the default cutoff (0.6).
    """
    return difflib.get_close_matches(name, available, n=n)


def format_not_found(kind: str, name: str, available: list[str]) -> str:
    """Format a helpful 'not found' message with suggestions.

    Args:
        kind: What was being looked up (e.g. "node", "router").
        name: The name that was not found.
        available: List of valid names to suggest from.

    Returns:
        A human-readable error message.
    """
    msg = f"{kind} '{name}' not found."
    suggestions = suggest_similar(name, available)
    if suggestions:
        quoted = ", ".join(f"'{s}'" for s in suggestions)
        msg += f" Did you mean: {quoted}?"
    elif available:
        quoted = ", ".join(f"'{s}'" for s in sorted(available))
        msg += f" Available {kind}s: {quoted}."
    return msg
