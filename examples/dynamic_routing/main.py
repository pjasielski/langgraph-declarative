"""Dynamic routing with Send: fan out to a variable number of workers at runtime.

The TaskState TypedDict below could also be declared in YAML since v1.1
(`state:` with `reducer: append` for the results field — see
examples/declared_state). It stays in Python here to show the v1
`state_class=` approach alongside Send-based routing.
"""

from __future__ import annotations

import operator
from pathlib import Path
from typing import Annotated, TypedDict

from langgraph.types import Send

from langgraph_declarative import Registry, build_graph

registry = Registry()


class TaskState(TypedDict):
    tasks: list[str]
    results: Annotated[list[str], operator.add]


@registry.node("split_tasks")
def split_tasks(state):
    return {"results": [f"splitting {len(state['tasks'])} tasks..."]}


@registry.router("dispatch_tasks")
def dispatch_tasks(state) -> list[Send]:
    """Dynamically create one worker per task — number determined at runtime."""
    return [
        Send("worker", {"tasks": [], "results": [task]})
        for task in state["tasks"]
    ]


@registry.node("process_task")
def process_task(state):
    task_name = state["results"][-1]
    return {"results": [f"done: {task_name}"]}


graph = build_graph(
    Path(__file__).with_name("workflow.yaml"),
    registry,
    state_class=TaskState,
)

result = graph.invoke({"tasks": ["clean data", "train model", "evaluate"], "results": []})

print("Dynamic routing (Send) example — runtime fan-out:\n")
for r in result["results"]:
    print(f"  {r}")
