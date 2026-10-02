"""Compile YAML ``state:`` declarations into LangGraph-compatible TypedDict classes.

Core technique: dynamically create ``typing.Annotated[type, reducer]`` fields
and assemble them into a TypedDict (functional form) that LangGraph accepts
as a state annotation.
"""

from __future__ import annotations

import operator
import sys
import warnings
from typing import Annotated, Any, TypedDict

from pydantic import Field, field_validator

from langgraph_declarative._base import StrictModel
from langgraph_declarative.errors import format_not_found

# YAML type name → Python type used in the state annotation.
_TYPE_MAP: dict[str, Any] = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
    "list[str]": list[str],
    "list[dict]": list[dict],
}

# Valid reducer names. "replace" means no reducer annotation (LangGraph default).
_REDUCER_NAMES = ("add_messages", "append", "replace")


class StateFieldConfig(StrictModel):
    """A single state field declaration from the YAML ``state:`` section."""

    name: str
    type: str
    # Deprecated (ADR-010): LangGraph never applies it. Marked in the JSON
    # Schema so IDEs flag it; build_state_class() warns at build time.
    default: Any | None = Field(default=None, json_schema_extra={"deprecated": True})
    reducer: str = "replace"

    @field_validator("type")
    @classmethod
    def _validate_type(cls, v: str) -> str:
        if v not in _TYPE_MAP:
            raise ValueError(format_not_found("state type", v, list(_TYPE_MAP)))
        return v

    @field_validator("reducer")
    @classmethod
    def _validate_reducer(cls, v: str) -> str:
        if v not in _REDUCER_NAMES:
            raise ValueError(format_not_found("reducer", v, list(_REDUCER_NAMES)))
        return v


def _resolve_reducer(name: str):
    """Map a reducer name to its callable. ``replace`` → None (no annotation)."""
    if name == "add_messages":
        # Lazy import: keeps module importable if langgraph internals move.
        from langgraph.graph import add_messages

        return add_messages
    if name == "append":
        return operator.add
    return None


def _external_stacklevel() -> int:
    """``stacklevel`` that attributes a warning to the first caller outside
    this package, so a script calling ``build_graph()`` actually sees it
    (``DeprecationWarning`` is only shown by default when raised in ``__main__``).
    """
    # Match on module name, not file path: paths differ under symlinked venvs.
    package = __name__.split(".")[0]
    frame = sys._getframe(2)  # the caller of the function that warns
    level = 2
    while frame is not None and (
        frame.f_globals.get("__name__", "").split(".")[0] == package
    ):
        frame = frame.f_back
        level += 1
    return level


def build_state_class(
    fields: list[StateFieldConfig], name: str = "DeclaredState"
) -> type:
    """Build a TypedDict state class from validated field configs.

    Fields with a reducer get an ``Annotated[type, reducer]`` annotation so
    LangGraph merges updates instead of overwriting them.

    Declared ``default:`` values are deprecated (ADR-010): LangGraph never
    applies them, so a node reading the field still finds it missing. They are
    kept on ``__field_defaults__`` for introspection only, and setting one
    emits a ``DeprecationWarning``.
    """
    defaulted = [f.name for f in fields if f.default is not None]
    if defaulted:
        names = ", ".join(f"'{n}'" for n in defaulted)
        warnings.warn(
            f"state field(s) {names} set 'default:', which is deprecated and has "
            "no runtime effect — LangGraph does not apply state defaults, so the "
            "field is absent until the graph input or a node writes it. "
            "Initialise it there instead. The value remains available on "
            "__field_defaults__ for introspection.",
            DeprecationWarning,
            stacklevel=_external_stacklevel(),
        )

    annotations: dict[str, Any] = {}
    for field in fields:
        py_type = _TYPE_MAP[field.type]
        reducer = _resolve_reducer(field.reducer)
        annotations[field.name] = (
            Annotated[py_type, reducer] if reducer is not None else py_type
        )

    state_cls = TypedDict(name, annotations)  # type: ignore[operator]
    state_cls.__field_defaults__ = {
        f.name: f.default for f in fields if f.default is not None
    }
    return state_cls
