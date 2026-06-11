# Task 023: Cross-File Node References
**Status:** todo
**Priority:** low
**Assigned:** unassigned
**Blocked by:** task-018
**Effort:** M
**Created:** 2026-06-11
**Completed:**

## Description
Allow YAML workflow files to import and reuse node/router definitions from other YAML files. Enables sharing common nodes (e.g., error handlers, logging nodes) across multiple workflows without duplicating registry setup.

## Acceptance Criteria
- [ ] `imports:` section in YAML references other YAML files
- [ ] Imported nodes available by name in the importing file's edges
- [ ] Import resolution follows relative paths from the importing file
- [ ] Circular imports detected and rejected with clear error
- [ ] Name collisions between imported and local nodes caught with error
- [ ] Tests: basic import, multi-file chain, circular detection, name collision

## Files
- `src/langgraph_declarative/schema.py` (add `imports:` to GraphConfig)
- `src/langgraph_declarative/builder.py` (resolve imports before compilation)
- `tests/test_cross_file.py` (new)
- `tests/fixtures/shared_nodes.yaml` (new)
- `tests/fixtures/importing_workflow.yaml` (new)

## Notes
- YAML format example:
  ```yaml
  imports:
    - file: "shared/error_handlers.yaml"
      nodes: ["error_handler", "retry_node"]
  
  nodes:
    - name: my_node
      function: process
  
  edges:
    - source: "my_node"
      target: "error_handler"  # from import
  ```
- Distinct from subgraph composition (task-018): imports merge node definitions into the current graph, while subgraphs embed a compiled graph as a single node
- This feature + subgraphs together enable full modular workflow architectures
- PRD: referenced in v2 roadmap
