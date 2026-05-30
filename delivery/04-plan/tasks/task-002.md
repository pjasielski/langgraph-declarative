# Task 002: Implement Errors Module

**Status:** todo
**Priority:** high
**Assigned:** unassigned
**Blocked by:** task-001
**Effort:** S
**Created:** 2026-05-30
**Completed:**

## Description

Implement custom exception classes and the typo-suggestion helper functions per SDD `errors.py` spec (~60 lines). These are used by registry, schema, and builder modules for consistent error handling.

## Acceptance Criteria

- [ ] Exception hierarchy: `DeclarativeError` (base), `ConfigLoadError`, `ConfigValidationError`, `NodeNotFoundError`, `RouterNotFoundError`
- [ ] `suggest_similar(name, available, n=3)` returns close matches using `difflib.get_close_matches`
- [ ] `format_not_found(kind, name, available)` formats a message with the missing name, kind, and suggestions
- [ ] Tests in `tests/test_errors.py` covering:
  - `suggest_similar` returns correct matches and handles empty lists
  - `format_not_found` includes kind, name, and suggestions in output
  - Exception hierarchy is correct (`isinstance` checks)

## Files

- `src/langgraph_declarative/errors.py` — implement
- `tests/test_errors.py` — create

## Notes

- Uses only `difflib` from stdlib — no extra dependencies
- `get_close_matches` default cutoff (0.6) is fine for typo detection
