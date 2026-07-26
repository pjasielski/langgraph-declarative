# HANDOFF — langgraph-declarative

**Status:** All milestones shipped — not yet published to PyPI
**Phase:** maintenance
**Updated:** 2026-07-26

---

## Current Focus

The library is feature-complete for its planned scope. Milestones v1, v1.1, and v2 are all implemented, tested (167 tests), and packaged as `0.2.0`.

Remaining work is operational, not feature work:

1. **First PyPI release** — name reserved, `release.yml` wired for Trusted Publishing via OIDC, but nothing has been published and no git release tag exists. See `.sessions/010-main-cleanup/06-pypi-next-steps.md`.
2. **PyPI-safe README assets** — PyPI strips SVG and cannot resolve relative paths, so the logo needs an absolute PNG URL before release.
3. **LangChain outreach** — drafted in `.sessions/007-promotion-marketing/02_langchain-outreach.md`.

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

Stack: Python 3.10+, LangGraph ≥0.2, Pydantic v2, PyYAML, hatchling.

## Where things are

| What | Where |
|------|-------|
| Requirements | `docs/02-requirements/REQUIREMENTS.md` |
| Design | `docs/03-design/DESIGN.md` |
| Delivery roadmap (canonical) | `docs/04-plan/ROADMAP.md` |
| Task files | `docs/04-plan/tasks/` |
| Reviews | `docs/06-review/` |
| Public roadmap | `ROADMAP.md` |
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
