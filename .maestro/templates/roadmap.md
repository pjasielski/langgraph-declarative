# ROADMAP — {Project Name}

**Version:** {current version}
**Updated:** {YYYY-MM-DD}
**Sources:** {sessions, reviews, or documents that informed this roadmap}

<!--
  Maestro Roadmap Template
  Strategic backlog organized by milestone. Not a substitute for task files —
  this is *what to build*; task files are *how to build it*.

  Columns:
  - #: Item ID `M{MM}.{NN}` — zero-padded (M01.01, M01.02, ...). The SAME ID is used
    in the task filename (`M01.01-{slug}.md`) and task title, so one search finds all.
  - Item: Short, descriptive name (bold)
  - Task: link to the task file once generated via /mae-plan, or "—"
  - Priority: P0 (bug) | P1 (required) | P2 (improvement) | P3 (future)
  - Effort: S (hours) | M (a session) | L (multiple sessions) | XL (multi-day)
  - Depends: Item numbers that must complete first, or "—"
  - Status: ☐ todo | 🔄 in progress | ⏳ blocked | ✅ done | ⊘ dropped
  - Source: Where the need was identified (session numbers, review findings)

  Keep item descriptions concise — one line. If more detail is needed,
  reference a task file or delivery artifact.

  Convert high-priority items to task files via /mae-plan when ready.
-->

---

## Milestone M01: {Theme} ({target version})

{One-line description of this milestone's goal.}

| # | Item | Priority | Effort | Depends | Status | Task | Source |
|---|------|----------|--------|---------|--------|------|--------|
| M01.01 | **{Item name — concise but descriptive enough to stand alone}** | P0 | S | — | ☐ todo | — | {session/review} |
| M01.02 | **{Item name}** | P1 | M | M01.01 | ☐ todo | — | {source} |

**Done when:** {One-line definition of done for this milestone.}

---

## Milestone M02: {Theme} ({target version})

{One-line description.}

| # | Item | Priority | Effort | Depends | Status | Task | Source |
|---|------|----------|--------|---------|--------|------|--------|
| M02.01 | **{Item name}** | P1 | M | — | ☐ todo | — | {source} |

**Done when:** {Definition of done.}

---

## Future (post {version})

| # | Item | Priority | Effort | Depends | Status | Source |
|---|------|----------|--------|---------|--------|--------|
| F.1 | **{Item name}** | P3 | L | {dependency} | ☐ todo | {source} |

---

## How to Use

This roadmap is maintained by `/mae-plan`. When ready to implement a milestone:

1. Run `/mae-plan` to enrich the milestone with execution notes and generate task files
2. Execute with `/mae-do` — status updates automatically
3. Run `/sync` at end of session to reconcile status

Milestones are not strictly sequential — items within a milestone can be picked independently.
P0 items should be addressed before feature work.
