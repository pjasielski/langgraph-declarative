# Task 016: JSON Schema for YAML Files
**Status:** done
**Priority:** medium
**Assigned:** unassigned
**Blocked by:** task-014
**Effort:** S
**Created:** 2026-06-11
**Completed:** 2026-06-11

## Description
Publish a JSON Schema derived from the Pydantic `GraphConfig` model so that IDEs (VS Code, JetBrains) can provide autocomplete, validation, and hover docs when editing workflow YAML files.

## Acceptance Criteria
- [x] `export_json_schema()` function returns the JSON Schema as a dict
- [x] Schema exported to `schema/workflow.schema.json` in the package
- [x] Schema covers all YAML fields including the v1.1 `state:` section
- [x] Users can reference the schema via `# yaml-language-server: $schema=...`
- [x] Public API exported from `__init__.py`
- [x] Tests: schema validates known-good YAML fixtures, rejects known-bad ones

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
