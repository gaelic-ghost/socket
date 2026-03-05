# Automation Prompt Templates

Use this section order in this file: Suitability, App template, CLI template, Placeholders, Customization Points.

## Suitability

- Codex App: `Strong` - recurring workspace hygiene checks map directly to unattended local automations.
- Codex CLI: `Strong` - `codex exec` works well for scheduled audit/fix runs with explicit sandbox control.

## Codex App Automation Prompt Template

```markdown
Use $project-docs-maintainer.

Scope:
- Workspace root: <WORKSPACE_ROOT_ABS_PATH>
- Exclude paths (repeatable): <EXCLUDE_PATHS_CSV_OR_NONE>
- Optional exclude-file: <EXCLUDE_FILE_PATH_OR_NONE>
- Optional repo cap: <MAX_REPOS_OR_NONE>

Execution policy:
- Run audit pass first.
- If <APPLY_FIXES_TRUE_FALSE> is true, run a second pass with safe docs-only fixes, then re-check.
- Never edit source code, manifests, lockfiles, or generated files.
- Do not scan or modify `AGENTS.md` (handled by a separate AGENTS maintainer workflow).
- Never commit, push, or open a PR.

Output contract:
- Return a Markdown summary with run context, discovery summary, unaligned repos, fixes applied, remaining issues, modified files, and errors.
- Include JSON-ready details for: run_context, repos_scanned, unaligned_repos, fixes_applied, post_fix_status, errors.
- Write reports to: <REPORT_MD_PATH> and <REPORT_JSON_PATH>.

No-findings handling:
- If there are no unaligned repos and no errors, output exactly `No findings.` and archive the run.
- Otherwise keep the run in inbox triage and summarize top issue categories.

Failure handling:
- If a required action is blocked by sandbox or permissions, report the blocked command, why it was needed, and the minimum required access.
```

## Codex CLI Automation Prompt Template (codex exec)

### Variant A: Audit-only (safer default)

- Recommended sandbox: `read-only`

Prompt template:

```markdown
Use $project-docs-maintainer.

Audit documentation alignment for repositories under <WORKSPACE_ROOT_ABS_PATH>.
Apply excludes: <EXCLUDE_PATHS_CSV_OR_NONE>.
Use exclude file: <EXCLUDE_FILE_PATH_OR_NONE>.
Use max repos: <MAX_REPOS_OR_NONE>.

Run audit only (no fixes). Do not edit files.
Return a Markdown summary and JSON-structured findings. Write outputs to:
- <REPORT_MD_PATH>
- <REPORT_JSON_PATH>

If there are no issues, output exactly `No findings.`.
If command execution is blocked, report the minimum required sandbox/permission adjustment.
```

Optional command wrapper:

```bash
codex exec --sandbox read-only --output-last-message <FINAL_MESSAGE_PATH> "<PASTE_PROMPT_TEXT>"
```

### Variant B: Audit + safe fixes

- Recommended sandbox: `workspace-write`

Prompt template:

```markdown
Use $project-docs-maintainer.

Audit documentation alignment for repositories under <WORKSPACE_ROOT_ABS_PATH>.
Apply excludes: <EXCLUDE_PATHS_CSV_OR_NONE>.
Use exclude file: <EXCLUDE_FILE_PATH_OR_NONE>.
Use max repos: <MAX_REPOS_OR_NONE>.

Run audit pass first. Then run safe docs-only fixes and re-check.
Never edit source code, manifests, or lockfiles.
Never commit or push.

Write outputs to:
- <REPORT_MD_PATH>
- <REPORT_JSON_PATH>

If there are no remaining issues, output exactly `No findings.`.
If blocked by sandbox/permissions, report the minimum required access to complete safely.
```

Optional machine-readable mode:

```bash
codex exec --sandbox workspace-write --json "<PASTE_PROMPT_TEXT>"
```

## Placeholders

- `<WORKSPACE_ROOT_ABS_PATH>`: Absolute workspace root to scan.
- `<EXCLUDE_PATHS_CSV_OR_NONE>`: Comma-separated absolute paths to exclude, or `none`.
- `<EXCLUDE_FILE_PATH_OR_NONE>`: Path to newline-delimited exclude file, or `none`.
- `<MAX_REPOS_OR_NONE>`: Integer cap or `none`.
- `<APPLY_FIXES_TRUE_FALSE>`: `true` to enable pass-2 safe fixes, `false` for audit only.
- `<REPORT_MD_PATH>`: Markdown report output path.
- `<REPORT_JSON_PATH>`: JSON report output path.
- `<FINAL_MESSAGE_PATH>`: File path for the final assistant message.
- `<PASTE_PROMPT_TEXT>`: Fully expanded prompt text for `codex exec`.

## Customization Points

- Workspace scope (`workspace`, excludes, max repos).
- Fix mode (`audit-only` vs `apply-fixes`).
- Failure posture (`fail-on-issues` policy in wrapper scripts).
- Output location and format (`--json`, markdown + JSON paths).
