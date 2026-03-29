# Automation Prompt Templates

Use this section order in this file: Suitability, App template, CLI template, Placeholders, Customization Points.

## Suitability

- Codex App: `Strong` - recurring weekly/daily planning digests are a direct automation fit.
- Codex CLI: `Conditional` - best when Things MCP is available or JSON exports are provided.

## Codex App Automation Prompt Template

```markdown
Use $things-digest-generator.

Scope:
- Target workspace/project: <PROJECT_ROOT_ABS_PATH>
- Data source mode: <THINGS_SOURCE_MODE_MCP_OR_JSON>
- Planning horizon days: <DAYS_AHEAD>
- Digest output path: <DIGEST_MD_PATH>

Execution policy:
- Prefer Things MCP reads first (areas, open projects, open todos, recent completed todos).
- If MCP permission/tool availability fails, fall back to JSON inputs:
  - <AREAS_JSON_PATH>
  - <PROJECTS_JSON_PATH>
  - <OPEN_TODOS_JSON_PATH>
  - <RECENT_DONE_JSON_PATH>
- Never modify Things data unless explicitly requested.

Output contract:
- If actionable data exists, produce markdown beginning with `# Things Planning Digest - YYYY-MM-DD`.
- Include `## Executive Summary` only when `outputStyle=executive`.
- Then produce the sections in order: Snapshot, Recently Active, Week/Weekend Ahead, Suggestions.
- Keep tone concise and operational.
- Include concrete task/project names where available.
- Write final digest to <DIGEST_MD_PATH>.

No-findings handling:
- If there are no open todos and no recent completed tasks in scope, output exactly `No findings.` and archive the run.
- Otherwise keep the run in inbox triage.

Failure handling:
- If MCP and JSON fallback are both unavailable, report one deterministic `Input error:` message that names the missing file, unreadable path, invalid JSON, or unsupported JSON shape.
```

## Codex CLI Automation Prompt Template (codex exec)

- Recommended sandbox: `read-only`

Prompt template:

```markdown
Use $things-digest-generator.

Build a Things planning digest for <PROJECT_ROOT_ABS_PATH> with days_ahead=<DAYS_AHEAD>.
Data source mode: <THINGS_SOURCE_MODE_MCP_OR_JSON>.

If mode is MCP:
- Attempt Things MCP reads first.
- If blocked, fall back to JSON files if provided.

If mode is JSON:
- Use only:
  - <AREAS_JSON_PATH>
  - <PROJECTS_JSON_PATH>
  - <OPEN_TODOS_JSON_PATH>
  - <RECENT_DONE_JSON_PATH>

Produce a markdown digest that starts with `# Things Planning Digest - YYYY-MM-DD`.
If `outputStyle=executive`, include `## Executive Summary` before the standard sections.
Then emit:
1) Snapshot
2) Recently Active
3) Week/Weekend Ahead
4) Suggestions

Write digest to <DIGEST_MD_PATH>.
If there is no actionable data, output exactly `No findings.`.
If inputs fail, report one deterministic `Input error:` message and stop.
```

Optional command wrapper:

```bash
codex exec --sandbox read-only --output-last-message <FINAL_MESSAGE_PATH> "<PASTE_PROMPT_TEXT>"
```

Optional machine-readable mode:

```bash
codex exec --sandbox read-only --json "<PASTE_PROMPT_TEXT>"
```

## Placeholders

- `<PROJECT_ROOT_ABS_PATH>`: Absolute project path for the run.
- `<THINGS_SOURCE_MODE_MCP_OR_JSON>`: `mcp` or `json`.
- `<DAYS_AHEAD>`: Integer planning horizon.
- `<DIGEST_MD_PATH>`: Output path for digest markdown.
- `<AREAS_JSON_PATH>`: Areas JSON export path.
- `<PROJECTS_JSON_PATH>`: Projects JSON export path.
- `<OPEN_TODOS_JSON_PATH>`: Open todos JSON export path.
- `<RECENT_DONE_JSON_PATH>`: Recent completed todos JSON export path.
- `<FINAL_MESSAGE_PATH>`: File path for final assistant message.
- `<PASTE_PROMPT_TEXT>`: Fully expanded prompt text for `codex exec`.

## Customization Points

- Source mode preference (`mcp` vs `json` fallback).
- Planning horizon (`days_ahead`).
- Digest verbosity/length target.
- Suggestion emphasis (risk-first vs momentum-first).
