<div align="center">

<img alt="langgraph-declarative" src="https://raw.githubusercontent.com/pjasielski/langgraph-declarative/main/assets/logo.png" width="440">

**Topology in YAML. Logic in Python. One line to compile.**

[![CI](https://github.com/pjasielski/langgraph-declarative/actions/workflows/ci.yml/badge.svg)](https://github.com/pjasielski/langgraph-declarative/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-6366F1)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-2DD4BF)](https://github.com/pjasielski/langgraph-declarative/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/langgraph-declarative?color=2DD4BF)](https://pypi.org/project/langgraph-declarative/)
[![Downloads](https://img.shields.io/pepy/dt/langgraph-declarative?color=64748B)](https://pypistats.org/packages/langgraph-declarative)



[Quickstart](#quickstart) · [Features](#features) · [YAML reference](#yaml-reference) · [Human-in-the-loop](#human-in-the-loop) · [Examples](https://github.com/pjasielski/langgraph-declarative/blob/main/examples/README.md) · [Roadmap](https://github.com/pjasielski/langgraph-declarative/blob/main/docs/04-plan/ROADMAP.md)

</div>

---

Describe a [LangGraph](https://github.com/langchain-ai/langgraph) workflow's **structure in YAML**, keep the **behaviour in Python**, and compile the two into a standard `CompiledStateGraph`. Nothing about how you run, stream, or deploy the graph changes.

> [!TIP]
> **Topology changes become config edits, not code rewrites.** Workflow structure can be diffed in review, validated in your IDE, rendered as a diagram, stored and versioned in a database, and read by people who don't write Python.

## Install

```bash
pip install langgraph-declarative                 # uv add langgraph-declarative
pip install "langgraph-declarative[anthropic]"    # optional: llm: support ([openai] too)
```

## Quickstart

**1. Register your functions.**

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

**2. Declare the graph.**

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

**3. Build and run.**

```python
graph = build_graph("workflow.yaml", registry)
result = graph.invoke({"messages": [{"role": "user", "content": "Hi there"}]})
```

That's the whole surface area. `build_graph()` validates the YAML with Pydantic, cross-checks every `function:` and `path:` against the registry, and hands you a compiled LangGraph.

> [!TIP]
> Every feature below has a commented, runnable example — see **[examples/](https://github.com/pjasielski/langgraph-declarative/blob/main/examples/README.md)**.

## How it fits together

```mermaid
flowchart LR
    Y["workflow.yaml<br/><i>or a DB row</i>"] --> V["Schema validation<br/><i>Pydantic</i>"]
    R["@registry.node<br/>@registry.router<br/>@registry.tool"] --> V
    V --> B["GraphBuilder"]
    B --> G["CompiledStateGraph<br/><i>.invoke() · .stream() · langgraph dev</i>"]
```

Three pieces: a **registry** of Python functions, a **definition** of the topology, and a **builder** that joins them. Validation happens before compilation, so a typo in the YAML gives you `Unknown node function 'classfy'. Did you mean 'classify'?` — not a stack trace at runtime.

## Features

| Feature | YAML | Since | Example |
|---|---|---|---|
| Simple & parallel edges | `target: "node"` / `target: [a, b]` | 0.1.0 | [quickstart](https://github.com/pjasielski/langgraph-declarative/tree/main/examples/quickstart/), [fan_out](https://github.com/pjasielski/langgraph-declarative/tree/main/examples/fan_out/) |
| Conditional routing | `path:` + `targets:` | 0.1.0 | [conditional_routing](https://github.com/pjasielski/langgraph-declarative/tree/main/examples/conditional_routing/) |
| Dynamic fan-out (`Send`) | `path:` without `targets` | 0.1.0 | [dynamic_routing](https://github.com/pjasielski/langgraph-declarative/tree/main/examples/dynamic_routing/) |
| Custom Python state class | `build_graph(..., state_class=...)` | 0.1.0 | [custom_state](https://github.com/pjasielski/langgraph-declarative/tree/main/examples/custom_state/) |
| State declared in YAML | `state:` with types & reducers | 0.2.0 | [declared_state](https://github.com/pjasielski/langgraph-declarative/tree/main/examples/declared_state/) |
| Match routing (no router fn) | `match:` + `targets:` | 0.2.0 | [match_routing](https://github.com/pjasielski/langgraph-declarative/tree/main/examples/match_routing/) |
| Mermaid diagrams | `draw_mermaid()` | 0.2.0 | [visualization](https://github.com/pjasielski/langgraph-declarative/tree/main/examples/visualization/) |
| IDE autocomplete & validation | [`workflow.schema.json`](https://github.com/pjasielski/langgraph-declarative/blob/main/schema/workflow.schema.json) | 0.2.0 | [visualization](https://github.com/pjasielski/langgraph-declarative/tree/main/examples/visualization/) |
| Subgraph composition | `subgraph: "child.yaml"` | 0.2.0 | [subgraph](https://github.com/pjasielski/langgraph-declarative/tree/main/examples/subgraph/) |
| Cross-file node imports | `imports:` | 0.2.0 | [cross_file_imports](https://github.com/pjasielski/langgraph-declarative/tree/main/examples/cross_file_imports/) |
| LLM config & tool binding | `llm:` + `tools:` | 0.2.0 | [llm_and_tools](https://github.com/pjasielski/langgraph-declarative/tree/main/examples/llm_and_tools/) |
| Database-stored workflows | `SQLiteLoader`, `build_graph_from_db()` | 0.2.0 | [db_workflow](https://github.com/pjasielski/langgraph-declarative/tree/main/examples/db_workflow/) |
| LangGraph project template | — | 0.2.0 | [template/](https://github.com/pjasielski/langgraph-declarative/tree/main/template/) |
| Human-in-the-loop | `build_graph(..., checkpointer=...)`, `destinations:`, `interrupt_before:` | 0.3.0 | [human_in_the_loop](https://github.com/pjasielski/langgraph-declarative/tree/main/examples/human_in_the_loop/) |

> [!NOTE]
> **Since** is the package version that introduced the feature. 0.2.0 was the first public release; 0.3.0 is unreleased — see [CHANGELOG.md](https://github.com/pjasielski/langgraph-declarative/blob/main/CHANGELOG.md).

## YAML reference

Only `nodes` is required. The simplest workflow is a list of nodes and edges.
Unknown keys are rejected with the closest valid key suggested (from 0.3.0), so a
typo such as `interupt_before:` fails loudly instead of silently doing nothing. Use
`description:` on the graph, a node or an edge for free-text documentation.

<details>
<summary><b>Full schema — state, llm, imports, nodes, edges</b></summary>

```yaml
description: "Support triage"       # optional free text — also on nodes and edges

state:                              # declare the state schema (default: MessagesState)
  - name: "category"
    type: "str"                     # str | int | float | bool | list | dict | list[str] | list[dict]
  - name: "notes"
    type: "list[str]"
    reducer: "append"               # append | add_messages | replace (default)
    # default: [...]                # deprecated (0.3.0): introspection-only, never
                                    # applied at runtime — initialise in the graph input

llm:                                # graph-level LLM default for opt-in nodes
  provider: "anthropic"             # anthropic | openai
  model: "claude-opus-4-8"

imports:                            # merge node declarations from other files
  - file: "shared_nodes.yaml"       # relative to this file
    nodes: ["error_handler"]        # omit to import all nodes

interrupt_before: ["approval"]      # pause before these nodes run (needs a checkpointer)
interrupt_after: []                 # pause after these nodes run

nodes:
  - name: "classifier"
    function: "classify"            # registered via @registry.node()
    description: "Tags the request" # optional free text
  - name: "research"
    subgraph: "child.yaml"          # embed another workflow, relative to the declaring file
  - name: "agent"
    function: "agent_fn"            # function must accept an `llm` parameter to opt in
    llm: { model: "claude-haiku-4-5" }  # node-level override, merged over graph llm
    tools: ["get_weather"]          # @registry.tool() names or "module.path:attr"
  - name: "approval"
    function: "approval_fn"
    destinations: ["execute", "END"]  # where this node routes itself via Command(goto=)

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

</details>

> [!TIP]
> Add this as the first line of any workflow file for autocomplete and inline validation in VS Code, JetBrains, and Neovim:
> ```yaml
> # yaml-language-server: $schema=path/to/workflow.schema.json
> ```
> The schema ships at [`schema/workflow.schema.json`](https://github.com/pjasielski/langgraph-declarative/blob/main/schema/workflow.schema.json), or regenerate it with `export_json_schema()`.

## Human-in-the-loop

Pause a graph for human approval, then resume it. Pass a checkpointer — `interrupt()`
pauses by *persisting* state, so without one a pause cannot be resumed.

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, interrupt

@registry.node("approval")
def approval(state):
    decision = interrupt({"question": "Approve this write?"})
    if decision == "accept":
        return Command(goto="execute")
    return Command(goto="END")

graph = build_graph("workflow.yaml", registry, checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": "run-1"}}
result = graph.invoke({"request": "write"}, config)   # pauses: __interrupt__ in result
graph.invoke(Command(resume="accept"), config)        # resumes and executes
```

Give the approval node a `destinations:` list in YAML. It routes itself with
`Command(goto=...)` and so has no static outgoing edges — without `destinations` the
Mermaid diagram invents a wrong `approval --> END` edge:

```yaml
nodes:
  - name: "approval"
    function: "approval"
    destinations: ["execute", "END"]
```

For a pause that needs no Python at all, declare it in YAML instead:

```yaml
interrupt_before: ["approval"]
```

> [!IMPORTANT]
> **The checkpointer is yours to supply — this library never defaults one.** Ownership
> flips by run mode: in your own process (CLI, FastAPI, script) you own it, but under
> `langgraph dev` / LangGraph Platform the **server** owns it and a checkpointer passed
> at compile time is silently ignored. A built-in default would appear to work locally
> and quietly do nothing once deployed.

See [human_in_the_loop](https://github.com/pjasielski/langgraph-declarative/tree/main/examples/human_in_the_loop/) for a runnable approval gate.

## API

| Function / Class | Description |
|---|---|
| `Registry()` | Holds node, router, and tool functions in separate namespaces |
| `@registry.node("name")` | Register a node function (transforms state) |
| `@registry.router("name")` | Register a router (returns a routing key or a list of `Send`) |
| `@registry.tool("name")` | Register a tool for `tools:` binding |
| `build_graph(path, registry, state_class=None, *, checkpointer=None, store=None)` | YAML file → compiled `CompiledStateGraph` |
| `build_graph_from_db(source, registry, db_path, *, checkpointer=None, store=None, base_dir=None)` | DB-stored definition → compiled graph (`"flow"` or `"flow@2"`). `base_dir` is required if the definition uses relative `imports:` / `subgraph:` paths |
| `draw_mermaid(path, registry, output_path=None)` | Compile and render a Mermaid diagram (`.md` → fenced block) |
| `export_json_schema(output_path=None)` | Emit the JSON Schema for workflow YAML files |
| `GraphBuilder(registry, state_class=None, *, checkpointer=None, store=None)` | Power-user class behind `build_graph()`; `.build(config, *, base_dir=None)` compiles an in-memory `GraphConfig` |
| `SQLiteLoader(db_path)` | Save/load versioned definitions; implements the pluggable `Loader` protocol |

## Documentation

| Document | Contents |
|---|---|
| [examples/](https://github.com/pjasielski/langgraph-declarative/blob/main/examples/README.md) | 13 runnable examples, one per feature, organized by milestone |
| [template/](https://github.com/pjasielski/langgraph-declarative/tree/main/template/) | Starter project for `langgraph dev` using the declarative pattern |
| [docs/04-plan/ROADMAP.md](https://github.com/pjasielski/langgraph-declarative/blob/main/docs/04-plan/ROADMAP.md) | What shipped per milestone, and unvalidated future ideas |
| [CHANGELOG.md](https://github.com/pjasielski/langgraph-declarative/blob/main/CHANGELOG.md) | Release history |
| [DECISIONS.md](https://github.com/pjasielski/langgraph-declarative/blob/main/DECISIONS.md) | Why the API and the scope look the way they do |
| [docs/02-requirements/REQUIREMENTS.md](https://github.com/pjasielski/langgraph-declarative/blob/main/docs/02-requirements/REQUIREMENTS.md) | Problem, users, success criteria |
| [docs/03-design/DESIGN.md](https://github.com/pjasielski/langgraph-declarative/blob/main/docs/03-design/DESIGN.md) | Architecture, module responsibilities, trade-offs |

<details>
<summary><b>Project layout</b></summary>

```
src/langgraph_declarative/   # library (registry, schema, builder, state/llm factories, loaders)
schema/                      # generated JSON Schema for workflow YAML
examples/                    # runnable examples — one folder per feature
template/                    # LangGraph starter template
tests/                       # pytest suite + YAML fixtures
docs/                        # requirements, design, roadmap, reviews
```

</details>

## Requirements

- Python 3.10+
- LangGraph ≥ 1.0 · PyYAML ≥ 6.0.1 · Pydantic ≥ 2.8 (0.2.0 declared LangGraph ≥ 0.2)
- Optional: `[anthropic]` / `[openai]` extras for `llm:` support

## Contributing

Issues and pull requests welcome. Run the suite with `uv run pytest` before opening a PR.

## License

[MIT](https://github.com/pjasielski/langgraph-declarative/blob/main/LICENSE). Community project — not affiliated with or endorsed by LangChain. Built on top of [LangGraph](https://github.com/langchain-ai/langgraph).
