"""Quickstart: build a simple linear graph from YAML."""

from pathlib import Path

from langgraph_declarative import Registry, build_graph

# 1. Create a registry and register your node functions
registry = Registry()


@registry.node("greet")
def greet(state):
    """Add a greeting message to state."""
    return {"messages": [{"role": "assistant", "content": "Hello! How can I help you?"}]}


@registry.node("respond")
def respond(state):
    """Add a response message to state."""
    return {"messages": [{"role": "assistant", "content": "Goodbye!"}]}


# 2. Build the graph from YAML + registry
graph = build_graph(Path(__file__).with_name("workflow.yaml"), registry)

# 3. Invoke the graph
result = graph.invoke({"messages": [{"role": "user", "content": "Hi there"}]})

for msg in result["messages"]:
    print(f"{msg.type}: {msg.content}")
