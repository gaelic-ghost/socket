# Project README Maintenance Automation Prompt Templates

## Suitability

- Codex App: `Strong`
- Codex CLI: `Strong`

## Codex App Automation Prompt Template

```markdown
Use $maintain-project-readme.

Scope:
- Project root: <PROJECT_ROOT_ABS_PATH>
- README path override: <README_PATH_OR_NONE>
- README config override: <README_CONFIG_OR_NONE>

Execution policy:
- Load the canonical README config first.
- Run `check-only` first and summarize customization state, schema contract, schema violations, and content-quality issues.
- If <APPLY_FIXES_TRUE_FALSE> is true, run bounded README fixes and re-check.
- Preserve existing preamble content such as badges, callouts, screenshots, and intro prose before the first H2.
- Treat the configured README structure as hard-enforced.
- Keep `Status` very short and plain about maturity or availability.
- Treat `What This Project Is` and `Motivation` as user-authored sections that should not be replaced with invented claims. Remind the user to author them, if they've yet to do so.
- Keep `Quick Start` and `Usage` short, succinct, human-focused and end-user friendly; prefer fenced code blocks with info strings in `Usage` when examples help.
- Never invent commands, setup steps, or unsupported product claims.
- Never edit files other than the target `README.md`.
- Confirm with the user before a commit or push.

Output contract:
- Return Markdown summary and JSON-ready fields for:
  run_context, customization_state, schema_contract, schema_violations,
  content_quality_issues, fixes_applied, post_fix_status, errors.
- Write reports to:
  - <REPORT_MD_PATH>
  - <REPORT_JSON_PATH>

No-findings handling:
- If there are no issues and no errors, output exactly `No findings.`.
```

## Codex CLI Automation Prompt Template

### Variant A: Audit-only

```markdown
Use $maintain-project-readme.

Audit the project README under <PROJECT_ROOT_ABS_PATH>.
If needed, use README override path <README_PATH_OR_NONE>.
If needed, use README config override <README_CONFIG_OR_NONE>.
Load the canonical README config first, then run `check-only`.
Report customization state, schema contract, schema violations, and content-quality issues.
Write outputs to <REPORT_MD_PATH> and <REPORT_JSON_PATH>.
If there are no issues and no errors, output exactly `No findings.`.
```

### Variant B: Audit + bounded fixes

```markdown
Use $maintain-project-readme.

Audit the project README under <PROJECT_ROOT_ABS_PATH>.
If needed, use README override path <README_PATH_OR_NONE>.
If needed, use README config override <README_CONFIG_OR_NONE>.
Load the canonical README config first, then run `check-only`, then bounded README fixes, then re-check.
Preserve badges, callouts, screenshots, and extra intro prose before the first H2.
Treat the configured structure as hard-enforced.
Keep `Status` very short and plain about maturity or availability.
Treat `What This Project Is` and `Motivation` as user-authored sections that should not be replaced with invented claims.
Keep `Quick Start` and `Usage` human-focused and end-user friendly; prefer fenced code blocks with info strings in `Usage` when examples help.
Do not invent commands or edit files other than the target `README.md`.
Write outputs to <REPORT_MD_PATH> and <REPORT_JSON_PATH>.
```

## Placeholders

- `<PROJECT_ROOT_ABS_PATH>`
- `<README_PATH_OR_NONE>`
- `<README_CONFIG_OR_NONE>`
- `<APPLY_FIXES_TRUE_FALSE>`
- `<REPORT_MD_PATH>`
- `<REPORT_JSON_PATH>`
