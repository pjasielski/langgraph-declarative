"""Database-driven workflows (v2): load graph definitions from SQLite.

SQLiteLoader stores workflow definitions (as YAML/JSON text) with per-source
version tracking — workflows can be created and updated at runtime without
deploying files. The database holds the *topology* only; node functions still
come from the registry.

Source syntax: "support_flow" loads the latest version, "support_flow@1"
pins an explicit version.
"""

import tempfile
from pathlib import Path

from langgraph_declarative import Registry, SQLiteLoader, build_graph_from_db

registry = Registry()


@registry.node("triage_ticket")
def triage_ticket(state):
    return {"messages": [{"role": "assistant", "content": "[triage] ticket categorized"}]}


@registry.node("resolve_ticket")
def resolve_ticket(state):
    return {"messages": [{"role": "assistant", "content": "[resolve] ticket closed"}]}


@registry.node("notify_customer")
def notify_customer(state):
    return {"messages": [{"role": "assistant", "content": "[notify] customer emailed"}]}


# v1 of the workflow: triage → resolve
DEFINITION_V1 = {
    "nodes": [
        {"name": "triage", "function": "triage_ticket"},
        {"name": "resolve", "function": "resolve_ticket"},
    ],
    "edges": [
        {"source": "START", "target": "triage"},
        {"source": "triage", "target": "resolve"},
        {"source": "resolve", "target": "END"},
    ],
}

# v2 adds a notification step — saved at runtime, no file deployment.
DEFINITION_V2 = {
    "nodes": DEFINITION_V1["nodes"] + [{"name": "notify", "function": "notify_customer"}],
    "edges": [
        {"source": "START", "target": "triage"},
        {"source": "triage", "target": "resolve"},
        {"source": "resolve", "target": "notify"},
        {"source": "notify", "target": "END"},
    ],
}

with tempfile.TemporaryDirectory() as tmp:
    db_path = Path(tmp) / "workflows.db"
    loader = SQLiteLoader(db_path)

    # Definitions can be dicts or raw YAML/JSON strings; save() returns the version.
    loader.save("support_flow", DEFINITION_V1)
    loader.save("support_flow", DEFINITION_V2)
    print(f"Stored versions of 'support_flow': {loader.versions('support_flow')}\n")

    for source in ["support_flow@1", "support_flow"]:  # pinned vs latest
        graph = build_graph_from_db(source, registry, db_path)
        result = graph.invoke({"messages": [{"role": "user", "content": "My order is broken"}]})
        steps = [m.content for m in result["messages"][1:]]
        print(f"{source:>16}: {' → '.join(steps)}")
