# Task 004: Implement Schema Module + Tests

**Status:** done
**Priority:** high
**Assigned:** unassigned
**Blocked by:** task-001, task-002
**Effort:** M
**Created:** 2026-05-30
**Completed:** 2026-05-31

## Description

Implement Pydantic models for YAML config validation and the cross-validation function per SDD spec (~80 lines). These catch structural errors before graph compilation.

## Acceptance Criteria

- [ ] `NodeConfig` model with `name: str` and `function: str`
- [ ] `EdgeConfig` model with validation: `target` or `path` required (not both absent), `target` and `path` mutually exclusive, `targets` only with `path`
- [ ] `GraphConfig` model with `nodes: list[NodeConfig]` and `edges: list[EdgeConfig]`
- [ ] Duplicate node name validation in `GraphConfig`
- [ ] `validate_config(raw: dict) -> GraphConfig` parses and validates
- [ ] `cross_validate(config, registry)` checks that all `function:` refs exist in registry nodes, all `path:` refs exist in registry routers, and all edge source/target names reference defined nodes or START/END
- [ ] `cross_validate` raises errors with typo suggestions
- [ ] Tests in `tests/test_schema.py` covering:
  - Valid config parses successfully
  - Missing `target` and `path` raises error
  - Both `target` and `path` raises error
  - `targets` without `path` raises error
  - Duplicate node names raises error
  - `cross_validate` catches missing node/router refs
  - `cross_validate` catches edge references to undefined nodes

## Files

- `src/langgraph_declarative/schema.py` — implement
- `tests/test_schema.py` — create

## Notes

- `cross_validate` needs a `Registry` instance — import from registry module
- START and END are valid edge source/target names (handled as special cases)
