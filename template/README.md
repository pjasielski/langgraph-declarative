# Declarative LangGraph Agent

A starter project using the **declarative pattern**: the workflow topology
lives in YAML (`workflow.yaml`), while node logic stays in plain Python
(`nodes.py`). Rewiring the graph never requires touching Python code.

## Structure

```
langgraph.json          LangGraph Studio / CLI entry point
src/agent/
├── workflow.yaml       Graph topology (nodes + edges) — edit freely
├── nodes.py            Node functions, registered by name
└── graph.py            Compiles YAML + registry into the runnable graph
```

## The pattern

1. **Write a node function** and register it:

   ```python
   @registry.node("my_step")
   def my_step(state):
       return {"messages": [...]}
   ```

2. **Reference it in workflow.yaml** and wire edges:

   ```yaml
   nodes:
     - name: "step"
       function: "my_step"
   edges:
     - source: "START"
       target: "step"
   ```

3. **Build and run:**

   ```python
   graph = build_graph("workflow.yaml", registry)
   graph.invoke({"messages": [...]})
   ```

Beyond the basics, the YAML supports conditional routing (`path:` /
`match:`), fan-out, custom `state:` declarations, per-node `llm:` config,
`tools:`, subgraphs, and cross-file `imports:` — see the
[langgraph-declarative docs](https://github.com/pjasielski/langgraph-declarative).

## Run it

```bash
pip install -e .          # or: uv pip install -e .
python src/agent/graph.py
```

Or open in LangGraph Studio:

```bash
pip install "langgraph-cli[inmem]"   # or: uv add "langgraph-cli[inmem]"
langgraph dev
```
