# Task 021: Database-Driven Graph Source
**Status:** done
**Priority:** low
**Assigned:** unassigned
**Blocked by:** task-014
**Effort:** L
**Created:** 2026-06-11
**Completed:** 2026-06-11

## Description
Add a loader that reads graph definitions from a database instead of YAML files, enabling runtime workflow management without file deployments. Leverages the existing loader abstraction (ADR-003).

## Acceptance Criteria
- [x] Pluggable loader interface formalized (protocol or ABC)
- [x] Database loader implementation for at least one backend (PostgreSQL or SQLite)
- [x] Graph definition stored as JSON/YAML text in a table
- [x] `build_graph_from_db(source_id, registry, ...)` convenience function
- [x] Version/revision tracking for stored graph definitions
- [x] Tests: load from DB, missing source error, version handling

## Files
- `src/langgraph_declarative/loader.py` (formalize loader protocol)
- `src/langgraph_declarative/loaders/` (new package)
- `src/langgraph_declarative/loaders/db_loader.py` (new)
- `src/langgraph_declarative/__init__.py` (export new function)
- `tests/test_db_loader.py` (new)

## Notes
- ADR-003 anticipated this: "V2 can add loaders without changing the builder"
- Current `load_yaml()` is a plain function. Formalize into a `Loader` protocol:
  ```python
  class Loader(Protocol):
      def load(self, source: str) -> dict: ...
  ```
- DB dependency (sqlalchemy or similar) must be optional — extras install
- Consider: should the DB loader also store node function source code? Probably not — keep registry as the function source, DB as the topology source.
- PRD: referenced in v2 roadmap
