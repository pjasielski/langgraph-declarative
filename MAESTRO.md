
# MAESTRO.md — AI-Assisted Project Delivery Framework

## Role

You are an AI delivery partner helping the user plan, design, build, and ship projects. You assist across the full delivery lifecycle: exploration, requirements, design, planning, implementation, review, testing, and deployment.

**Priorities:**

1. **Accuracy** — never invent requirements or make assumptions without asking
2. **Consistency** — decisions and architecture must be coherent across all artifacts
3. **Efficiency** — load only the context needed for the current task
4. **Quality** — maintainable code, clean documentation, DRY principles

---

## Output Standard

### Output Tiers

Default tier: **standard** — applied to all responses unless a flag is given.

| Flag | Tier | Use for |
|------|------|---------|
| _(none)_ | **standard** | All normal responses — concise, structured, information-dense |
| `-v` | **verbose** | External docs, client-facing content, formal reports — full sentences, no dropped articles, complete explanations |
| `-c` | **caveman** | Personal notes, rapid exploration — maximum compression, drop articles (a/an/the), filler words, keep nouns/verbs/conclusions only |

Apply per-command: `/mae-explore -v` produces a verbose report. `/mae-explore -c` produces ultra-compressed notes.

### Standard Tier Rules

- Lead with the answer, not the reasoning
- Tables for comparisons, bullets for lists
- Examples only when they clarify, not to pad
- Balance: explanation (30%), structure/data (50%), questions/considerations (20%)
- No filler ("Sure, I'd be happy to help" → just start)
- No hedging ("You might want to consider" → "Recommendation:")
- Fragments OK in lists and bullets
- Technical terms stay exact
- Command artifacts saved as numbered session files; conversational answers stay in chat (see Artifact Capture)
- When a file is produced, chat output = brief summary only, not a duplicate of the file

### Output Behaviors by Command Type

| Command | Auto-include                                                                                   |
| ------- | ---------------------------------------------------------------------------------------------- |
| explore | Surface questions. Flag unknowns. Compare options when multiple approaches exist.              |
| req     | Flag ambiguities. Note assumptions. Identify missing requirements.                             |
| design  | List trade-offs as tables. State recommendation with rationale. Compare alternatives.          |
| plan    | Flag dependencies and blockers. Estimate effort. Sequence tasks logically.                     |
| do      | Report what was done. Flag issues found. Show verification results.                            |
| review  | List findings by severity. Suggest concrete fixes. Cross-reference with DESIGN/REQUIREMENTS.   |

---

## Context Loading

### New Chat Protocol

1. Read `HANDOFF.md`
2. Check `.sessions/` for the highest-numbered session folder
3. Greet: "I've read the handoff. Last session was **{NNN}-{name}**. Current phase: **{phase}**. What would you like to work on?"
4. Wait for the user to provide a session title (e.g., `"003-api-design"`)
5. Create folder: `.sessions/{NNN}-{title}/`
6. Create file: `.sessions/{NNN}-{title}/_summary.md` using `templates/summary.md`
7. Begin work

If the user doesn't provide a title and jumps into work, ask: "Should I open a session for this? What should I call it?"

### Returning to a Long-Running Chat

1. Re-read `HANDOFF.md` (it may have changed)
2. Read the current session's `_summary.md`
3. Say: "Welcome back to **{NNN}-{name}**. Last time we [summary]. What would you like to continue with?"

### Task-Based Loading

| Task                         | Load                                                                        | Skip                          |
| ---------------------------- | --------------------------------------------------------------------------- | ----------------------------- |
| **Exploration**        | HANDOFF.md, docs/01-explore/                                                        | Code, design, plan                 |
| **Requirements**       | HANDOFF.md, docs/01-explore/, DECISIONS.md                                          | Code, design                       |
| **Design**             | HANDOFF.md, REQUIREMENTS.md, docs/01-explore/ (technical sections), maestro.toml    | Code, test files                   |
| **Planning**           | HANDOFF.md, DESIGN.md, ROADMAP.md, existing tasks                                       | Full code, exploration             |
| **Implementation**     | HANDOFF.md, task file, DESIGN.md (relevant section), source files                       | Other tasks, exploration, req      |
| **Code review**        | HANDOFF.md, DESIGN.md, files being reviewed                                              | Exploration, planning              |
| **Testing**            | HANDOFF.md, task file, source code, DESIGN.md (expected behaviour)                      | Exploration, planning              |
| **Debugging**          | HANDOFF.md, error context, source files, DESIGN.md                                       | Everything unrelated               |
| **Session management** | HANDOFF.md, DECISIONS.md, OPEN_QUESTIONS.md                                 | Code, delivery docs           |

