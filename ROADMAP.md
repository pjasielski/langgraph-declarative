# Roadmap

## v1 (shipped)

Core library: define LangGraph graphs in YAML, compile with one line of Python.

- **Registry** with `@registry.node()` and `@registry.router()` decorators
- **All edge types:** simple, parallel fan-out, conditional (mapped routing), dynamic (Send)
- **YAML schema validation** with Pydantic — catches errors before compilation
- **Actionable error messages** with typo detection and available-name suggestions
- **`build_graph()` convenience function** — one-line compilation defaulting to `MessagesState`
- **`GraphBuilder` class** for power users who need control over state class and compilation
- **Test suite** — 77 tests covering all modules, edge types, and error paths
- **Runnable examples** — quickstart (linear graph) and conditional routing

## v1.1 (shipped)

Extending the core with features that don't change the architecture.

| Feature | What it enables |
|---------|----------------|
| **State declaration in YAML** | Define state fields, types, and reducers in the YAML file instead of writing a Python state class. Ported from a production model factory (~250 lines). |
| **Auto-Mermaid generation** | Generate visual graph diagrams by exposing LangGraph's `.draw_mermaid()` after compilation. |
| **JSON Schema for YAML files** | Publish a schema so IDEs provide autocomplete and validation when editing workflow YAML. Leverages Pydantic's built-in JSON Schema export. |
| **`match:` routing syntax** | Simple value-matching routing in YAML (`match: "state.field"` + `targets:`) without writing a Python router function. No `eval()` — dict lookup only. |

## v2 (shipped)

Larger features that extend what the library can express.

| Feature | What it enables |
|---------|----------------|
| **Subgraph composition** | `subgraph: "file.yaml"` in a node definition compiles and embeds a sub-graph. Enables modular, multi-file workflows. |
| **Tool configuration in YAML** | Reference LangChain or MCP tools by name in the YAML file, wired to nodes automatically. |
| **LLM configuration per node** | Specify model, temperature, and other LLM parameters per node in YAML. Nodes get a pre-configured LLM without manual setup. |
| **Database-driven graph source** | Load graph definitions from a database instead of YAML files. Enables runtime workflow management without file deployments. |
| **LangGraph Template packaging** | Publish as an official LangGraph Template for `langgraph new` scaffolding. |
| **Cross-file node references** | Import and reuse node/router definitions across multiple YAML workflow files. |

> v1, v1.1, and v2 are internal milestone labels, not package version numbers. See [CHANGELOG.md](CHANGELOG.md) for package releases.

## v2.1 — Human-in-the-loop (planned)

Approval gates, pauses for input, and resumable runs — the one class of workflow the
library cannot currently express. Every change is additive and backward compatible.

| Feature | What it enables |
|---------|----------------|
| **Caller-supplied `checkpointer`** | `build_graph(..., checkpointer=saver)` reaches `compile()`, so `interrupt()` can pause a run and resume it later on the same `thread_id`. Never defaulted — see below. |
| **`destinations:` on nodes** | Approval nodes that route themselves with `Command(goto=...)` have no static edges; declaring their destinations keeps the Mermaid diagram correct. |
| **`interrupt_before:` / `interrupt_after:`** | Declare a static pause point in YAML — an approval gate with no Python change. |
| **Optional `store`** | Cross-thread memory, alongside the per-thread checkpointer. |

The checkpointer is deliberately **not** defaulted. Ownership flips by run mode: in
your own process you own it, but under `langgraph dev` / LangGraph Platform the server
owns it and a compile-time checkpointer is silently ignored. A built-in default would
appear to work while doing nothing.

## Ideas (unvalidated)

These are possibilities, not commitments. They may or may not make sense after real-world usage.

- **Graph diffing** — compare two YAML files and report topology changes
- **Hot-reload** — watch a YAML file and recompile the graph on change
- **CLI tool** — `lgd validate workflow.yaml`, `lgd visualize workflow.yaml`
- **Graph versioning** — run A/B tests between YAML workflow variants
- **Export to LangGraph Studio format**

*(YAML include/import shipped in v2 as `imports:` — see [cross_file_imports](examples/cross_file_imports/).)*

---

Delivery detail — milestone tracker, task index, and known risks — lives in [docs/04-plan/ROADMAP.md](docs/04-plan/ROADMAP.md).
