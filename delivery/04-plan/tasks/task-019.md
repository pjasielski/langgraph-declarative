# Task 019: Tool Configuration in YAML
**Status:** todo
**Priority:** medium
**Assigned:** unassigned
**Blocked by:** task-020
**Effort:** L
**Created:** 2026-06-11
**Completed:**

## Description
Allow YAML to reference LangChain tools or MCP tools by name and wire them to nodes automatically. Nodes with a `tools:` list receive the tools as an argument or have them bound to the LLM.

## Acceptance Criteria
- [ ] `tools:` list on node definitions in YAML
- [ ] Tools resolved from a tool registry or by import path
- [ ] Tools automatically bound to the node's LLM (requires task-020)
- [ ] Support for LangChain tool classes and `@tool` decorated functions
- [ ] Error if referenced tool not found, with suggestions
- [ ] Tests: tool binding, missing tool error, integration with LLM config

## Files
- `src/langgraph_declarative/schema.py` (extend NodeConfig with `tools:`)
- `src/langgraph_declarative/builder.py` (tool resolution and binding)
- `src/langgraph_declarative/registry.py` (optional: tool registry)
- `tests/test_tools.py` (new)
- `tests/fixtures/tools_workflow.yaml` (new)

## Notes
- Tool wiring depends on LLM config (task-020) since tools are typically bound via `llm.bind_tools()`
- Consider supporting both registered tools and import-path tools:
  ```yaml
  nodes:
    - name: agent
      function: chat_node
      tools: ["search_web", "calculator"]
  ```
- Design decision needed: separate tool registry (`@registry.tool()`) vs. reuse node registry
- PRD: referenced in v2 roadmap