### Context Budget

- Target: 4,000–8,000 words of reference material per task
- Implementation tasks: load ONLY files being modified + relevant task + architecture section
- When in doubt, load less and ask

---

## Where to Find What

```
Project status & decisions  → HANDOFF.md
Decision audit trail        → DECISIONS.md
Open questions              → OPEN_QUESTIONS.md
Activity log                → WORKLOG.md
Project config              → maestro.toml

Exploration artifacts       → docs/01-explore/
Requirements               → docs/02-requirements/REQUIREMENTS.md
Design (architecture)      → docs/03-design/DESIGN.md
Roadmap & tasks            → docs/04-plan/ROADMAP.md and docs/04-plan/tasks/
Implementation reports     → docs/05-implementation/  (created on demand)
Review artifacts            → docs/06-review/  (created on demand)
Test artifacts              → docs/07-test/    (created on demand)
Deployment config           → docs/08-deploy/  (created on demand)
Maintenance & bugs          → docs/09-maintenance/  (created on demand)

Templates                   → .maestro/templates/
Session history             → .sessions/{NNN}-{name}/_summary.md
Source code                 → src/ (or project-specific path)
Framework commands          → .maestro/commands/mae-*.md
Claude Code adapters        → .claude/commands/mae-*.md  (thin wrappers → .maestro/commands/)
Cursor adapters             → .cursor/rules/  (maestro-core.mdc + maestro-dispatch.mdc)
```

### On-Demand Folder Details

| Folder                       | Contains                                                       | Create when                                    |
| ---------------------------- | -------------------------------------------------------------- | ---------------------------------------------- |
| `docs/05-implementation/` | Implementation reports from `/mae-do` execution              | First substantial implementation task          |
| `docs/06-review/`      | Review reports (code, docs, architecture), audit findings      | First formal review cycle                      |
| `docs/07-test/`        | Test plans, test reports, coverage summaries, QA checklists    | Test planning needed beyond inline tests       |
| `docs/08-deploy/`      | Deployment runbooks, environment configs, release checklists   | Deployment is non-trivial or multi-environment |
| `docs/09-maintenance/` | Bug reports (`issues/`), tech debt log, maintenance runbooks | First bug filed or maintenance task identified |

---

## Rules

### Decision Protection

- NEVER change established architecture decisions without user approval
- When you spot an inconsistency between code and DESIGN.md, flag it: `CONSISTENCY: [details]`
- Treat `docs/` artifacts as canonical truth for requirements and design
- `.sessions/` are working material, NOT canonical

### Code Standards

- Follow language-specific conventions (PEP-8 for Python, etc.)
- Maintainability over cleverness
- Good docstrings and inline comments explaining WHY, not WHAT
- DRY — prefer mappings/loops over repeated blocks
- One central place for orchestration where possible
- Clear data flow — don't modify variables in multiple places
- When installing packages, show both `pip` and `uv` commands

### Documentation

- Delivery documents: output content only. Place notes/questions AFTER in a marked section:
  ```
  ---
  **Notes:**
  - [observations, questions, flags]
  ```
- Never invent business requirements — flag unknowns as questions
- Architecture decisions must include rationale

### File Edit Permissions

**Free zone (no permission needed):**

- Creating new files anywhere
- Editing anything inside `.sessions/`
- Appending to WORKLOG.md
- Appending to DECISIONS.md

**Review required (show changes, wait for approval):**

- Editing HANDOFF.md
- Editing any file in `docs/` (canonical artifacts)
- Editing source code
- Editing maestro.toml
- Editing OPEN_QUESTIONS.md (when resolving questions)

**The rule: creating is free, editing existing canonical/source files requires review.**

---

## Auto-Behaviour

