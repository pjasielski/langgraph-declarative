# Lock In a Decision

Record a decision in DECISIONS.md and optionally resolve an open question.

## Usage

```
/decide [decision description]
```

## Behavior

1. Ask the Architect to confirm the decision if not already clear from context
2. Append one row to `DECISIONS.md`:
   - Date: today
   - Session: current session name
   - Decision: the decision text
   - Status: confirmed (or leaning/rejected if specified)
3. Check `OPEN_QUESTIONS.md` — if this decision resolves a question:
   - Show the question being resolved
   - Ask for approval to update OPEN_QUESTIONS.md (review required)
   - Remove or mark resolved
4. Update the current session's `_summary.md` with the decision

## Rules

- Only record **major decisions** — not every micro-choice
- Include enough context that someone reading DECISIONS.md months later understands what was decided and why
- Do NOT modify canonical files (docs/, HANDOFF.md, ROADMAP.md) — that's what `/sync` is for
