# Changelog

## v0.3.0 (2026-10-02)

Human-in-the-loop (milestone M05) and hardening (milestone M06) — see
[the roadmap](docs/04-plan/ROADMAP.md).

Approval gates, pauses for input, and resumable runs. Previously the library could
not express these at all: nothing on the call chain reached `graph.compile()`, so
`interrupt()` had nowhere to persist state and a pause could not be resumed.

The HITL additions are backward compatible. The hardening fixes include breaking
changes, listed first — each turns a silent misbehaviour into an explicit error.

### Breaking changes

- **Relative paths resolve against the declaring file; no more working-directory
  fallback.** `GraphBuilder.build(config)` and `build_graph_from_db()` used to resolve
  relative `imports:` / `subgraph:` paths against the process working directory, so
  the same stored definition behaved differently depending on where the process
  started. Both now take a keyword `base_dir=`, and a relative path with no file
  origin and no `base_dir` raises `ConfigValidationError`. Absolute paths and
  `build_graph(path)` are unaffected. **Migrate:** pass `base_dir=` where you build
  in-memory or DB definitions that use relative paths.
- **`subgraph:` in an imported file is relative to that file.** With `build_graph()`
  too: a node pulled in through `imports:` used to resolve its `subgraph:` against
  the *importing* file, so a library file had to spell paths from its consumer's
  location. **Migrate:** write `subgraph:` paths in imported files relative to the
  file they are in (the natural spelling — it is what failed before).
- **Unknown YAML keys are rejected.** Every config model now forbids extra keys.
  Previously `tool:`, `temprature:` or `interupt_before:` validated cleanly and did
  nothing — with HITL, a typo in `interrupt_before` silently removed an approval
  gate. The error names the key and its location and suggests the closest valid
  key. `schema/workflow.schema.json` now sets `additionalProperties: false`.
  **Migrate:** remove or fix unknown keys; move free-text notes to the new
  `description:` field. This includes top-level keys used only to hold YAML anchors
  (e.g. `x-llm: &llm {...}`) — inline the anchor on its first real use instead.
- **Dependency floors raised: `langgraph>=1.0`, `pydantic>=2.8.2`, `pyyaml>=6.0.2`.**
  0.2.0 declared `langgraph>=0.2`, but only the lockfile was ever tested. Measured
  with the full suite: LangGraph 0.2.0 cannot import it and 0.2.x/0.3.x fail the
  HITL tests. LangGraph 1.0 itself needs Pydantic ≥2.7.4. Pydantic 2.8.2 and PyYAML
  6.0.2 are the first releases with Python 3.13 wheels on Linux, macOS and Windows,
  so no supported Python has to compile them from source. No upper cap. CI now
  tests the locked, lowest and latest resolution on Python 3.10, 3.12 and 3.13.

### Fixed

- **Mapped routers keep their signature** — a router used with `targets:` can now be
  `async def` and can take LangGraph's injected `config` parameter. Previously the
  validating wrapper called it synchronously with `state` only, so an async router
  failed with "returned coroutine" and a `config`-taking router with a `TypeError`.
  Dynamic routers (no `targets:`) were never affected.
- **Imported subgraph nodes** — see *Breaking changes*; a path written relative to
  the imported file used to fail with `Config file not found`.
- **Mapped routers that are callable objects** with `async def __call__` are now
  awaited instead of failing with "returned coroutine".
- **`destinations: ["START"]`** is rejected at validation with a clear message,
  instead of a raw LangGraph `ValueError` at compile time.
- **HITL docs and example** use LangGraph's `END` constant in
  `Command(goto=END)`. The string `"END"` is only translated inside YAML; in Python
  it names a nonexistent node, which LangGraph logs and ignores.
- **`SQLiteLoader.save()` under concurrent writers** — the next version is now
  allocated and inserted in one statement inside `BEGIN IMMEDIATE`, with a busy
  timeout. Previously two writers could both read `MAX(version)` and one failed
  with `UNIQUE constraint failed`. Connections are now also closed after each call.

### Deprecated

- **State `default:`** — setting it now emits a `DeprecationWarning`. LangGraph never
  applied these values: a node reading a field declared with `default: 5` found it
  missing. The value stays on `__field_defaults__` for introspection. Initialise
  fields in the graph input or in a node instead.

### Added

- **Caller-supplied `checkpointer`** — `build_graph()`, `GraphBuilder()`, and
  `build_graph_from_db()` accept a keyword-only `checkpointer`, passed to
  `compile()`. This is what makes `interrupt()` / `Command(resume=...)` and
  `thread_id` scoping work.
- **`destinations:` on nodes** — forwarded to `add_node(destinations=...)` so a node
  that routes itself with `Command(goto=...)` renders correctly. Without it,
  LangGraph draws a *wrong* `node --> END` edge rather than simply omitting edges.