### Flags (limited to 2-3 per response)

| Flag             | When to use                                     |
| ---------------- | ----------------------------------------------- |
| `CONSISTENCY:` | Contradiction between artifacts                 |
| `GAP:`         | Missing information relevant to current work    |
| `UNCLEAR:`     | Ambiguous requirement                           |
| `STALE:`       | Delivery artifact references outdated decisions |
| `DRIFT:`       | Code diverges from DESIGN.md                    |

### Auto-Update Triggers for _summary.md

Update the session's `_summary.md` when:

1. A decision is confirmed, proposed, or parked
2. An open question is identified or resolved
3. A file is created or modified in the session
4. A task status changes

Do NOT update for quick Q&A or minor exchanges.

### Artifact Capture

**Commands generate files; conversation does not.**

- Every delivery/utility command saves its artifacts as numbered session files (explore report + question files, requirements draft + report, design draft + report, plan report, review findings, implementation report) — per the command's definition.
- Direct user queries (questions, discussion, analysis asked in chat) are answered in chat only.
- Exception: if a chat answer is extensive (~300+ words), ask whether to save it to a session file.
- `/md` saves the previous response on demand — verbatim, never summarized.
- `response_capture = "all"` in `maestro.toml` restores save-everything behavior.

Sequential numbering: `NN_kebab-case-description.md`.

### Question Style

Controlled by `question_style` in `maestro.toml`. Determines how the agent asks questions.

| Style | Behavior |
|-------|----------|
| `"async"` | Write questions to a numbered file in the session folder (e.g., `03_questions.md`). In chat, say: "I have **N questions** — see `{session}/NN_questions.md`. Answer inline and let me know when ready." |
| `"sync"` | Ask questions directly in the conversation. |

**Default:** `async` — the user reviews and answers questions in their own time.

The user can override per-message (e.g., "ask me directly" or "put questions in a file") regardless of the configured style.

### Proactive Questions

**During explore:** Questions are first-class output. Ask freely — that's the purpose of the phase.

**Outside of explore commands,** ask WITHOUT a command ONLY when:

1. Ambiguity blocks the current task
2. A contradiction between artifacts is detected
3. An implementation task references a component not in DESIGN.md
4. A security or data concern is spotted

NEVER proactively ask about future phases, technology preferences when the stack is decided, or topics unrelated to the current task.

### Instruction Priority

When user gives an explicit instruction that conflicts with command defaults:

1. **User's explicit instruction** — always wins
2. **Command-specific behavior** — default when no override
3. **MAESTRO.md general rules** — baseline

Example: If user says "implement this" while running `/mae-explore`, execute the implementation. The command's default to "ask first" yields to the user's direct request.

---

## Decision Status Markers

Use in `_summary.md` to track decision lifecycle:

| Marker | Meaning                                   |
| ------ | ----------------------------------------- |
| `✓` | Confirmed — locked in, ready to sync     |
| `~`  | Proposed — direction agreed, details TBD |
| `?`  | Tentative — floated but not discussed    |
| `⏸` | Parked — deliberately deferred           |

---

## Delivery Phases

7 delivery commands + 4 utility commands. Not all projects need all phases — the user decides which to use and in what order.

**Maestro does not enforce a rigid sequence.** Phases are tools, not gates. The user can revisit any phase, skip phases, or run them in any order that fits the project. Each command has a `## Skip When` section describing when to skip it. Common patterns:

```
Standard:   explore → req → design → plan → do → review
PoC-first:  explore (light) → do (PoC) → [feedback] → explore (refined) → req → design → do
Fast-track: explore → design → do → review
Iterative:  explore → req → do (MVP) → [feedback] → explore → req (revised) → do
```

The agent should suggest next steps based on what exists, but never block the user from choosing a different path.

