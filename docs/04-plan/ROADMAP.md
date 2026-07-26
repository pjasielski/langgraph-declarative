# Implementation Plan: langgraph-declarative

**Date:** 2026-05-30 (updated 2026-06-11)
**SDD:** delivery/03-design/SDD.md
**PRD:** delivery/02-prd/PRD.md
**Total tasks:** 23 (13 v1 done + 4 v1.1 + 6 v2)
**V1 status:** Complete — 77 tests passing, 2 examples, package builds

---

## Overview

**V1 (tasks 001-009):** Complete. All modules implemented, tested, packaged.

**Post-v1 (tasks 010-013):** Expand examples to cover all edge types, add ROADMAP.md for public visibility into future scope, and add edge-case tests discovered after v1 shipped.

---

## Task Summary

| Task | Title | Effort | Priority | Depends On |
|------|-------|--------|----------|------------|
| 001 | Scaffold project structure | S | high | — |
| 002 | Implement errors module | S | high | 001 |
| 003 | Implement registry module + tests | M | high | 001, 002 |
| 004 | Implement schema module + tests | M | high | 001, 002 |
| 005 | Implement loader module + tests | S | high | 001, 002 |
| 006 | Implement builder module + tests | L | high | 002, 003, 004, 005 |
| 007 | Implement public API + integration tests | M | high | 006 |
| 008 | Create examples | S | medium | 007 |
| 009 | Finalize packaging and README | S | medium | 007 |

---

## Dependency Graph

```
task-001 (scaffold)
    │
    ├── task-002 (errors)
    │       │
    │       ├── task-003 (registry + tests)  ─┐
    │       ├── task-004 (schema + tests)     ├── task-006 (builder + tests)
    │       └── task-005 (loader + tests)     ─┘         │
    │                                                     │
    │                                              task-007 (public API + integration tests)
    │                                                     │
    │                                          ┌──────────┴──────────┐
    │                                    task-008 (examples)   task-009 (packaging)
```

## Parallelization

- **After task-001:** tasks 002 can start immediately
- **After task-002:** tasks 003, 004, 005 can run in parallel
- **After task-006:** tasks 008 and 009 can run in parallel

---

## Test Strategy

Tests are co-located with their module tasks (not a separate phase). Each module task includes its test file. This avoids the anti-pattern of writing all code first and bolting tests on later.

| Test file | Covers | Key scenarios |
|-----------|--------|---------------|
| test_errors.py | Error classes, typo suggestion | `suggest_similar` accuracy, `format_not_found` output |
| test_registry.py | Node/router registration | Register, lookup, duplicate rejection, missing-name suggestions, namespace isolation |
| test_schema.py | Pydantic validation | Valid configs, missing fields, mutual exclusion (target vs path), duplicate node names |
| test_builder.py | Graph compilation | All 4 edge types, START/END resolution, cross-validation failures, compiled graph structure |
| test_loader.py | YAML loading | Valid file, missing file, malformed YAML |
| test_integration.py | End-to-end | YAML file → build_graph() → invoke → verify output for each edge type |

Integration tests (task-007) exercise the full pipeline with real LangGraph graph invocation, confirming the compiled graph actually works — not just that it compiles.

---

## Risks

| Risk | Mitigation |
|------|------------|
| LangGraph API differences across versions | Pin minimum version in pyproject.toml; test against it |
| Pydantic v2 validator edge cases | Keep validators simple; test invalid configs thoroughly |
| Test fixtures drift from YAML spec | YAML fixtures are the spec — tests validate against them |

---

## Notes
- Each task includes its own tests — no separate "write tests" phase
- Tasks are sized for single-session agentic execution (pick up task, implement, test, done)
- The builder (task-006) is the largest task as it orchestrates all other modules
- Examples (task-008) serve as additional integration validation

---

## Post-v1 Tasks

