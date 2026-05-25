# Save Response to Markdown

Save the current response (or a specified topic) to a Markdown file in the active session folder.

## Usage

```
/md                           → Save current response
/md "topic description"       → Save response about a specific topic
```

## Behavior

1. **Identify the active session folder:**
   - Check `sessions/` for the highest-numbered session folder (e.g., `sessions/003-api-design/`)
   - If no session folder exists, ask: "No active session found. Should I create one? What should I call it?"

2. **Determine the file number:**
   - List all files in the session folder matching the `NN_*.md` pattern
   - Find the highest `NN` prefix number
   - Use `NN+1` as the new prefix (zero-padded to 2 digits: `01`, `02`, ... `10`, `11`)
   - If no numbered files exist, start at `01`
   - Note: files without the `NN_` prefix (like `_summary.md`, `analysis_report.md`) are ignored for numbering

3. **Generate the filename:**
   - Format: `{NN}_{descriptive_slug}.md`
   - The slug should be a short, kebab-case description of the content (3-5 words max)
   - Examples: `01_command_architecture.md`, `02_installation_guide.md`, `03_auth_design_decisions.md`

4. **Write the file with a header:**
   ```markdown
   # {Title}

   **Date:** {YYYY-MM-DD}
   **Session:** {NNN}-{session-name}

   ---

   {content}
   ```

5. **Update `_summary.md`** — append the new file to the "Files Created" or "What Was Done" section.

## Rules

- Content should be well-structured markdown — use headers, tables, and lists for clarity
- If the response naturally splits into multiple topics, create multiple files (each with its own incremented number)
- Never overwrite existing files — always create new ones with the next number
- Keep filenames short but descriptive
