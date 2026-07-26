"""Decorator-based registry for node and router functions."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from langgraph_declarative.errors import (
    NodeNotFoundError,
    RouterNotFoundError,
    ToolNotFoundError,
    format_not_found,
)


class Registry:
    """Store and look up node/router/tool functions by name.

    Maintains separate namespaces so that a typo in a YAML ``path:``
    field cannot silently resolve to a node function (and vice-versa).
    """

    def __init__(self) -> None:
        self._nodes: dict[str, Callable] = {}
        self._routers: dict[str, Callable] = {}
        self._tools: dict[str, Any] = {}

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

    def tool(self, name: str) -> Callable:
        """Decorator: register a tool (LangChain tool object or plain callable).

        >>> registry = Registry()
        >>> @registry.tool("calculator")
        ... def calculator(expression: str) -> str:
        ...     '''Evaluate a math expression.'''
        ...     return "42"
        """

        def decorator(obj: Any) -> Any:
            if name in self._tools:
                raise ValueError(f"Duplicate tool name: '{name}'")
            self._tools[name] = obj
            return obj

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

    def get_tool(self, name: str) -> Any:
        """Look up a tool by name. Raises ``ToolNotFoundError`` with suggestions."""
        try:
            return self._tools[name]
        except KeyError:
            raise ToolNotFoundError(
                format_not_found("tool", name, list(self._tools))
            ) from None

    # -- listing --

    def list_nodes(self) -> list[str]:
        """Return all registered node names."""
        return list(self._nodes)

    def list_routers(self) -> list[str]:
        """Return all registered router names."""
        return list(self._routers)

    def list_tools(self) -> list[str]:
        """Return all registered tool names."""
        return list(self._tools)
