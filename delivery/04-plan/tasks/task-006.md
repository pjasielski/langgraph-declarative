# Task 006: Implement Builder Module + Tests

**Status:** done
**Priority:** high
**Assigned:** unassigned
**Blocked by:** task-002, task-003, task-004, task-005
**Effort:** L
**Created:** 2026-05-30
**Completed:** 2026-05-31

## Description

Implement the `GraphBuilder` class that compiles a validated config + registry into a LangGraph `CompiledStateGraph` per SDD spec (~120 lines). This is the core engine of the library.

## Acceptance Criteria

- [ ] `GraphBuilder(registry, state_class=None)` — defaults `state_class` to `MessagesState`
- [ ] `build(config: GraphConfig) -> CompiledStateGraph` compiles a validated config
- [ ] `build_from_file(path) -> CompiledStateGraph` — full pipeline: load → validate → cross-validate → build
- [ ] Correctly handles all 4 edge types:
  - Simple edge: `target: "node_name"` → `add_edge()`
  - Fan-out: `target: ["a", "b"]` → multiple `add_edge()` calls
  - Conditional (mapped): `path` + `targets` → `add_conditional_edges()` with `path_map`
  - Dynamic (Send): `path` without `targets` → `add_conditional_edges()` without `path_map`
- [ ] START/END string literals resolve to LangGraph `START` and `END` constants
- [ ] Tests in `tests/test_builder.py` covering:
  - Build a simple linear graph (START → A → B → END)
  - Build a fan-out graph (A → [B, C])
  - Build a conditional routing graph (path + targets)
  - Build a dynamic routing graph (path without targets)
  - Cross-validation failure (missing function ref) raises error
  - Custom `state_class` is used when provided
- [ ] YAML test fixtures created for each edge type

## Files

- `src/langgraph_declarative/builder.py` — implement
- `tests/test_builder.py` — create
- `tests/fixtures/simple.yaml` — create or update
- `tests/fixtures/fan_out.yaml` — create
- `tests/fixtures/conditional.yaml` — create
- `tests/fixtures/dynamic_routing.yaml` — create

## Notes

- The builder calls `StateGraph()`, `add_node()`, `add_edge()`, `add_conditional_edges()`, and `.compile()`
- `_resolve_sentinel` maps "START"/"END" strings to `langgraph.graph.START`/`END`
- For conditional edges with `targets`: pass `path_map=targets` to `add_conditional_edges`
- For dynamic routing (no targets): pass the router function directly, no `path_map`
