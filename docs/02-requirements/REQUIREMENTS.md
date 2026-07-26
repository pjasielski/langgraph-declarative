# Requirements: langgraph-declarative

**Date:** 2026-05-30
**Version:** v1
**Status:** Draft
**Explore report:** [docs/01-explore/explore-report.md](../01-explore/explore-report.md)

---

## 1. Problem Statement

### 1.1 Background

LangGraph is the leading framework for building stateful, multi-step AI agent applications. However, every LangGraph application requires developers to write imperative Python code to wire graph topology — nodes, edges, conditional routing, and parallel fan-out. This graph-wiring code is repetitive, hard to diff in code review, and creates a **code-redeployment tax**: any change to workflow structure requires code changes, testing, and redeployment.

The broader software industry has solved this problem in other domains through declarative configuration: Terraform for infrastructure, Kubernetes YAML for container orchestration, GitHub Actions for CI/CD. LangGraph lacks an equivalent declarative layer.

### 1.2 Problem

Developers building LangGraph applications spend significant effort on graph-wiring boilerplate. When workflow topology changes — adding nodes, rerouting edges, adjusting conditional logic — the entire code-test-deploy cycle must run even though the underlying node logic hasn't changed.

Non-technical stakeholders (PMs, analysts, domain experts) cannot read or modify graph topology because it's embedded in Python code. This creates a bottleneck where developers are required for every workflow iteration.

### 1.3 Evidence

- Production validation: the declarative pattern was implemented and deployed in a prior production project, demonstrating that YAML-defined graphs work at scale with parallel fan-out and subgraph composition.
- Ecosystem gap: no existing LangGraph extension library provides a generic YAML-to-graph engine. `langgraph-supervisor` and `langgraph-swarm` are pattern-specific, not declarative builders.
- Industry precedent: declarative workflow definition is proven in Terraform, Kubernetes, Apache Airflow, and GitHub Actions.

---

## 2. Users & Personas

| Persona | Description | Goals | Pain Points | Usage Frequency |
|---|---|---|---|---|
| Dev (primary) | Python developer building LangGraph apps | Less boilerplate, faster graph iteration, testable topology | Writing repetitive `add_node`/`add_edge` code; graph structure buried in Python | Daily during development |
| Team Lead | Technical lead managing AI application workflows | Review graph changes in PRs, onboard team members | Graph diffs in Python are noisy; new team members struggle to understand topology | Weekly during review |
| Domain Expert | PM or analyst who understands the workflow but not Python | Understand and propose changes to graph topology | Cannot read Python graph code; depends on developers for every change | Occasionally |

**Primary user:** Dev — the developer who installs the library and uses it to build graphs.

---

## 3. Goals & Success Criteria

### 3.1 Business Goals

| # | Goal | Metric | Target | How to Measure |
|---|---|---|---|---|
| 1 | Reduce graph-wiring effort | Lines of Python for graph definition | YAML config + 1-line build replaces manual wiring | Compare equivalent graphs |
| 2 | Enable topology-as-configuration | Workflow changes requiring code changes | Zero for topology-only changes | Count code changes per workflow update |
| 3 | Community availability | Package availability | Published on PyPI, installable via pip | `pip install langgraph-declarative` works |

### 3.2 User Goals

| Persona | Goal | How We'll Know It's Met |
|---|---|---|
| Dev | Define any LangGraph graph via YAML + registry | All LangGraph edge types (simple, fan-out, conditional, Send) expressible |
| Dev | Get clear errors on invalid YAML | Typos, missing refs, and schema violations caught with actionable messages |
| Team Lead | Review graph topology in YAML diffs | Graph structure readable without running the code |
| Domain Expert | Read YAML to understand workflow | YAML structure self-documenting with `targets:` maps showing routing |

---

## 4. Requirements

### 4.1 Functional Requirements

