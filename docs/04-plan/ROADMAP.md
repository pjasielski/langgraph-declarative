# ROADMAP — langgraph-declarative

**Version:** 0.2.0 (released, tag `v0.2.0`) → 0.3.0 (M05 + M06) → 0.4.0 (M07)
**Updated:** 2026-10-01
**Sources:** `.sessions/11-hitl/` (HITL handoff from the agentic-testing project), `.sessions/013-codex-review/` (external review, verified), docs/06-review/, prior delivery sessions

The single delivery roadmap for this project. Milestone status, item detail, and the
task index all live here.

**Requirements:** [docs/02-requirements/REQUIREMENTS.md](../02-requirements/REQUIREMENTS.md)
**Design:** [docs/03-design/DESIGN.md](../03-design/DESIGN.md)
**Tasks:** [tasks/](tasks/)

**Status:** ☐ todo · 🔄 in progress · ⏳ blocked · ✅ done · ⊘ dropped
**Priority:** P0 (bug) · P1 (required) · P2 (improvement) · P3 (future)
**Effort:** S (hours) · M (a session) · L (multiple sessions) · XL (multi-day)

> **Task ID note.** M01–M04 task files keep their original `task-NNN.md` names —
> shipped history, referenced from commit messages. Tasks from M05 on use the
> Maestro 0.4 `M{MM}.{NN}` scheme.

---

## Milestone summary

| # | Milestone | Theme | Target | Status |
|---|-----------|-------|--------|--------|
| M01 | Core library | Registry, loader, schema, builder, errors, packaging | 0.1.0 | ✅ done |
| M02 | Examples & hardening | Edge-type example coverage, public roadmap, edge-case tests | 0.1.0 | ✅ done |
| M03 | Declarative surface | State in YAML, match routing, Mermaid, JSON Schema | 0.2.0 | ✅ done |
| M04 | Composition & config | Subgraphs, imports, LLM/tools, DB source, template | 0.2.0 | ✅ done |
| M05 | Human-in-the-loop | Checkpointer, destinations, static interrupts, store | 0.3.0 | ✅ done (unreleased) |
| M06 | Hardening | Correctness fixes, strict schema, compatibility band, packaging, release | 0.3.0 | 🔄 in progress |
| M07 | Capabilities | Node params, side-effect-free diagrams, loader pipeline, graph lint | 0.4.0 | ☐ todo |
| M08 | Embedding & platform adapters | Neutral IR, restricted mode, digests — **demand-gated** | — | ⏳ gated |

M01–M02 were the internal 0.1.0; M01–M04 shipped publicly as `v0.2.0`. M05 is done
but unreleased (committed on `feat/hitl`): 0.3.0 ships M05 and M06
together, so the HITL feature does not land on top of known correctness bugs and an
untested dependency range. The v1 / v1.1 / v2 labels used in earlier docs were
milestone names, not package versions — see [CHANGELOG.md](../../CHANGELOG.md).

---

## Milestone M01: Core library (0.1.0)

✅ Shipped.

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

---

## Milestone M02: Examples & hardening (0.1.0)

✅ Shipped.

| # | Title | Effort | Status |
|---|-------|--------|--------|
| 010 | Add fan-out and Send examples | S | ✅ done |
| 011 | Add custom state example | S | ✅ done |
| 012 | Create ROADMAP.md | S | ✅ done |
| 013 | Edge-case tests and hardening | S | ✅ done |

---

## Milestone M03: Declarative surface (0.2.0)

✅ Shipped.

| # | Title | Effort | Requirement | Status |
|---|-------|--------|-------------|--------|
| 014 | State declaration in YAML | L | FR-14 | ✅ done |
| 015 | Auto-Mermaid generation | S | FR-15 | ✅ done |
| 016 | JSON Schema for YAML files | S | FR-16 | ✅ done |
| 017 | Match routing syntax | M | FR-18 | ✅ done |

---

## Milestone M04: Composition & config (0.2.0)

✅ Shipped.

