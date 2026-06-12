# README update

**Date:** 2026-06-12

Rewrote the root `README.md`. Changes:

- **Better library explanation** — the intro now describes the three-piece model (Registry → YAML definition → Builder) and states the value proposition explicitly (topology changes as config edits; diffable, IDE-validated, diagrammable, DB-storable workflows).
- **Features section replaced** with a compact table covering all v1/v1.1/v2 features, each row linking to its runnable example. The old per-feature code blocks (v1-only, duplicated example content) were removed.
- **YAML reference updated** to the full current syntax: `state:`, `llm:`, `imports:`, `subgraph:`, `tools:`, `match:` — previously it only showed v1 keys. Added the IDE `$schema` modeline tip.
- **API table updated** with `@registry.tool()`, `draw_mermaid()`, `export_json_schema()`, `SQLiteLoader`, `build_graph_from_db()`.
- **New Documentation section** linking examples README, ROADMAP, CHANGELOG, DECISIONS, PRD (`delivery/02-prd/PRD.md`), SDD (`delivery/03-design/SDD.md`), PLAN (`delivery/04-plan/PLAN.md`), and `template/`.
- **Project layout trimmed** from a stale 30-line tree to a 6-line directory overview (the old tree listed pre-v1.1 modules and missed `llm_factory`, `state_factory`, `loaders/`, `schema/`, `template/`).
- **Status section fixed** — previously claimed v1.1 was "next" and v2 "future"; both are implemented.
- **Install section** now mentions the `[anthropic]`/`[openai]` extras.
