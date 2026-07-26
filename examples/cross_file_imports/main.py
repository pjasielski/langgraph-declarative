"""Cross-file imports (v2): share node declarations between workflows.

workflow.yaml imports the `error_handler` node from shared_nodes.yaml.
Imports merge node *declarations* only — the underlying function
(`handle_error`) is still registered here like any other node function.
"""

from pathlib import Path

from langgraph_declarative import Registry, build_graph

registry = Registry()


@registry.node("process_order")
def process_order(state):
    order = state["messages"][-1].content
    status = "ok" if "valid" in order else "failed"
    return {"status": status}


@registry.node("confirm_order")
def confirm_order(state):
    return {"messages": [{"role": "assistant", "content": "Order confirmed!"}]}


# Backs the node imported from shared_nodes.yaml
@registry.node("handle_error")
def handle_error(state):
    return {"messages": [{"role": "assistant", "content": "Something went wrong — order routed to support."}]}


graph = build_graph(Path(__file__).with_name("workflow.yaml"), registry)

for order in ["valid order #123", "corrupted order"]:
    result = graph.invoke({"messages": [{"role": "user", "content": order}]})
    print(f"'{order}' → {result['messages'][-1].content}")
