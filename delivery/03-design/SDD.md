# SDD: langgraph-declarative

**Date:** 2026-05-30
**Version:** v1
**Status:** Draft
**PRD:** delivery/02-prd/PRD.md

---

## 1. Overview

### 1.1 Purpose

Technical architecture for `langgraph-declarative` — a Python library that compiles YAML workflow definitions into LangGraph `CompiledStateGraph` objects using a decorator-based node/router registry. Covers all v1 functional requirements (FR-01 through FR-13) with architecture designed for v1.1/v2 extensibility.

### 1.2 Scope

- `langgraph_declarative` Python package (src layout)
- Registry, builder, schema validation, error handling modules
- YAML format specification
- Test suite and packaging

### 1.3 Design Principles

1. **Thin wrapper** — translate YAML to LangGraph API calls, don't abstract them away. The compiled graph should be identical to one built by hand.
2. **Fail fast, fail clearly** — validate everything before compilation. Every error message should say what's wrong, where, and how to fix it.
3. **Extensible by design** — v1 architecture must not block v2 features (subgraphs, state-in-YAML, database sources). Use interfaces/protocols where extension points are known.
4. **Minimal surface area** — expose only what users need. Internals stay internal.

---

## 2. Architecture

### 2.1 System Diagram

```
                    User Code                          Library
              ┌─────────────────┐        ┌──────────────────────────────┐
              │                 │        │  langgraph_declarative       │
              │  @registry.node │───────►│                              │
              │  @registry.router│       │  ┌──────────┐               │
              │                 │        │  │ Registry  │               │
              │  build_graph()  │───┐    │  └─────┬────┘               │
              │                 │   │    │        │                     │
              └─────────────────┘   │    │  ┌─────▼────┐  ┌─────────┐ │
                                    │    │  │  Loader   │  │ Schema  │ │
              workflow.yaml ────────┘───►│  │  (YAML)   ├─►│Validator│ │
                                         │  └─────┬────┘  └────┬────┘ │
                                         │        │            │      │
                                         │  ┌─────▼────────────▼──┐  │
                                         │  │    GraphBuilder      │  │
                                         │  │  (resolve + compile) │  │
                                         │  └──────────┬──────────┘  │
                                         │             │              │
                                         └─────────────┼──────────────┘
                                                       │
                                                       ▼
                                              CompiledStateGraph
                                                (LangGraph)
```

### 2.2 Component Overview

| Component | Responsibility | Module | Notes |
|---|---|---|---|
| Registry | Store and look up node/router functions by name | `registry.py` | Two namespaces: nodes, routers |
| Loader | Read YAML files, parse into Python dicts | `loader.py` | Thin wrapper around PyYAML; extensible for future sources |
| Schema | Validate parsed config structure against Pydantic models | `schema.py` | Catches structural errors before compilation |
| GraphBuilder | Resolve references, translate config to LangGraph API calls, compile | `builder.py` | Core engine — calls `StateGraph.add_node/add_edge/add_conditional_edges` |
| Errors | Custom exceptions, typo suggestion logic | `errors.py` | Uses `difflib.get_close_matches` for suggestions |
| Public API | `build_graph()` convenience function, re-exports | `__init__.py` | Thin entry point combining loader + validator + builder |

### 2.3 Data Flow

| Step | From | To | Data | Notes |
|---|---|---|---|---|
| 1 | User | Registry | Python functions | Via `@registry.node()` / `@registry.router()` decorators at import time |
| 2 | User | `build_graph()` | YAML path + registry + optional state_class | Single entry point |
| 3 | `build_graph()` | Loader | File path | Returns parsed dict |
| 4 | Loader | Schema Validator | Parsed dict | Returns validated `GraphConfig` Pydantic model |
| 5 | Schema Validator | GraphBuilder | `GraphConfig` + Registry + state_class | Cross-validates refs against registry |
| 6 | GraphBuilder | LangGraph | `StateGraph` API calls | Produces `CompiledStateGraph` |
| 7 | `build_graph()` | User | `CompiledStateGraph` | Ready for `.ainvoke()` / `.invoke()` |

---

## 3. Tech Stack

| Category | Choice | Alternatives Considered | Rationale |
|---|---|---|---|
| Language | Python 3.10+ | 3.9 | `X \| Y` union syntax; matches LangGraph minimum |
| Graph engine | LangGraph >=0.2 | — | Target framework — this library wraps it |
| Config format | YAML (PyYAML) | JSON, TOML | YAML supports comments, is human-friendly; standard for declarative config |
| Validation | Pydantic v2 | dataclasses, attrs | Rich validation, JSON Schema generation (useful for v1.1), ecosystem standard |
| Build backend | Hatchling | setuptools, poetry | Modern, minimal config, used by LangGraph itself |
| Testing | pytest | unittest | Community standard, better fixtures/parametrize |
| Typo matching | `difflib` (stdlib) | `thefuzz`, `rapidfuzz` | Zero extra dependencies; `get_close_matches` is sufficient |

