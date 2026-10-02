"""Human-in-the-loop: pause for approval before a write, then accept or reject.

Runs offline — the "agent" is a deterministic stub, so the example is about the
approval mechanism rather than about an LLM.

    python examples/human_in_the_loop/main.py
"""

from pathlib import Path

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END
from langgraph.types import Command, interrupt

from langgraph_declarative import Registry, build_graph

# The side effect the approval gate protects. In a real system this is a
# database write, a file edit, or an outbound API call.
DATABASE: dict[str, str] = {}

registry = Registry()


@registry.node("agent")
def agent(state):
    """Stub agent — a real one would decide this from an LLM tool call."""
    return {"log": [f"agent received a '{state['request']}' request"]}


@registry.node("read_file")
def read_file(state):
    """Read-only tool. Runs freely: nothing to approve."""
    return {"log": [f"read the file (db currently holds {len(DATABASE)} records)"]}


@registry.node("approval")
def approval(state):
    """Pause and hand control to the human.

    `interrupt()` suspends the run here and persists state via the checkpointer.
    The value passed in is what the caller sees in `__interrupt__`; whatever the
    caller later resumes with becomes this call's return value.
    """
    decision = interrupt({"question": "Approve writing to the database?"})

    if decision == "accept":
        return Command(goto="execute", update={"log": ["human approved"]})
    # In Python, use LangGraph's END constant. The string "END" is only
    # translated inside YAML; Command(goto="END") would name a node that
    # does not exist.
    return Command(goto=END, update={"log": ["human rejected — nothing written"]})


@registry.node("execute")
def execute(state):
    """The gated write. Reachable only through an approved resume."""
    DATABASE["record"] = "written"
    return {"log": ["write committed"]}


# The checkpointer is what makes pause/resume possible — and it is supplied by
# you, never defaulted by the library. See the note at the bottom of this file.
graph = build_graph(
    Path(__file__).with_name("workflow.yaml"),
    registry,
    checkpointer=InMemorySaver(),
)


def show(label, state):
    print(f"\n{label}")
    for entry in state.get("log", []):
        print(f"  · {entry}")
    print(f"  DATABASE = {DATABASE}")


def main():
    print("=" * 62)
    print("1. READ REQUEST — read-only, should not pause")
    print("=" * 62)
    cfg = {"configurable": {"thread_id": "read-1"}}
    show("result:", graph.invoke({"request": "read", "log": []}, cfg))

    print("\n" + "=" * 62)
    print("2. WRITE REQUEST, REJECTED — must not touch the database")
    print("=" * 62)
    cfg = {"configurable": {"thread_id": "write-reject"}}
    paused = graph.invoke({"request": "write", "log": []}, cfg)
    print(f"\npaused: {paused['__interrupt__'][0].value['question']}")
    show("after reject:", graph.invoke(Command(resume="reject"), cfg))
    assert "record" not in DATABASE, "rejection must leave the database untouched"

    print("\n" + "=" * 62)
    print("3. WRITE REQUEST, ACCEPTED — the write happens")
    print("=" * 62)
    cfg = {"configurable": {"thread_id": "write-accept"}}
    paused = graph.invoke({"request": "write", "log": []}, cfg)
    print(f"\npaused: {paused['__interrupt__'][0].value['question']}")
    show("after accept:", graph.invoke(Command(resume="accept"), cfg))
    assert DATABASE["record"] == "written", "approval must produce the write"

    print("\n" + "=" * 62)
    print("Diagram — `approval` shows both routes: execute (accept) and END (reject)")
    print("=" * 62)
    print(graph.get_graph().draw_mermaid())

    print("A note on checkpointers".center(62, "-"))
    print(
        "This example owns its checkpointer because it runs in its own process.\n"
        "Under `langgraph dev` / LangGraph Platform the *server* owns persistence\n"
        "and a checkpointer passed at compile time is silently ignored — which is\n"
        "why this library never supplies one for you. A built-in default would\n"
        "appear to work locally and quietly do nothing once deployed."
    )


if __name__ == "__main__":
    main()
