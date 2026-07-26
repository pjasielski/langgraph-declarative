# /mae-init — Initialize Maestro Framework

Initialize the Maestro delivery framework in the current project.

$ARGUMENTS — optional: project name

## Usage

```
/mae-init                    → interactive profile setup
/mae-init {project-name}     → set project name + profile setup
```

## Behavior

**Note:** Folder creation and file scaffolding are handled by `install.sh`. mae-init is for profile setup and project configuration.

1. Check if framework is already initialized (look for HANDOFF.md, maestro.toml)
   - If no: "Run the installer first (`install.sh`), then come back for profile setup."
   - If yes: proceed to profile setup

2. If no project name in `maestro.toml`, ask: "What's the project name?"

3. **Profile setup (conversational).**
   Ask: "Would you like to set up a profile? This helps Maestro tailor its assistance. (You can skip and add later.)"

   **Individual `[user]` section:**
   ```toml
   [user]
   description = "Senior Python architect, new to frontend"
   strengths = ["backend", "python", "system-design"]
   needs_help = ["frontend", "ux"]
   ```

   **Team `[[team.members]]` array:**
   Ask: "Who's on the team?" Then build the members list conversationally.
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

   When `[[team.members]]` is defined, team behaviors activate automatically (e.g., "Who" column in WORKLOG.md, agent asks "Who am I working with?" at session start).

   If skipped, omit the section entirely. The framework works without it — all commands behave generically.

4. Save report to session folder

## What init does NOT do
- Create folder structure (that's `install.sh` — creates docs/01-explore/, 02-requirements/, 03-design/, 04-plan/)
- Create tracking files (that's `install.sh`)
- Set up source code structure (that's a `/mae-do` task after `/mae-design`)
- Choose tech stack (that's `/mae-explore` and `/mae-design`)
- Create or modify CLAUDE.md (user's responsibility)

## Output
Report: profile configured (or skipped), suggested next step (`/mae-explore`)
