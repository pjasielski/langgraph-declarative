# /mae-design — Technical Architecture

Design the technical solution. Works at three levels of granularity, top-down and iterative.

## Modes

### Full solution (no arguments)
```
/mae-design
```
Reads PRD.md. Generates SDD.md using `templates/sdd.md` as structure:
- Core sections (1-6) always included
- Optional sections (7-11) included when relevant — omit if not applicable
- Architecture overview (system boundaries, high-level flow)
- Component list (names, responsibilities, interfaces)
- Tech stack (language, frameworks, databases, infra)
- Data model (entities, relationships)
- Source structure (directories, key files)
- Open design questions

### Component detail
```
/mae-design {component_name}
```
Adds detailed specs for one component to SDD.md:
- API contracts (endpoints, request/response schemas)
- Internal architecture (modules, data flow)
- Error handling strategy
- Dependencies on other components
- Acceptance criteria

### File-level spec
```
/mae-design {path/to/file}
```
Generates implementation specs for a specific file:
- Function signatures with types
- Business logic rules
- Edge cases and error scenarios
- Test scenarios

## Prerequisites
- Full solution: `delivery/02-prd/PRD.md` must exist
- Component: `delivery/03-design/SDD.md` must exist (run full first)
- File-level: SDD.md with relevant component section

## Behavior

1. **Read inputs (prioritized):**
   - `delivery/02-prd/PRD.md` (requirements — primary input)
   - `delivery/01-explore/` — final explore report, especially Technical Analysis sections (3.1-3.4: current state, data landscape, integrations, constraints)
   - If many files in explore folder: read the final report; ask user which others to include
   - `delivery/03-design/SDD.md` (if exists — for component/file-level modes)
   - `DECISIONS.md` (confirmed technical decisions)
   - `maestro.toml` (project context, user profile, tech preferences if configured)
   - `templates/sdd.md` (output structure for full solution mode)

2. **Technical questionnaire (full solution mode only):**
   Before generating the SDD, identify technical decisions the agent cannot make from available information:

   ```markdown
   ## Technical Decisions Needed

   ### Must Answer (blocks architecture)
   1. {decision} — why it's needed, what it blocks

   ### Recommend (I have a suggestion — confirm or override)
   2. {decision} — recommendation: {X} because {rationale}. Agree?

   ### Your Call (multiple valid approaches)
   3. {decision} — options: {A} vs {B}, trade-offs: {comparison}
   ```

   Present the questionnaire to the user. Once answered, generate the SDD incorporating the responses.
   If all decisions can be made from available information, skip the questionnaire and state the rationale for each choice in the SDD.

3. **Generate or extend SDD.md** (iterative — each invocation adds to it)

4. **Save SDD draft to session folder** (numbered file)

5. **Offer promotion:** "SDD draft saved to session. Ready to promote to delivery/03-design/SDD.md?"
   - If user confirms → copy to `delivery/03-design/SDD.md`
   - If user wants changes → iterate in session first
   - If user says "save directly to delivery" in the original prompt → skip the ask
   - For component/file-level: update the existing SDD.md in delivery/ (with review)

6. **Save report** to session folder

## Cross-Phase Awareness

If the design process reveals missing information:
- Suggest: "This design decision requires information we don't have. Consider running `/mae-explore {topic}` to investigate."
- Flag in the SDD with `GAP:` tag so it's visible in reviews
- Do not invent technical decisions when information is insufficient — ask or flag

## Output Behaviors
- Compare alternatives when multiple approaches exist (table format)
- State recommendation with rationale for every design choice
- List trade-offs explicitly
- Flag decisions needing user input vs agent-decidable
- Include source structure section (for later `/mae-do` scaffolding task)
- When user profile indicates technical expertise, offer lighter explanations; when non-technical, explain trade-offs in plain terms

## Direction
Top-down: architecture → components → files. The PRD drives the architecture.

## File Size
- Target: 2,000-4,000 words
- Hard max: 6,000 words
- If exceeding, split: SDD.md (overview) + component-{name}.md per component
