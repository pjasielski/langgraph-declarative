# Task 014: State Declaration in YAML
**Status:** todo
**Priority:** high
**Assigned:** unassigned
**Blocked by:** —
**Effort:** L
**Created:** 2026-06-11
**Completed:**

## Description
Allow users to define state fields, types, and reducers directly in YAML instead of writing a Python state class. A `state:` section in the YAML file is compiled into an `Annotated` TypedDict at build time. When `state:` is present, it overrides the default `MessagesState` and any `state_class` parameter.

Ported from a production model factory (~250 lines). Core technique: dynamically create `typing.Annotated[type, reducer]` fields and assemble into a TypedDict subclass that LangGraph accepts as a state annotation.

## Acceptance Criteria
- [ ] YAML `state:` section accepts fields with `name`, `type`, `default`, and `reducer`
- [ ] Supported types: `str`, `int`, `float`, `bool`, `list`, `dict`, `list[str]`, `list[dict]`
- [ ] Supported reducers: `add_messages`, `append`, `replace` (default)
- [ ] Generated state class is a valid LangGraph state annotation
- [ ] When `state:` is present, `state_class` parameter is ignored (with warning)
- [ ] When `state:` is absent, behavior unchanged (backwards compatible)
- [ ] Schema validation catches invalid type/reducer names with suggestions
- [ ] New module `state_factory.py` (~100-150 lines)
- [ ] Tests: valid state generation, type mapping, reducer wiring, invalid configs, integration

## Files
- `src/langgraph_declarative/state_factory.py` (new)
- `src/langgraph_declarative/schema.py` (extend GraphConfig with optional `state:`)
- `src/langgraph_declarative/builder.py` (use state factory when state config present)
- `src/langgraph_declarative/__init__.py` (re-export if needed)
- `tests/test_state_factory.py` (new)
- `tests/fixtures/state_declaration.yaml` (new)

## Notes
- YAML format example:
  ```yaml
  state:
    - name: messages
      type: list
      reducer: add_messages
    - name: summary
      type: str
  ```
- The `add_messages` reducer maps to `langgraph.graph.add_messages`
- `append` reducer = `operator.add` on lists
- `replace` = no annotation (default LangGraph behavior)
- PRD: FR-14
