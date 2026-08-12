# Decision Log

| Date | Session | Decision | Status |
|------|---------|----------|--------|
| 2026-05-25 | 001-exploration | API: `Registry()` instance with `@registry.node()` and `@registry.router()` decorators | Confirmed |
| 2026-05-25 | 001-exploration | API: `build_graph()` convenience function + `GraphBuilder` power-user class | Confirmed |
| 2026-05-25 | 001-exploration | Conditional edges: mapped routing — `path:` (registry router) + `targets:` (key-to-node map) | Confirmed |
| 2026-05-25 | 001-exploration | V1 scope: registry, builder, conditional edges, YAML validation, error messages, tests, README, PyPI | Confirmed |
| 2026-05-25 | 001-exploration | Model factory deferred to v1.1 (code exists in prior production project, port later) | Confirmed |
| 2026-05-25 | 001-exploration | Library first, templates later | Confirmed |
| 2026-05-25 | 001-exploration | License: MIT (matches LangGraph) | Confirmed |
| 2026-05-25 | 001-exploration | Package name: `langgraph-declarative` / import: `langgraph_declarative` | Confirmed |
| 2026-05-30 | 001-exploration | Delivery approach: scope v1+v2, implement v1 first | Confirmed |
| 2026-05-30 | 001-exploration | Send supported from v1 via router return type (not a default edge type) | Confirmed |
| 2026-05-30 | 001-exploration | `build_graph()` defaults to `MessagesState`, optional `state_class` override | Confirmed |
| 2026-05-30 | 001-exploration | Repo: `src/` layout, `pyproject.toml` with hatchling, pytest, Python 3.10+ | Confirmed |
| 2026-08-12 | 11-hitl | HITL is milestone M06 targeting v2.1, on branch `feat/hitl` off `dev` | Confirmed |
| 2026-08-12 | 11-hitl | Checkpointer is caller-supplied and never defaulted — a default is silently ignored under `langgraph dev`/Platform (ADR-004) | Confirmed |
| 2026-08-12 | 11-hitl | Checkpointer goes only to the top-level `compile()`; nested subgraphs inherit the parent's (ADR-005, verified on LangGraph 1.2.2) | Confirmed |
| 2026-08-12 | 11-hitl | `destinations:` declared per node rather than inferred — without it, `Command(goto=…)` nodes render a *wrong* `--> END` edge (ADR-006) | Confirmed |
| 2026-08-12 | 11-hitl | HITL acceptance asserts side effects (accept writes / reject does not), not return status | Confirmed |
| 2026-08-12 | 11-hitl | Maestro upgraded to v0.4.0; roadmap migrated to `M{MM}.{NN}` format, `docs/04-plan/ROADMAP.md` canonical | Confirmed |
