"""Conditional routing: route messages to different handlers based on intent.

A Python router function (@registry.router) gives you arbitrary routing
logic. Since v1.1 there is a lighter alternative for the common case of
routing on a single state field's value: `match:` routing, which needs no
Python function at all (see examples/match_routing).
"""

from pathlib import Path

from langgraph_declarative import Registry, build_graph

registry = Registry()


# --- Node functions ---


@registry.node("classify")
def classify(state):
    """Classify the user's intent (simplified for demo)."""
    last_msg = state["messages"][-1]
    content = last_msg.content.lower()
    if "?" in content:
        intent = "question"
    elif any(w in content for w in ["bad", "broken", "issue", "problem"]):
        intent = "complaint"
    else:
        intent = "other"
    return {"messages": [{"role": "assistant", "content": f"[classified as: {intent}]"}]}


@registry.node("answer_question")
def answer_question(state):
    return {"messages": [{"role": "assistant", "content": "Let me answer your question..."}]}


@registry.node("handle_complaint")
def handle_complaint(state):
    return {"messages": [{"role": "assistant", "content": "I'm sorry to hear that. Let me help resolve this."}]}


@registry.node("handle_other")
def handle_other(state):
    return {"messages": [{"role": "assistant", "content": "Thanks for reaching out!"}]}


# --- Router function ---


@registry.router("intent_router")
def intent_router(state):
    """Inspect the classification and return the routing key."""
    last_msg = state["messages"][-1]
    content = last_msg.content
    if "question" in content:
        return "question"
    elif "complaint" in content:
        return "complaint"
    return "other"


# --- Run ---

graph = build_graph(Path(__file__).with_name("workflow.yaml"), registry)

# Try different inputs to see different paths
for user_msg in ["What is LangGraph?", "This is broken!", "Hello there"]:
    print(f"\n--- Input: '{user_msg}' ---")
    result = graph.invoke({"messages": [{"role": "user", "content": user_msg}]})
    for msg in result["messages"]:
        print(f"  {msg.type}: {msg.content}")
