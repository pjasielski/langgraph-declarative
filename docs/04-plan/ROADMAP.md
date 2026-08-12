# ROADMAP — langgraph-declarative

**Version:** 0.2.0 (released) → 0.3.0 (M06 target)
**Updated:** 2026-08-12
**Sources:** `.sessions/11-hitl/` (HITL handoff from the agentic-testing project), docs/06-review/, prior delivery sessions

Canonical delivery tracker. The root [ROADMAP.md](../../ROADMAP.md) is the user-facing
summary of the same information — **this file is updated first**.

**Requirements:** [docs/02-requirements/REQUIREMENTS.md](../02-requirements/REQUIREMENTS.md)
**Design:** [docs/03-design/DESIGN.md](../03-design/DESIGN.md)
**Tasks:** [tasks/](tasks/)

**Status values:** ☐ todo · 🔄 in progress · ⏳ blocked · ✅ done · ⊘ dropped
**Priority:** P0 (bug) · P1 (required) · P2 (improvement) · P3 (future)
**Effort:** S (hours) · M (a session) · L (multiple sessions) · XL (multi-day)

---

## Milestone summary

| # | Milestone | Theme | Status |
|---|-----------|-------|--------|
| M01 | Core library (v1) | Registry, loader, schema, builder, errors, packaging | ✅ done |
| M02 | Examples & hardening | Edge-type example coverage, public roadmap, edge-case tests | ✅ done |
| M03 | Declarative surface (v1.1) | State in YAML, match routing, Mermaid, JSON Schema | ✅ done |
| M04 | Composition & config (v2) | Subgraphs, imports, LLM/tools, DB source, template | ✅ done |
| M05 | Backlog | Unvalidated ideas — no commitment | ☐ todo |
| M06 | Human-in-the-loop (v2.1) | Checkpointer, destinations, static interrupts, store | ☐ todo |

M01–M04 released as `v0.2.0`. v1 / v1.1 / v2 are milestone labels, not package
versions — see [CHANGELOG.md](../../CHANGELOG.md).

> **Task ID note.** M01–M04 task files keep their original `task-NNN.md` names —
> shipped history, referenced from commit messages. Tasks from M06 on use the
> Maestro 0.4 `M{MM}.{NN}` scheme.

---

## Milestone M06: Human-in-the-loop (v2.1)

Make approval gates, pauses for input, and resumable runs expressible in YAML —
the one capability class the library cannot currently express at all.

| # | Item | Priority | Effort | Depends | Status | Task | Source |
|---|------|----------|--------|---------|--------|------|--------|
| M06.01 | **Thread `checkpointer` through all four entry points to `compile()`** | P1 | S | — | ☐ todo | [M06.01](tasks/M06.01-checkpointer-threading.md) | HITL handoff |
| M06.02 | **Behavioural HITL test — pause, resume-accept, resume-reject, thread persistence** | P1 | M | M06.01 | ☐ todo | [M06.02](tasks/M06.02-hitl-behavioural-test.md) | HITL handoff |
| M06.03 | **`destinations:` node field for `Command(goto=...)` routing nodes** | P2 | S | — | ☐ todo | [M06.03](tasks/M06.03-destinations-field.md) | HITL handoff |
| M06.04 | **`interrupt_before:` / `interrupt_after:` static interrupt points in YAML** | P2 | S | M06.01 | ☐ todo | [M06.04](tasks/M06.04-static-interrupts.md) | HITL handoff |
| M06.05 | **Runnable `human_in_the_loop` example + README/schema docs** | P1 | M | M06.01, M06.03 | ☐ todo | [M06.05](tasks/M06.05-hitl-example-docs.md) | Project convention |
| M06.06 | **Optional `store` passthrough for cross-thread memory** | P3 | S | M06.01 | ☐ todo | [M06.06](tasks/M06.06-store-passthrough.md) | HITL handoff |

**Done when:** a YAML-defined graph with an approval node pauses on a write, resumes
with accept (side effect happens) or reject (side effect does not), survives across
turns on one `thread_id`, and renders a correct Mermaid diagram — with the checkpointer
supplied by the caller and never defaulted.

### Execution notes

**Dependency graph:**
```
M06.01 ──┬─→ M06.02
         ├─→ M06.04
         ├─→ M06.06
         └─┐
M06.03 ────┴─→ M06.05
```

**Critical path:** M06.01 → M06.02 (the capability is not proven until the
behavioural test passes)
**Parallelizable:** M06.03 is independent of M06.01 and can be done alongside it.
**Do first:** M06.01 — everything except M06.03 is blocked on it.

**Design constraints** (see ADR-004..006 in DESIGN.md):
- Never default the checkpointer. Under `langgraph dev` / LangGraph Platform the
  server owns it and a compile-time checkpointer is silently ignored — a default
  would look like it worked while doing nothing.
- Do **not** pass the checkpointer to nested subgraph compiles. Verified on
  LangGraph 1.2.2: the parent's checkpointer already covers subgraph interrupts.
- Assert **side effects**, not return status. A graph that returns cleanly having
  written nothing — or having written despite a rejection — passes a status test
  and fails the only thing that matters.

**Backward compatibility:** every item is additive. `compile(checkpointer=None)`
is current behaviour, and the new YAML fields are all optional.

---

## M05 — Backlog

Possibilities, not commitments. Each needs validation against real usage before it
earns a task.

