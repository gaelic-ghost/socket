# Plugin Docs Maintenance Automation Prompt Templates

## Suitability

- Codex App: `Strong`
- Codex CLI: `Strong`

## Codex App Automation Prompt Template

```markdown
Use $maintain-plugin-docs.

Scope:
- Workspace root: <WORKSPACE_ROOT_ABS_PATH>
- Repo glob: *-skills
- Exclude paths: <EXCLUDE_PATHS_CSV_OR_NONE>

Execution policy:
- Run audit first.
- If <APPLY_FIXES_TRUE_FALSE> is true, run bounded `README.md` and `ROADMAP.md` fixes for the requested doc scope and re-check.
- Suggest AGENTS snippets when requested; edit `AGENTS.md` only with explicit user approval and only for targeted snippet insertion.
- Never edit source code, manifests, lockfiles, or CI files.
- Never commit or push.

Output contract:
- Return Markdown summary and JSON-ready fields for:
  run_context, repos_scanned, profile_assignments, readme_findings,
  roadmap_findings, cross_doc_findings, fixes_applied, post_fix_status, errors.
- Write reports to:
  - <REPORT_MD_PATH>
  - <REPORT_JSON_PATH>

No-findings handling:
- If there are no current plugin-docs maintenance issues and no errors, output exactly `No findings.`.
```

## Codex CLI Automation Prompt Template

### Variant A: Audit-only

```markdown
Use $maintain-plugin-docs.

Audit plugin-docs maintenance needs across `*-skills` under <WORKSPACE_ROOT_ABS_PATH>.
Apply excludes: <EXCLUDE_PATHS_CSV_OR_NONE>.
Run audit only (no fixes) for `--doc-scope <readme|roadmap|all>`.
Write outputs to <REPORT_MD_PATH> and <REPORT_JSON_PATH>.
If no issues remain, output exactly `No findings.`.
```

### Variant B: Audit + bounded fixes

```markdown
Use $maintain-plugin-docs.

Audit plugin-docs maintenance needs across `*-skills` under <WORKSPACE_ROOT_ABS_PATH>.
Apply excludes: <EXCLUDE_PATHS_CSV_OR_NONE>.
Run audit pass first, then bounded fixes for the requested `--doc-scope <readme|roadmap|all>` and re-check.
Only edit AGENTS.md for targeted snippet insertion after explicit user approval.
Do not edit non-doc files.
Write outputs to <REPORT_MD_PATH> and <REPORT_JSON_PATH>.
```

## Placeholders

- `<WORKSPACE_ROOT_ABS_PATH>`
- `<EXCLUDE_PATHS_CSV_OR_NONE>`
- `<APPLY_FIXES_TRUE_FALSE>`
- `<REPORT_MD_PATH>`
- `<REPORT_JSON_PATH>`
