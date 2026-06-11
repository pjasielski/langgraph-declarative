# Examples

Runnable examples demonstrating each feature of `langgraph-declarative`. Each example is self-contained — a `workflow.yaml` defining the graph and a `main.py` that registers functions and runs it.

## Prerequisites

```bash
pip install langgraph-declarative
# or
uv add langgraph-declarative
```

## Running

From the repository root:

```bash
python examples/quickstart/main.py
python examples/fan_out/main.py
python examples/conditional_routing/main.py
python examples/dynamic_routing/main.py
python examples/custom_state/main.py
```

## Examples

### quickstart — Linear graph

The simplest possible graph: two nodes in sequence.

```
START → greeter → responder → END
```

- **YAML:** [workflow.yaml](quickstart/workflow.yaml)
- **Python:** [main.py](quickstart/main.py)
- **Demonstrates:** `@registry.node()`, simple edges, `build_graph()`, `MessagesState`

### fan_out — Parallel branches

One node fans out to multiple branches that run in parallel, then converge.

```
START → loader → [sentiment_analysis, keyword_extraction] → summarizer → END
```

- **YAML:** [workflow.yaml](fan_out/workflow.yaml)
- **Python:** [main.py](fan_out/main.py)
- **Demonstrates:** `target: [list]` for static fan-out, convergence with multiple edges to one target

### conditional_routing — Mapped routing

A classifier node followed by a router that directs flow based on a routing key.

```
START → classifier → (intent_router) → handle_question | handle_complaint | handle_other → END
```

- **YAML:** [workflow.yaml](conditional_routing/workflow.yaml)
- **Python:** [main.py](conditional_routing/main.py)
- **Demonstrates:** `@registry.router()`, `path:` + `targets:` for conditional edges

### dynamic_routing — Send-based fan-out

A router that creates a variable number of parallel worker invocations at runtime using `Send`.

```
START → task_splitter → (dispatch_tasks) → worker × N → END
```

- **YAML:** [workflow.yaml](dynamic_routing/workflow.yaml)
- **Python:** [main.py](dynamic_routing/main.py)
- **Demonstrates:** `path:` without `targets`, router returning `list[Send]`, custom `TypedDict` state, runtime-determined parallelism

### custom_state — Non-MessagesState workflow

A data processing pipeline using a custom `TypedDict` state instead of the default `MessagesState`. Shows that the library works for any domain, not just chatbots.

```
START → ingest → validate → (validation_router) → transform → END
                                    ↘ invalid → ingest (retry)
```

- **YAML:** [workflow.yaml](custom_state/workflow.yaml)
- **Python:** [main.py](custom_state/main.py)
- **Demonstrates:** `state_class=PipelineState` parameter, conditional routing for retry logic, non-chat workflows
