# Task 017: Match Routing Syntax
**Status:** todo
**Priority:** medium
**Assigned:** unassigned
**Blocked by:** —
**Effort:** M
**Created:** 2026-06-11
**Completed:**

## Description
Add a `match:` routing syntax to YAML that enables simple value-matching routing without writing a Python router function. `match: "field_name"` reads `state.field_name` and uses the value as a lookup key in the `targets:` map. No `eval()` — pure `getattr` + dict lookup.

## Acceptance Criteria
- [ ] `match:` field added to EdgeConfig as alternative to `path:`
- [ ] `match:`, `path:`, and `target:` are mutually exclusive (schema enforces)
- [ ] `match: "field_name"` reads `state.field_name` at runtime
- [ ] Supports dot-notation for nested access: `match: "result.status"` (one level)
- [ ] Value looked up in `targets:` map; `default` key used as fallback
- [ ] Error if value not found in targets and no default
- [ ] No `eval()`, no arbitrary expressions — attribute access only
- [ ] Schema validation rejects `match:` without `targets:`
- [ ] Tests: basic matching, default fallback, missing key error, nested access, schema validation

## Files
- `src/langgraph_declarative/schema.py` (extend EdgeConfig with `match:`)
- `src/langgraph_declarative/builder.py` (generate router function from match config)
- `tests/test_match_routing.py` (new)
- `tests/fixtures/match_routing.yaml` (new)

## Notes
- YAML format example:
  ```yaml
  edges:
    - source: "classifier"
      match: "category"
      targets:
        billing: "billing_agent"
        technical: "tech_agent"
        default: "general_agent"
  ```
- At build time, the builder creates a synthetic router function equivalent to:
  ```python
  def _match_router(state):
      value = getattr(state, "category")
      return value
  ```
- The generated function is passed to `add_conditional_edges` with the targets path_map
- PRD: FR-18 (originally v2, moved to v1.1 in ROADMAP)
