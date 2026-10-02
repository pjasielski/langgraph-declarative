# HANDOFF — langgraph-declarative

**Status:** 0.2.0 on PyPI (tag `v0.2.0`). M05 (HITL) and M06.01–M06.09 (hardening) done on `feat/hitl`, version bumped to 0.3.0 — not yet pushed or published. Next: release 0.3.0 (rest of M06.10)
**Phase:** maintenance
**Updated:** 2026-10-02

---

## Current Focus

1. **Release 0.3.0 (M06.10)** — follow `docs/08-deploy/RELEASE.md`. Before tagging:
   date the CHANGELOG heading and remove the "unreleased" wording from README and
   `examples/README.md` (the README becomes the PyPI page and cannot be changed after
   upload). Then push `feat/hitl` and the `v0.2.0` tag, PR to `main`, green CI (first
   run of the new matrix and package jobs), merge, tag `v0.3.0`, GitHub release →
   PyPI. Automated publishing needs a one-time PyPI trusted-publisher setup (see
   RELEASE.md); 0.2.0 was uploaded by hand.
2. **M07 — Capabilities for 0.4.0** (one session): node `params:`, side-effect-free
   `draw_mermaid()`, `build_from_loader()`, graph lint.
3. **M08 — platform adapters**: demand-gated; do not start without a consumer.

Plan and evidence: `.sessions/013-codex-review/02-review-assessment-and-plan.md`.
Roadmap: `docs/04-plan/ROADMAP.md`.

## Key Decisions

| Decision | Date | Status |
|----------|------|--------|
| API: `Registry()` with `@registry.node()` / `@registry.router()` decorators | 2026-05-25 | Confirmed |
| API: `build_graph()` convenience + `GraphBuilder` power-user class | 2026-05-25 | Confirmed |
| Conditional edges: mapped routing (`path:` + `targets:`) | 2026-05-25 | Confirmed |
| License: MIT | 2026-05-25 | Confirmed |
| Package: `langgraph-declarative` / import: `langgraph_declarative` | 2026-05-25 | Confirmed |
| Repo: `src/` layout, hatchling, pytest, Python 3.10+ | 2026-05-30 | Confirmed |
| Send supported from v1 via router return type | 2026-05-30 | Confirmed |
| `build_graph()` defaults to `MessagesState` | 2026-05-30 | Confirmed |
| Match routing uses dict lookup, never `eval()` | 2026-06-11 | Confirmed |
| LLM providers ship as optional extras with lazy imports | 2026-06-11 | Confirmed |
| DB loader stores config as JSON text with a version field | 2026-06-11 | Confirmed |
| Publish `0.2.0` as the first public release, not `1.0.0` | 2026-06-12 | Confirmed |
| v1 / v1.1 / v2 are milestone labels, not package versions | 2026-06-12 | Confirmed |
| `requires-python = ">=3.10"` — do not raise the floor | 2026-07-26 | Confirmed |
| Task files keep `task-NNN.md` names; new tasks use `M{MM}.{NN}` | 2026-07-26 | Confirmed |
| Checkpointer caller-supplied, never defaulted (ADR-004) | 2026-08-12 | Confirmed |
| `langgraph>=1.0`, no upper cap (ADR-008) | 2026-10-01 | Confirmed |
| Unknown YAML keys rejected (ADR-007) | 2026-10-01 | Confirmed |
| Relative paths resolve against declaring file; `base_dir=` for file-less builds (ADR-009) | 2026-10-01 | Confirmed |
| Feature tables use package versions; tags only for published releases | 2026-10-01 | Confirmed |

## Architecture

```
User Code                          Library (langgraph_declarative)
┌─────────────────┐        ┌──────────────────────────────┐
│ @registry.node  │───────>│  Registry → Loader → Schema  │
│ @registry.router│        │       Validator → Builder     │
│ @registry.tool  │        │              ↓                │
│ build_graph()   │───────>│    CompiledStateGraph         │
└─────────────────┘        └──────────────────────────────┘
    workflow.yaml ────────────────────┘
    (or SQLiteLoader)
```

8 modules:

| Module | Responsibility |
|--------|----------------|
| `registry.py` | Node / router / tool namespaces, decorator registration |
| `loader.py` | YAML → dict, `Loader` protocol |
| `loaders/db_loader.py` | `SQLiteLoader` — versioned definitions from a database |
| `schema.py` | Pydantic models, validation, JSON Schema export |
| `builder.py` | `GraphBuilder` — topology assembly, subgraphs, imports, compilation |
| `state_factory.py` | `state:` declarations → TypedDict with reducers |
| `llm_factory.py` | `llm:` config → provider client, tool binding |
| `errors.py` | Error types, `difflib` "did you mean?" suggestions |

Stack: Python 3.10+, LangGraph ≥1.0, Pydantic ≥2.8.2, PyYAML ≥6.0.2, hatchling.

## Where things are

| What | Where |
|------|-------|
| Requirements | `docs/02-requirements/REQUIREMENTS.md` |
| Design | `docs/03-design/DESIGN.md` |
| Roadmap (the only one) | `docs/04-plan/ROADMAP.md` |
| Task files | `docs/04-plan/tasks/` |
| Reviews | `docs/06-review/` |
| Decision log | `DECISIONS.md` |

## Recent Changes

| Date | Change |
|------|--------|
| 2026-05-30 | Requirements and design promoted; 9 v1 tasks created |
| 2026-05-31 | v1 complete — internal `0.1.0` |
| 2026-06-11 | v1.1 and v2 implemented — tasks 014–023 |
| 2026-06-12 | Version set to `0.2.0`; CHANGELOG and public roadmap updated |
| 2026-06-22 | Examples expanded to 12; LangGraph starter template added |
| 2026-07-26 | Maestro upgraded 0.2 → 0.3 (`delivery/` → `docs/`); README rewritten with logo; repo root cleaned; `feat/v1+` promoted to `main` |
| 2026-07-26 | 0.2.0 published to PyPI |
| 2026-08-12 | M05 human-in-the-loop implemented (188 tests); Maestro 0.4.0; single roadmap |
| 2026-10-01 | External review verified; M06–M08 planned; HITL committed; `v0.2.0` tagged; feature tables switched to package versions |
| 2026-10-02 | M06.01–M06.09 implemented (219 tests): router wrapper, `base_dir=`, strict schema, `default:` deprecation, LangGraph ≥1.0 + CI matrix, schema in wheel, durable HITL test, trust docs, atomic SQLite save. Version 0.3.0; `docs/08-deploy/RELEASE.md` added |
