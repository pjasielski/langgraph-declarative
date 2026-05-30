# Task 009: Finalize Packaging and README

**Status:** todo
**Priority:** medium
**Assigned:** unassigned
**Blocked by:** task-007
**Effort:** S
**Created:** 2026-05-30
**Completed:**

## Description

Finalize `pyproject.toml` metadata for PyPI publishing, update README with quickstart, features, and API reference. Create CHANGELOG.md.

## Acceptance Criteria

- [ ] `pyproject.toml` has complete metadata: name, version (0.1.0), description, author, license (MIT), classifiers, URLs (repository, homepage)
- [ ] README.md includes:
  - One-line description and badges placeholder
  - Installation instructions (`pip install langgraph-declarative`)
  - Quickstart (from examples/quickstart)
  - Feature list (all edge types)
  - YAML format reference
  - API reference (`Registry`, `GraphBuilder`, `build_graph`)
- [ ] `LICENSE` file with MIT license text
- [ ] `CHANGELOG.md` with v0.1.0 entry
- [ ] Package builds successfully (`python -m build` or `hatch build`)

## Files

- `pyproject.toml` — update metadata
- `README.md` — update
- `LICENSE` — create
- `CHANGELOG.md` — create

## Notes

- Version 0.1.0 (not 1.0.0) — signals initial release, pre-stable
- README quickstart should match examples/quickstart exactly
- Test the build step to catch packaging issues before publishing
