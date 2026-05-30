# TODO — langgraph-declarative

Project backlog. V1 tasks are tracked in `delivery/04-plan/tasks/`. This file captures future work beyond v1.

## v1.1 (fast follow)

- [ ] State declaration in YAML (model factory integration — port from prior project)
- [ ] Auto-Mermaid generation (expose LangGraph's `.draw_mermaid()`)
- [ ] JSON Schema for YAML files (IDE autocomplete when editing workflow YAML)
- [ ] `match:` syntax for simple value-matching routing (no eval, just dict lookup on state field)

## v2 (future)

- [ ] Subgraph composition (`subgraph: "file.yaml"` in node definitions)
- [ ] Tool configuration in YAML (reference LangChain / MCP tools by name)
- [ ] LLM configuration per node in YAML (model, temperature, etc.)
- [ ] Database-driven graph source (alternative to YAML files)
- [ ] LangGraph Template packaging (official template repo)
- [ ] Cross-file model/node references (import mechanism)

## Ideas (unvalidated)

- [ ] Graph diffing — compare two YAML files and report topology changes
- [ ] Hot-reload support — watch YAML file, recompile on change
- [ ] CLI tool (`lgd validate workflow.yaml`, `lgd visualize workflow.yaml`)
- [ ] YAML include/import for shared node definitions across workflows
- [ ] Graph versioning — run A/B tests between YAML variants
- [ ] Export to LangGraph Studio format