### ADRs

**ADR-001: Separate node and router namespaces**
- **Context:** Nodes transform state (return dicts), routers decide routing (return strings/Send). Mixing them in one namespace means a typo in `path:` could silently resolve to a node function, producing confusing runtime errors.
- **Decision:** Registry maintains separate `_nodes` and `_routers` dicts. YAML `function:` resolves from nodes, `path:` resolves from routers.
- **Consequences:** Slightly more API surface (`@registry.node` + `@registry.router`), but validation catches wiring errors at build time.

**ADR-002: Pydantic for YAML schema, not just runtime validation**
- **Context:** The YAML structure needs validation. Options: manual dict checking, JSON Schema, Pydantic.
- **Decision:** Use Pydantic `BaseModel` subclasses to define the expected YAML structure. Parse YAML to dict, then validate with Pydantic.
- **Consequences:** Pydantic is already a dependency (used by LangGraph). Enables JSON Schema export in v1.1 for IDE autocomplete. Gives typed access to config fields inside the builder.

**ADR-003: Loader abstraction for v2 extensibility**
- **Context:** V1 loads from YAML files. V2 may support databases, APIs, or other sources.
- **Decision:** The `Loader` is a simple function (`load_config(source) -> dict`) that the builder calls. V1 implements YAML file loading. V2 can add loaders without changing the builder.
- **Consequences:** Minimal v1 overhead (one function), clean extension point for v2.

---

## 4. Data Model

### 4.1 YAML Config Schema

The YAML file is the primary data model. Pydantic models mirror this structure for validation.

```yaml
# Complete YAML format specification
nodes:
  - name: "node_name"              # unique within this file
    function: "registry_node_name"  # must exist in registry.nodes

edges:
  # Simple edge
  - source: "START"                 # or any node name
    target: "node_name"            # or "END"

  # Parallel fan-out
  - source: "node_name"
    target: ["node_a", "node_b"]   # list = fan-out

  # Conditional edge (mapped routing)
  - source: "node_name"
    path: "registry_router_name"   # must exist in registry.routers
    targets:                        # path_map: router return value → node
      key_a: "node_a"
      key_b: "node_b"
      default: "fallback_node"     # optional default

  # Dynamic routing (Send / direct return)
  - source: "node_name"
    path: "registry_router_name"   # router returns node names or Send objects
    # no targets = no path_map
```

### 4.2 Pydantic Models

```python
from pydantic import BaseModel, field_validator

class NodeConfig(BaseModel):
    name: str
    function: str

class EdgeConfig(BaseModel):
    source: str
    target: str | list[str] | None = None
    path: str | None = None
    targets: dict[str, str] | None = None

    @field_validator(...)  # ensure target or path is provided, not both absent

class GraphConfig(BaseModel):
    nodes: list[NodeConfig]
    edges: list[EdgeConfig]
```

**Validation rules (enforced by Pydantic + custom validators):**

| Rule | Error if violated |
|---|---|
| Every edge has `source` | "Edge missing 'source' field" |
| Every edge has `target` OR `path` | "Edge from '{source}' has neither 'target' nor 'path'" |
| `target` and `path` are mutually exclusive | "Edge from '{source}' has both 'target' and 'path' — use one or the other" |
| `targets` only appears with `path` | "Edge from '{source}' has 'targets' without 'path'" |
| Node names are unique | "Duplicate node name: '{name}'" |

---

## 5. Source Structure

```
langgraph-declarative/
├── src/
│   └── langgraph_declarative/
│       ├── __init__.py             # Public API: Registry, GraphBuilder, build_graph
│       ├── registry.py             # Registry class with @node() and @router() decorators
│       ├── builder.py              # GraphBuilder class — config → CompiledStateGraph
│       ├── schema.py               # Pydantic models: GraphConfig, NodeConfig, EdgeConfig
│       ├── loader.py               # load_yaml(path) → dict (thin PyYAML wrapper)
│       └── errors.py               # Custom exceptions + typo suggestion helpers
├── tests/
│   ├── conftest.py                 # Shared fixtures (registry, sample configs)
│   ├── test_registry.py            # Registration, lookup, errors, namespaces
│   ├── test_schema.py              # Pydantic validation: valid/invalid configs
│   ├── test_builder.py             # Graph compilation: all edge types
│   ├── test_loader.py              # YAML loading, file-not-found handling
│   ├── test_errors.py              # Typo suggestions, error message formatting
│   ├── test_integration.py         # End-to-end: YAML → build_graph → invoke
│   └── fixtures/
│       ├── simple.yaml             # Basic linear graph
│       ├── fan_out.yaml            # Parallel fan-out
│       ├── conditional.yaml        # Conditional routing with targets
│       ├── dynamic_routing.yaml    # Send-based routing (no targets)
│       ├── full_featured.yaml      # All features combined
│       └── invalid/
│           ├── missing_node.yaml   # References undefined node
│           ├── duplicate_name.yaml # Same node name twice
│           ├── no_edges.yaml       # Nodes but no edges
│           └── bad_structure.yaml  # Wrong YAML shape
├── examples/
│   ├── quickstart/
│   │   ├── workflow.yaml
│   │   └── main.py
│   └── conditional_routing/
│       ├── workflow.yaml
│       └── main.py
├── pyproject.toml
├── README.md
├── LICENSE
├── TODO.md
├── CHANGELOG.md
└── .gitignore
```

