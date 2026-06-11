# Task 018: Subgraph Composition
**Status:** todo
**Priority:** high
**Assigned:** unassigned
**Blocked by:** task-014
**Effort:** XL
**Created:** 2026-06-11
**Completed:**

## Description
Enable modular, multi-file workflows by allowing a node definition to reference another YAML file as a subgraph. `subgraph: "file.yaml"` compiles the referenced file into a sub-graph and embeds it as a node in the parent graph.

## Acceptance Criteria
- [ ] `subgraph:` field on NodeConfig as alternative to `function:`
- [ ] Subgraph YAML file compiled and embedded as a compiled graph node
- [ ] Registry shared between parent and subgraph (or explicitly scoped)
- [ ] Relative paths resolved from parent YAML location
- [ ] Circular subgraph references detected and rejected with clear error
- [ ] Subgraph can declare its own `state:` (v1.1 feature)
- [ ] Tests: basic subgraph, nested subgraphs (2 levels), circular detection, state isolation

## Files
- `src/langgraph_declarative/schema.py` (extend NodeConfig with optional `subgraph:`)
- `src/langgraph_declarative/builder.py` (handle subgraph compilation and embedding)
- `tests/test_subgraph.py` (new)
- `tests/fixtures/subgraph_parent.yaml` (new)
- `tests/fixtures/subgraph_child.yaml` (new)

## Notes
- LangGraph supports compiled graphs as nodes via `graph.add_node("name", compiled_subgraph)`
- Key design decision: should subgraphs share the parent registry or have their own?
  Recommendation: shared registry (simpler, covers most use cases)
- Circular detection: track file paths during recursive compilation
- PRD: FR-17