| ID | Requirement | Priority | Phase | Acceptance Criteria |
|---|---|---|---|---|
| FR-01 | Node registry with decorator-based registration | Must | v1 | `@registry.node("name")` registers a function; duplicate names raise `ValueError` |
| FR-02 | Router registry with decorator-based registration | Must | v1 | `@registry.router("name")` registers routing functions; separate namespace from nodes |
| FR-03 | YAML-defined nodes | Must | v1 | `nodes:` section maps names to registered functions via `function:` key |
| FR-04 | Simple edges in YAML | Must | v1 | `target: "node_name"` creates `add_edge(source, target)` |
| FR-05 | Parallel fan-out edges | Must | v1 | `target: ["a", "b", "c"]` creates multiple edges from source |
| FR-06 | START/END sentinel support | Must | v1 | String literals `"START"` and `"END"` resolve to LangGraph constants |
| FR-07 | Conditional edges via mapped routing | Must | v1 | `path: "router_name"` + `targets: {key: node}` creates `add_conditional_edges()` |
| FR-08 | Dynamic routing (Send support) | Must | v1 | `path: "router_name"` without `targets` allows router to return `Send` objects |
| FR-09 | YAML schema validation | Must | v1 | Invalid YAML structure raises clear errors before graph compilation |
| FR-10 | Error messages with suggestions | Must | v1 | Typos in node/router references suggest closest match; missing refs list available names |
| FR-11 | `build_graph()` convenience function | Must | v1 | One-line graph compilation: `build_graph("file.yaml", registry)` |
| FR-12 | `GraphBuilder` class for power users | Must | v1 | Explicit API: `GraphBuilder(registry, state_class).build("file.yaml")` |
| FR-13 | Default to `MessagesState` | Should | v1 | `build_graph()` uses `MessagesState` when `state_class` not provided |
| FR-14 | State declaration in YAML | Should | v1.1 | `state:` section in YAML defines state fields, types, and reducers |
| FR-15 | Auto-Mermaid generation | Nice | v1.1 | Expose LangGraph's `.draw_mermaid()` after compilation |
| FR-16 | JSON Schema for YAML files | Nice | v1.1 | Published schema enables IDE autocomplete for workflow YAML |
| FR-17 | Subgraph composition | Should | v2 | `subgraph: "file.yaml"` in node definition compiles and embeds a sub-graph |
| FR-18 | Simple value-matching routing | Nice | v2 | `match: "state.field"` + `targets:` for routing without a Python function |

### 4.2 Non-Functional Requirements

| ID | Category | Requirement | Target |
|---|---|---|---|
| NFR-01 | Compatibility | Support Python 3.10+ | Matches LangGraph's minimum version |
| NFR-02 | Compatibility | Support LangGraph >=0.2 | Compatible with current and recent LangGraph releases |
| NFR-03 | Dependencies | Minimal dependency footprint | Only `langgraph`, `pyyaml`, `pydantic` |
| NFR-04 | Performance | Zero runtime overhead vs hand-written graphs | Compilation happens once; compiled graph is identical to manual construction |
| NFR-05 | Packaging | Installable from PyPI | `pip install langgraph-declarative` |
| NFR-06 | Testing | Comprehensive test coverage | All edge types, validation paths, and error cases covered |
| NFR-07 | Documentation | README with quickstart and examples | New user can build first graph in <5 minutes |

---

## 5. Scope

### 5.1 In Scope (v1)

- `Registry` class with `@registry.node()` and `@registry.router()` decorators
- `GraphBuilder` class that compiles YAML + registry into `CompiledStateGraph`
- `build_graph()` convenience function
- YAML format supporting: nodes, simple edges, fan-out, conditional edges (mapped routing), dynamic routing (Send)
- Pydantic-based YAML schema validation
- Error messages with typo detection and available-name suggestions
- Test suite (pytest)
- README with quickstart, examples, and API reference
- PyPI package (`langgraph-declarative`)
- `TODO.md` with v1.1/v2 backlog

### 5.2 Out of Scope (deferred)

- State declaration in YAML (v1.1)
- Pydantic model factory integration (v1.1)
- Auto-Mermaid generation (v1.1)
- JSON Schema for IDE autocomplete (v1.1)
- Subgraph composition (v2)
- Tool/LLM configuration in YAML (v2)
- Database-driven graph sources (v2)
- LangGraph Template packaging (v2)
- Expression-based routing / `eval()` (rejected for security)
- CLI tooling (future idea)

### 5.3 Assumptions

- LangGraph's `StateGraph` API remains stable across 0.2+ releases
- Users are familiar with LangGraph concepts (nodes, edges, state)
- Python node/router functions are co-located with or importable by the code that calls `build_graph()`
- YAML is the primary config format (JSON/TOML support is future work)

### 5.4 Dependencies

| # | Dependency | Owner | Risk if Unavailable |
|---|---|---|---|
| 1 | LangGraph >=0.2 | LangChain Inc. | Cannot build — core dependency |
| 2 | Pydantic >=2.0 | Pydantic team | Cannot validate YAML schema |
| 3 | PyYAML >=6.0 | YAML community | Cannot parse config files |

---

## 6. Epics & User Stories

### Epic 1: Node & Router Registry
**Description:** Decorator-based registration system for node functions and router functions
**Priority:** 1

| Story ID | User Story | Acceptance Criteria | Priority |
|---|---|---|---|
| US-1.1 | As a developer, I want to register node functions with `@registry.node("name")` so that they can be referenced in YAML | Function is callable via `registry.get_node("name")`; duplicate names raise `ValueError` | Must |
| US-1.2 | As a developer, I want to register router functions with `@registry.router("name")` so that they can be used for conditional edges | Function is callable via `registry.get_router("name")`; separate namespace from nodes | Must |
| US-1.3 | As a developer, I want helpful error messages when looking up missing names so that I can fix typos quickly | `KeyError` message lists available names; suggests closest match if possible | Must |

### Epic 2: YAML Graph Definition
**Description:** YAML format for declaring graph topology — nodes, edges, and conditional routing
**Priority:** 1

