"""LLM config + tools in YAML (v2): nodes receive a pre-configured LLM.

The opt-in contract: a node function that accepts an `llm` keyword parameter
gets a ready-made LangChain chat model injected, built from the YAML config
(graph-level default, merged with any node-level override) with the node's
`tools:` already bound via bind_tools().

This example makes real API calls, so it needs:
    pip install "langgraph-declarative[anthropic]"   # langchain-anthropic
    export ANTHROPIC_API_KEY=...
It exits with instructions when either is missing.
"""

import os
import sys
from pathlib import Path

try:
    import langchain_anthropic  # noqa: F401
except ImportError:
    print("This example needs the anthropic extra:")
    print('  pip install "langgraph-declarative[anthropic]"')
    sys.exit(0)

if not os.environ.get("ANTHROPIC_API_KEY"):
    print("This example calls the Anthropic API. Set ANTHROPIC_API_KEY and re-run.")
    sys.exit(0)

from langchain_core.messages import ToolMessage

from langgraph_declarative import Registry, build_graph

registry = Registry()


@registry.tool("get_weather")
def get_weather(city: str) -> str:
    """Return the current weather for a city."""
    return f"Sunny, 22°C in {city}"


@registry.node("weather_agent")
def weather_agent(state, llm=None):
    """`llm=None` in the signature is the opt-in. At runtime `llm` is a
    ChatAnthropic instance (claude-opus-4-8 from the graph-level config)
    with get_weather bound to it."""
    response = llm.invoke(state["messages"])
    new_messages = [response]
    while response.tool_calls:
        for call in response.tool_calls:
            result = get_weather(**call["args"])
            new_messages.append(ToolMessage(content=result, tool_call_id=call["id"]))
        response = llm.invoke(state["messages"] + new_messages)
        new_messages.append(response)
    return {"messages": new_messages}


@registry.node("summarize_chat")
def summarize_chat(state, llm=None):
    """Here `llm` is claude-haiku-4-5 — the node-level override merged over
    the graph default (provider kept, model and max_tokens replaced)."""
    prompt = state["messages"] + [
        {"role": "user", "content": "Summarize this conversation in one sentence."}
    ]
    return {"messages": [llm.invoke(prompt)]}


graph = build_graph(Path(__file__).with_name("workflow.yaml"), registry)

result = graph.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in Warsaw?"}]}
)

print("LLM + tools example:\n")
for msg in result["messages"]:
    text = msg.content if isinstance(msg.content, str) else str(msg.content)
    print(f"  {msg.type}: {text[:120]}")
