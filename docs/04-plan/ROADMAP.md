# Roadmap: langgraph-declarative

**Updated:** 2026-07-26
**Requirements:** [docs/02-requirements/REQUIREMENTS.md](../02-requirements/REQUIREMENTS.md)
**Design:** [docs/03-design/DESIGN.md](../03-design/DESIGN.md)
**Tasks:** [tasks/](tasks/)

Canonical delivery tracker. The root [ROADMAP.md](../../ROADMAP.md) is the user-facing summary of the same information — this file is the one that gets updated first.

**Status values:** ☐ todo · 🔄 in progress · ⏳ blocked · ✅ done · ⊘ dropped

---

## Milestones

| # | Milestone | Scope | Tasks | Status |
|---|-----------|-------|-------|--------|
| M01 | Core library (v1) | Registry, loader, schema, builder, errors, packaging | 001–009 | ✅ done |
| M02 | Examples & hardening | Full edge-type example coverage, public roadmap, edge-case tests | 010–013 | ✅ done |
| M03 | Declarative surface (v1.1) | State in YAML, match routing, Mermaid, JSON Schema | 014–017 | ✅ done |
| M04 | Composition & config (v2) | Subgraphs, imports, LLM/tools, DB source, template | 018–023 | ✅ done |
| M05 | Backlog | Unvalidated ideas — no commitment | — | ☐ todo |

Released as `v0.2.0`. v1 / v1.1 / v2 are milestone labels, not package versions — see [CHANGELOG.md](../../CHANGELOG.md).

---

## Task index

Task files keep their original `task-NNN.md` names (shipped history, referenced from commit messages). Tasks created from here on use the Maestro 0.3 `M{MM}.{NN}` scheme.

### M01 — Core library

| # | Title | Effort | Status |
|---|-------|--------|--------|
| 001 | Scaffold project structure | S | ✅ done |
| 002 | Implement errors module | S | ✅ done |
| 003 | Implement registry module + tests | M | ✅ done |
| 004 | Implement schema module + tests | M | ✅ done |
| 005 | Implement loader module + tests | S | ✅ done |
| 006 | Implement builder module + tests | L | ✅ done |
| 007 | Implement public API + integration tests | M | ✅ done |
| 008 | Create examples | S | ✅ done |
| 009 | Finalize packaging and README | S | ✅ done |

### M02 — Examples & hardening

| # | Title | Effort | Status |
|---|-------|--------|--------|
| 010 | Add fan-out and Send examples | S | ✅ done |
| 011 | Add custom state example | S | ✅ done |
| 012 | Create ROADMAP.md | S | ✅ done |
| 013 | Edge-case tests and hardening | S | ✅ done |

### M03 — Declarative surface (v1.1)

| # | Title | Effort | Requirement | Status |
|---|-------|--------|-------------|--------|
| 014 | State declaration in YAML | L | FR-14 | ✅ done |
| 015 | Auto-Mermaid generation | S | FR-15 | ✅ done |
| 016 | JSON Schema for YAML files | S | FR-16 | ✅ done |
| 017 | Match routing syntax | M | FR-18 | ✅ done |

### M04 — Composition & config (v2)

| # | Title | Effort | Status |
|---|-------|--------|--------|
| 018 | Subgraph composition | XL | ✅ done |
| 019 | Tool configuration in YAML | L | ✅ done |
| 020 | LLM configuration per node | M | ✅ done |
| 021 | Database-driven graph source | L | ✅ done |
| 022 | LangGraph Template packaging | S | ✅ done |
| 023 | Cross-file node references | M | ✅ done |

---

## M05 — Backlog

Possibilities, not commitments. Each needs validation against real usage before it earns a task.

| Idea | What it would enable | Status |
|------|---------------------|--------|
| Graph diffing | Compare two YAML files, report topology changes | ☐ todo |
| Hot-reload | Watch a YAML file, recompile the graph on change | ☐ todo |
| CLI tool | `lgd validate workflow.yaml`, `lgd visualize workflow.yaml` | ☐ todo |
| Graph versioning | A/B test between YAML workflow variants | ☐ todo |
| LangGraph Studio export | Emit Studio-compatible format | ☐ todo |

YAML include/import shipped as task-023 (`imports:`) and is no longer a backlog item.

### Near-term operational work

| Item | Why | Status |
|------|-----|--------|
| First PyPI release | Name reserved, `release.yml` wired for Trusted Publishing, nothing published yet | ☐ todo |
| README logo asset for PyPI | PyPI strips SVG and can't resolve relative paths — needs an absolute PNG | ☐ todo |
| LangChain outreach | See `.sessions/007-promotion-marketing/02_langchain-outreach.md` | ☐ todo |

---

## Known risks

Carried forward from delivery — still relevant as maintenance context.

| Risk | Mitigation |
|------|------------|
| LangGraph API differences across versions | Minimum version pinned in `pyproject.toml`; CI tests against it |
| Pydantic v2 validator edge cases | Validators kept simple; invalid configs tested thoroughly |
| Subgraph state scoping complexity | Shared registry + state sharing via common keys only |
| LLM provider dependency sprawl | Providers are optional extras with lazy imports and a clear error when missing |
| DB loader schema migrations | Graph config stored as JSON text with a version field, not normalized tables |
| Test fixtures drift from the YAML spec | YAML fixtures in `tests/fixtures/` are the spec; tests validate against them |

---

## Test strategy

Tests are co-located with their module tasks rather than run as a separate phase — each module task included its test file.

| Test file | Covers |
|-----------|--------|
| `test_errors.py` | Error classes, `suggest_similar` accuracy, `format_not_found` output |
| `test_registry.py` | Registration, lookup, duplicate rejection, namespace isolation |
| `test_schema.py` | Pydantic validation, mutual exclusion (`target` vs `path`), duplicate node names |
| `test_builder.py` | All edge types, START/END resolution, cross-validation failures |
| `test_loader.py` | Valid file, missing file, malformed YAML |
| `test_integration.py` | End-to-end: YAML → `build_graph()` → `invoke()` |

Integration tests exercise the full pipeline against real LangGraph invocation — confirming compiled graphs actually run, not merely that they compile.

---

**Notes:**
- All delivery milestones are complete; the project is in maintenance.
- Update this file before the root `ROADMAP.md` — the root file summarises this one.
