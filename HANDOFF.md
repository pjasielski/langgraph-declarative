# HANDOFF — langgraph-declarative

**Status:** Planning complete, ready for implementation
**Phase:** implementation
**Updated:** 2026-05-30

---

## Current Focus

Implementing v1 of `langgraph-declarative` — a Python library that compiles YAML workflow definitions into LangGraph `CompiledStateGraph` objects using a decorator-based node/router registry.

9 implementation tasks created in `delivery/04-plan/tasks/`. Next step: scaffold project structure (task-001).

## Key Decisions

| Decision | Date | Status |
|----------|------|--------|
| API: `Registry()` with `@registry.node()` / `@registry.router()` decorators | 2026-05-25 | Confirmed |
| API: `build_graph()` convenience + `GraphBuilder` power-user class | 2026-05-25 | Confirmed |
| Conditional edges: mapped routing (`path:` + `targets:`) | 2026-05-25 | Confirmed |
| V1 scope: registry, builder, validation, errors, tests, README, PyPI | 2026-05-25 | Confirmed |
| Model factory deferred to v1.1 | 2026-05-25 | Confirmed |
| Library first, templates later | 2026-05-25 | Confirmed |
| License: MIT | 2026-05-25 | Confirmed |
| Package: `langgraph-declarative` / import: `langgraph_declarative` | 2026-05-25 | Confirmed |
| Delivery: scope v1+v2, implement v1 first | 2026-05-30 | Confirmed |
| Send supported from v1 via router return type | 2026-05-30 | Confirmed |
| `build_graph()` defaults to `MessagesState` | 2026-05-30 | Confirmed |
| Repo: `src/` layout, hatchling, pytest, Python 3.10+ | 2026-05-30 | Confirmed |

## Architecture

```
User Code                          Library (langgraph_declarative)
┌─────────────────┐        ┌──────────────────────────────┐
│ @registry.node  │───────>│  Registry → Loader → Schema  │
│ @registry.router│        │       Validator → Builder     │
│ build_graph()   │───────>│              ↓                │
└─────────────────┘        │    CompiledStateGraph         │
    workflow.yaml ────────>└──────────────────────────────┘
```

5 modules: `registry.py`, `loader.py`, `schema.py`, `builder.py`, `errors.py`
Stack: Python 3.10+, LangGraph >=0.2, Pydantic v2, PyYAML, hatchling

## Recent Changes

| Date | Change |
|------|--------|
| 2026-05-25 | Session 001: exploration started |
| 2026-05-30 | PRD completed and promoted to delivery/02-prd/ |
| 2026-05-30 | SDD completed and promoted to delivery/03-design/ |
| 2026-05-30 | Session 002: plan phase — 9 tasks created |
