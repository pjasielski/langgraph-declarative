"""Declared state (v1.1): define state fields, types, and reducers in YAML.

Compare with examples/custom_state, which builds the same kind of pipeline
with a hand-written Python TypedDict passed as `state_class=`. Here the YAML
`state:` section replaces that class entirely.

Note: when the YAML declares `state:`, it always wins — passing `state_class=`
to build_graph() alongside it is ignored (with a UserWarning).
"""

from pathlib import Path

from langgraph_declarative import Registry, build_graph

registry = Registry()


@registry.node("load_document")
def load_document(state):
    return {"notes": ["loaded document"]}


@registry.node("compute_stats")
def compute_stats(state):
    words = len(state["document"].split())
    return {"notes": [f"stats: {words} words"]}


@registry.node("extract_tags")
def extract_tags(state):
    tags = [w.strip(".,") for w in state["document"].split() if w.istitle()]
    return {"notes": [f"tags: {', '.join(tags)}"]}


@registry.node("summarize")
def summarize(state):
    return {"summary": f"Analysis finished with {len(state['notes'])} notes."}


graph = build_graph(Path(__file__).with_name("workflow.yaml"), registry)

result = graph.invoke({
    "document": "LangGraph Declarative makes Graph definitions simple.",
    "notes": [],
    "summary": "",
})

print("Declared state example — state schema defined in YAML:\n")
for note in result["notes"]:
    print(f"  - {note}")
print(f"\n  {result['summary']}")
