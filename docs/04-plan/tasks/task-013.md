# Task 013: Edge-Case Tests and Hardening

**Status:** done
**Priority:** medium
**Assigned:** unassigned
**Blocked by:** —
**Effort:** S
**Created:** 2026-06-11
**Completed:** 2026-06-11

## Description

Add targeted tests for boundary conditions and edge cases not covered by the v1 test suite. These are meaningful gaps — not padding.

## Acceptance Criteria

- [x] Test: empty YAML file raises `ConfigLoadError` (not a cryptic error)
- [x] Test: YAML with only nodes and no edges raises clear validation error
- [x] Test: YAML with unknown extra fields (strict parsing behavior documented via test)
- [x] Test: custom state class works end-to-end via `build_graph()` with invoke
- [x] Test: graph with START→single_node→END (minimal viable graph)
- [x] All existing 77 tests still pass (84 total now)
- [x] New tests pass

## Files

- `tests/test_loader.py` (edit — add empty-file and structural tests)
- `tests/test_schema.py` (edit — add unknown-fields and no-edges tests)
- `tests/test_integration.py` (edit — add custom-state and minimal-graph tests)
- `tests/fixtures/` (add any new YAML fixtures needed)

## Notes

- Each test should verify a specific behavior, not just "doesn't crash"
- If the library currently allows unknown fields in YAML, the test documents that as intentional (not a bug)
- The custom-state integration test is the most valuable — it proves the `state_class` parameter works through the full pipeline
