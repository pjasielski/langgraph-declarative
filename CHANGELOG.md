# Changelog

## v0.2.0 (2026-07-26)

First public release — includes everything from milestones v1, v1.1, and v2.

### v1.1 features

- **State declaration in YAML** — define state fields, types (`str`, `int`, `list[str]`, …), and reducers (`append`, `add_messages`, `replace`) directly in the workflow file instead of writing a Python state class
- **Match routing** — route on a state field's value with `match:` + `targets:` in YAML, no Python router function needed; supports dot-notation for nested fields and a `default` fallback key
- **Mermaid diagram generation** — `draw_mermaid()` compiles a workflow and renders it as a Mermaid diagram (`.md` fenced block or raw output)
- **JSON Schema for YAML files** — `export_json_schema()` emits a schema that gives IDEs autocomplete and validation for workflow YAML; ships at `schema/workflow.schema.json`

### v2 features

- **Subgraph composition** — `subgraph: "child.yaml"` on a node embeds another workflow as a single node, with parent/child state sharing via common keys
- **Cross-file node imports** — `imports:` merges node declarations from shared library files; selective import with `nodes: [...]`
- **LLM configuration in YAML** — graph-level `llm:` default and node-level overrides; nodes opt in by accepting an `llm` parameter; supports `anthropic` and `openai` providers
- **Tool binding in YAML** — `tools:` on a node binds `@registry.tool()` functions or `"module.path:attr"` references to the node's LLM
- **Database-driven workflow source** — `SQLiteLoader` saves/loads versioned definitions; `build_graph_from_db()` compiles from DB with `"source"` or `"source@version"` pinning
- **LangGraph project template** — starter project scaffold for `langgraph dev` using the declarative pattern
- **12 runnable examples** — one per feature, organized by milestone

### Other

- Test suite expanded to 167 tests
- Pydantic cross-validation catches function/router reference errors with "did you mean?" suggestions

## v0.1.0 (2026-05-31)

Initial release (internal milestone v1).

### Features

- **Registry** -- `@registry.node()` and `@registry.router()` decorators for function registration
- **YAML graph definition** -- declare nodes and edges in YAML
- **All edge types** -- simple, fan-out (parallel), conditional (mapped routing), dynamic (Send)
- **Schema validation** -- Pydantic-based YAML validation with clear error messages
- **Cross-validation** -- checks function/router refs exist, edge targets reference defined nodes
- **Typo suggestions** -- `difflib`-based "did you mean?" on lookup failures
- **`build_graph()`** -- one-line convenience function for YAML-to-compiled-graph
- **`GraphBuilder`** -- power-user class for more control over compilation
- **Default `MessagesState`** -- chatbot graphs need no explicit state class
