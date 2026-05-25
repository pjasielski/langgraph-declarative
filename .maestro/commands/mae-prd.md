# /mae-prd — Formalize Requirements

Generate a Product Requirements Document from confirmed explore artifacts.

## Prerequisites
- `delivery/01-explore/` should contain confirmed artifacts (ideally the final explore report)
- If empty: warn and suggest running `/mae-explore` first
- If the explore report contains unresolved `GAP:` or `UNCLEAR:` tags, warn: "The explore report has N unresolved gaps. Consider resolving these first, or I'll flag them in the PRD."

## Behavior

1. **Read inputs (prioritized):**
   - Final explore report in `delivery/01-explore/` (primary input — this is the synthesis)
   - If no final report exists: read all individual explore artifacts (warn if >5 files about context budget)
   - `DECISIONS.md` (relevant prior decisions)
   - `OPEN_QUESTIONS.md` (check for unresolved items affecting requirements)
   - `maestro.toml` (project context, user profile if configured)
   - `templates/prd.md` (output structure)
   - Do NOT read raw sources (docs/, data/) — that's explore's job

2. **Generate PRD.md** using `templates/prd.md` as the structure:
   - Core sections (1-7) always included
   - Optional sections (8-9, Glossary) included when relevant to the project
   - Omit optional sections that don't apply — don't leave empty placeholders
   - Fill in content from explore artifacts, not invented
   - **Section 6 (Epics & User Stories):** populate with concrete user stories derived from requirements in Section 4, grouped into logical epics. Each story must have acceptance criteria.

3. **Save PRD draft to session folder** (numbered file, e.g., `04_prd-draft.md`)

4. **Offer promotion:** "PRD draft saved to session. Ready to promote to delivery/02-prd/PRD.md?"
   - If user confirms → copy to `delivery/02-prd/PRD.md`
   - If user wants changes → iterate in session first
   - If user says "save directly to delivery" in the original prompt → skip the ask

5. **Save report** to session folder

## Output Behaviors
- Flag ambiguities with `UNCLEAR:` tag
- Note assumptions explicitly
- Identify missing requirements
- Cross-reference with explore artifacts

## File Size
- Target: 1,500-3,000 words
- Hard max: 5,000 words
- If exceeding, split into PRD.md + user-stories.md
