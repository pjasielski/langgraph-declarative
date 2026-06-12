"""Match routing (v1.1): route on a state field value, no Python router needed.

Compare with examples/conditional_routing, where routing requires a Python
function registered with @registry.router(). With `match:`, the classifier
node writes a routing key into state and the YAML maps values to targets —
the router function disappears.
"""

from pathlib import Path

from langgraph_declarative import Registry, build_graph

registry = Registry()


@registry.node("classify")
def classify(state):
    """Write the routing key into state — the match edge reads it."""
    content = state["messages"][-1].content.lower()
    if any(w in content for w in ["invoice", "refund", "charge"]):
        category = "billing"
    elif any(w in content for w in ["error", "crash", "bug"]):
        category = "technical"
    else:
        category = "other"  # not in targets → falls through to "default"
    return {"category": category}


@registry.node("handle_billing")
def handle_billing(state):
    return {"messages": [{"role": "assistant", "content": "Billing team here — let's look at your invoice."}]}


@registry.node("handle_technical")
def handle_technical(state):
    return {"messages": [{"role": "assistant", "content": "Tech support here — can you share the error log?"}]}


@registry.node("handle_general")
def handle_general(state):
    return {"messages": [{"role": "assistant", "content": "Thanks for reaching out! How can we help?"}]}


graph = build_graph(Path(__file__).with_name("workflow.yaml"), registry)

for user_msg in ["I want a refund", "The app crashes on startup", "Hello!"]:
    result = graph.invoke({"messages": [{"role": "user", "content": user_msg}]})
    print(f"'{user_msg}' → [{result['category']}] {result['messages'][-1].content}")