| # | Title | Effort | Status |
|---|-------|--------|--------|
| 018 | Subgraph composition | XL | ✅ done |
| 019 | Tool configuration in YAML | L | ✅ done |
| 020 | LLM configuration per node | M | ✅ done |
| 021 | Database-driven graph source | L | ✅ done |
| 022 | LangGraph Template packaging | S | ✅ done |
| 023 | Cross-file node references | M | ✅ done |

---

## Milestone M05: Human-in-the-loop (0.3.0)

Make approval gates, pauses for input, and resumable runs expressible in YAML — the
one capability class the library could not express at all.

| # | Item | Priority | Effort | Depends | Status | Task | Source |
|---|------|----------|--------|---------|--------|------|--------|
| M05.01 | **Thread `checkpointer` through all four entry points to `compile()`** | P1 | S | — | ✅ done | [M05.01](tasks/M05.01-checkpointer-threading.md) | HITL handoff |
| M05.02 | **Behavioural HITL test — pause, resume-accept, resume-reject, thread persistence** | P1 | M | M05.01 | ✅ done | [M05.02](tasks/M05.02-hitl-behavioural-test.md) | HITL handoff |
| M05.03 | **`destinations:` node field for `Command(goto=...)` routing nodes** | P2 | S | — | ✅ done | [M05.03](tasks/M05.03-destinations-field.md) | HITL handoff |
| M05.04 | **`interrupt_before:` / `interrupt_after:` static interrupt points in YAML** | P2 | S | M05.01 | ✅ done | [M05.04](tasks/M05.04-static-interrupts.md) | HITL handoff |
| M05.05 | **Runnable `human_in_the_loop` example + README/schema docs** | P1 | M | M05.01, M05.03 | ✅ done | [M05.05](tasks/M05.05-hitl-example-docs.md) | Project convention |
| M05.06 | **Optional `store` passthrough for cross-thread memory** | P3 | S | M05.01 | ✅ done | [M05.06](tasks/M05.06-store-passthrough.md) | HITL handoff |

**Done when:** a YAML-defined graph with an approval node pauses on a write, resumes
with accept (side effect happens) or reject (side effect does not), survives across
turns on one `thread_id`, and renders a correct Mermaid diagram — with the checkpointer
supplied by the caller and never defaulted.

### Execution notes

**Dependency graph:**
```
M05.01 ──┬─→ M05.02
         ├─→ M05.04
         ├─→ M05.06
         └─┐
M05.03 ────┴─→ M05.05
```

**Critical path:** M05.01 → M05.02 (the capability is not proven until the
behavioural test passes)
**Parallelizable:** M05.03 is independent of M05.01.

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
is the previous behaviour, and the new YAML fields are all optional.

---

## Milestone M06: Hardening (0.3.0)

Fix what an external review found (verified and reproduced in session 013) before
anything else is released. Every P1 bug here was reproduced. Each fix lands with its
reproduction as a regression test.

**Estimate:** 1 session.

| # | Item | Scope | Priority | Effort | Depends | Status | Task |
|---|------|-------|----------|--------|---------|--------|------|
| M06.01 | **Mapped routers: preserve sync/async and `config` injection** | Bug | P1 | S | — | ✅ done | [M06.01](tasks/M06.01-router-wrapper-async-config.md) |
| M06.02 | **Definition origin: imported subgraphs resolve against their own file; explicit `base_dir=`** | Bug | P1 | M | — | ✅ done | [M06.02](tasks/M06.02-definition-origin.md) |
| M06.03 | **Strict schema: reject unknown YAML keys; add explicit `description:`** | Bug (breaking) | P1 | S | — | ✅ done | [M06.03](tasks/M06.03-strict-schema.md) |
| M06.04 | **State `default:` — deprecate, document as introspection-only** | Bug | P1 | S | — | ✅ done | [M06.04](tasks/M06.04-state-default-deprecation.md) |
| M06.05 | **LangGraph `>=1.0` + CI version matrix** | Release | P1 | M | — | ✅ done | [M06.05](tasks/M06.05-langgraph-compat-band.md) |
| M06.06 | **Ship JSON Schema in the wheel, add `py.typed`, installed-wheel smoke test** | Release | P1 | S | M06.03 | ☐ todo | [M06.06](tasks/M06.06-packaging.md) |
| M06.07 | **HITL durable-restart test with a persistent saver** | HITL | P1 | S | — | ☐ todo | [M06.07](tasks/M06.07-hitl-durable-restart-test.md) |
| M06.08 | **Docs: trust boundary + host responsibilities for HITL** | Docs | P1 | S | — | ☐ todo | [M06.08](tasks/M06.08-trust-boundary-docs.md) |
| M06.09 | **SQLite loader: atomic version allocation** | Bug | P2 | S | — | ☐ todo | [M06.09](tasks/M06.09-sqlite-atomic-versioning.md) |
| M06.10 | **Release 0.3.0: version bump, CHANGELOG, tag, GitHub release** | Release | P1 | S | all | ☐ todo | [M06.10](tasks/M06.10-release-0.3.0.md) |

