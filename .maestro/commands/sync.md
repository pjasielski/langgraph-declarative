# Sync Decisions to Canonical Files

Batch-update canonical project files based on accumulated decisions.

## Behavior

1. Read the current session's `_summary.md`
2. Find all `✓` confirmed decisions not yet marked `[synced]`
3. Read `DECISIONS.md` — identify entries not yet reflected in canonical files
4. Read `HANDOFF.md` for current state
5. Identify which canonical files need updating:
   - HANDOFF.md (status, architecture decisions table)
   - delivery/ artifacts (if decisions affect requirements/design)
   - CLAUDE.md (if decisions affect conventions/architecture)
   - OPEN_QUESTIONS.md (if decisions resolve open questions)
6. For each file that needs changes:
   - Draft the proposed change
   - Show the change to the user for review
   - Apply only what is approved
7. Mark synced decisions in `_summary.md` (append `[synced]` to ✓ items)
8. Add "Artifact Changes" entry to `_summary.md`:
   ```
   ## Artifact Changes (Sync YYYY-MM-DD)
   - **HANDOFF.md** — updated status and decisions table
   - **DECISIONS.md** — 3 rows appended
   ```
9. Update HANDOFF.md "Recent Changes" section

## Rules

- **Every edit to canonical files requires review** — show diff, wait for approval
- Group related changes for review efficiency
- If a decision contradicts an existing canonical entry, flag the conflict explicitly
- Never auto-apply changes to delivery/ artifacts
- After sync, append a WORKLOG.md entry logging the sync activity
