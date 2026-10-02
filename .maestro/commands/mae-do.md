# /mae-do — Execute a Task

Universal task executor. Handles code, docs, config — whatever the task requires.

## Arguments
- `/mae-do` — no args: smart task suggestion
- `/mae-do {task-id}` — execute one task (`M01.03`, `task-003`)
- `/mae-do {milestone}` — execute **every** todo task in a milestone (`M01`)
- `/mae-do poc` — execute the whole PoC milestone from `docs/02-poc/POC.md`
- `/mae-do all` — execute every todo task in the roadmap
- `/mae-do "{description}"` — ad-hoc task (not from plan)
- `/mae-do path/to/file.md` — read task/prompt from file (treats file contents as task description; `/mae-do docs/02-poc/POC.md` is equivalent to `/mae-do poc`)
- `/mae-do issue-{NNN}` — fix a reported issue from `docs/09-maintenance/issues/`

## Task Sources

Resolve the task list from the first of these that exists:

1. `docs/04-plan/tasks/` — individual task files (full track)
2. `docs/04-plan/ROADMAP.md` § milestone tables
3. **`docs/02-poc/POC.md` § 4 Roadmap** — the PoC track, where tasks are table rows rather than files

On the PoC track there are no task files. Status lives in the POC.md roadmap table's Status column, and the audit trail is the per-task session report plus § 6 Current State.

## Multi-Task Execution (`M01`, `poc`, `all`)

When the argument names a milestone rather than a single task:

1. **Resolve the task list** and order it by the dependency graph (respect the `Depends on` column; where the roadmap names a critical path, follow it).
2. **Confirm before starting:** "M01 has N todo tasks: [list IDs + titles]. Estimated scope: {S/M/L counts}. Execute all in sequence?" Never auto-start a multi-task run.
3. **Execute each task** through the normal Execution Flow below.
4. **After every task**, update the status column *and* § 6 Current State in POC.md before starting the next one. Do not batch these to the end — an interrupted run must leave an accurate record of what completed.
5. **Stop on first failure.** Report which task failed, why, and what state the work is in. Do not continue past a failure on the assumption it was cosmetic.
6. **Report at the end:** tasks completed, tasks skipped, verification results, and what remains.

If the milestone defines a **spine** (see `.maestro/templates/poc.md`), build the spine tasks first and confirm the end-to-end path works before starting anything outside it.

## Smart Task Suggestion (no arguments)

When invoked without arguments, suggest work in this priority order:

1. **Conversation context** — if the previous exchange implied work:
   "You were discussing X. Should I work on that?"

2. **Planned tasks** — check the task sources above for the next `todo` task:
   "Next task: M01.03 — Set up database schema [M] [high]. Proceed?"
   If a PoC milestone has several todo tasks, also offer: "…or `/mae-do poc` to run all N."

3. **Open issues** — check `docs/09-maintenance/issues/` for open bugs:
   "There are N open issues (M critical). Want to fix one?"

4. **Open questions** — check OPEN_QUESTIONS.md:
   "There are N open questions. Want to address one?"

5. **Fallback:** "What would you like me to do?"

**Rules:**
- Never auto-execute. Always confirm with the user first.
- Show 2-3 options max, not the entire backlog.
- If suggesting from plan, show title + one-line description.

## Execution Flow

1. **Load task** (from a task source above, or ad-hoc description)
2. **Load context** (referenced files only — minimal):
   - Full track: task file + referenced DESIGN.md section + source files
   - PoC track: `docs/02-poc/POC.md` — read it once and keep it; it contains requirements, design, and roadmap in one file
   - Ad-hoc: relevant files based on description
3. **Update task status** to `in-progress`
4. **Execute** the work
5. **Verify** (run checks, lint, tests if applicable)
6. **Update task status** to `done` (with completion date)
7. **Update roadmap status** — set the Status column to ✅ in whichever source owns the task: `docs/04-plan/ROADMAP.md` or `docs/02-poc/POC.md` § 4
8. **Update § 6 Current State** (PoC track) — done / in progress / next / blocked
9. **Save report** to session folder (or promote to `docs/05-implementation/` if substantial)
10. **Update `_summary.md`** → Tasks Touched section

## Output Behaviors
- Report what was done clearly
- Flag issues found during execution
- Show verification results
- Suggest next task if sequential dependency exists

## Skip When
- No planned tasks exist and no ad-hoc work is needed — nothing to do

## Special: Source Code Scaffolding
When executing the scaffolding task (typically the first task in M01):
- Read `docs/03-design/DESIGN.md` § Tech Stack and § Source Structure — or, on the PoC track, `docs/02-poc/POC.md` § 3 Design
- Create directory tree, package files, config files
- Show both `pip` and `uv` install commands

## Special: PoC / Prototype
`/mae-do` can be used at any point to build a quick proof of concept — even before requirements are fully defined. This is encouraged when:
- The user wants to validate direction before investing in full requirements
- A visual prototype would help stakeholders understand the vision
- Technical feasibility needs to be tested early

```
/mae-do "build a PoC for the dashboard visualization"
/mae-do "create an HTML prototype of the main workflow"
```

After a PoC, the user can return to `/mae-explore` with new insights and continue the delivery process with better understanding.
