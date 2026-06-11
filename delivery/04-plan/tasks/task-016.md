# Task 016: JSON Schema for YAML Files
**Status:** todo
**Priority:** medium
**Assigned:** unassigned
**Blocked by:** task-014
**Effort:** S
**Created:** 2026-06-11
**Completed:**

## Description
Publish a JSON Schema derived from the Pydantic `GraphConfig` model so that IDEs (VS Code, JetBrains) can provide autocomplete, validation, and hover docs when editing workflow YAML files.

## Acceptance Criteria
- [ ] `export_json_schema()` function returns the JSON Schema as a dict
- [ ] Schema exported to `schema/workflow.schema.json` in the package
- [ ] Schema covers all YAML fields including the v1.1 `state:` section
- [ ] Users can reference the schema via `# yaml-language-server: $schema=...`
- [ ] Public API exported from `__init__.py`
- [ ] Tests: schema validates known-good YAML fixtures, rejects known-bad ones

## Files
- `src/langgraph_declarative/schema.py` (add `export_json_schema` function)
- `src/langgraph_declarative/__init__.py` (export)
- `schema/workflow.schema.json` (generated artifact, committed)
- `tests/test_json_schema.py` (new)

## Notes
- Pydantic v2's `model_json_schema()` does most of the work
- Blocked by task-014 because the schema should include `state:` fields
- Consider adding `$schema` to example YAML files as a demonstration
- PRD: FR-16
