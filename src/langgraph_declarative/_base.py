"""Shared Pydantic base for every workflow config model."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class StrictModel(BaseModel):
    """Rejects unknown keys (ADR-007).

    A misspelled key is otherwise accepted and does nothing — with HITL, a typo
    in ``interrupt_before`` silently removes an approval gate.
    """

    model_config = ConfigDict(extra="forbid")
