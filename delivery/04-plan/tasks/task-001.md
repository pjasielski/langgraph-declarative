# Task 001: Scaffold Project Structure

**Status:** todo
**Priority:** high
**Assigned:** unassigned
**Blocked by:** —
**Effort:** S
**Created:** 2026-05-30
**Completed:**

## Description

Create the source tree, pyproject.toml, and test infrastructure per SDD section 5. This establishes the foundation for all subsequent tasks.

## Acceptance Criteria

- [ ] `src/langgraph_declarative/` package directory exists with `__init__.py`
- [ ] Empty module files created: `registry.py`, `builder.py`, `schema.py`, `loader.py`, `errors.py`
- [ ] `tests/` directory with `conftest.py` and `tests/fixtures/` directory
- [ ] `pyproject.toml` configured with hatchling, Python >=3.10, dependencies: `langgraph>=0.2`, `pyyaml>=6.0`, `pydantic>=2.0`
- [ ] Dev dependencies: `pytest`
- [ ] `pytest` runs successfully (0 tests collected, no errors)
- [ ] `.gitignore` includes standard Python entries

## Files

- `src/langgraph_declarative/__init__.py` — create (placeholder)
- `src/langgraph_declarative/registry.py` — create (empty)
- `src/langgraph_declarative/builder.py` — create (empty)
- `src/langgraph_declarative/schema.py` — create (empty)
- `src/langgraph_declarative/loader.py` — create (empty)
- `src/langgraph_declarative/errors.py` — create (empty)
- `tests/conftest.py` — create (empty)
- `tests/fixtures/` — create directory
- `pyproject.toml` — create
- `.gitignore` — create or update

## Notes

- SDD specifies hatchling as build backend
- Keep `__init__.py` minimal — just the package marker for now (public API added in task-007)
