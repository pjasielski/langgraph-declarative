# /mae-review — Review Code or Documentation

Review existing code or delivery artifacts for quality, consistency, and completeness.

## Arguments

- `/mae-review` — review recent changes (git diff)
- `/mae-review {path}` — review a specific file or directory
- `/mae-review prd` or `sdd` — review a delivery artifact by name

## Behavior

1. **Determine scope:**

   - No args: review uncommitted changes (git diff + untracked)
   - Path: review specified file(s)
   - Artifact name: review the delivery artifact
2. **Load reference material:**

   - For code: SDD.md (architecture), coding standards
   - For PRD: explore artifacts, DECISIONS.md
   - For SDD: PRD.md (does design match requirements?)
3. **Generate review** using `templates/review.md` structure, findings categorized:

   - 🔴 **Critical** — must fix (security, correctness, data loss risk)
   - 🟡 **Important** — should fix (consistency, maintainability, performance)
   - 🟢 **Suggestion** — nice to have (style, naming, documentation)
4. **Cross-reference** with canonical artifacts:

   - Code matches SDD? Flag `DRIFT:` if not.
   - SDD matches PRD? Flag `CONSISTENCY:` if not.
5. **Save report** to session folder
6. **On-demand folder:** If creating `delivery/05-review/` for the first time, offer to create it.

## Output Behaviors

- List findings by severity
- Quote the specific code/text being reviewed
- Suggest concrete fixes, not just "improve this"

## What Review Is NOT

- Not a gate or approval process
- Not automated testing
- It's the agent's analysis and suggestions for the user to consider
