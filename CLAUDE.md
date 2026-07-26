# CLAUDE.md

## Framework Instructions

See `MAESTRO.md` for all delivery framework behavior, commands, output standards, and conventions. MAESTRO.md is the canonical framework reference.

When interacting, always apply instructions from `MAESTRO.md`.
Always save substantive responses to a file in the session folder unless the response is very short (< 80 words).

## Project

- **Framework:** Maestro (command prefix: `mae-`, aliases: `mex`/`mrq`/`mds`/`mpl`/`mdo`/`mrv`)
- **What this is:** A Python library that compiles declarative workflow definitions into LangGraph graphs. Topology lives in YAML (or a database), node/router/tool logic stays in Python behind a decorator registry, and `build_graph()` returns a standard `CompiledStateGraph`.
- **Current phase:** maintenance — v1, v1.1, and v2 milestones all shipped; next step is the first PyPI release
- **Stack:** Python 3.10+, LangGraph ≥0.2, Pydantic v2, PyYAML, hatchling, pytest, uv
- **Language:** English

## Conventions

- Source lives in `src/langgraph_declarative/`; tests in `tests/` with YAML fixtures in `tests/fixtures/`
- Every user-facing feature has a runnable example in `examples/` — add one when adding a feature
- `tests/fixtures/*.yaml` are the de facto spec for the YAML schema; update them and `schema/workflow.schema.json` together
- Run tests with `uv run pytest`
- Milestone labels (v1 / v1.1 / v2) are not package versions — see `CHANGELOG.md`

## Framework deviations

`OPEN_QUESTIONS.md` and `WORKLOG.md` are **intentionally absent** from this repo. `MAESTRO.md`, `/status`, `/sync`, and `/decide` reference them — treat that as expected, do not recreate them. Open questions go in the session `_summary.md`; confirmed decisions go straight to `DECISIONS.md`. If `install.sh` regenerates the two stubs, delete them again.

`docs/04-plan/ROADMAP.md` is the canonical delivery roadmap. The root `ROADMAP.md` is a user-facing summary of it — update the `docs/` one first.
