# langgraph-declarative

Declarative graph definition for [LangGraph](https://github.com/langchain-ai/langgraph) — describe your workflow's **topology in YAML**, keep the **logic in Python**, and compile with one line of code.

The library has three pieces:

1. **Registry** — register node, router, and tool functions in Python with decorators (`@registry.node()`, `@registry.router()`, `@registry.tool()`).
2. **Workflow definition** — declare nodes, edges, state, and LLM config in YAML (or load it from a database). Definitions are validated with Pydantic and cross-checked against the registry, with actionable "did you mean…?" error messages.
3. **Builder** — `build_graph()` turns definition + registry into a standard LangGraph `CompiledStateGraph`, ready for `.invoke()`. Nothing about downstream usage changes.

Why bother? **Topology changes become config edits, not code rewrites.** Workflow structure can be diffed in review, validated in IDEs, rendered as a diagram, stored and versioned in a database, and read by people who don't write Python.

## Quickstart

### Install

```bash
pip install langgraph-declarative          # uv add langgraph-declarative
pip install "langgraph-declarative[anthropic]"   # optional: LLM config support ([openai] also available)
```

### Register node functions

```python
from langgraph_declarative import Registry, build_graph

registry = Registry()

@registry.node("greet")
def greet(state):
    return {"messages": [{"role": "assistant", "content": "Hello! How can I help?"}]}

@registry.node("respond")
def respond(state):
    return {"messages": [{"role": "assistant", "content": "Goodbye!"}]}
```

### Declare the graph in YAML

```yaml
# workflow.yaml
nodes:
  - name: "greeter"
    function: "greet"
  - name: "responder"
    function: "respond"

edges:
  - source: "START"
    target: "greeter"
  - source: "greeter"
    target: "responder"
  - source: "responder"
    target: "END"
```

### Build and run

```python
graph = build_graph("workflow.yaml", registry)
result = graph.invoke({"messages": [{"role": "user", "content": "Hi there"}]})
```

## Features

Every feature has a commented, runnable example — see **[examples/](examples/README.md)** for the full guide.

| Feature | YAML | Since | Example |
|---|---|---|---|
| Simple & parallel edges | `target: "node"` / `target: [a, b]` | v1 | [quickstart](examples/quickstart/), [fan_out](examples/fan_out/) |
| Conditional routing | `path:` + `targets:` | v1 | [conditional_routing](examples/conditional_routing/) |
| Dynamic fan-out (`Send`) | `path:` without `targets` | v1 | [dynamic_routing](examples/dynamic_routing/) |
| Custom Python state class | `build_graph(..., state_class=...)` | v1 | [custom_state](examples/custom_state/) |
| State declared in YAML | `state:` with types & reducers | v1.1 | [declared_state](examples/declared_state/) |
| Match routing (no router fn) | `match:` + `targets:` | v1.1 | [match_routing](examples/match_routing/) |
| Mermaid diagrams | `draw_mermaid()` | v1.1 | [visualization](examples/visualization/) |
| IDE autocomplete & validation | `export_json_schema()` + [schema](schema/workflow.schema.json) | v1.1 | [visualization](examples/visualization/) |
| Subgraph composition | `subgraph: "child.yaml"` | v2 | [subgraph](examples/subgraph/) |
| Cross-file node imports | `imports:` | v2 | [cross_file_imports](examples/cross_file_imports/) |
| LLM config & tool binding | `llm:` + `tools:` | v2 | [llm_and_tools](examples/llm_and_tools/) |
| Database-stored workflows | `SQLiteLoader`, `build_graph_from_db()` | v2 | [db_workflow](examples/db_workflow/) |
| LangGraph project template | — | v2 | [template/](template/) |

## YAML reference

All sections except `nodes` are optional.

```yaml
state:                              # declare the state schema (default: MessagesState)
  - name: "category"
    type: "str"                     # str | int | float | bool | list | dict | list[str] | list[dict]
  - name: "notes"
    type: "list[str]"
    reducer: "append"               # append | add_messages | replace (default)

llm:                                # graph-level LLM default for opt-in nodes
  provider: "anthropic"             # anthropic | openai
  model: "claude-opus-4-8"

imports:                            # merge node declarations from other files
  - file: "shared_nodes.yaml"
    nodes: ["error_handler"]        # omit to import all nodes

nodes:
  - name: "classifier"
    function: "classify"            # registered via @registry.node()
  - name: "research"
    subgraph: "child.yaml"          # embed another workflow (function XOR subgraph)
  - name: "agent"
    function: "agent_fn"            # function must accept an `llm` parameter to opt in
    llm: { model: "claude-haiku-4-5" }  # node-level override, merged over graph llm
    tools: ["get_weather"]          # @registry.tool() names or "module.path:attr"

edges:
  - source: "START"                 # START, END, or a node name
    target: "classifier"            # simple edge
  - source: "loader"
    target: ["a", "b"]              # parallel fan-out
  - source: "classifier"
    path: "router_name"             # @registry.router(); omit targets for Send routing
    targets: { key: "node" }
  - source: "classifier"
    match: "category"               # route on a state field's value — no Python router
    targets:
      billing: "billing_agent"
      default: "fallback"           # reserved fallback key
```

Add `# yaml-language-server: $schema=path/to/workflow.schema.json` as the first line to get IDE validation and autocomplete (schema ships at [schema/workflow.schema.json](schema/workflow.schema.json)).

## API

| Function / Class | Description |
|---|---|
| `Registry()` | Holds node, router, and tool functions in separate namespaces |
| `@registry.node("name")` | Register a node function (transforms state) |
| `@registry.router("name")` | Register a router function (returns a routing key or `Send` list) |
| `@registry.tool("name")` | Register a tool for `tools:` binding |
| `build_graph(path, registry, state_class=None)` | YAML file → compiled `CompiledStateGraph` |
| `build_graph_from_db(source, registry, db_path)` | DB-stored definition → compiled graph (`"flow"` or `"flow@2"`) |
| `draw_mermaid(path, registry, output_path=None)` | Compile and render a Mermaid diagram (`.md` → fenced block) |
| `export_json_schema(output_path=None)` | Emit the JSON Schema for workflow YAML files |
| `GraphBuilder(registry, state_class=None)` | Power-user class behind `build_graph()` |
| `SQLiteLoader(db_path)` | Save/load versioned definitions; implements the pluggable `Loader` protocol |

## Documentation

| Document | Contents |
|---|---|
| [examples/README.md](examples/README.md) | 12 runnable examples, organized by version, with a feature map |
| [ROADMAP.md](ROADMAP.md) | Shipped scope per version and unvalidated future ideas |
| [CHANGELOG.md](CHANGELOG.md) | Release history |
| [DECISIONS.md](DECISIONS.md) | Decision log — why the API and scope look the way they do |
| [PRD](delivery/02-prd/PRD.md) | Product requirements: problem, users, success criteria |
| [SDD](delivery/03-design/SDD.md) | Software design: architecture, module responsibilities, trade-offs |
| [PLAN](delivery/04-plan/PLAN.md) | Implementation plan and task breakdown |
| [template/](template/) | Starter project for `langgraph dev` using the declarative pattern |

## Project layout

```
src/langgraph_declarative/   # library code (registry, schema, builder, state/llm factories, loaders)
schema/                      # generated JSON Schema for workflow YAML
examples/                    # runnable examples (one folder per feature)
template/                    # LangGraph starter template
tests/                       # pytest suite + YAML fixtures
delivery/                    # PRD, SDD, plan, reviews
```

## Status

v1 (core), v1.1 (state-in-YAML, match routing, Mermaid, JSON Schema), and v2 (subgraphs, imports, LLM/tools, DB source, template) are implemented. See [ROADMAP.md](ROADMAP.md) for future ideas (graph diffing, hot-reload, CLI, …).

## Requirements

- Python 3.10+
- LangGraph ≥ 0.2, PyYAML ≥ 6.0, Pydantic ≥ 2.0
- Optional extras: `[anthropic]` / `[openai]` for `llm:` support

## License

MIT
