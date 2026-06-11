"""Node implementations — pure Python logic, referenced by name from workflow.yaml."""

from langgraph_declarative import Registry

registry = Registry()


@registry.node("understand_request")
def understand_request(state):
    """Inspect the incoming request. Replace with your own logic (or an LLM call)."""
    return {"messages": [{"role": "assistant", "content": "Understood the request."}]}


@registry.node("generate_response")
def generate_response(state):
    """Produce the main answer. Swap in an LLM call here."""
    return {"messages": [{"role": "assistant", "content": "Here is my response."}]}


@registry.node("finalize_answer")
def finalize_answer(state):
    """Post-process / format the final answer."""
    return {"messages": [{"role": "assistant", "content": "Done."}]}