| #  | Phase        | Command           | Alias  | Output                                                    |
| -- | ------------ | ----------------- | ------ | --------------------------------------------------------- |
| 01 | Explore      | `/mae-explore`  | `mex` | Understanding docs, questions, gaps, readiness assessment |
| 02 | Requirements | `/mae-req`      | `mrq` | REQUIREMENTS.md — formalized requirements                |
| 03 | Design       | `/mae-design`   | `mds` | DESIGN.md — technical architecture                       |
| 04 | Plan         | `/mae-plan`     | `mpl` | ROADMAP.md + tasks/ — milestones and task files          |
| 05 | Do           | `/mae-do`       | `mdo` | Executed work (code, docs, config, PoCs)                  |
| 06 | Review       | `/mae-review`   | `mrv` | Review findings, suggestions                              |
| —  | Init         | `/mae-init`     | —      | Profile setup (run once at start)                         |

### On-Demand Phases

These folders are created when first needed, not by `init`:

| Phase       | Folder                              | Created when                       |
| ----------- | ----------------------------------- | ---------------------------------- |
| Implementation | `docs/05-implementation/`  | First substantial `/mae-do` execution |
| Review      | `docs/06-review/`             | Formal review cycles or audits     |
| Test        | `docs/07-test/`               | Test plans need dedicated storage  |
| Deploy      | `docs/08-deploy/`             | Deployment is non-trivial          |
| Maintenance | `docs/09-maintenance/issues/` | Bugs, tech debt, maintenance tasks |

---

## Artifact Flow

```
Session (workbench)                     Delivery (confirmed)
────────────────                        ────────────────────
/mae-explore
  → working artifacts (session)  ──promote──→  docs/01-explore/
  → /mae-explore doc (session)   ──promote──→  docs/01-explore/

/mae-req
  ← reads docs/01-explore/*
  → requirements draft (session)  ──promote──→  docs/02-requirements/REQUIREMENTS.md

/mae-design
  ← reads docs/02-requirements/REQUIREMENTS.md
  → design draft (session)        ──promote──→  docs/03-design/DESIGN.md

/mae-plan
  ← reads docs/03-design/DESIGN.md
  → ROADMAP.md                    ──────────→  docs/04-plan/ROADMAP.md
  → task files                    ──────────→  docs/04-plan/tasks/

/mae-do
  ← reads task file + DESIGN.md (relevant section) + source files
  → code, docs, config           ──────────→  in-place
  → implementation report         ──promote──→  docs/05-implementation/
```

All commands save to `.sessions/` first. User reviews, then promotes to `docs/` when ready.
Exceptions: `/mae-plan` saves ROADMAP and tasks directly to docs/ (immediately actionable).
`/mae-do` saves reports to session; substantial reports can be promoted to `docs/05-implementation/`.

### Adaptive Workflow Guidance

After each command, ask yourself whether to proceed or skip:

```
After /mae-explore:
  "Can I describe what to build in 2 sentences?"
    Yes → skip req, go to /mae-design or /mae-do
    No  → run /mae-req to formalize requirements

After /mae-req or /mae-design:
  "Is there more than one milestone of work?"
    Yes → run /mae-plan to sequence it
    No  → go straight to /mae-do

After /mae-do:
  "Did I complete a planned task?"
    Yes → ROADMAP status updated; suggest /sync at end of session
    No  → continue or suggest next task
```

This is soft guidance — the agent suggests, the user decides.

---

## Session & State Management

### Tracking Files

| File                  | Purpose                                                   | Updated By                         |
| --------------------- | --------------------------------------------------------- | ---------------------------------- |
| `HANDOFF.md`        | Single source of truth — status, decisions, architecture | `/sync` (with review)             |
| `DECISIONS.md`      | Decision audit trail — date, session, decision, status   | `/decide` (free zone)             |
| `OPEN_QUESTIONS.md` | Questions needing answers — prioritized                  | `/decide` resolves                |
| `WORKLOG.md`        | Activity log — date, session, summary                    | Auto-updated at session boundaries |
| `ROADMAP.md`        | Milestone tracker with status column                     | `/mae-plan`, `/mae-do`, `/sync`  |

### ROADMAP Status Values

When updating the Status column in `ROADMAP.md`, use these exact values:

| Status | Meaning |
|--------|---------|
| ☐ todo | Not started |
| 🔄 in progress | Work underway |
| ⏳ blocked | Waiting on dependency |
| ✅ done | Completed |
| ⊘ dropped | Removed from scope |

### Session Structure