**Done when:** every P1 item is green; CI passes on the full matrix; an installed
wheel contains the schema; `v0.3.0` is tagged and on PyPI.

### Execution notes

**Order:** M06.01–M06.05, M06.07–M06.09 are independent → M06.06 → M06.10.
**Critical path:** M06.03 → M06.06 → M06.10.

**Breaking changes (allowed in 0.x, listed in CHANGELOG):**
- Unknown YAML keys now fail validation (M06.03).
- A DB/in-memory definition with relative `imports:`/`subgraph:` and no `base_dir=`
  now raises instead of resolving against the process working directory (M06.02).
- `langgraph>=1.0` instead of `>=0.2` (M06.05).

---

## Milestone M07: Capabilities (0.4.0)

Features users need for reusable node types and safer tooling. All additive.

**Estimate:** 1 session.

| # | Item | Scope | Priority | Effort | Depends | Status | Task |
|---|------|-------|----------|--------|---------|--------|------|
| M07.01 | **Node `params:` with optional Pydantic validation** | Capability | P2 | M | M06.03 | ☐ todo | [M07.01](tasks/M07.01-node-params.md) |
| M07.02 | **Side-effect-free `draw_mermaid()`: no LLM clients, no persistence** | Capability | P2 | M | — | ☐ todo | [M07.02](tasks/M07.02-structural-render.md) |
| M07.03 | **`build_from_loader()`: one pipeline for YAML, SQLite and custom loaders** | Capability | P2 | S | M06.02 | ☐ todo | [M07.03](tasks/M07.03-build-from-loader.md) |
| M07.04 | **Graph lint: unreachable nodes, no path to END, dead routing keys** | Capability | P2 | M | — | ☐ todo | [M07.04](tasks/M07.04-graph-lint.md) |
| M07.05 | **HITL resume semantics tests: stale, double and post-reject resume** | HITL | P2 | S | M06.07 | ☐ todo | [M07.05](tasks/M07.05-hitl-resume-semantics.md) |
| M07.06 | **Node `retry:` / `cache:` / `defer:`** | Capability | P3 | S | M06.05 | ☐ todo | [M07.06](tasks/M07.06-node-runtime-policies.md) |
| M07.07 | **LLM parameter validation in the schema** | Capability | P3 | S | M06.03 | ☐ todo | [M07.07](tasks/M07.07-llm-param-validation.md) |
| M07.08 | **Optional runtime guard for `destinations`** | HITL | P3 | S | — | ☐ todo | [M07.08](tasks/M07.08-destinations-runtime-guard.md) |

**Done when:** each item has a runnable example or test, the JSON Schema is
regenerated, and `v0.4.0` is released.

### Execution notes

**Order:** M07.01, M07.02, M07.04, M07.05, M07.07, M07.08 are independent;
M07.03 follows M06.02; M07.06 follows M06.05. P3 items are droppable.

---

## Milestone M08: Embedding & platform adapters (demand-gated, unversioned)

Work that only pays off when a second compile target exists — e.g. emitting another
platform's workflow format instead of a LangGraph graph. **Do not start without a
confirmed consumer.** The first candidate is an external workflow platform; details
stay in `.sessions/013-codex-review/` (not public).

