# CLAUDE.md

## Framework Instructions

See `MAESTRO.md` for all delivery framework behavior, commands, output standards, and conventions. MAESTRO.md is the canonical framework reference.

When interacting, always apply instructions from `MAESTRO.md`.
Always save substantive responses to a file in the session folder unless the response is very short (< 80 words).

## Project

- **Framework:** Maestro (command prefix: `mae-`, aliases: `mex`/`mrq`/`mds`/`mpl`/`mdo`/`mrv`)
- **What this is:** A Python library that compiles declarative workflow definitions into LangGraph graphs. Topology lives in YAML (or a database), node/router/tool logic stays in Python behind a decorator registry, and `build_graph()` returns a standard `CompiledStateGraph`.
- **Current phase:** maintenance — 0.2.0 on PyPI; M05 (HITL) done, unreleased; next is M06 hardening → 0.3.0 release, then M07 (0.4.0)
- **Stack:** Python 3.10+, LangGraph ≥1.0, Pydantic ≥2.8.2, PyYAML ≥6.0.2, hatchling, pytest, uv
- **Language:** English

## Conventions

- Source lives in `src/langgraph_declarative/`; tests in `tests/` with YAML fixtures in `tests/fixtures/`
- Every user-facing feature has a runnable example in `examples/` — add one when adding a feature
- `tests/fixtures/*.yaml` are the de facto spec for the YAML schema; update them together with `schema/workflow.schema.json` and its packaged copy `src/langgraph_declarative/workflow.schema.json` (tests enforce all three match `export_json_schema()`)
- Run tests with `uv run --extra dev pytest` (the dev extra brings pytest, jsonschema and the SQLite checkpointer)
- Milestone labels (v1 / v1.1 / v2, M01–M08) are not package versions. User-facing docs cite package versions (0.1.0 / 0.2.0 / 0.3.0); tags `vX.Y.Z` only for published releases

## Framework deviations

`OPEN_QUESTIONS.md` and `WORKLOG.md` are **intentionally absent** from this repo. `MAESTRO.md`, `/status`, `/sync`, and `/decide` reference them — treat that as expected, do not recreate them. Open questions go in the session `_summary.md`; confirmed decisions go straight to `DECISIONS.md`. If `install.sh` regenerates the two stubs, delete them again.

`docs/04-plan/ROADMAP.md` is the **only** roadmap, per the Maestro standard. The root `ROADMAP.md` was removed in session 11 — it duplicated information and drifted. Do not recreate it; README links point at the `docs/` one.
