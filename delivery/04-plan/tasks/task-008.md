# Task 008: Create Examples

**Status:** todo
**Priority:** medium
**Assigned:** unassigned
**Blocked by:** task-007
**Effort:** S
**Created:** 2026-05-30
**Completed:**

## Description

Create runnable example projects demonstrating library usage per SDD source structure. Each example should be self-contained and serve as both documentation and additional validation.

## Acceptance Criteria

- [ ] `examples/quickstart/` — minimal working example (linear graph, 2-3 nodes)
  - `workflow.yaml` — graph definition
  - `main.py` — registry setup + build_graph + invoke
- [ ] `examples/conditional_routing/` — conditional edges with mapped routing
  - `workflow.yaml` — graph with path + targets
  - `main.py` — router function + invocation showing different paths
- [ ] Both examples run successfully and produce expected output
- [ ] Examples use comments explaining key concepts

## Files

- `examples/quickstart/workflow.yaml` — create
- `examples/quickstart/main.py` — create
- `examples/conditional_routing/workflow.yaml` — create
- `examples/conditional_routing/main.py` — create

## Notes

- Examples should be copy-paste ready for the README quickstart section
- Keep them minimal — demonstrate the concept, not every feature
