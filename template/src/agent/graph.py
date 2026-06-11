"""Compile the YAML workflow into a runnable graph.

LangGraph Studio / `langgraph dev` discovers the `graph` object via
langgraph.json.
"""

from pathlib import Path

from langgraph_declarative import build_graph

from agent.nodes import registry

graph = build_graph(Path(__file__).parent / "workflow.yaml", registry)


if __name__ == "__main__":
    result = graph.invoke({"messages": [{"role": "user", "content": "Hello!"}]})
    for message in result["messages"]:
        print(f"{message.type}: {message.content}")
