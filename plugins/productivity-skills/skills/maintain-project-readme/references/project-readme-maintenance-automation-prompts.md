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

Execution policy:
- Detect the repo profile from project files first.
- Run `check-only` first and summarize schema issues, command integrity issues, content-quality issues, and profile assignment.
- If <APPLY_FIXES_TRUE_FALSE> is true, run bounded README fixes and re-check.
- Preserve existing preamble content such as badges, callouts, screenshots, and intro prose before the first H2.
- Only add a profile-specific section automatically when the repo profile is clear.
- Never invent commands, setup steps, or unsupported product claims.
- Never edit files other than the target `README.md`.
- Never commit or push.

Output contract:
- Return Markdown summary and JSON-ready fields for:
  run_context, profile_assignment, schema_violations, command_integrity_issues,
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
Detect the repo profile first, then run `check-only`.
Report profile assignment, schema issues, command integrity issues, and content-quality issues.
Write outputs to <REPORT_MD_PATH> and <REPORT_JSON_PATH>.
If there are no issues and no errors, output exactly `No findings.`.
```

### Variant B: Audit + bounded fixes

```markdown
Use $maintain-project-readme.

Audit the project README under <PROJECT_ROOT_ABS_PATH>.
If needed, use README override path <README_PATH_OR_NONE>.
Detect the repo profile first, then run `check-only`, then bounded README fixes, then re-check.
Preserve badges, callouts, screenshots, and extra intro prose before the first H2.
Only add a profile-specific section when the repo profile is clear.
Do not invent commands or edit files other than the target `README.md`.
Write outputs to <REPORT_MD_PATH> and <REPORT_JSON_PATH>.
```

## Placeholders

- `<PROJECT_ROOT_ABS_PATH>`
- `<README_PATH_OR_NONE>`
- `<APPLY_FIXES_TRUE_FALSE>`
- `<REPORT_MD_PATH>`
- `<REPORT_JSON_PATH>`
