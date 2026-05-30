# /mae-init — Initialize Maestro Framework

Initialize the Maestro delivery framework in the current project.

$ARGUMENTS — optional: project name, mode (solo/team)

## Usage

```
/mae-init                    → interactive (asks for name and mode)
/mae-init {project-name}     → solo mode (default)
/mae-init {project-name} team → team mode
```

## Behavior

1. Check if framework is already initialized (look for HANDOFF.md, delivery/)
   - If yes: "Framework already initialized. Use `/mae-explore` to start."
   - If no: proceed

2. If no project name provided, ask: "What's the project name?"

3. Determine mode (default: solo). Mode differences:

   | Aspect | Solo | Team |
   |--------|------|------|
   | `.gitignore` | sessions/ and notes/ NOT gitignored | sessions/ and notes/ ARE gitignored |
   | `WORKLOG.md` | No "Who" column | "Who" column added |
   | `maestro.toml` | `mode = "solo"` | `mode = "team"` |

4. Create folder structure:
   ```
   delivery/
   ├── 01-explore/
   ├── 02-prd/
   ├── 03-design/
   └── 04-plan/
       └── tasks/
   sessions/
   notes/
   templates/
   ```

5. Create tracking files (empty templates):
   - HANDOFF.md — with project name and empty sections
   - DECISIONS.md — header row only
   - OPEN_QUESTIONS.md — header only
   - WORKLOG.md — header only (with "Who" column in team mode)
   - notes/ideas.md — empty with header

6. Copy templates: task.md, summary.md, report.md, prd.md, sdd.md, explore.md

7. Create maestro.toml:
   ```toml
   [project]
   name = "{project name}"
   mode = "{solo|team}"
   ```

8. **Optional: Profile setup.**
   Ask: "Would you like to set up a profile? This helps Maestro tailor its assistance. (You can skip and add later.)"

   **Solo mode — `[user]` section:**
   ```toml
   [user]
   description = "Senior Python architect, new to frontend"
   strengths = ["backend", "python", "system-design"]
   needs_help = ["frontend", "ux"]
   ```

   **Team mode — `[[team.members]]` array:**
   ```toml
   [[team.members]]
   name = "Piotr"
   role = "architect"
   strengths = ["backend", "python", "system-design"]
   needs_help = ["frontend"]

   [[team.members]]
   name = "Anna"
   role = "frontend-developer"
   strengths = ["react", "css", "ux"]
   needs_help = ["backend", "databases"]
   ```

   In team mode, the agent asks at session start: "Who am I working with?" and adapts to that member's profile.

   If skipped, omit the section entirely. The framework works without it — all commands behave generically.

9. In team mode: add to .gitignore:
   ```
   sessions/
   notes/
   ```

10. Save report to session folder

## What init does NOT do
- Set up source code structure (that's a `/mae-do` task after `/mae-design`)
- Choose tech stack (that's `/mae-explore` and `/mae-design`)
- Create or modify CLAUDE.md (user's responsibility)
- Install MAESTRO.md (that's done by the install script)

## Output
Report: what was created, mode selected, suggested next step (`/mae-explore`)
