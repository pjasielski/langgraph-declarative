# Project Review: langgraph-declarative (`dev`)

**Date:** 2026-05-31
**Repo reviewed:** `https://github.com/pjasielski/langgraph-declarative` (`dev`)
**Scope:** `src/`, `tests/`, `examples/`, packaging metadata, and runtime behavior checks

**Model:** Codex 5.3

## Findings (by severity)

### High

1. **Conditional routing can fail silently when router returns an unmapped key.**In mapped conditional mode (`path` + `targets`), if a router returns a key not present in `targets`, LangGraph logs a warning (`wrote to unknown channel ... ignoring it`) and continues. This can skip intended branches without a hard failure, producing partial output.
   - **Why this matters:** Silent routing drops are hard to detect and can cause incorrect business behavior in production.
   - **Where:** `src/langgraph_declarative/builder.py` (mapped routing path in `_add_edges`)
   - **Observed via probe:** custom config with empty/invalid target map compiled and returned partial result instead of raising.

### Medium

2. **Examples are not runnable from repo root (path handling issue).**`examples/*/main.py` use `build_graph("workflow.yaml", registry)`, which fails unless executed from the example directory.

   - **Why this matters:** New users commonly run example scripts from project root; first-run failure hurts onboarding.
   - **Where:** `examples/quickstart/main.py`, `examples/conditional_routing/main.py`
   - **Observed:** running from repo root throws `ConfigLoadError: Config file not found: workflow.yaml`.
3. **Packaging metadata points to wrong repository URLs.**`pyproject.toml` uses `https://github.com/piotr/langgraph-declarative` for `Repository`/`Homepage`, while reviewed repo is `pjasielski/langgraph-declarative`.

   - **Why this matters:** Broken package metadata hurts trust/discoverability and directs users to the wrong place.
   - **Where:** `pyproject.toml` (`[project.urls]`)
4. **No CI workflow is present to protect quality on future changes.**Tests are strong and pass locally, but there is no checked-in CI pipeline to enforce them on PRs/branch changes.

   - **Why this matters:** Regressions can slip in once contributors or release cadence grow.
   - **Where:** no `.github/workflows/*` found.

## Strengths

- **Core architecture is clean and intentionally thin.** `Registry` + `GraphBuilder` + schema/cross-validation are easy to reason about and map directly to LangGraph.
- **Test suite quality is strong.** 73 tests passed (`uv run --extra dev pytest`), with good coverage across builder/schema/errors/integration.
- **Feature set aligns with v1 promise.** Simple edges, fan-out, mapped conditional routing, and dynamic Send-based routing are implemented.
- **Packaging/build works.** `uv build` successfully produced both sdist and wheel.

## Recommendations (what to change and how)

1. **Enforce strict mapped-routing behavior in builder.**

   - In mapped mode (`targets` is present), wrap router execution:
     - if return is not `str`, raise `ConfigValidationError`
     - if returned key is not in `targets`, raise `ConfigValidationError` with allowed keys
   - Add tests for:
     - unknown routing key raises
     - non-string mapped key raises
     - empty `targets` rejected during validation.
2. **Fix example path resolution for reliable execution from any working directory.**

   - In each example `main.py`, compute YAML path using:
     - `workflow_path = Path(__file__).with_name("workflow.yaml")`
   - Use `build_graph(workflow_path, registry)`.
   - Add a small smoke test or README instruction verifying root-level invocation.
3. **Correct package URLs in `pyproject.toml`.**

   - Update `Repository` and `Homepage` to the canonical GitHub path.
   - Validate before release (`uv build` + check wheel metadata).
4. **Add baseline CI.**

   - Add GitHub Actions workflow for:
     - `uv run --extra dev pytest`
     - `uv build`
   - Start with Python 3.10 + latest stable, then expand matrix if needed.
5. **Optional hardening improvements (next increment).**

   - Wrap raw LangGraph entrypoint errors with framework-specific errors for clearer diagnostics.
   - Add explicit validation for empty `targets` maps in mapped-routing mode.

## Verification Snapshot

- `uv run --extra dev pytest` -> **73 passed**
- `uv build` -> **sdist + wheel built successfully**
- Example scripts:
  - from repo root -> **fail** (workflow file not found)
  - from example folders -> **pass**
