"""Subgraph composition (v2): embed one YAML workflow inside another.

workflow.yaml declares the node `research` with `subgraph: "research_subgraph.yaml"`.
The child file is compiled into its own graph and embedded as a single node.
Parent and child share the "messages" state key, so updates flow through.

All node functions — parent's and child's — come from the same registry.
"""

from pathlib import Path

from langgraph_declarative import Registry, build_graph

registry = Registry()


# --- Parent nodes ---


@registry.node("intro_step")
def intro_step(state):
    return {"messages": [{"role": "assistant", "content": "[parent] starting research task"}]}


@registry.node("outro_step")
def outro_step(state):
    return {"messages": [{"role": "assistant", "content": "[parent] research task complete"}]}


# --- Child (subgraph) nodes ---


@registry.node("gather_sources")
def gather_sources(state):
    return {"messages": [{"role": "assistant", "content": "[child] gathered 3 sources"}]}


@registry.node("condense_findings")
def condense_findings(state):
    return {"messages": [{"role": "assistant", "content": "[child] condensed findings into a brief"}]}


graph = build_graph(Path(__file__).with_name("workflow.yaml"), registry)

result = graph.invoke({"messages": [{"role": "user", "content": "Research LangGraph"}]})

print("Subgraph example — parent embeds research_subgraph.yaml:\n")
for msg in result["messages"]:
    print(f"  {msg.type}: {msg.content}")