| Task | Title | Effort | Priority | Depends On |
|------|-------|--------|----------|------------|
| 010 | Add fan-out and Send examples | S | medium | 007 (done) |
| 011 | Add custom state example | S | medium | 007 (done) |
| 012 | Create ROADMAP.md | S | medium | — |
| 013 | Edge-case tests and hardening | S | medium | 007 (done) |

### Dependency Graph (post-v1)

```
(all v1 tasks done)
     │
     ├── task-010 (fan-out + Send examples)
     ├── task-011 (custom state example)
     ├── task-012 (ROADMAP.md)
     └── task-013 (edge-case tests)
```

All 4 tasks are independent and can run in parallel.

---

## v1.1 Tasks

Extending the core with features that don't change the architecture. Estimated total effort: ~L (one large + one medium + two small).

| Task | Title | Effort | Priority | Depends On | PRD |
|------|-------|--------|----------|------------|-----|
| 014 | State declaration in YAML | L | high | — | FR-14 |
| 015 | Auto-Mermaid generation | S | medium | — | FR-15 |
| 016 | JSON Schema for YAML files | S | medium | 014 | FR-16 |
| 017 | Match routing syntax | M | medium | — | FR-18 |

### Dependency Graph (v1.1)

```
(all v1 tasks done)
     │
     ├── task-014 (state in YAML) ──► task-016 (JSON Schema — needs state: in schema)
     ├── task-015 (auto-Mermaid)
     └── task-017 (match: routing)
```

Tasks 014, 015, and 017 can run in parallel. Task 016 is blocked by 014 because the JSON Schema should include the `state:` section.

### Suggested Execution Order (v1.1)

1. **task-014** (State in YAML) — largest task, enables task-016, high value
2. **task-017** (Match routing) — medium effort, independent
3. **task-015** (Auto-Mermaid) — small, independent
4. **task-016** (JSON Schema) — small, depends on 014

---

## v2 Tasks

Larger features that extend what the library can express. Estimated total effort: ~XL (one XL + two large + two medium + one small).

| Task | Title | Effort | Priority | Depends On |
|------|-------|--------|----------|------------|
| 018 | Subgraph composition | XL | high | 014 |
| 019 | Tool configuration in YAML | L | medium | 020 |
| 020 | LLM configuration per node | M | medium | — |
| 021 | Database-driven graph source | L | low | 014 |
| 022 | LangGraph Template packaging | S | low | 018 |
| 023 | Cross-file node references | M | low | 018 |

### Dependency Graph (v2)

```
(v1.1 complete)
     │
     ├── task-018 (subgraphs) ──┬── task-022 (LangGraph Template)
     │                          └── task-023 (cross-file refs)
     │
     ├── task-020 (LLM config) ──── task-019 (tool config)
     │
     └── task-021 (DB loader)
```

### Suggested Execution Order (v2)

1. **task-020** (LLM config) — independent, unblocks task-019
2. **task-018** (Subgraph composition) — largest v2 task, unblocks 022 + 023
3. **task-019** (Tool config) — after 020
4. **task-021** (DB loader) — independent
5. **task-023** (Cross-file refs) — after 018
6. **task-022** (LangGraph Template) — after 018, low priority

### v2 Risks

| Risk | Mitigation |
|------|------------|
| Subgraph state scoping complexity | Start with shared registry + isolated state; add state passing later |
| LLM provider dependency sprawl | Make providers optional extras; lazy imports; clear error when missing |
| DB loader schema migrations | Store graph config as JSON text, not normalized tables; version field |
| Template registry coordination | Can ship template in repo first; coordinate with LangChain team later |

---

### Test Additions (task-013)

| Area | What to test | Why |
|------|-------------|-----|
| Builder | Graph with only START→END (minimal) | Boundary case: no user nodes |
| Builder | Node registered but never used in edges | Unreachable node detection / warning |
| Integration | Custom state class with non-messages fields | Confirms state_class override works end-to-end |
| Schema | YAML with extra unknown fields | Strict vs permissive parsing behavior |
| Loader | Empty YAML file | Edge case: file exists but has no content |
| Loader | YAML with only nodes, no edges | Structural boundary |
