# Implementation Plan: langgraph-declarative v1

**Date:** 2026-05-30
**SDD:** delivery/03-design/SDD.md
**PRD:** delivery/02-prd/PRD.md
**Total tasks:** 9
**Estimated total effort:** M (library ~400 LOC, tests ~800 LOC)

---

## Overview

9 tasks covering scaffold, 5 library modules, integration tests, examples, and packaging. The library is deliberately small — the plan reflects that. Each task produces a working, testable increment.

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