### Module Details

**`registry.py`** (~90 lines)

```python
class Registry:
    def __init__(self):
        self._nodes: dict[str, Callable] = {}
        self._routers: dict[str, Callable] = {}

    def node(self, name: str) -> Callable:
        """Decorator: register a node function."""

    def router(self, name: str) -> Callable:
        """Decorator: register a router function."""

    def get_node(self, name: str) -> Callable:
        """Look up node by name. Raises NodeNotFoundError with suggestions."""

    def get_router(self, name: str) -> Callable:
        """Look up router by name. Raises RouterNotFoundError with suggestions."""

    def list_nodes(self) -> list[str]: ...
    def list_routers(self) -> list[str]: ...
```

**`builder.py`** (~120 lines)

```python
class GraphBuilder:
    def __init__(self, registry: Registry, state_class: type | None = None):
        self.registry = registry
        self.state_class = state_class or MessagesState

    def build(self, config: GraphConfig) -> CompiledStateGraph:
        """Build and compile a StateGraph from a validated config."""

    def build_from_file(self, path: str | Path) -> CompiledStateGraph:
        """Load YAML, validate, build. Convenience method."""

    def _add_nodes(self, builder: StateGraph, nodes: list[NodeConfig]) -> None: ...
    def _add_edges(self, builder: StateGraph, edges: list[EdgeConfig]) -> None: ...
    def _resolve_sentinel(self, name: str) -> str | Constant: ...
```

**`loader.py`** (~30 lines)

```python
def load_yaml(path: str | Path) -> dict:
    """Load and parse a YAML file. Raises ConfigLoadError on failure."""
```

**`schema.py`** (~80 lines)

```python
class NodeConfig(BaseModel): ...
class EdgeConfig(BaseModel): ...
class GraphConfig(BaseModel): ...

def validate_config(raw: dict) -> GraphConfig:
    """Parse raw dict into validated GraphConfig. Raises ConfigValidationError."""

def cross_validate(config: GraphConfig, registry: Registry) -> None:
    """Check that all function/path refs exist in registry. Check edge targets
    reference defined nodes. Raises ReferenceError with suggestions."""
```

**`errors.py`** (~60 lines)

```python
class DeclarativeError(Exception): """Base exception."""
class ConfigLoadError(DeclarativeError): """YAML file loading failed."""
class ConfigValidationError(DeclarativeError): """YAML structure invalid."""
class NodeNotFoundError(DeclarativeError): """Node name not in registry."""
class RouterNotFoundError(DeclarativeError): """Router name not in registry."""

def suggest_similar(name: str, available: list[str], n: int = 3) -> list[str]:
    """Return up to n close matches using difflib."""

def format_not_found(kind: str, name: str, available: list[str]) -> str:
    """Format a helpful error message with suggestions."""
```

**`__init__.py`** (~15 lines)

```python
from langgraph_declarative.registry import Registry
from langgraph_declarative.builder import GraphBuilder

def build_graph(
    path: str | Path,
    registry: Registry,
    state_class: type | None = None,
) -> CompiledStateGraph:
    """One-line graph compilation from YAML file + registry."""
    builder = GraphBuilder(registry=registry, state_class=state_class)
    return builder.build_from_file(path)

__all__ = ["Registry", "GraphBuilder", "build_graph"]
```

---

## 6. Open Questions

| # | Question | Blocks | Owner | Notes |
|---|---|---|---|---|
| 1 | Should `cross_validate` also warn about unreachable nodes (defined but never targeted)? | Error quality | Implementation | Low priority — nice-to-have warning, not a blocking error |
| 2 | Should `build_graph()` accept a dict in addition to a file path (for programmatic config)? | API flexibility | Implementation | Easy to add: `build_from_dict(config_dict)` on GraphBuilder |

---

**Notes:**
- Total estimated library code: ~400 lines across 5 modules. Compact by design.
- Test suite will likely be 2-3x the library code (many edge cases to cover).
- Architecture is deliberately simple — no plugin system, no abstract base classes, no dependency injection. Extension points (loader, schema) are plain functions that can be replaced in v2 without breaking v1's API.
- The `GraphBuilder.build()` method accepts a `GraphConfig` (validated Pydantic model), while `build_from_file()` handles the full pipeline (load → validate → cross-validate → build). This separation lets power users inject configs from any source.
