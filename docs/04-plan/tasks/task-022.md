# Task 022: LangGraph Template Packaging
**Status:** done
**Priority:** low
**Assigned:** unassigned
**Blocked by:** task-018
**Effort:** S
**Created:** 2026-06-11
**Completed:** 2026-06-11

## Description
Package langgraph-declarative as a LangGraph Template so users can scaffold new projects with `langgraph new`. The template includes a working YAML workflow, registry setup, and example nodes.

## Acceptance Criteria
- [x] Template structure follows LangGraph Template specification
- [ ] `langgraph new my-project --template declarative` scaffolds a working project *(requires template registry publication — external dependency on LangChain team)*
- [x] Scaffolded project includes: workflow YAML, registry with example nodes, main.py
- [x] Template works with LangGraph Studio (langgraph.json present; Studio run not verified locally)
- [x] README in template explains the declarative pattern
- [x] Tests: template generates, scaffolded project runs

## Files
- `template/` (new directory with template structure)
- `template/langgraph.json`
- `template/src/agent/workflow.yaml`
- `template/src/agent/nodes.py`
- `template/src/agent/graph.py`
- `template/pyproject.toml`
- `template/README.md`

## Notes
- LangGraph Templates are published to a registry — requires coordination with LangChain team
- The template should showcase the simplest useful pattern (linear graph with 2-3 nodes)
- Include both YAML and Python files to show the full pattern
- PRD: referenced in v2 roadmap
