# PoC — {project}

**Status:** {draft | active | complete} · **Generated:** {date} · **Source:** {explore report / reference material}

## 1. Scope

**Problem:** {2–3 sentences — what is broken or missing, and why it matters}

**In scope:**
- {bullet}

**Non-goals:** *(what we are deliberately not building)*
- {bullet}

**Done when:** {one sentence defining PoC success — concrete enough to demo}

## 2. Requirements

| #  | Requirement          | Priority | Verified by       |
| -- | -------------------- | -------- | ----------------- |
| R1 | {testable statement} | MUST     | {how you'd check} |
| R2 | {testable statement} | SHOULD   | {how you'd check} |

Priorities: MUST (PoC fails without it) / SHOULD (expected, cuttable under pressure) / WON'T (explicitly deferred).

## 3. Design

**Architecture:** {diagram, or 3–5 sentences on the shape of the system}

**Components:**

| Component | Responsibility  | Interface  |
| --------- | --------------- | ---------- |
| {name}    | {one sentence}  | {in → out} |

**Stack:** {language, key libraries, and why each earns its place}

**Data model:** {entities and their shape}

**Key decisions:**

| Decision | Chosen | Rejected | Why |
| -------- | ------ | -------- | --- |
| {area}   | {what} | {what}   | {reasoning} |

## 4. Roadmap — M01

| #      | Task   | Effort | Depends on | Done when   | Status |
| ------ | ------ | ------ | ---------- | ----------- | ------ |
| M01.01 | {task} | S/M/L  | —          | {criterion} | ☐      |
| M01.02 | {task} | S/M/L  | M01.01     | {criterion} | ☐      |

**Critical path:** M01.01 → M01.02 → …
**Parallelizable:** {IDs that don't block each other}

**Spine:** {the narrowest end-to-end path — the thing that must work before anything is broadened}
**Cut order if behind:** {first to drop} → {next} → {next}. Never cut: {non-negotiables}.

## 5. Risks & Assumptions

| Risk / Assumption | Impact | Mitigation |
| ----------------- | ------ | ---------- |
| {statement}       | {what breaks} | {what you'd do} |

Mark inferences you could not verify as `ASSUMPTION` and name the task that confirms them.

## 6. Current State

> Rehydration key — a fresh session reads this section to know where things stand. `/mae-do` keeps it current.

**Done:** {task IDs, or "none"}
**In progress:** {task ID + what specifically, or "none"}
**Next:** {task ID}
**Blocked:** {task ID + reason, or "none"}
**Notes:** {anything a fresh session would otherwise have to rediscover}
