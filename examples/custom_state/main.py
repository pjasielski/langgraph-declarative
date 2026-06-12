"""Custom state: data processing pipeline without MessagesState.

This example passes a hand-written Python TypedDict via `state_class=` — the
v1 approach, still fully supported and the right choice when you need types
or reducers beyond what YAML can express. Since v1.1 the same schema can be
declared directly in YAML with a `state:` section (see examples/declared_state).
Note: if the YAML declares `state:`, it wins over `state_class=` (a UserWarning
is emitted).
"""

from __future__ import annotations

from pathlib import Path
from typing import TypedDict

from langgraph_declarative import Registry, build_graph

registry = Registry()


class PipelineState(TypedDict):
    raw_values: list[float]
    cleaned: list[float]
    is_valid: bool
    run_count: int


@registry.node("ingest_data")
def ingest_data(state):
    return {
        "cleaned": [],
        "is_valid": False,
        "run_count": state.get("run_count", 0) + 1,
    }


@registry.node("validate_data")
def validate_data(state):
    values = state["raw_values"]
    is_valid = len(values) > 0 and all(isinstance(v, (int, float)) for v in values)
    return {"is_valid": is_valid}


@registry.router("validation_router")
def validation_router(state) -> str:
    return "valid" if state["is_valid"] else "invalid"


@registry.node("transform_data")
def transform_data(state):
    values = state["raw_values"]
    normalized = [(v - min(values)) / (max(values) - min(values)) for v in values]
    return {"cleaned": normalized}


graph = build_graph(
    Path(__file__).with_name("workflow.yaml"),
    registry,
    state_class=PipelineState,
)

input_data = {"raw_values": [10.0, 20.0, 30.0, 40.0, 50.0], "cleaned": [], "is_valid": False, "run_count": 0}
result = graph.invoke(input_data)

print("Custom state example — data processing pipeline:\n")
print(f"  Input:      {input_data['raw_values']}")
print(f"  Normalized: {[round(v, 2) for v in result['cleaned']]}")
print(f"  Valid:      {result['is_valid']}")
print(f"  Runs:       {result['run_count']}")
