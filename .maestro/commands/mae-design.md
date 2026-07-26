# /mae-design — Technical Architecture

Design the technical solution. Works at three levels of granularity, top-down and iterative.

## Modes

### Full solution (no arguments)
```
/mae-design
```
Reads REQUIREMENTS.md. Generates DESIGN.md using `.maestro/templates/design.md` as structure:
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
Adds detailed specs for one component to DESIGN.md:
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
- Full solution: `docs/02-requirements/REQUIREMENTS.md` must exist
- Component: `docs/03-design/DESIGN.md` must exist (run full first)
- File-level: DESIGN.md with relevant component section

## Behavior

1. **Read inputs (prioritized):**
   - `docs/02-requirements/REQUIREMENTS.md` (requirements — primary input)
   - `docs/01-explore/` — final explore report, especially Technical Analysis sections (3.1-3.4: current state, data landscape, integrations, constraints)
   - If many files in explore folder: read the final report; ask user which others to include
   - `docs/03-design/DESIGN.md` (if exists — for component/file-level modes)
   - `DECISIONS.md` (confirmed technical decisions)
   - `maestro.toml` (project context, user profile, tech preferences if configured)
   - `.maestro/templates/design.md` (output structure for full solution mode)

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

   Present the questionnaire to the user. Once answered, generate the DESIGN.md incorporating the responses.
   If all decisions can be made from available information, skip the questionnaire and state the rationale for each choice in the design document.

3. **Generate or extend DESIGN.md** (iterative — each invocation adds to it)

4. **Save design draft to session folder** (numbered file)

5. **Offer promotion:** "Design draft saved to session. Ready to promote to docs/03-design/DESIGN.md?"
   - If user confirms → copy to `docs/03-design/DESIGN.md`
   - If user wants changes → iterate in session first
   - If user says "save directly to docs" in the original prompt → skip the ask
   - For component/file-level: update the existing DESIGN.md in docs/ (with review)

6. **Save report** to session folder

## Cross-Phase Awareness

If the design process reveals missing information:
- Suggest: "This design decision requires information we don't have. Consider running `/mae-explore {topic}` to investigate."
- Flag in DESIGN.md with `GAP:` tag so it's visible in reviews
- Do not invent technical decisions when information is insufficient — ask or flag

## Output Behaviors
- Compare alternatives when multiple approaches exist (table format)
- State recommendation with rationale for every design choice
- List trade-offs explicitly
- Flag decisions needing user input vs agent-decidable
- Include source structure section (for later `/mae-do` scaffolding task)
- When user profile indicates technical expertise, offer lighter explanations; when non-technical, explain trade-offs in plain terms

## Direction
Top-down: architecture → components → files. The requirements drive the architecture.

## Skip When
- Project is a single-file tool or script — go straight to `/mae-do`
- Implementation is obvious from explore output alone — skip to `/mae-do`
- Building a PoC — capture design decisions informally in the explore output

## File Size
- Target: 2,000-4,000 words
- Hard max: 6,000 words
- If exceeding, split: DESIGN.md (overview) + component-{name}.md per component
