# Task 011: Add Custom State Example
**Status:** done
**Priority:** medium
**Assigned:** unassigned
**Blocked by:** —
**Effort:** S
**Created:** 2026-06-11
**Completed:** 2026-06-11

## Description
Add a runnable example that uses a custom state class instead of the default `MessagesState`. This demonstrates the `state_class` parameter of `build_graph()` / `GraphBuilder` and shows users how to use the library for non-chatbot workflows.

## Acceptance Criteria
- [x] `examples/custom_state/workflow.yaml` + `examples/custom_state/main.py`
- [x] Custom `TypedDict` or `BaseModel` state class with domain-specific fields (not messages)
- [x] Script runs successfully with `python3 examples/custom_state/main.py`
- [x] Output shows state transformations through the graph
- [x] No new dependencies added

## Files
- `examples/custom_state/workflow.yaml` (create)
- `examples/custom_state/main.py` (create)

## Notes
- Good domain example: data processing pipeline (input → transform → validate → output)
- Keep it simple — 3-4 nodes, linear or branching, with typed state fields
- Show the `state_class=MyState` parameter in the `build_graph()` call
