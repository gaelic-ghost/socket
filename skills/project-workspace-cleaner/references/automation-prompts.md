# Automation Prompt Templates

Use this section order in this file: Suitability, App template, CLI template, Placeholders, Customization Points.

## Suitability

- Codex App: `Strong` - recurring read-only scans are a direct fit for unattended local automations.
- Codex CLI: `Strong` - `codex exec` can run deterministic scan/report jobs with read-only safety.

## Codex App Automation Prompt Template

```markdown
Use $project-workspace-cleaner.

Scope:
- Workspace root: <WORKSPACE_ROOT_ABS_PATH>
- Min finding size MiB: <MIN_MB>
- Stale threshold days: <STALE_DAYS>
- Max findings: <MAX_FINDINGS>

Execution policy:
- Run read-only scan only.
- Never delete, move, or edit files.
- Never run cleanup commands automatically.

Output contract:
- Return ranked findings with severity, repo, directory, category, size_human, score, why_flagged, suggested_cleanup.
- Include a repo-level summary ranked by total flagged size.
- Write JSON report to <REPORT_JSON_PATH> and markdown/operator summary to <REPORT_MD_PATH>.

No-findings handling:
- If no findings meet thresholds, output exactly `No findings.` and archive the run.
- Otherwise keep the run in inbox triage with top critical/high findings first.

Failure handling:
- If access is blocked or directory traversal fails, report the impacted path and continue with remaining paths when possible.
- If any path is skipped, include a partial-results warning and list skipped paths in both markdown/operator output and JSON output.
```

## Codex CLI Automation Prompt Template (codex exec)

- Recommended sandbox: `read-only`

Prompt template:

```markdown
Use $project-workspace-cleaner.

Run a read-only cleanup scan for <WORKSPACE_ROOT_ABS_PATH> with:
- min_mb=<MIN_MB>
- stale_days=<STALE_DAYS>
- max_findings=<MAX_FINDINGS>

Do not modify or delete any files.
Return a ranked report with per-finding fields and repo-level totals.
Write outputs to:
- <REPORT_MD_PATH>
- <REPORT_JSON_PATH>

If there are no findings, output exactly `No findings.`.
If any path is inaccessible, include a partial-results warning and list skipped paths.
Reserve exact `No findings.` for complete runs with no findings and no skipped paths.
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

- `<WORKSPACE_ROOT_ABS_PATH>`: Absolute workspace path to scan.
- `<MIN_MB>`: Noise floor in MiB for reported findings.
- `<STALE_DAYS>`: Staleness threshold in days for score boosts.
- `<MAX_FINDINGS>`: Maximum findings to keep in output.
- `<REPORT_MD_PATH>`: Markdown/operator summary output path.
- `<REPORT_JSON_PATH>`: JSON report output path.
- `<FINAL_MESSAGE_PATH>`: File path for final assistant output.
- `<PASTE_PROMPT_TEXT>`: Fully expanded prompt text for `codex exec`.

## Customization Points

- Scan scope (`workspace`).
- Noise tuning (`min_mb`, `stale_days`, `max_findings`).
- Report shape (`markdown`, `json`, or both).
- Severity triage emphasis (critical/high-first summaries).
