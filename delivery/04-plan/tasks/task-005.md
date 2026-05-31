# Task 005: Implement Loader Module + Tests

**Status:** done
**Priority:** high
**Assigned:** unassigned
**Blocked by:** task-001, task-002
**Effort:** S
**Created:** 2026-05-30
**Completed:** 2026-05-31

## Description

Implement the YAML file loader per SDD spec (~30 lines). Thin wrapper around PyYAML with proper error handling.

## Acceptance Criteria

- [ ] `load_yaml(path: str | Path) -> dict` loads and parses a YAML file
- [ ] Missing file raises `ConfigLoadError` with the file path in the message
- [ ] Malformed YAML raises `ConfigLoadError` with parse error details
- [ ] Tests in `tests/test_loader.py` covering:
  - Successfully loads a valid YAML file
  - Missing file raises `ConfigLoadError`
  - Malformed YAML raises `ConfigLoadError`

## Files

- `src/langgraph_declarative/loader.py` — implement
- `tests/test_loader.py` — create
- `tests/fixtures/simple.yaml` — create (minimal valid YAML for loader test)

## Notes

- Accept both `str` and `Path` for the path argument
- The loader does NOT validate the YAML structure — that's the schema module's job