| # | Item | Scope | Effort | Status |
|---|------|-------|--------|--------|
| M08.01 | Neutral intermediate representation: a resolved, origin-annotated definition independent of LangGraph; the LangGraph compiler becomes one target | Architecture | L | ⏳ gated |
| M08.02 | Restricted mode: no `module:attr` imports, root-confined path resolver, registry allowlist, size/depth/count limits | Architecture | M | ⏳ gated |
| M08.03 | Canonical serialization + definition digest; loader provenance | Architecture | M | ⏳ gated |
| M08.04 | Property/fuzz tests: recursive imports, routing, malformed configs | Architecture | M | ⏳ gated |

Recommended first step if demand is confirmed: a proof-of-concept adapter as a
**separate package** consuming the strict `GraphConfig`, not changes to the core.

---

## Operational work

| # | Item | Priority | Effort | Depends | Status | Source |
|---|------|----------|--------|---------|--------|--------|
| OPS.1 | **First PyPI release** — `0.2.0` published 2026-07-26; tagged `v0.2.0` retroactively on 2026-10-01 (source verified identical to the PyPI wheel) | P1 | S | — | ✅ done | delivery |
| OPS.2 | **README logo asset for PyPI** — PyPI strips SVG and can't resolve relative paths | P2 | S | — | ✅ done | session 010 |
| OPS.3 | **LangChain outreach** — see `.sessions/007-promotion-marketing/02_langchain-outreach.md` | P3 | S | — | ☐ todo | session 007 |

---

## Future (unscheduled)

Possibilities, not commitments. Each needs validation against real usage before it
earns a milestone.

| # | Item | Priority | Effort | Depends | Status | Source |
|---|------|----------|--------|---------|--------|--------|
| F.1 | **Graph diffing** — compare two YAML files, report topology changes | P3 | M | — | ☐ todo | delivery |
| F.2 | **Hot-reload** — watch a YAML file, recompile the graph on change | P3 | M | — | ☐ todo | delivery |
| F.3 | **CLI tool** — `lgd validate` / `lgd visualize` | P3 | L | — | ☐ todo | delivery |
| F.4 | **Graph versioning** — A/B test between YAML workflow variants | P3 | L | — | ☐ todo | delivery |
| F.5 | **LangGraph Studio export** — emit Studio-compatible format | P3 | M | — | ☐ todo | delivery |

YAML include/import shipped as task-023 (`imports:`) and is no longer a future item.

---

## Known risks

| Risk | Mitigation |
|------|------------|
| LangGraph API differences across versions | `langgraph>=1.0` from 0.3.0; CI tests the locked, lowest and latest resolution on Python 3.10/3.12/3.13 (M06.05) |
| Pydantic v2 validator edge cases | Validators kept simple; invalid configs tested thoroughly |
| Subgraph state scoping complexity | Shared registry + state sharing via common keys only |
| LLM provider dependency sprawl | Providers are optional extras with lazy imports and a clear error when missing |
| DB loader schema migrations | Graph config stored as JSON text with a version field, not normalized tables |
| Test fixtures drift from the YAML spec | YAML fixtures in `tests/fixtures/` are the spec; tests validate against them |
| Untrusted YAML selects code and reads files | Definitions are trusted input — documented (M06.08); a restricted mode is M08.02 |
| Package docs drift from what ships | Installed-wheel smoke test (M06.06); release checklist (M06.10) |
| HITL checkpointer ignored under `langgraph dev` | Never default one; ownership split documented in README and the example |
| `interrupt()` semantics shifting across LangGraph versions | Behavioural tests assert side effects, so a semantic change fails loudly |

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
| `test_hitl.py` | Pause/resume behaviour, accept vs reject side effects, thread persistence, static interrupts, `store` |

Integration tests exercise the full pipeline against real LangGraph invocation —
confirming compiled graphs actually run, not merely that they compile.

---

## How to use

Maintained by `/mae-plan`. To implement a milestone:

1. `/mae-plan {milestone}` — enrich with execution notes and generate task files
2. `/mae-do` — execute tasks; status updates as work completes
3. `/sync` — reconcile status at end of session

P0 items are addressed before feature work.
