"""Human-in-the-loop behaviour — pause, resume, and the side effects that follow.

These tests assert the *side effect*, not the return status. A graph that returns
cleanly while having written nothing — or having written despite a rejection —
passes a status-code test and fails the only thing that matters.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, interrupt

from langgraph_declarative import Registry, build_graph, draw_mermaid
from langgraph_declarative.errors import ConfigValidationError

FIXTURES = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# Shared HITL graph: read-only tools run freely, write tools need approval
# ---------------------------------------------------------------------------


def _hitl_registry(audit: dict):
    """Registry for hitl_workflow.yaml.

    ``audit`` is the observable side effect — the "database write" the approval
    gate is protecting. Nothing else mutates it.
    """
    reg = Registry()

    @reg.node("agent")
    def agent(state):
        # `action` is set by the caller's input; the agent just passes it along.
        return {"log": ["agent"]}

    @reg.node("read_tool")
    def read_tool(state):
        # Read-only: runs freely, no approval needed.
        return {"log": ["read"]}

    @reg.node("approval")
    def approval(state):
        decision = interrupt({"question": "Approve this write?"})
        if decision == "accept":
            return Command(goto="execute", update={"log": ["approved"]})
        return Command(goto="END", update={"log": ["rejected"]})

    @reg.node("execute")
    def execute(state):
        # The gated side effect. Reachable only via an approved resume.
        audit["written"] = True
        audit["writes"] = audit.get("writes", 0) + 1
        return {"log": ["executed"]}

    return reg


def _build_hitl(audit: dict, checkpointer=None):
    return build_graph(
        FIXTURES / "hitl_workflow.yaml",
        _hitl_registry(audit),
        checkpointer=checkpointer,
    )


class TestApprovalGate:
    """The capability: a write pauses for a human and honours their answer."""

    def test_write_path_pauses(self):
        audit = {}
        graph = _build_hitl(audit, InMemorySaver())
        cfg = {"configurable": {"thread_id": "t-pause"}}

        out = graph.invoke({"action": "write"}, cfg)

        assert "__interrupt__" in out, "write path must pause for approval"
        assert audit.get("written") is not True, (
            "nothing may be written before a human approves"
        )

    def test_resume_accept_performs_the_write(self):
        audit = {}
        graph = _build_hitl(audit, InMemorySaver())
        cfg = {"configurable": {"thread_id": "t-accept"}}

        graph.invoke({"action": "write"}, cfg)
        result = graph.invoke(Command(resume="accept"), cfg)

        assert audit.get("written") is True, "accept must produce the side effect"
        assert audit["writes"] == 1
        assert "executed" in result["log"]

    def test_resume_reject_leaves_side_effect_untouched(self):
        audit = {}
        graph = _build_hitl(audit, InMemorySaver())
        cfg = {"configurable": {"thread_id": "t-reject"}}

        graph.invoke({"action": "write"}, cfg)
        result = graph.invoke(Command(resume="reject"), cfg)

        # The assertion that matters: a clean return is not enough.
        assert "written" not in audit, "reject must NOT produce the side effect"
        assert "rejected" in result["log"]
        assert "executed" not in result["log"]

    def test_read_path_runs_without_pausing(self):
        audit = {}
        graph = _build_hitl(audit, InMemorySaver())
        cfg = {"configurable": {"thread_id": "t-read"}}

        out = graph.invoke({"action": "read"}, cfg)

        assert "__interrupt__" not in out, "read-only tools must not be gated"
        assert "read" in out["log"]
        assert "written" not in audit


class TestThreadPersistence:
    """State must survive across turns, scoped by thread_id."""

    def test_state_survives_across_turns_on_one_thread(self):
        audit = {}
        graph = _build_hitl(audit, InMemorySaver())
        cfg = {"configurable": {"thread_id": "t-persist"}}

        graph.invoke({"action": "write"}, cfg)
        # A separate invocation, later in time — it must see the earlier state.
        result = graph.invoke(Command(resume="accept"), cfg)

        assert "agent" in result["log"], "state from the first turn must persist"
        assert graph.get_state(cfg).values["log"], "checkpoint must be readable"

    def test_threads_are_isolated(self):
        audit = {}
        graph = _build_hitl(audit, InMemorySaver())
        a = {"configurable": {"thread_id": "thread-a"}}
        b = {"configurable": {"thread_id": "thread-b"}}

        graph.invoke({"action": "write"}, a)
        graph.invoke({"action": "read"}, b)

        # Thread A is still paused; thread B finished independently.
        assert graph.get_state(a).next, "thread A must still be paused"
        assert not graph.get_state(b).next, "thread B must have completed"


class TestBackwardCompatibility:
    """Omitting a checkpointer must behave exactly as before."""

    def test_graph_without_checkpointer_still_builds_and_runs(self):
        audit = {}
        graph = _build_hitl(audit)  # no checkpointer

        out = graph.invoke({"action": "read"})

        assert "read" in out["log"]

    def test_no_checkpointer_means_no_persistence(self):
        audit = {}
        graph = _build_hitl(audit)
        with pytest.raises(Exception):
            # Without a checkpointer there is no thread state to read.
            graph.get_state({"configurable": {"thread_id": "nope"}})

    def test_existing_fixture_unaffected(self):
        reg = Registry()

        @reg.node("greet")
        def greet(state):
            return {"messages": []}

        @reg.node("respond")
        def respond(state):
            return {"messages": []}

        graph = build_graph(FIXTURES / "simple.yaml", reg)
        assert graph is not None


class TestCheckpointerNotDefaulted:
    """ADR-004: a default checkpointer would be silently ignored on Platform."""

    def test_builder_has_no_checkpointer_by_default(self):
        from langgraph_declarative import GraphBuilder

        builder = GraphBuilder(Registry())
        assert builder.checkpointer is None
        assert builder.store is None


class TestSubgraphInheritsParentCheckpointer:
    """ADR-005: subgraphs compile without persistence; the parent's covers them."""

    def test_interrupt_inside_subgraph_resumes(self, tmp_path):
        child = tmp_path / "child.yaml"
        child.write_text(
            """
state:
  - name: "log"
    type: "list[str]"
    reducer: "append"
nodes:
  - name: "inner"
    function: "inner"
edges:
  - source: "START"
    target: "inner"
  - source: "inner"
    target: "END"
""",
            encoding="utf-8",
        )
        parent = tmp_path / "parent.yaml"
        parent.write_text(
            """
state:
  - name: "log"
    type: "list[str]"
    reducer: "append"
nodes:
  - name: "child"
    subgraph: "child.yaml"
edges:
  - source: "START"
    target: "child"
  - source: "child"
    target: "END"
""",
            encoding="utf-8",
        )

        audit = {}
        reg = Registry()

        @reg.node("inner")
        def inner(state):
            answer = interrupt("approve?")
            if answer == "accept":
                audit["written"] = True
            return {"log": [f"inner-{answer}"]}

        graph = build_graph(parent, reg, checkpointer=InMemorySaver())
        cfg = {"configurable": {"thread_id": "t-sub"}}

        out = graph.invoke({"log": []}, cfg)
        assert "__interrupt__" in out, "subgraph interrupt must propagate"
        assert "written" not in audit

        graph.invoke(Command(resume="accept"), cfg)
        assert audit.get("written") is True, "subgraph must resume via parent"

    def test_nested_subgraph_compiles_without_its_own_checkpointer(self):
        """ADR-005 directly: the builder used for a subgraph carries no persistence.

        This is a design assertion, not a correctness one — LangGraph tolerates a
        checkpointer on a nested compile. It is pinned because passing one is a
        deliberate isolation mechanism, and doing it implicitly would be wrong.
        """
        from langgraph_declarative import GraphBuilder

        parent = GraphBuilder(
            Registry(), checkpointer=InMemorySaver(), store=object()
        )
        child = parent._subgraph_builder()

        assert child is not parent
        assert child.checkpointer is None
        assert child.store is None

    def test_builder_without_persistence_reuses_itself(self):
        """No checkpointer means no twin is needed — avoids pointless allocation."""
        from langgraph_declarative import GraphBuilder

        plain = GraphBuilder(Registry())
        assert plain._subgraph_builder() is plain


