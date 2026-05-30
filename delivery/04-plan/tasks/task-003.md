# Task 003: Implement Registry Module + Tests

**Status:** todo
**Priority:** high
**Assigned:** unassigned
**Blocked by:** task-001, task-002
**Effort:** M
**Created:** 2026-05-30
**Completed:**

## Description

Implement the `Registry` class with `@node()` and `@router()` decorators per SDD spec (~90 lines). The registry is the user-facing entry point for function registration.

## Acceptance Criteria

- [ ] `Registry` class with separate `_nodes` and `_routers` dicts
- [ ] `@registry.node("name")` decorator registers a function in the nodes namespace
- [ ] `@registry.router("name")` decorator registers a function in the routers namespace
- [ ] `get_node(name)` returns the function or raises `NodeNotFoundError` with suggestions
- [ ] `get_router(name)` returns the function or raises `RouterNotFoundError` with suggestions
- [ ] Duplicate registration raises `ValueError`
- [ ] `list_nodes()` and `list_routers()` return registered names
- [ ] Decorators preserve the original function (return it unwrapped)
- [ ] Tests in `tests/test_registry.py` covering:
  - Register and retrieve a node function
  - Register and retrieve a router function
  - Duplicate name raises `ValueError`
  - Missing name raises appropriate error with suggestion
  - Node and router namespaces are isolated (same name in both is OK)
  - `list_nodes` / `list_routers` accuracy

## Files

- `src/langgraph_declarative/registry.py` — implement
- `tests/test_registry.py` — create

## Notes

- Decorators should return the original function unchanged so decorated functions remain callable outside the graph context
