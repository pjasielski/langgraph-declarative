# /mae-do — Execute a Task

Universal task executor. Handles code, docs, config — whatever the task requires.

## Arguments
- `/mae-do` — no args: smart task suggestion
- `/mae-do task-{NNN}` — execute a specific planned task
- `/mae-do "{description}"` — ad-hoc task (not from plan)
- `/mae-do issue-{NNN}` — fix a reported issue from `delivery/08-maintenance/issues/`

## Smart Task Suggestion (no arguments)

When invoked without arguments, suggest work in this priority order:

1. **Conversation context** — if the previous exchange implied work:
   "You were discussing X. Should I work on that?"

2. **Planned tasks** — check `delivery/04-plan/tasks/` for next `todo` task:
   "Next task: task-003 — Set up database schema [M] [high]. Proceed?"

3. **Open issues** — check `delivery/08-maintenance/issues/` for open bugs:
   "There are N open issues (M critical). Want to fix one?"

4. **Open questions** — check OPEN_QUESTIONS.md:
   "There are N open questions. Want to address one?"

5. **Fallback:** "What would you like me to do?"

**Rules:**
- Never auto-execute. Always confirm with the user first.
- Show 2-3 options max, not the entire backlog.
- If suggesting from plan, show title + one-line description.

## Execution Flow

1. **Load task** (from plan file or ad-hoc description)
2. **Load context** (referenced files only — minimal):
   - Planned task: task file + referenced SDD section + source files
   - Ad-hoc: relevant files based on description
3. **Update task status** to `in-progress` (if planned)
4. **Execute** the work
5. **Verify** (run checks, lint, tests if applicable)
6. **Update task status** to `done` (if planned, with completion date)
7. **Save report** to session folder
8. **Update `_summary.md`** → Tasks Touched section

## Output Behaviors
- Report what was done clearly
- Flag issues found during execution
- Show verification results
- Suggest next task if sequential dependency exists

## Special: Source Code Scaffolding
When executing the scaffolding task (typically task-001):
- Read `delivery/03-design/SDD.md` § Tech Stack and § Source Structure
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