| # | Item | Priority | Effort | Depends | Status | Source |
|---|------|----------|--------|---------|--------|--------|
| M05.01 | **Graph diffing** — compare two YAML files, report topology changes | P3 | M | — | ☐ todo | delivery |
| M05.02 | **Hot-reload** — watch a YAML file, recompile the graph on change | P3 | M | — | ☐ todo | delivery |
| M05.03 | **CLI tool** — `lgd validate` / `lgd visualize` | P3 | L | — | ☐ todo | delivery |
| M05.04 | **Graph versioning** — A/B test between YAML workflow variants | P3 | L | — | ☐ todo | delivery |
| M05.05 | **LangGraph Studio export** — emit Studio-compatible format | P3 | M | — | ☐ todo | delivery |

YAML include/import shipped as task-023 (`imports:`) and is no longer a backlog item.

### Near-term operational work

| # | Item | Priority | Effort | Depends | Status | Source |
|---|------|----------|--------|---------|--------|--------|
| OPS.1 | **First PyPI release** — name reserved, `release.yml` wired for Trusted Publishing, nothing published yet | P1 | S | — | ☐ todo | delivery |
| OPS.2 | **README logo asset for PyPI** — PyPI strips SVG and can't resolve relative paths | P2 | S | — | ✅ done | session 010 |
| OPS.3 | **LangChain outreach** — see `.sessions/007-promotion-marketing/02_langchain-outreach.md` | P3 | S | — | ☐ todo | session 007 |

---

## Shipped milestones

### M01 — Core library (v1)

| # | Title | Effort | Status |
|---|-------|--------|--------|
| 001 | Scaffold project structure | S | ✅ done |
| 002 | Implement errors module | S | ✅ done |
| 003 | Implement registry module + tests | M | ✅ done |
| 004 | Implement schema module + tests | M | ✅ done |
| 005 | Implement loader module + tests | S | ✅ done |
| 006 | Implement builder module + tests | L | ✅ done |
| 007 | Implement public API + integration tests | M | ✅ done |
| 008 | Create examples | S | ✅ done |
| 009 | Finalize packaging and README | S | ✅ done |

### M02 — Examples & hardening

| # | Title | Effort | Status |
|---|-------|--------|--------|
| 010 | Add fan-out and Send examples | S | ✅ done |
| 011 | Add custom state example | S | ✅ done |
| 012 | Create ROADMAP.md | S | ✅ done |
| 013 | Edge-case tests and hardening | S | ✅ done |

### M03 — Declarative surface (v1.1)

| # | Title | Effort | Requirement | Status |
|---|-------|--------|-------------|--------|
| 014 | State declaration in YAML | L | FR-14 | ✅ done |
| 015 | Auto-Mermaid generation | S | FR-15 | ✅ done |
| 016 | JSON Schema for YAML files | S | FR-16 | ✅ done |
| 017 | Match routing syntax | M | FR-18 | ✅ done |

### M04 — Composition & config (v2)

| # | Title | Effort | Status |
|---|-------|--------|--------|
| 018 | Subgraph composition | XL | ✅ done |
| 019 | Tool configuration in YAML | L | ✅ done |
| 020 | LLM configuration per node | M | ✅ done |
| 021 | Database-driven graph source | L | ✅ done |
| 022 | LangGraph Template packaging | S | ✅ done |
| 023 | Cross-file node references | M | ✅ done |

---

## Known risks

| Risk | Mitigation |
|------|------------|
| LangGraph API differences across versions | Minimum version pinned in `pyproject.toml`; CI tests against it |
| Pydantic v2 validator edge cases | Validators kept simple; invalid configs tested thoroughly |
| Subgraph state scoping complexity | Shared registry + state sharing via common keys only |
| LLM provider dependency sprawl | Providers are optional extras with lazy imports and a clear error when missing |
| DB loader schema migrations | Graph config stored as JSON text with a version field, not normalized tables |
| Test fixtures drift from the YAML spec | YAML fixtures in `tests/fixtures/` are the spec; tests validate against them |
| HITL checkpointer ignored under `langgraph dev` | Never default one; document the ownership split in README and the example (M06.05) |
| `interrupt()` semantics shifting across LangGraph versions | Behavioural test (M06.02) asserts side effects, so a semantic change fails loudly |

---

## Test strategy

Tests are co-located with their module tasks rather than run as a separate phase.

| Test file | Covers |
|-----------|--------|
| `test_errors.py` | Error classes, `suggest_similar` accuracy, `format_not_found` output |
| `test_registry.py` | Registration, lookup, duplicate rejection, namespace isolation |
| `test_schema.py` | Pydantic validation, mutual exclusion (`target` vs `path`), duplicate node names |
| `test_builder.py` | All edge types, START/END resolution, cross-validation failures |
| `test_loader.py` | Valid file, missing file, malformed YAML |
| `test_integration.py` | End-to-end: YAML → `build_graph()` → `invoke()` |
| `test_hitl.py` *(M06)* | Pause/resume behaviour, accept vs reject side effects, thread persistence |

Integration tests exercise the full pipeline against real LangGraph invocation —
confirming compiled graphs actually run, not merely that they compile.

---

## How to use

Maintained by `/mae-plan`. To implement a milestone:

1. `/mae-plan {milestone}` — enrich with execution notes and generate task files
2. `/mae-do` — execute tasks; status updates as work completes
3. `/sync` — reconcile status at end of session

P0 items are addressed before feature work.
