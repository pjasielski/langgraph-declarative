# Task 015: Auto-Mermaid Generation
**Status:** done
**Priority:** medium
**Assigned:** unassigned
**Blocked by:** —
**Effort:** S
**Created:** 2026-06-11
**Completed:** 2026-06-11

## Description
Expose LangGraph's built-in `.get_graph().draw_mermaid()` through a convenience function so users can generate visual graph diagrams from YAML without manually accessing the compiled graph internals.

## Acceptance Criteria
- [x] `draw_mermaid(path, registry, state_class=None)` convenience function added
- [x] `GraphBuilder.draw_mermaid(config)` method added for power users
- [x] Returns Mermaid-format string (same output as LangGraph's native method)
- [x] Optional `output_path` parameter writes to file (`.md` or `.mmd`)
- [x] Public API exported from `__init__.py`
- [x] Tests: output contains expected node names, edge structure matches YAML

## Files
- `src/langgraph_declarative/__init__.py` (add `draw_mermaid` function)
- `src/langgraph_declarative/builder.py` (add `draw_mermaid` method to GraphBuilder)
- `tests/test_mermaid.py` (new)

## Notes
- LangGraph's `compiled_graph.get_graph().draw_mermaid()` does the heavy lifting
- This is a thin wrapper — compile the graph, call draw_mermaid, return/write result
- Keep it simple: no custom styling or layout options in v1.1
- PRD: FR-15
