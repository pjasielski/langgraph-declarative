# /mae-plan — Plan & Roadmap

Own the roadmap lifecycle. Create milestones, enrich them with execution details, generate task files.

$ARGUMENTS — optional: milestone number, "roadmap", or specific items

## Usage

```
/mae-plan                    → smart default: create roadmap or enrich next milestone
/mae-plan roadmap            → create or update the full roadmap
/mae-plan {milestone}        → enrich a specific milestone with execution notes + tasks
/mae-plan {item numbers}     → generate task files for specific roadmap items
```

## Prerequisites
- `docs/03-design/DESIGN.md` must exist (architecture informs the plan)
- `docs/02-requirements/REQUIREMENTS.md` should exist (requirements inform priorities)
- If neither exists: warn and suggest running `/mae-design` first

## Behavior

### Create Roadmap (no roadmap exists)

1. **Read inputs:**
   - `docs/03-design/DESIGN.md` (components, tech stack, architecture)
   - `docs/02-requirements/REQUIREMENTS.md` (requirements, epics, priorities)
   - `DECISIONS.md` (confirmed decisions)
   - `.maestro/templates/roadmap.md` (output structure)

2. **Generate `docs/04-plan/ROADMAP.md`:**
   - Group work into milestones by theme (foundation, features, polish, etc.)
   - Each milestone gets a version target, description, and item table
   - Items include: priority, effort estimate, dependencies, status (☐ todo)
   - Include "Done when" definition for each milestone

3. **Save report** to session folder

### Enrich Milestone (roadmap exists)

1. **Read inputs:**
   - `docs/04-plan/ROADMAP.md` (the milestone to enrich)
   - `docs/03-design/DESIGN.md` (architecture details)
   - Existing tasks in `docs/04-plan/tasks/` (avoid duplicates)

2. **Add execution notes** to the milestone section in ROADMAP.md:
   ```markdown
   ### Execution Notes
   **Dependency graph:**
     1.1 → 1.3 → 1.5
     1.2, 1.4 can run in parallel

   **Critical path:** 1.1 → 1.7
   **Parallelizable:** 1.2, 1.4, 1.6
   ```

3. **Generate task files** directly in `docs/04-plan/tasks/`:
   - One file per task: `M{MM}.{NN}-{slug}.md` (e.g., `M03.01-skill-spike.md`) — the ID matches the ROADMAP `#` column exactly; sub-tasks append a letter (`M03.01a-…`)
   - Using `.maestro/templates/task.md` format (ID + Milestone fields filled)
   - Add a link to the new task file in the ROADMAP item's Task column

4. **Save report** to session folder

### Update Roadmap

When invoked with `roadmap` argument on an existing roadmap:
- Re-read requirements and design for changes
- Suggest additions, removals, or reprioritizations
- Show proposed changes for review before applying

## Output Behaviors
- Flag dependencies and blockers
- Estimate effort (S/M/L/XL) for each task
- Group tasks by component or phase
- Identify tasks that can run in parallel
- Status column uses: ☐ todo | 🔄 in progress | ⏳ blocked | ✅ done | ⊘ dropped

## Why tasks go directly to docs/
Task files are immediately actionable — they ARE the plan. Saving drafts to .sessions/ adds friction with no safety benefit since tasks are small, easily edited, and meant to be picked up by `/mae-do`.

## Skip When
- Project is simple enough to go straight from design to `/mae-do`
- Only one milestone of work — roadmap adds overhead without value
- Building a PoC — just use `/mae-do` directly

## Task Statuses
`todo` → `in-progress` → `done` (or `blocked`)
