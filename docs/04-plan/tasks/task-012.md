# Task 012: Create ROADMAP.md
**Status:** done
**Priority:** medium
**Assigned:** unassigned
**Blocked by:** —
**Effort:** S
**Created:** 2026-06-11
**Completed:** 2026-06-11

## Description
Create a public-facing `ROADMAP.md` in the repo root that clearly communicates what's been shipped (v1), what's coming next (v1.1), and what's planned for the future (v2). This replaces the terse `TODO.md` as the primary future-scope document. `TODO.md` can remain as the working backlog.

## Acceptance Criteria
- [x] `ROADMAP.md` exists in repo root
- [x] Clear sections for: v1 (shipped), v1.1 (next), v2 (future), ideas
- [x] v1 section summarizes what shipped (registry, builder, all edge types, validation, examples, PyPI)
- [x] v1.1 section details: state-in-YAML, auto-Mermaid, JSON Schema, `match:` routing
- [x] v2 section details: subgraph composition, tool/LLM config, database sources
- [x] Each future item has a one-line description of what it enables for users
- [x] README.md updated to link to ROADMAP.md

## Files
- `ROADMAP.md` (create)
- `README.md` (edit — add link)

## Notes
- Source material: `TODO.md` (since folded into `ROADMAP.md`), `docs/02-requirements/REQUIREMENTS.md` (section 5), `.sessions/001-exploration/04_delivery-approach-and-open-items.md`
- Tone: user-facing, not internal. Written for someone evaluating the library.
- Keep it concise — each item is 1-2 lines, not a spec