| Story ID | User Story | Acceptance Criteria | Priority |
|---|---|---|---|
| US-2.1 | As a developer, I want to define nodes in YAML with `name` and `function` so that I don't write `add_node()` calls | YAML `nodes:` section parsed; each node resolved from registry | Must |
| US-2.2 | As a developer, I want to define simple edges with `source` and `target` so that I don't write `add_edge()` calls | YAML `edges:` section parsed; `START`/`END` resolve to LangGraph constants | Must |
| US-2.3 | As a developer, I want to define parallel fan-out with `target: [list]` so that multiple nodes run concurrently | List targets create multiple edges from same source | Must |
| US-2.4 | As a developer, I want to define conditional edges with `path` and `targets` so that routing is visible in YAML | `path:` resolves router from registry; `targets:` becomes `path_map`; calls `add_conditional_edges()` | Must |
| US-2.5 | As a developer, I want to use `path` without `targets` for dynamic routing (Send) so that runtime fan-out works | Router returning `list[Send]` handled correctly; no `path_map` passed to LangGraph | Must |

### Epic 3: Validation & Error Handling
**Description:** Schema validation of YAML files and actionable error messages
**Priority:** 1

| Story ID | User Story | Acceptance Criteria | Priority |
|---|---|---|---|
| US-3.1 | As a developer, I want YAML structure validated before compilation so that malformed configs fail fast | Pydantic model validates required fields, types, and structure | Must |
| US-3.2 | As a developer, I want cross-reference validation so that typos in node/router names are caught | All `function:` refs exist in node registry; all `path:` refs exist in router registry | Must |
| US-3.3 | As a developer, I want edge consistency validation so that edges reference defined nodes | Source/target of every edge must be a defined node, `START`, or `END` | Must |
| US-3.4 | As a developer, I want actionable error messages so that I can fix issues quickly | Errors include: what's wrong, where in the YAML, and suggestions for fixes | Must |

### Epic 4: Build API & Packaging
**Description:** Public API, convenience functions, and PyPI packaging
**Priority:** 1

| Story ID | User Story | Acceptance Criteria | Priority |
|---|---|---|---|
| US-4.1 | As a developer, I want a one-line `build_graph()` function so that simple cases are trivial | `build_graph("file.yaml", registry)` returns `CompiledStateGraph` | Must |
| US-4.2 | As a developer, I want `build_graph()` to default to `MessagesState` so that chatbot graphs need no state class | Omitting `state_class` uses `MessagesState`; providing it overrides | Should |
| US-4.3 | As a developer, I want a `GraphBuilder` class for more control so that I can customize compilation | `GraphBuilder(registry, state_class).build("file.yaml")` works | Must |
| US-4.4 | As a developer, I want to install via pip so that I can use it in any project | `pip install langgraph-declarative` installs from PyPI | Must |

---

## 7. Risks

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| 1 | LangGraph API breaking changes | M | H | Pin minimum version; test against latest in CI; thin wrapper layer |
| 2 | YAML validation too strict or too loose | M | M | Start strict with clear error messages; relax based on user feedback |
| 3 | Conditional edge design doesn't cover edge cases | L | H | Design maps 1:1 to native API; Send handles dynamic cases; extensible |
| 4 | Low initial adoption | M | M | Clear README, runnable examples, community posting (LangChain forums, LinkedIn) |
| 5 | Scope creep during implementation | M | M | Strict v1 boundary; TODO.md for future work; no v2 features in v1 |

---

## 9. Release Strategy

**MVP definition (v1):** A pip-installable library that can build any LangGraph `StateGraph` from a YAML file + Python registry. Supports all edge types (simple, fan-out, conditional, Send). Validates YAML with actionable errors.

**Phasing:**
- **v1:** Core library — registry, builder, conditional edges, validation, packaging
- **v1.1:** State-in-YAML (model factory), auto-Mermaid, JSON Schema for IDE support
- **v2:** Subgraph composition, tool/LLM config, database sources, LangGraph Template

**Acceptance testing:** Pytest suite covering all edge types, validation paths, and error cases. Manual testing with example workflows.

---

## Appendix: Glossary

| Term | Definition |
|---|---|
| Node | A function that transforms graph state (receives state, returns dict updates) |
| Router | A function that inspects state and returns a routing key (determines which node runs next) |
| Send | A LangGraph object for dynamic fan-out — spawns parallel node executions with custom state per invocation |
| Registry | A collection of named node and router functions that YAML configurations reference by name |
| `MessagesState` | LangGraph's built-in state class with a `messages` list and `add_messages` reducer |
| Reducer | A function that defines how state updates are merged (e.g., append vs. replace) |
| Mapped routing | Conditional edge pattern where a router returns a key and a YAML `targets:` map translates keys to node names |
| Fan-out | An edge pattern where one source connects to multiple targets for parallel execution |

---

**Notes:**
- V1.1 and v2 features are scoped in this PRD for architectural awareness but implementation is deferred
- The model factory code from a prior production project (~250 lines) can be ported directly for v1.1
- Architecture should account for v2 extensibility (pluggable loaders, extensible YAML schema)
