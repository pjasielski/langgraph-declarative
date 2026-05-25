# /mae-checkpoint — Save Project Checkpoint

Save a named snapshot of current project state for tracking progress over time.

$ARGUMENTS — checkpoint name, or sub-command (list, compare)

## Usage

```
/mae-checkpoint {name}           → save checkpoint with given name
/mae-checkpoint list             → list all checkpoints
/mae-checkpoint compare {a} {b}  → compare two checkpoints
```

If no arguments: prompt for a checkpoint name.

## Behavior

### Save Checkpoint

1. Read current state:
   - `HANDOFF.md` → current phase, status
   - `DECISIONS.md` → count by status (confirmed / proposed / tentative / parked)
   - `OPEN_QUESTIONS.md` → count by priority
   - `delivery/04-plan/tasks/` → count by status (todo / in-progress / done / blocked)
   - `sessions/` → current session name
   - `maestro.toml` → project name

2. Create checkpoint folder if needed: `sessions/{current-session}/checkpoints/`

3. Save checkpoint file: `sessions/{current-session}/checkpoints/{YYYY-MM-DD}_{name}.md`

```markdown
# Checkpoint: {name}
**Date:** {YYYY-MM-DD HH:MM}
**Session:** {NNN}-{name}
**Phase:** {current phase}

## State

| Metric | Value |
|--------|-------|
| Decisions | {N} confirmed, {N} proposed, {N} tentative, {N} parked |
| Open Questions | {N} total ({N} high, {N} medium, {N} low) |
| Tasks | {N} todo, {N} in-progress, {N} done, {N} blocked |
| Delivery artifacts | {list of files in delivery/} |
| Session files | {count} in current session |

## Recent Activity
{Last 3 WORKLOG entries}

## Note
{User-provided note, or auto-generated summary of current focus}
```

4. Report: "Checkpoint **{name}** saved."

### List Checkpoints

Read all checkpoint files across all sessions. Display:

```
CHECKPOINTS
  {date} | {session} | {name} | Phase: {phase} | {D}D {Q}Q {T}T
  ...
```

D = decisions confirmed, Q = questions open, T = tasks done.

### Compare Checkpoints

Read two checkpoint files. Show delta:

```
COMPARE: {a} → {b}
  Phase: {a.phase} → {b.phase}
  Decisions: +{N} confirmed, +{N} proposed
  Questions: +{N} added, -{N} resolved
  Tasks: +{N} done, +{N} added
  New artifacts: {list}
  Time span: {days between}
```

## Rules

- Checkpoint names: kebab-case (e.g., `pre-design`, `mvp-ready`, `sprint-1-end`)
- Same name + same day = overwrite (allows corrections)
- Checkpoints are lightweight — metadata only, not file copies
- Always save to current session's checkpoints/ subfolder
