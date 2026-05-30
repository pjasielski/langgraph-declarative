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