- **`interrupt_before:` / `interrupt_after:`** — declare static pause points in YAML,
  no Python change needed. Cross-validated against declared nodes with a
  closest-match suggestion on typos.
- **Optional `store`** — cross-thread memory, passed through to `compile()`.
- **`human_in_the_loop` example** — a runnable approval gate showing the accept vs.
  reject side-effect difference.
- **`base_dir=`** on `GraphBuilder.build()`, `GraphBuilder.draw_mermaid()` and
  `build_graph_from_db()` — see *Breaking changes*.
- **`description:`** — optional free text on the graph, nodes and edges. It is the
  one documentation key that strict validation allows.
- **JSON Schema inside the package** — `langgraph_declarative/workflow.schema.json`,
  readable with `importlib.resources`. 0.2.0 documented the schema but shipped it
  only in the sdist and the repo, not in the installed wheel.
- **`py.typed`** — type checkers now use the package's annotations.

### Documentation

- **Security & trust** — workflow definitions are trusted input: they can import
  modules (`tools: ["module:attr"]`), read reachable YAML files (`imports:`,
  `subgraph:`) and select registered callables. Do not build graphs from untrusted
  definitions.
- **What the host owns in HITL** — thread-ID ownership, resume authorization,
  decision validation, stale/repeated decisions and audit. Static interrupts are a
  pause, not an authorization check; `destinations:` is diagram metadata and is not
  enforced at runtime.

### Notes

- **The checkpointer is never defaulted, by design.** Ownership flips by run mode:
  in your own process you own it, but under `langgraph dev` / LangGraph Platform the
  server owns it and one passed at compile time is silently ignored. Defaulting to
  an in-memory saver would appear to work locally and quietly do nothing once
  deployed.
- **Subgraphs do not receive their own checkpointer** — the parent's already covers
  interrupts raised inside them (verified against LangGraph 1.2.2).
- **HITL survives a restart** — a test pauses in one "process" and resumes in a
  fresh one that rebuilds the graph from YAML with a new `SqliteSaver` on the same
  file; the approved write happens exactly once and a rejection writes nothing.
- **Release process** — see [docs/08-deploy/RELEASE.md](docs/08-deploy/RELEASE.md).

## v0.2.0 (2026-07-26)

First public release — includes everything from milestones v1, v1.1, and v2.

### v1.1 features

- **State declaration in YAML** — define state fields, types (`str`, `int`, `list[str]`, …), and reducers (`append`, `add_messages`, `replace`) directly in the workflow file instead of writing a Python state class
- **Match routing** — route on a state field's value with `match:` + `targets:` in YAML, no Python router function needed; supports dot-notation for nested fields and a `default` fallback key
- **Mermaid diagram generation** — `draw_mermaid()` compiles a workflow and renders it as a Mermaid diagram (`.md` fenced block or raw output)
- **JSON Schema for YAML files** — `export_json_schema()` emits a schema that gives IDEs autocomplete and validation for workflow YAML; ships at `schema/workflow.schema.json`

### v2 features

- **Subgraph composition** — `subgraph: "child.yaml"` on a node embeds another workflow as a single node, with parent/child state sharing via common keys
- **Cross-file node imports** — `imports:` merges node declarations from shared library files; selective import with `nodes: [...]`
- **LLM configuration in YAML** — graph-level `llm:` default and node-level overrides; nodes opt in by accepting an `llm` parameter; supports `anthropic` and `openai` providers
- **Tool binding in YAML** — `tools:` on a node binds `@registry.tool()` functions or `"module.path:attr"` references to the node's LLM
- **Database-driven workflow source** — `SQLiteLoader` saves/loads versioned definitions; `build_graph_from_db()` compiles from DB with `"source"` or `"source@version"` pinning
- **LangGraph project template** — starter project scaffold for `langgraph dev` using the declarative pattern
- **12 runnable examples** — one per feature, organized by milestone

### Other

- Test suite expanded to 167 tests
- Pydantic cross-validation catches function/router reference errors with "did you mean?" suggestions

## v0.1.0 (2026-05-31)

Initial release (internal milestone v1).

### Features

- **Registry** -- `@registry.node()` and `@registry.router()` decorators for function registration
- **YAML graph definition** -- declare nodes and edges in YAML
- **All edge types** -- simple, fan-out (parallel), conditional (mapped routing), dynamic (Send)
- **Schema validation** -- Pydantic-based YAML validation with clear error messages
- **Cross-validation** -- checks function/router refs exist, edge targets reference defined nodes
- **Typo suggestions** -- `difflib`-based "did you mean?" on lookup failures
- **`build_graph()`** -- one-line convenience function for YAML-to-compiled-graph
- **`GraphBuilder`** -- power-user class for more control over compilation
- **Default `MessagesState`** -- chatbot graphs need no explicit state class
