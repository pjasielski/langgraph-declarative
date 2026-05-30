# /mae-plan — Create Implementation Plan

Break the design into actionable tasks.

## Prerequisites
- `delivery/03-design/SDD.md` must exist
- If missing: warn and suggest running `/mae-design` first

## Behavior

1. **Read inputs:**
   - `delivery/03-design/SDD.md` (and component files if split)
   - `delivery/02-prd/PRD.md` (for acceptance criteria)
   - Existing tasks in `delivery/04-plan/tasks/` (avoid duplicates)

2. **Generate PLAN.md** in `delivery/04-plan/`:
   - Overview (total tasks, effort estimate)
   - Task dependency graph (which tasks block which)
   - Suggested execution order
   - Risk items

3. **Generate task files** directly in `delivery/04-plan/tasks/`:
   - One file per task: task-001.md, task-002.md, etc.
   - Using `templates/task.md` format
   - First task should be "Scaffold source code structure" (reads SDD tech stack)

4. **Save report** to session folder

## Why tasks go directly to delivery/
Task files are immediately actionable — they ARE the plan. Saving drafts to sessions/ adds friction with no safety benefit since tasks are small, easily edited, and meant to be picked up by `/mae-do`.

## Output Behaviors
- Flag dependencies and blockers
- Estimate effort (S/M/L/XL) for each task
- Group tasks by component or phase
- Identify tasks that can run in parallel
- If tasks already exist, continue from highest number

## Task Statuses
`todo` → `in-progress` → `done` (or `blocked`)
