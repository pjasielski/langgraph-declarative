# Task 020: LLM Configuration per Node
**Status:** todo
**Priority:** medium
**Assigned:** unassigned
**Blocked by:** —
**Effort:** M
**Created:** 2026-06-11
**Completed:**

## Description
Allow each node in YAML to specify LLM parameters (model, temperature, etc.). Nodes receive a pre-configured LLM instance without requiring manual setup in Python. Supports the common pattern where different nodes need different models or settings.

## Acceptance Criteria
- [ ] `llm:` section on node definitions in YAML
- [ ] Supported fields: `model`, `temperature`, `max_tokens`, `provider` (at minimum)
- [ ] LLM instance created at build time and passed to the node function
- [ ] Node functions opt in via a parameter (e.g., `def my_node(state, llm=None)`)
- [ ] Default LLM config at graph level, overridable per node
- [ ] Provider support: at least `openai` and `anthropic` via `langchain_openai`/`langchain_anthropic`
- [ ] Tests: LLM config parsing, per-node override, missing provider error

## Files
- `src/langgraph_declarative/schema.py` (add `LLMConfig` model, extend NodeConfig)
- `src/langgraph_declarative/builder.py` (LLM instantiation and injection)
- `src/langgraph_declarative/llm_factory.py` (new — LLM creation from config)
- `tests/test_llm_config.py` (new)
- `tests/fixtures/llm_workflow.yaml` (new)

## Notes
- YAML format example:
  ```yaml
  llm:  # graph-level default
    provider: openai
    model: gpt-4o
    temperature: 0.7

  nodes:
    - name: summarizer
      function: summarize
      llm:
        model: gpt-4o-mini  # override for this node
        temperature: 0
  ```
- LLM providers are optional dependencies — import lazily, error clearly if missing
- Design decision: inject LLM via function parameter vs. wrap function. Parameter injection is more explicit.
- PRD: referenced in v2 roadmap