# ---------------------------------------------------------------------------
# destinations: (ADR-006)
# ---------------------------------------------------------------------------


class TestDestinations:
    """A Command(goto=...) node with no static edges must still draw correctly."""

    def test_no_spurious_end_edge(self):
        mermaid = draw_mermaid(
            FIXTURES / "hitl_workflow.yaml", _hitl_registry({})
        )
        approval_edges = [
            line.strip()
            for line in mermaid.splitlines()
            if "-->" in line and "approval" in line
        ]
        # Without destinations, LangGraph invents `approval --> __end__`.
        assert not any(
            "approval --> __end__" in e for e in approval_edges
        ), f"spurious END edge present: {approval_edges}"

    def test_declared_destinations_appear(self):
        mermaid = draw_mermaid(
            FIXTURES / "hitl_workflow.yaml", _hitl_registry({})
        )
        assert "approval" in mermaid
        assert "execute" in mermaid

    def test_unknown_destination_rejected_with_suggestion(self, tmp_path):
        bad = tmp_path / "bad.yaml"
        bad.write_text(
            """
nodes:
  - name: "a"
    function: "a"
    destinations: ["excute"]
  - name: "execute"
    function: "a"
edges:
  - source: "START"
    target: "a"
""",
            encoding="utf-8",
        )
        reg = Registry()

        @reg.node("a")
        def a(state):
            return {}

        with pytest.raises(ConfigValidationError) as exc:
            build_graph(bad, reg)
        assert "execute" in str(exc.value), "should suggest the closest match"


