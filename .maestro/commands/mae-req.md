# /mae-req — Formalize Requirements

Generate a Requirements Document from confirmed explore artifacts.

$ARGUMENTS — optional: topic focus, flags

## Prerequisites
- `docs/01-explore/` should contain confirmed artifacts (ideally the final explore report)
- If empty: warn and suggest running `/mae-explore` first
- If the explore report contains unresolved `GAP:` or `UNCLEAR:` tags, warn: "The explore report has N unresolved gaps. Consider resolving these first, or I'll flag them in the requirements."

## Behavior

1. **Read inputs (prioritized):**
   - Final explore report in `docs/01-explore/` (primary input — this is the synthesis)
   - If no final report exists: read all individual explore artifacts (warn if >5 files about context budget)
   - `DECISIONS.md` (relevant prior decisions)
   - `OPEN_QUESTIONS.md` (check for unresolved items affecting requirements)
   - `maestro.toml` (project context, user profile if configured)
   - `.maestro/templates/requirements.md` (output structure)
   - Do NOT read raw sources (docs/, data/) — that's explore's job

2. **Generate REQUIREMENTS.md** using `.maestro/templates/requirements.md` as the structure:
   - Core sections (1-7) always included
   - Optional sections (8-9, Glossary) included when relevant to the project
   - Omit optional sections that don't apply — don't leave empty placeholders
   - Fill in content from explore artifacts, not invented
   - **Section 6 (Epics & User Stories):** populate with concrete user stories derived from requirements in Section 4, grouped into logical epics. Each story must have acceptance criteria.

3. **Save draft to session folder** (numbered file, e.g., `04_requirements-draft.md`)

4. **Offer promotion:** "Requirements draft saved to session. Ready to promote to docs/02-requirements/REQUIREMENTS.md?"
   - If user confirms → copy to `docs/02-requirements/REQUIREMENTS.md`
   - If user wants changes → iterate in session first
   - If user says "save directly to docs" in the original prompt → skip the ask

5. **Save report** to session folder

## Output Behaviors
- Flag ambiguities with `UNCLEAR:` tag
- Note assumptions explicitly
- Identify missing requirements
- Cross-reference with explore artifacts

## Skip When
- Project is a single-file tool or script — go straight to `/mae-explore` → `/mae-do`
- Scope is already clear from a prior explore with < 5 requirements — skip to `/mae-design`
- Running in PoC mode — lightweight requirements captured in explore output

## File Size
- Target: 1,500-3,000 words
- Hard max: 5,000 words
- If exceeding, split into REQUIREMENTS.md + user-stories.md
