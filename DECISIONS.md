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
| 2026-08-12 | 11-hitl | HITL is milestone M05 (the old "M05 backlog" bucket was never a milestone; ideas moved to Future/F.N), on branch `feat/hitl` off `dev` | Confirmed |
| 2026-08-12 | 11-hitl | Checkpointer is caller-supplied and never defaulted — a default is silently ignored under `langgraph dev`/Platform (ADR-004) | Confirmed |
| 2026-08-12 | 11-hitl | Checkpointer goes only to the top-level `compile()`; nested subgraphs inherit the parent's (ADR-005, verified on LangGraph 1.2.2) | Confirmed |
| 2026-08-12 | 11-hitl | `destinations:` declared per node rather than inferred — without it, `Command(goto=…)` nodes render a *wrong* `--> END` edge (ADR-006) | Confirmed |
| 2026-08-12 | 11-hitl | HITL acceptance asserts side effects (accept writes / reject does not), not return status | Confirmed |
| 2026-08-12 | 11-hitl | Maestro upgraded to v0.4.0; roadmap migrated to `M{MM}.{NN}` format | Confirmed |
| 2026-08-12 | 11-hitl | Root `ROADMAP.md` deleted — one roadmap only, at `docs/04-plan/ROADMAP.md`, per the Maestro standard | Confirmed |
| 2026-10-01 | 013-codex-review | Codex review (2026-09-25) verified and accepted as the basis for M06 (0.3.0 hardening) and M07 (0.4.0 capabilities); platform-adapter work is M08, demand-gated | Confirmed |
| 2026-10-01 | 013-codex-review | 0.3.0 ships M05 (HITL) and M06 (hardening) together | Confirmed |
| 2026-10-01 | 013-codex-review | LangGraph dependency is `langgraph>=1.0`, no upper cap — `>=0.4,<2` rejected as confusing (ADR-008) | Confirmed |
| 2026-10-01 | 013-codex-review | Unknown YAML keys are rejected (`extra="forbid"`) with an explicit `description:` field — breaking, 0.x (ADR-007) | Confirmed |
| 2026-10-01 | 013-codex-review | Relative paths resolve against the declaring file; file-less builds need `base_dir=` or raise (ADR-009) | Confirmed |
| 2026-10-01 | 013-codex-review | State `default:` deprecated and documented as introspection-only (ADR-010) | Confirmed |
| 2026-10-01 | 013-codex-review | Workflow definitions are trusted input; HITL host responsibilities documented, restricted mode deferred to M08 (ADR-011) | Confirmed |
| 2026-10-01 | 013-codex-review | Versioning: feature tables use package versions (0.1.0/0.2.0/0.3.0), not milestone labels; tags `vX.Y.Z` only for published releases | Confirmed |
| 2026-10-01 | 013-codex-review | `v0.2.0` tagged retroactively on `f17b9be` — source and README verified identical to the PyPI wheel; 0.1.0 (internal) stays untagged | Confirmed |
| 2026-10-01 | 013-codex-review | Milestone estimate: one session per milestone | Confirmed |
