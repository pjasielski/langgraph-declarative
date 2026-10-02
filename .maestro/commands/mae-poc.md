# /mae-poc — PoC Specification

Collapse requirements, design, and roadmap into a single actionable spec. For prototypes, spikes, and time-boxed builds where the full track costs more than it returns.

$ARGUMENTS — optional: scope hint, or `--tasks` to also emit task files

## Usage

```
/mae-poc                    → generate POC.md from explore artifacts
/mae-poc {scope hint}       → bias the spec toward a stated scope
/mae-poc --tasks            → additionally emit task files to docs/04-plan/tasks/
```

## Prerequisites

- `docs/01-explore/` should contain confirmed explore artifacts
- If empty: warn, and offer to proceed from `docs/00-reference/` + conversation context (PoCs often start before a formal explore)
- If the explore report has unresolved `GAP:` or `UNCLEAR:` tags, surface them and ask whether to resolve them first or record them as assumptions

## Behavior

1. **Read inputs (prioritized — stop once you have enough):**

   - `docs/00-reference/` — source materials you did not write (client briefs, specs, transcripts). **Authoritative** over inferences drawn from code.
   - `docs/01-explore/` — final explore report (primary synthesis)
   - `DECISIONS.md`, `OPEN_QUESTIONS.md`
   - `maestro.toml` (project context, user profile, tech preferences)
   - `.maestro/templates/poc.md` (output structure)
   - Do NOT read source code or raw data files — that is explore's job

2. **Ask only blocking questions.** PoC mode is speed-optimized. Ask only where a wrong guess invalidates the build — stack choice, external dependency, data source, deployment target. Everything else: decide, and record the call under § Risks & Assumptions. Respect `question_style` from `maestro.toml`.

3. **Generate POC.md** using `.maestro/templates/poc.md`:

   - § 1 Scope — problem, in-scope, explicit non-goals, done-when
   - § 2 Requirements — numbered, testable, prioritized (MUST / SHOULD / WON'T)
   - § 3 Design — architecture, components, stack, data model, key decisions
   - § 4 Roadmap — milestone M01, task table with IDs `M01.01`…, critical path
   - § 5 Risks & Assumptions
   - § 6 Current State — see step 4

4. **Populate § 6 Current State.** This section is the rehydration key: a fresh session must be able to read POC.md alone and know exactly where the work stands. On generation it reads "not started". `/mae-do` updates it after each task. Keep it to five lines — what's done, what's next, what's blocked.

5. **Save to `docs/02-poc/POC.md` directly.** Unlike `/mae-req` and `/mae-design`, PoC output is immediately actionable, so it follows the `/mae-plan` convention and skips the session-then-promote step. Also save a report to the session folder.

6. **If `--tasks`:** additionally emit `docs/04-plan/tasks/M01.NN-{slug}.md` using `.maestro/templates/task.md`. Off by default — the roadmap table plus `/mae-do` session reports already provide the audit trail.

7. **Suggest next step:**

   > "POC spec ready — N tasks in M01. Run `/mae-do poc` to execute the whole milestone, or `/mae-do M01.01` for the first task only."

## Task IDs

PoC work uses the standard `M{MM}.{NN}` scheme — the PoC is milestone **M01**. No separate ID namespace. If the PoC graduates into a full project, `/mae-plan` continues at M02 and the PoC's history stays intact.

## Output Behaviors

- Flag ambiguities with `UNCLEAR:`; record judgement calls under § Risks & Assumptions
- Every requirement must be verifiable — no "should be fast"
- Every task must be independently completable and have a done-when
- Prefer fewer, larger tasks over many small ones (PoC mode: 5–10 tasks)
- Identify the **spine**: the narrowest end-to-end path through the system. Mark it in the roadmap and state the cut order if time runs short.

## Skip When

- The build is more than one milestone of work — use the full track (`/mae-req` → `/mae-design` → `/mae-plan`)
- Requirements are genuinely contested or externally reviewed — use `/mae-req`
- A single-file script — go straight to `/mae-do`

## File Size

- Target: 1,500–2,500 words
- Hard max: 4,000 — past this the project is not a PoC. Recommend the full track and offer to split into REQUIREMENTS.md + DESIGN.md + ROADMAP.md.

## Artifact Flow

```
docs/00-reference/ + docs/01-explore/  →  /mae-poc  →  docs/02-poc/POC.md
                                                          ↓
                                                      /mae-do poc
```