# ---------------------------------------------------------------------------
# interrupt_before / interrupt_after
# ---------------------------------------------------------------------------


class TestStaticInterrupts:
    """A pause declared in YAML, with no Python change."""

    def _static_yaml(self, tmp_path, field="interrupt_before"):
        path = tmp_path / "static.yaml"
        path.write_text(
            f"""
state:
  - name: "log"
    type: "list[str]"
    reducer: "append"

{field}: ["gated"]

nodes:
  - name: "gated"
    function: "gated"
edges:
  - source: "START"
    target: "gated"
  - source: "gated"
    target: "END"
""",
            encoding="utf-8",
        )
        return path

    def test_interrupt_before_pauses(self, tmp_path):
        audit = {}
        reg = Registry()

        @reg.node("gated")
        def gated(state):
            audit["written"] = True
            return {"log": ["gated"]}

        graph = build_graph(
            self._static_yaml(tmp_path), reg, checkpointer=InMemorySaver()
        )
        cfg = {"configurable": {"thread_id": "t-static"}}

        graph.invoke({"log": []}, cfg)
        # Paused *before* the node ran, so the side effect must not exist yet.
        assert "written" not in audit
        assert graph.get_state(cfg).next == ("gated",)

        graph.invoke(None, cfg)
        assert audit.get("written") is True

    def test_interrupt_after_runs_node_then_pauses(self, tmp_path):
        audit = {}
        reg = Registry()

        @reg.node("gated")
        def gated(state):
            audit["written"] = True
            return {"log": ["gated"]}

        graph = build_graph(
            self._static_yaml(tmp_path, "interrupt_after"),
            reg,
            checkpointer=InMemorySaver(),
        )
        cfg = {"configurable": {"thread_id": "t-after"}}

        graph.invoke({"log": []}, cfg)
        assert audit.get("written") is True, "interrupt_after runs the node first"

    def test_unknown_interrupt_node_rejected(self, tmp_path):
        path = tmp_path / "bad.yaml"
        path.write_text(
            """
interrupt_before: ["gatd"]
nodes:
  - name: "gated"
    function: "gated"
edges:
  - source: "START"
    target: "gated"
""",
            encoding="utf-8",
        )
        reg = Registry()

        @reg.node("gated")
        def gated(state):
            return {}

        with pytest.raises(ConfigValidationError) as exc:
            build_graph(path, reg)
        assert "interrupt_before" in str(exc.value)
        assert "gated" in str(exc.value), "should suggest the closest match"

    def test_omitting_interrupts_is_unchanged(self, tmp_path):
        reg = Registry()

        @reg.node("greet")
        def greet(state):
            return {"messages": []}

        @reg.node("respond")
        def respond(state):
            return {"messages": []}

        graph = build_graph(FIXTURES / "simple.yaml", reg)
        assert graph.invoke({"messages": []}) is not None


