# /mae-explore (lite) — Build Understanding

Build mutual understanding of the project — business and technical. Adapts to what exists and what's needed.

$ARGUMENTS — optional: topic, file path, "ask", or "doc"

> **This is the lighter variant of mae-explore.** Differences from the standard version:
> - Questions are encouraged but not mandatory on every artifact
> - The agent uses judgment about when questions add value vs. when the analysis speaks for itself
> - First explore still produces questions; subsequent artifacts include them when genuinely useful

## Usage

```
/mae-explore                  → smart default: produce whatever is most useful now
/mae-explore {topic}          → targeted analysis of a specific area
/mae-explore {file path}      → analyze/summarize a specific document or transcript
/mae-explore ask              → generate questions to deepen understanding
/mae-explore ask {audience}   → questions for: user, client, team, technical
/mae-explore doc              → synthesize final explore report from all artifacts
```

## Smart Default (no arguments)

### First Explore (nothing exists)

1. **Scan for existing project resources:**
   - Always read: `README.md`, `maestro.toml`, `HANDOFF.md`
   - Scan `docs/` — list file names and sizes (do NOT read contents yet)
   - Scan `data/` — list file names only (flag if folder is large)
   - Scan source code — directory tree structure only (no file contents)
   - Report findings: "I see these existing resources: [list]. Which should I include in my analysis?"
   - Wait for user direction before reading large files or datasets

2. **Produce initial scope artifact** containing:
   - Business + technical overview (from whatever is available)
   - Identified gaps and potential problems (`GAP:` / `UNCLEAR:` tags)
   - **Questions section** — questions the agent needs answered to proceed

### Subsequent Explores

Detect what exists and assess readiness:

| Readiness signal | What it checks |
|------------------|----------------|
| **Scope defined** | Is there a business + technical overview? |
| **Key questions resolved** | Ratio of resolved vs. open questions in `_summary.md` and prior artifacts |
| **Coverage breadth** | Do artifacts cover business, technical, AND stakeholder angles? |
| **Blocking gaps** | Any `GAP:` or `UNCLEAR:` flags still unresolved? |
| **User intent** | Has the user indicated readiness to move on? |

Based on readiness, produce the most useful next artifact:
- **Gap analysis** — what's missing based on existing artifacts
- **Deeper analysis** — drill into an area that needs more understanding
- **Risk identification** — flags and concerns from available material
- **Question list** — questions for specific audiences

When coverage is strong and gaps are few, suggest:
> "Coverage looks solid — [list what's covered]. Remaining gaps: [list]. Consider `/mae-explore doc` when ready, or continue exploring [specific areas]."

### Readiness Indicator

After each explore artifact, append a readiness assessment to `_summary.md`:

```markdown
## Explore Readiness
- Scope: ✓ defined / ✗ missing
- Business context: ✓ covered / ~ partial / ✗ missing
- Technical context: ✓ covered / ~ partial / ✗ missing
- Stakeholders: ✓ identified / ~ partial / ✗ missing
- Blocking questions: N remaining
- Recommendation: [continue exploring / ready for doc synthesis]
```

## Targeted Analysis (topic or file)

### Topic
```
/mae-explore "auth system"
/mae-explore "competitor landscape"
/mae-explore "data pipeline"
```
Produces a focused deep-dive analysis on the specified area. Reads existing explore artifacts for context to avoid redundancy.

### File / Transcript
```
/mae-explore /path/to/transcript.md
/mae-explore /path/to/meeting-notes.txt
```
Reads the file and produces a structured summary:
- Key points and takeaways
- Decisions mentioned
- Questions raised
- Action items
- Relevance to project scope

## Questions (ask)

```
/mae-explore ask               → questions to deepen mutual understanding (default: for user)
/mae-explore ask {audience}    → questions for: user, client, team, technical
```

Generates a structured question document saved to the session folder. Questions are designed to be answered asynchronously — each question has space for a response.

**Output format:**

```markdown
# Explore: Questions for {audience}

## Blocking (answers needed before we can proceed)

### Q1: {question}
**Unblocks:** {what this enables}

**Response:** _

### Q2: {question}
**Unblocks:** {what this enables}

**Response:** _

## Important (significantly affects direction)

### Q3: {question}
**Affects:** {what it impacts}

**Response:** _

## Clarifying (would improve quality)

### Q4: {question}
**Improves:** {what it refines}

**Response:** _
```

The user or client fills in responses directly in the file. On next explore, the agent reads answered questions and incorporates them.

## Final Report (doc)

```
/mae-explore doc
```

1. Read ALL explore working artifacts from the current and previous sessions
2. Read any existing material in `docs/01-explore/`
3. Produce structured report using `.maestro/templates/explore.md`
4. Save to session folder
5. Ask: "Ready to promote to docs/01-explore/?"

The explore report is a **living document** — running `explore doc` again replaces the previous version (session keeps the history via numbered files).

## Behavior

1. **Read context:**
   - `docs/01-explore/` (confirmed artifacts)
   - Current session files (working artifacts)
   - `DECISIONS.md`, `OPEN_QUESTIONS.md`
   - `maestro.toml` (project context, user profile if configured)
   - `README.md` (if exists)
   - On first explore (no prior artifacts): scan `docs/`, `data/`, `src/` — report what's available, ask before reading
   - For `doc` mode: `.maestro/templates/explore.md` (report structure)

2. **Generate artifact** — type depends on mode (see above)

3. **Include questions when they add value** — especially on first explore and when significant gaps exist. Use judgment: a focused technical analysis may not need questions if the findings are clear. But when the agent is uncertain or spots gaps, questions are the right move.

4. **Save to session folder** (numbered file, e.g., `03_scope-analysis.md`)

5. **Update readiness indicator** in `_summary.md`

6. **For `doc` mode only:** offer promotion to `docs/01-explore/`

## Output Behaviors

- Surface unknowns and flag gaps (`GAP:`, `UNCLEAR:`)
- Include questions when gaps or uncertainties are identified — don't force questions when the analysis is self-sufficient
- Compare options when multiple approaches exist
- Rank questions by importance when included (blocking → important → clarifying)
- When uncertain about what to read or analyze, ask the user rather than guessing

## Artifact Flow

All explore artifacts → .sessions/ (working material)
Final report (`doc`) → .sessions/ → user promotes to docs/01-explore/
When ready → user runs `/mae-req` to formalize requirements

## Rules

- Never invent business requirements — flag unknowns as questions
- Each invocation produces ONE artifact (or a small set if content requires splitting)
- Working artifacts are free-form — no template required
- Only the final report (`doc`) uses the template
- If no material exists and no topic specified, scan for resources and ask orientation questions
- Questions are a first-class output — not an afterthought
- Never auto-read large datasets or extensive doc folders without asking the user first
