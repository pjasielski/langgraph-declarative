"""Decorator-based registry for node and router functions."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from langgraph_declarative.errors import (
    NodeNotFoundError,
    RouterNotFoundError,
    format_not_found,
)


class Registry:
    """Store and look up node/router functions by name.

    Maintains two separate namespaces so that a typo in a YAML ``path:``
    field cannot silently resolve to a node function (and vice-versa).
    """

    def __init__(self) -> None:
        self._nodes: dict[str, Callable] = {}
        self._routers: dict[str, Callable] = {}

    # -- decorators --

    def node(self, name: str) -> Callable:
        """Decorator: register a node function.

        >>> registry = Registry()
        >>> @registry.node("greet")
        ... def greet(state):
        ...     return {"messages": ["hello"]}
        """

        def decorator(fn: Callable) -> Callable:
            if name in self._nodes:
                raise ValueError(f"Duplicate node name: '{name}'")
            self._nodes[name] = fn
            return fn

        return decorator

    def router(self, name: str) -> Callable:
        """Decorator: register a router function.

        >>> registry = Registry()
        >>> @registry.router("route_by_type")
        ... def route_by_type(state):
        ...     return "branch_a"
        """

        def decorator(fn: Callable) -> Callable:
            if name in self._routers:
                raise ValueError(f"Duplicate router name: '{name}'")
            self._routers[name] = fn
            return fn

        return decorator

    # -- lookups --

    def get_node(self, name: str) -> Callable:
        """Look up a node by name. Raises ``NodeNotFoundError`` with suggestions."""
        try:
            return self._nodes[name]
        except KeyError:
            raise NodeNotFoundError(
                format_not_found("node", name, list(self._nodes))
            ) from None

    def get_router(self, name: str) -> Callable:
        """Look up a router by name. Raises ``RouterNotFoundError`` with suggestions."""
        try:
            return self._routers[name]
        except KeyError:
            raise RouterNotFoundError(
                format_not_found("router", name, list(self._routers))
            ) from None

    # -- listing --

    def list_nodes(self) -> list[str]:
        """Return all registered node names."""
        return list(self._nodes)

    def list_routers(self) -> list[str]:
        """Return all registered router names."""
        return list(self._routers)
