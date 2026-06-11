"""Fan-out: run parallel analyses on the same data, then merge results."""

from pathlib import Path

from langgraph_declarative import Registry, build_graph

registry = Registry()


@registry.node("load_data")
def load_data(state):
    return {"messages": [{"role": "assistant", "content": "[loaded] The product is excellent but shipping was slow."}]}


@registry.node("analyze_sentiment")
def analyze_sentiment(state):
    return {"messages": [{"role": "assistant", "content": "[sentiment] mixed — positive product, negative shipping"}]}


@registry.node("extract_keywords")
def extract_keywords(state):
    return {"messages": [{"role": "assistant", "content": "[keywords] product, excellent, shipping, slow"}]}


@registry.node("summarize")
def summarize(state):
    return {"messages": [{"role": "assistant", "content": "[summary] Analysis complete with sentiment and keywords."}]}


graph = build_graph(Path(__file__).with_name("workflow.yaml"), registry)

result = graph.invoke({"messages": [{"role": "user", "content": "Analyze this review"}]})

print("Fan-out example — parallel analysis pipeline:\n")
for msg in result["messages"]:
    print(f"  {msg.type}: {msg.content}")
