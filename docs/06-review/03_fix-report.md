# Fix Report: Codex Review Findings

**Date:** 2026-06-01
**Review:** 01_langgraph-declarative-project-review.md
**Assessment:** 02_codex-review-assessment.md
**Status:** All findings resolved

---

## Fixes Applied

### Fix 1 — Strict Mapped Routing (HIGH)

**Problem:** When a mapped conditional router returned a key not present in `targets`, LangGraph silently dropped the branch. No error was raised, producing partial output.

**Root cause:** The builder passed `path_map` directly to `add_conditional_edges()` without validating the router's return value. LangGraph's default behavior is to log a warning and ignore unknown channels.

**Fix:**
- `builder.py` — Added `_wrap_mapped_router()` that intercepts the router at runtime and validates: (a) return type is `str`, (b) returned key exists in the `targets` map. Raises `ConfigValidationError` with the bad key and allowed keys listed.
- `schema.py` — Added validator rejecting empty `targets: {}` at config parse time.

**Tests added:** 4 (unmapped key raises, non-string return raises, empty targets rejected, valid key passes through).

---

### Fix 2 — Example Path Resolution (MEDIUM)

**Problem:** Example scripts used `build_graph("workflow.yaml", registry)` with a bare relative path, failing when run from any directory other than the example folder itself.

**Fix:** Both `examples/quickstart/main.py` and `examples/conditional_routing/main.py` now resolve the YAML path relative to the script: `Path(__file__).with_name("workflow.yaml")`.

---

### Fix 3 — Package URLs (MEDIUM)

**Problem:** `pyproject.toml` pointed Repository and Homepage to `github.com/piotr/...` instead of `github.com/pjasielski/...`.

**Fix:** Updated both URLs to the correct GitHub path.

---

### Fix 4 — Baseline CI (MEDIUM)

**Problem:** No CI workflow existed. Tests passed locally but were not enforced on PRs.

**Fix:** Added `.github/workflows/ci.yml` — GitHub Actions running `pytest` and `uv build` on Python 3.10 and 3.12, triggered on push to `main`/`dev` and on PRs to `main`.

---

## Verification

| Check | Result |
|-------|--------|
| `uv run --extra dev pytest` | **77 passed** (73 original + 4 new) |
| No existing tests broken | Confirmed |
| Examples runnable from repo root | Confirmed (path resolution fixed) |
| Package URLs correct | Confirmed |

---

## Deferred Items

| Item | Source | Reason | Track in |
|------|--------|--------|----------|
| Wrap LangGraph entrypoint errors with framework-specific errors | Codex recommendation #5 | v1.1 improvement, not a v1 defect | TODO.md |