# ---------------------------------------------------------------------------
# store passthrough
# ---------------------------------------------------------------------------


class TestStorePassthrough:
    def test_store_reaches_the_compiled_graph(self, tmp_path):
        from langgraph.store.memory import InMemoryStore

        store = InMemoryStore()
        seen = {}

        reg = Registry()

        @reg.node("greet")
        def greet(state, *, store=None):
            seen["store"] = store
            return {"messages": []}

        @reg.node("respond")
        def respond(state):
            return {"messages": []}

        graph = build_graph(FIXTURES / "simple.yaml", reg, store=store)
        graph.invoke({"messages": []})

        assert seen["store"] is store, "store must be injected into nodes"


# ---------------------------------------------------------------------------
# Durable restart: the pause survives a process boundary (M06.07)
# ---------------------------------------------------------------------------


class TestDurableRestart:
    """``InMemorySaver`` proves the API; this proves recovery.

    Each "process" gets a fresh registry, compiled graph, saver connection and
    audit dict. Only the SQLite file on disk is shared — exactly what survives a
    real restart. The pause happens in process 1, the resume in process 2.
    """

    @staticmethod
    def _process(db_path: Path):
        """Start a 'process': build from YAML with a new saver on the DB file."""
        import sqlite3

        from langgraph.checkpoint.sqlite import SqliteSaver

        conn = sqlite3.connect(db_path, check_same_thread=False)
        audit: dict = {}
        graph = _build_hitl(audit, SqliteSaver(conn))
        return graph, audit, conn

    def _pause(self, db_path: Path, cfg: dict) -> None:
        graph, audit, conn = self._process(db_path)
        try:
            out = graph.invoke({"action": "write"}, cfg)
            assert "__interrupt__" in out, "write path must pause"
            assert audit == {}, "nothing may be written before approval"
        finally:
            conn.close()
        del graph  # the compiled graph and its saver die with the "process"

    def test_accept_after_restart_writes_exactly_once(self, tmp_path):
        db_path = tmp_path / "checkpoints.sqlite"
        cfg = {"configurable": {"thread_id": "durable-accept"}}
        self._pause(db_path, cfg)

        graph, audit, conn = self._process(db_path)
        try:
            assert graph.get_state(cfg).next == ("approval",)
            out = graph.invoke(Command(resume="accept"), cfg)
            assert audit == {"written": True, "writes": 1}
            assert out["log"] == ["agent", "approved", "executed"]
            assert graph.get_state(cfg).next == ()
        finally:
            conn.close()

    def test_reject_after_restart_writes_nothing(self, tmp_path):
        db_path = tmp_path / "checkpoints.sqlite"
        cfg = {"configurable": {"thread_id": "durable-reject"}}
        self._pause(db_path, cfg)

        graph, audit, conn = self._process(db_path)
        try:
            out = graph.invoke(Command(resume="reject"), cfg)
            assert audit == {}
            assert out["log"] == ["agent", "rejected"]
        finally:
            conn.close()
