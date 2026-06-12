"""Visualization & IDE support (v1.1): Mermaid diagrams and JSON Schema export.

Two developer-experience features:

1. draw_mermaid() — compile the workflow and return its Mermaid diagram
   source. Pass output_path= to also write a file (a `.md` path produces a
   fenced ```mermaid block that GitHub renders; any other suffix gets raw
   Mermaid text).

2. export_json_schema() — emit the JSON Schema for workflow YAML files so
   IDEs can validate and autocomplete them. The repository ships the schema
   at schema/workflow.schema.json; workflow.yaml here references it via the
   `# yaml-language-server: $schema=...` modeline on its first line.
"""

from pathlib import Path

from langgraph_declarative import Registry, draw_mermaid, export_json_schema

registry = Registry()


@registry.node("draft")
def draft(state):
    return {"messages": [{"role": "assistant", "content": "[draft v2]"}], "approved": False}


@registry.node("review")
def review(state):
    return {"approved": True}


@registry.node("publish")
def publish(state):
    return {"messages": [{"role": "assistant", "content": "[published]"}]}


# 1. Mermaid: render the compiled graph as a diagram.
#    To write it to a file instead: draw_mermaid(path, registry, output_path="graph.md")
mermaid = draw_mermaid(Path(__file__).with_name("workflow.yaml"), registry)
print("Mermaid source for this workflow:\n")
print(mermaid)

# 2. JSON Schema: regenerate the IDE schema (this is how schema/workflow.schema.json
#    is produced). Pass output_path= to write it to disk.
schema = export_json_schema()
print("JSON Schema title:", schema["title"])
print("Top-level properties:", ", ".join(schema["properties"]))
