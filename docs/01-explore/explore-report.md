# Explore Report: langgraph-declarative

**Date:** 2026-05-30
**Version:** v1
**Status:** Confirmed
**Session(s):** 001-exploration

---

## 1. Executive Summary

`langgraph-declarative` is a Python library that enables developers to define LangGraph graphs via YAML configuration files and a Python node registry, eliminating graph-wiring boilerplate. The pattern has been validated in a prior production project with working registry and builder implementations. No competing library exists in the LangGraph ecosystem — the space is open. The core technical risk (conditional edge design) has been resolved with a mapped-routing approach that maps 1:1 to LangGraph's native API. Recommendation: proceed to PRD and design.

---

## 2. Business Analysis

### 2.1 Problem & Context

Building LangGraph applications requires writing Python code to wire nodes, edges, and conditional routing. Every workflow change — adding a node, rerouting an edge, adjusting parallelism — requires code changes and redeployment. This creates a **code-redeployment tax** that slows iteration, especially in environments where graph topology evolves faster than surrounding application code.

The industry is shifting toward declarative architectures (Terraform, Kubernetes YAML, GitHub Actions) where infrastructure and workflows are treated as configuration. LangGraph lacks a declarative layer for graph definition.

### 2.2 Users & Stakeholders

| User / Stakeholder | Role | Goals | Pain Points |
|---------------------|------|-------|-------------|
| Python developers | Primary users — build LangGraph apps | Less boilerplate, faster iteration | Writing repetitive graph-wiring code |
| Enterprise teams | Secondary users — modify workflows | Change graph topology without code changes | Waiting for developer cycles to modify routing |
| Non-technical users | Beneficiaries — PMs, analysts | Understand and review graph structure | Python code is opaque to non-developers |

### 2.3 Current Process

Developers write Python code to construct LangGraph `StateGraph` objects:
- `builder.add_node(name, fn)` for each node
- `builder.add_edge(source, target)` for each connection
- `builder.add_conditional_edges(source, fn, path_map)` for routing
- State classes defined as Python `TypedDict` subclasses

This is repeated for every graph, with no reuse of topology definitions across projects.

### 2.4 Goals & Success Criteria

| # | Goal | Metric | Target |
|---|------|--------|--------|
| 1 | Reduce graph-wiring boilerplate | Lines of Python for graph definition | YAML config + 1-line `build_graph()` call replaces manual wiring |
| 2 | Enable non-code graph iteration | Workflow changes requiring code changes | Zero code changes for topology-only modifications |
| 3 | Community adoption | PyPI downloads, GitHub stars | Published on PyPI, discoverable by LangGraph users |

---

## 3. Technical Analysis

### 3.1 Current State

**Validated prior art (prior production project):**

- **Node Registry** — decorator-based singleton pattern (`@registry.register("name")`), ~73 lines. Duplicate-name protection, helpful error messages on lookup failures.
- **Graph Builder** — translates config dict to compiled `StateGraph`. Supports node resolution, simple edges, parallel fan-out (list targets), START/END sentinels. ~76 lines.
- **YAML Config** — simple `nodes` + `edges` structure. Proven in production with financial analysis subgraphs.
- **Model Factory** — separate module (~250 lines) that generates Pydantic v2 models from YAML. Topological sorting, cycle detection, full type support. Candidate for v1.1 integration.

**Gap: conditional edges** — the production implementation only supports simple and fan-out edges. Conditional routing (LangGraph's `add_conditional_edges`) was handled in Python, not declaratively. Resolved via the mapped-routing design (see below).

### 3.2 Integration Points

| System | Purpose | Interface | Status |
|--------|---------|-----------|--------|
| LangGraph | Graph compilation & execution | `StateGraph` API | Available — library wraps it |
| PyYAML | YAML file parsing | `yaml.safe_load()` | Available — standard dependency |
| Pydantic v2 | YAML schema validation | `BaseModel` validation | Available — validates config structure |
| LangGraph `MessagesState` | Default state class | `TypedDict` import | Available — used as default |

### 3.3 Key Technical Decisions

**Conditional edges — Mapped Routing pattern:**
- Router functions registered via `@registry.router("name")`, referenced in YAML as `path: "name"`
- YAML `targets:` map provides the `path_map` (routing key → node name)
- Maps 1:1 to LangGraph's native `add_conditional_edges(source, path, path_map)`
- `target` (singular) = simple edge; `targets` (plural) + `path` = conditional edge

**Send support:**
- Supported from v1 via router return type — routers can return `list[Send]`
- No special YAML syntax needed — `path:` without `targets:` signals dynamic routing
- No extra implementation work — falls naturally from the conditional edges design

**API design:**
- `Registry()` instance (not singleton) with `@registry.node()` and `@registry.router()` decorators
- `build_graph(yaml_path, registry, state_class=MessagesState)` convenience function
- `GraphBuilder` class for power users needing more control

### 3.4 Technical Constraints

- Python 3.10+ (required for `X | Y` union syntax, matches LangGraph)
- Dependencies: `langgraph>=0.2`, `pyyaml>=6.0`, `pydantic>=2.0`
- `src/` layout for proper PyPI packaging
- MIT license (matches LangGraph)

---

## 4. Risk Register

| # | Risk | Category | Likelihood | Impact | Mitigation |
|---|------|----------|------------|--------|------------|
| 1 | LangGraph API changes break compatibility | Technical | M | H | Pin minimum version, test against latest |
| 2 | Conditional edge design insufficient for complex routing | Technical | L | H | Mapped routing covers LangGraph's full API; Send handles dynamic cases |
| 3 | Low adoption due to niche audience | Business | M | M | Clear docs, examples, community posting |
| 4 | Scope creep into v2 features during v1 build | Organizational | M | M | Strict v1 scope boundary, TODO.md for future work |

---

## 5. Questions & Gaps

### Open Questions

All blocking questions have been resolved. Remaining items are clarifying and tracked in session artifacts.

### Identified Gaps

No critical gaps remain. V1 scope is well-defined. V2 features (subgraph composition, tool/LLM config, database-driven graphs) are scoped but deferred.

---

## 6. Recommendations & Next Steps

1. **Proceed to PRD** — formalize v1 requirements with v2 scoped as future phases
2. **Design (SDD)** — technical architecture accounting for v2 extensibility
3. **Implement v1** — registry, builder, conditional edges, validation, tests, packaging
4. **Publish to PyPI** — `langgraph-declarative` package
5. **Community outreach** — LangChain forums, LinkedIn, GitHub visibility

---

**Notes:**
- The core builder and registry code from the prior production project can be ported directly — estimated 60-70% code reuse for those modules
- The model factory is a strong v1.1 candidate since the code already exists
- Delivery approach: scope v1+v2 together, build v1 first (architecture protects v2 extensibility)
