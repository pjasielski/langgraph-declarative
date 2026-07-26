# /mae-review — Review Code or Documentation

Review existing code or delivery artifacts for quality, consistency, and completeness.

## Arguments

- `/mae-review` — review recent changes (git diff)
- `/mae-review {path}` — review a specific file or directory
- `/mae-review requirements` or `design` — review a delivery artifact by name

## Behavior

1. **Determine scope:**

   - No args: review uncommitted changes (git diff + untracked)
   - Path: review specified file(s)
   - Artifact name: review the delivery artifact
2. **Load reference material:**

   - For code: DESIGN.md (architecture), coding standards
   - For requirements: explore artifacts, DECISIONS.md
   - For design: REQUIREMENTS.md (does design match requirements?)
3. **Generate review** using `.maestro/templates/review.md` structure, findings categorized:

   - 🔴 **Critical** — must fix (security, correctness, data loss risk)
   - 🟡 **Important** — should fix (consistency, maintainability, performance)
   - 🟢 **Suggestion** — nice to have (style, naming, documentation)
4. **Cross-reference** with canonical artifacts:

   - Code matches DESIGN.md? Flag `DRIFT:` if not.
   - DESIGN.md matches REQUIREMENTS.md? Flag `CONSISTENCY:` if not.
5. **Save report** to session folder
6. **On-demand folder:** If creating `docs/06-review/` for the first time, offer to create it.

## Output Behaviors

- List findings by severity
- Quote the specific code/text being reviewed
- Suggest concrete fixes, not just "improve this"

## Skip When
- No changes to review — nothing new since last review
- Quick one-off fix that doesn't warrant formal review

## What Review Is NOT

- Not a gate or approval process
- Not automated testing
- It's the agent's analysis and suggestions for the user to consider
