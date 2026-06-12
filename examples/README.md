# Examples

Runnable examples demonstrating each feature of `langgraph-declarative`. Each example is self-contained — one or more `workflow.yaml` files defining the graph and a `main.py` that registers functions and runs it. The YAML files carry comments explaining the feature they demonstrate.

Examples are grouped by the release that introduced the feature: **v1** (core), **v1.1** (extensions), **v2** (composition & integration).

## Prerequisites

```bash
pip install langgraph-declarative
# or
uv add langgraph-declarative
```

The `llm_and_tools` example additionally needs an LLM provider package and an API key:

```bash
pip install "langgraph-declarative[anthropic]"   # or [openai]
export ANTHROPIC_API_KEY=...
```

## Running

From the repository root, run any example directly:

```bash
python examples/quickstart/main.py
```

All examples run offline except `llm_and_tools`, which calls a real LLM API (and exits with instructions if the provider package or API key is missing).

## Feature → example map

| Feature | Version | Example |
|---|---|---|
| Simple edges, `build_graph()` | v1 | [quickstart](#quickstart--linear-graph-v1) |
| Static fan-out (parallel branches) | v1 | [fan_out](#fan_out--parallel-branches-v1) |
| Conditional routing (`path:` + `targets:`) | v1 | [conditional_routing](#conditional_routing--mapped-routing-v1) |
| Dynamic routing (`Send`) | v1 | [dynamic_routing](#dynamic_routing--send-based-fan-out-v1) |
| Custom Python state class (`state_class=`) | v1 | [custom_state](#custom_state--non-messagesstate-workflow-v1) |
| State declaration in YAML (`state:`) | v1.1 | [declared_state](#declared_state--state-schema-in-yaml-v11) |
| Match routing (`match:` + `targets:`) | v1.1 | [match_routing](#match_routing--route-on-a-state-field-v11) |
| Mermaid diagrams, JSON Schema for IDEs | v1.1 | [visualization](#visualization--mermaid--json-schema-v11) |
| Subgraph composition (`subgraph:`) | v2 | [subgraph](#subgraph--embed-a-workflow-in-a-node-v2) |
| Cross-file imports (`imports:`) | v2 | [cross_file_imports](#cross_file_imports--shared-node-libraries-v2) |
| LLM config (`llm:`) + tool binding (`tools:`) | v2 | [llm_and_tools](#llm_and_tools--llm-config-and-tools-in-yaml-v2) |
| Database-driven definitions (`SQLiteLoader`) | v2 | [db_workflow](#db_workflow--load-definitions-from-sqlite-v2) |

v2 also added **LangGraph Template packaging** — that one is not an example but a project scaffold; see [`template/`](../template/) at the repository root.

---

## v1 — core

### quickstart — Linear graph (v1)

The simplest possible graph: two nodes in sequence.

```
START → greeter → responder → END
```

- **Files:** [workflow.yaml](quickstart/workflow.yaml), [main.py](quickstart/main.py)
- **Demonstrates:** `@registry.node()`, simple edges, `build_graph()`, default `MessagesState`

### fan_out — Parallel branches (v1)

One node fans out to multiple branches that run in parallel, then converge.

```
START → loader → [sentiment_analysis, keyword_extraction] → summarizer → END
```

- **Files:** [workflow.yaml](fan_out/workflow.yaml), [main.py](fan_out/main.py)
- **Demonstrates:** `target: [list]` for static fan-out, convergence with multiple edges to one target

### conditional_routing — Mapped routing (v1)

A classifier node followed by a router that directs flow based on a routing key.

```
START → classifier → (intent_router) → handle_question | handle_complaint | handle_other → END
```

- **Files:** [workflow.yaml](conditional_routing/workflow.yaml), [main.py](conditional_routing/main.py)
- **Demonstrates:** `@registry.router()`, `path:` + `targets:` for conditional edges
- **Since v1.1:** when the routing decision is just "look at one state field", `match:` routing does the same job without a Python router — see [match_routing](match_routing/).

### dynamic_routing — Send-based fan-out (v1)

A router that creates a variable number of parallel worker invocations at runtime using `Send`.

```
START → task_splitter → (dispatch_tasks) → worker × N → END
```

- **Files:** [workflow.yaml](dynamic_routing/workflow.yaml), [main.py](dynamic_routing/main.py)
- **Demonstrates:** `path:` without `targets`, router returning `list[Send]`, custom `TypedDict` state, runtime-determined parallelism
- **Since v1.1:** the `TaskState` TypedDict could be declared in YAML instead (`state:` with `reducer: append`).

### custom_state — Non-MessagesState workflow (v1)

A data processing pipeline using a custom `TypedDict` state instead of the default `MessagesState`. Shows that the library works for any domain, not just chatbots.

```
START → ingest → validate → (validation_router) → transform → END
                                    ↘ invalid → ingest (retry)
```

- **Files:** [workflow.yaml](custom_state/workflow.yaml), [main.py](custom_state/main.py)
- **Demonstrates:** `state_class=PipelineState` parameter, conditional routing for retry logic, non-chat workflows
- **Since v1.1:** the same schema can be declared in YAML — see [declared_state](declared_state/). `state_class=` remains supported; note that a YAML `state:` section takes precedence over it (with a `UserWarning`).

---

## v1.1 — extensions

### declared_state — State schema in YAML (v1.1)

Declares state fields, types, and reducers in the YAML file — no Python state class. Two parallel branches append to the same list field, which only works because of the `append` reducer.

```
START → loader → [stats, tags] → summarizer → END
```

- **Files:** [workflow.yaml](declared_state/workflow.yaml), [main.py](declared_state/main.py)
- **Demonstrates:** `state:` section, field types (`str`, `list[str]`, …), reducers (`append`, `add_messages`, default `replace`)

### match_routing — Route on a state field (v1.1)

A classifier writes a category into state; the edge routes on that value directly. No Python router function, no `eval()` — pure dict lookup with a `default` fallback.

```
START → classifier → match: category → billing_agent | tech_agent | general_agent → END
```

- **Files:** [workflow.yaml](match_routing/workflow.yaml), [main.py](match_routing/main.py)
- **Demonstrates:** `match:` + `targets:`, the reserved `default` key, dot-notation for nested fields (`result.status`)

### visualization — Mermaid + JSON Schema (v1.1)

Developer-experience features: render any workflow as a Mermaid diagram and export the JSON Schema that gives IDEs autocomplete/validation for workflow YAML files. The example's own `workflow.yaml` starts with the `# yaml-language-server: $schema=...` modeline wired to the schema shipped in [`schema/workflow.schema.json`](../schema/workflow.schema.json).

- **Files:** [workflow.yaml](visualization/workflow.yaml), [main.py](visualization/main.py)
- **Demonstrates:** `draw_mermaid()` (with `output_path=` for `.md`/raw output), `export_json_schema()`, the IDE modeline

---

## v2 — composition & integration

### subgraph — Embed a workflow in a node (v2)

A parent workflow embeds a child workflow file as a single node. The child declares its own state and shares the `messages` key with the parent, so data flows across the boundary.

```
START → intro → research (= research_subgraph.yaml) → outro → END
                 └── START → gather → condense → END
```

- **Files:** [workflow.yaml](subgraph/workflow.yaml), [research_subgraph.yaml](subgraph/research_subgraph.yaml), [main.py](subgraph/main.py)
- **Demonstrates:** `subgraph:` on a node, relative path resolution, parent/child state sharing, one registry serving both graphs

### cross_file_imports — Shared node libraries (v2)

A workflow imports node declarations from a shared library file. Useful for nodes that appear in many workflows (error handlers, audit loggers).

```
START → processor → match: status → confirmation | error_handler (imported) → END
```

- **Files:** [workflow.yaml](cross_file_imports/workflow.yaml), [shared_nodes.yaml](cross_file_imports/shared_nodes.yaml), [main.py](cross_file_imports/main.py)
- **Demonstrates:** `imports:` with selective `nodes: [...]` (omit to import all), declarations vs. functions (functions still come from the registry)

### llm_and_tools — LLM config and tools in YAML (v2)

Nodes receive a pre-configured LangChain chat model built from YAML: a graph-level `llm:` default, a node-level override (cheaper model for a simple step), and tools bound automatically. **Requires `langchain-anthropic` and `ANTHROPIC_API_KEY`** — exits with instructions otherwise.

```
START → agent (opus + get_weather tool) → summarizer (haiku) → END
```

- **Files:** [workflow.yaml](llm_and_tools/workflow.yaml), [main.py](llm_and_tools/main.py)
- **Demonstrates:** graph-level `llm:`, node-level override merging, `tools:` binding, `@registry.tool()`, the `llm=None` opt-in contract (a node with `llm:`/`tools:` config whose function does not accept `llm` is a build-time error)

### db_workflow — Load definitions from SQLite (v2)

Stores two versions of a workflow definition in SQLite and builds graphs from both — the pinned `@1` and the latest. Enables runtime workflow management without file deployments; the DB stores topology only, functions stay in the registry.

- **Files:** [main.py](db_workflow/main.py) (definitions are inline dicts — no YAML file needed)
- **Demonstrates:** `SQLiteLoader.save()` / `.versions()`, `build_graph_from_db()`, `"source"` vs `"source@version"` pinning