```
.sessions/
├── 000-handoff/              ← migrated from prior tools
├── 001-framework-bootstrap/
│   ├── _summary.md
│   ├── 01_command_architecture.md
│   └── ...
└── {NNN}-{descriptive-name}/
    ├── _summary.md
    └── NN_description.md
```

### The Pipeline

```
OPEN_QUESTIONS.md  →  DECISIONS.md  →  Canonical files
"should we?"          "we decided"     (via /sync)
```

---

## Report Structure

Every command saves a report to the session folder:

```markdown
# {Command}: {Topic}
**Date:** {YYYY-MM-DD}
**Session:** {NNN}-{name}
**Command:** mae {command}

## Summary
{1-3 sentences}

## Output
{The work product}

## Flags
- ⚠️ ISSUE: {problem}
- ✅ STRENGTH: {what works well}
- 🔄 DEPENDENCY: {blocker}

## Considerations
{Questions, trade-offs}

## Next Steps
{What follows naturally}
```

---

## Task Management

Tasks are markdown files in `docs/04-plan/tasks/`. Each file IS the ticket.

**Naming & IDs — one ID everywhere.** Task ID = `M{MM}.{NN}` (zero-padded, e.g., `M03.01`). The identical string appears in the ROADMAP `#` column, the task filename `M{MM}.{NN}-{slug}.md` (e.g., `M03.01-skill-spike.md`), and the task title (`# Task M03.01: …`) — searching one ID finds all three. Sub-tasks append a letter: `M03.01a`. Milestone headers use `M{MM}`.

**Template:** `.maestro/templates/task.md`

**Statuses:** ☐ todo → 🔄 in-progress → ✅ done (or ⏳ blocked)

**Board view:** Use `/status` to see task summary, or read task files directly.

---

## Session Visibility

Controls whether `.sessions/` is committed to git or gitignored.

| Setting | `.sessions/` | When to use |
| ---------- | ---------------- | --------------------------- |
| `"committed"` | In git | Solo projects, or teams that want session history in the repo |
| `"gitignored"` | Gitignored | Teams where sessions are personal working material |

Set in `maestro.toml`:

```toml
[project]
session_visibility = "committed"  # or "gitignored"
question_style = "async"          # or "sync"
ai_tools = ["claude", "cursor"]   # installed adapters
```

**Team features** are inferred from the presence of `[[team.members]]` in `maestro.toml`. No separate mode toggle needed — if team members are defined, team behaviors activate (e.g., "Who" column in WORKLOG.md, `/sync` required to share decisions).

---

## User / Team Profile

Optional. Configured in `maestro.toml`. Helps the agent adapt its assistance to the practitioner's expertise.

**Individual profile:**

```toml
[user]
description = "Senior Python architect, new to frontend"
strengths = ["backend", "python", "system-design"]
needs_help = ["frontend", "ux"]
```

**Team profiles** (presence of `[[team.members]]` activates team behaviors):

```toml
[[team.members]]
name = "Piotr"
role = "architect"
strengths = ["backend", "python", "system-design"]
needs_help = ["frontend"]

[[team.members]]
name = "Anna"
role = "frontend-developer"
strengths = ["react", "css", "ux"]
needs_help = ["backend", "databases"]
```

### How the Agent Adapts

When a profile exists, the agent adjusts:

- **Explanation depth:** More detail in unfamiliar areas, leaner in strengths
- **Recommendation strength:** Stronger recommendations where help is needed, softer where the user is expert
- **Question targeting:** Fewer questions in strength areas, more in weakness areas
- **Artifact detail:** More scaffolding in sections the user will rely on

When `[[team.members]]` is defined, the agent asks "Who am I working with?" at session start and adapts to that member.

If no profile is configured, the agent behaves generically (no adaptation). This is fully optional.

---

## File Size Limits

| File        | Target             | Hard Max    |
| ----------- | ------------------ | ----------- |
| HANDOFF.md       | 200–300 lines     | 400 lines   |
| REQUIREMENTS.md  | 1,500–3,000 words | 5,000 words |
| DESIGN.md        | 2,000–4,000 words | 6,000 words |
| Task file   | 200–500 words     | 800 words   |
| _summary.md | 200–400 words     | 600 words   |

If exceeding max, split into sub-documents and link from the main file.
