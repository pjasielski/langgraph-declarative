# langgraph-declarative

Declarative graph definition for [LangGraph](https://github.com/langchain-ai/langgraph) — define your graph topology in YAML, register node functions in Python, and compile with one line of code.

**Remove the code-redeployment tax:** when your workflow changes, edit a YAML file instead of rewriting Python graph-wiring code.

## Quickstart

### Install

```bash
pip install langgraph-declarative
# or
uv add langgraph-declarative
```

### Define your nodes

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

### Define your graph in YAML

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

### Simple edges

```yaml
edges:
  - source: START
    target: "process"
  - source: "process"
    target: END
```

### Parallel fan-out

```yaml
edges:
  - source: START
    target: ["analyzer_a", "analyzer_b", "analyzer_c"]
```

### Conditional routing

Register a router function that returns a routing key, then map keys to nodes in YAML:

```python
@registry.router("route_by_category")
def route_by_category(state) -> str:
    return state.get("category", "general")
```

```yaml
edges:
  - source: "classifier"
    path: "route_by_category"
    targets:
      billing: "handle_billing"
      technical: "handle_technical"
      general: "handle_general"
```

### Dynamic routing (Send)

For runtime fan-out where the number of targets is determined dynamically:

```python
from langgraph.types import Send

@registry.router("fan_out")
def fan_out(state) -> list[Send]:
    return [
        Send("processor", {"item": item})
        for item in state["items"]
    ]
```

```yaml
edges:
  - source: "loader"
    path: "fan_out"
```

### Custom state class

By default, `build_graph()` uses LangGraph's `MessagesState`. Override with your own:

```python
graph = build_graph("workflow.yaml", registry=registry, state_class=MyState)
```

## YAML Format Reference

```yaml
nodes:
  - name: "node_name"            # unique name for this node
    function: "registry_name"     # registered via @registry.node()

edges:
  # Simple edge
  - source: "START"               # START, END, or node name
    target: "node_name"

  # Fan-out (parallel)
  - source: "node_name"
    target: ["a", "b", "c"]

  # Conditional (mapped routing)
  - source: "node_name"
    path: "router_name"           # registered via @registry.router()
    targets:
      key: "target_node"

  # Dynamic (Send / direct)
  - source: "node_name"
    path: "router_name"           # returns node names or Send objects
```

## API

| Function / Class | Description |
|---|---|
| `Registry()` | Create a registry for node and router functions |
| `@registry.node("name")` | Register a node function (transforms state) |
| `@registry.router("name")` | Register a router function (decides routing) |
| `build_graph(path, registry, state_class=None)` | Compile YAML + registry into a `CompiledStateGraph` |
| `GraphBuilder(registry, state_class)` | Power-user class for more control over compilation |

## Project Structure

```
langgraph-declarative/
├── src/
│   └── langgraph_declarative/
│       ├── __init__.py          # Public API: Registry, GraphBuilder, build_graph
│       ├── registry.py          # Registry class, @node/@router decorators
│       ├── builder.py           # GraphBuilder — YAML config to CompiledStateGraph
│       ├── schema.py            # Pydantic models for YAML validation
│       ├── loader.py            # YAML file loading
│       └── errors.py            # Custom exceptions, typo suggestions
├── tests/
│   ├── test_registry.py
│   ├── test_builder.py
│   ├── test_schema.py
│   ├── test_integration.py
│   └── fixtures/                # Sample YAML files for tests
├── examples/
│   ├── quickstart/
│   └── conditional_routing/
├── pyproject.toml
├── TODO.md                      # Roadmap: v1.1, v2, ideas
├── LICENSE                      # MIT
└── CHANGELOG.md
```

## Roadmap

See [TODO.md](TODO.md) for the full backlog.

- **v1** (current): Registry, builder, conditional edges, validation, packaging
- **v1.1**: State declaration in YAML, auto-Mermaid generation, JSON Schema for IDE support
- **v2**: Subgraph composition, tool/LLM config in YAML, database-driven graphs

## Requirements

- Python 3.10+
- LangGraph >= 0.2
- PyYAML >= 6.0
- Pydantic >= 2.0

## License

MIT
