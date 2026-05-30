# Task 007: Implement Public API + Integration Tests

**Status:** todo
**Priority:** high
**Assigned:** unassigned
**Blocked by:** task-006
**Effort:** M
**Created:** 2026-05-30
**Completed:**

## Description

Wire up the public API in `__init__.py` and write end-to-end integration tests that exercise the full pipeline: YAML file → `build_graph()` → graph invocation → verify output.

## Acceptance Criteria

- [ ] `__init__.py` exports: `Registry`, `GraphBuilder`, `build_graph`
- [ ] `build_graph(path, registry, state_class=None)` convenience function works
- [ ] `__all__` defined correctly
- [ ] Integration tests in `tests/test_integration.py` covering:
  - Simple linear graph: invoke and verify state transitions
  - Fan-out graph: invoke and verify parallel execution
  - Conditional routing: invoke with different inputs, verify correct path taken
  - Dynamic routing (Send): invoke and verify Send-based fan-out
  - Full-featured graph (combines multiple edge types)
- [ ] Tests use real LangGraph graph invocation (`.invoke()`) — not mocked
- [ ] YAML fixture `tests/fixtures/full_featured.yaml` created

## Files

- `src/langgraph_declarative/__init__.py` — implement public API
- `tests/test_integration.py` — create
- `tests/fixtures/full_featured.yaml` — create
- `tests/conftest.py` — add shared fixtures (sample registry with test node/router functions)

## Notes

- Integration tests need actual node/router functions — define them in `conftest.py` or in the test file
- These tests confirm the compiled graph is functionally identical to a hand-built equivalent
- This is where the library proves it works end-to-end
