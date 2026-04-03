# Maintainer Workflow Atlas

This document is maintainer-only. It is the repo-level workflow reference for every skill in this repository.

Audit procedure, review criteria, and maintainer operating rules live in `docs/maintainers/reality-audit.md`.

## Packaging Context

- Root `skills/` is the canonical workflow-authoring surface.
- `plugins/agent-plugin-skills/` is the plugin packaging root for Codex and Claude scaffolds.
- `.agents/skills` and `.claude/skills` mirror root `skills/` for local project discovery on macOS and Linux.
- `plugins/agent-plugin-skills/skills` mirrors root `skills/` for local plugin packaging alignment.
- `.agents/plugins/marketplace.json` points local Codex plugin discovery at the plugin subtree.

## Skill Index

| Skill | Canonical role | Workflows covered |
| --- | --- | --- |
| `bootstrap-skills-plugin-repo` | Repo bootstrap and structural alignment for skills and plugin repos | `check-only`, `apply`, scaffold creation, symlink mirror alignment |
| `maintain-skills-readme` | README maintainer for skills and plugin repos | audit-only, audit plus bounded fixes, clean run, error path |
| `sync-skills-repo-guidance` | Repo-wide guidance reconciler for skills and plugin repos | `check-only`, audit plus bounded fixes, upstream-doc refresh, misroute and defer handling |

## `bootstrap-skills-plugin-repo`

### Workflow: `check-only`

- Triggered when the user wants to audit or plan the structural bootstrap of a skills or plugin repository.
- Primary workflow.
- `read-only`

Inputs:

- Required: `--repo-root <path>`
- Required: `--run-mode check-only`
- Optional: `--plugin-name <name>`
- Tool or script input: `scripts/bootstrap_skills_plugin_repo.py`

Outputs:

- Markdown plus JSON with `run_context`, `findings`, `apply_actions`, `created_paths`, `errors`
- Exact clean-run text: `No findings.`

### Workflow: `apply`

- Triggered when the user wants missing repo structure created or aligned.
- Variant workflow.
- `bounded-write`

Outputs:

- Same Markdown plus JSON shape as `check-only`
- Exact clean-run text: `No findings.` when no findings, no apply actions, and no errors remain

## `maintain-skills-readme`

### Workflow: audit-only

- Triggered when the user wants `README.md` maintenance for a skills, plugin, or similar agent-stack repository without applying fixes.
- Primary workflow.
- `read-only`

Inputs:

- Required: `--workspace <path>`
- Optional: `--repo-glob <glob>`
- Optional: repeatable `--exclude <path>`
- Tool or script input: `scripts/maintain_skills_readme.py`

Outputs:

- Markdown plus JSON with `run_context`, `repos_scanned`, `profile_assignments`, `schema_violations`, `command_integrity_issues`, `fixes_applied`, `post_fix_status`, `errors`
- Exact clean-run text: `No findings.`

### Workflow: audit plus bounded fixes

- Triggered when the user wants README fixes for a skills or plugin repository.
- Variant workflow.
- `bounded-write`

Outputs:

- Same Markdown plus JSON report shape as audit-only
- Exact clean-run text: `No findings.` when no issues and no errors remain

## `sync-skills-repo-guidance`

### Workflow: `check-only`

- Triggered when the user wants a repo-wide guidance audit for an existing skills or plugin repository.
- Primary workflow.
- `read-only`

Inputs:

- Required: `--repo-root <path>`
- Required: `--run-mode check-only`
- Optional: `--plugin-name <name>`
- Tool or script input: `scripts/sync_skills_repo_guidance.py`

Branch conditions:

- README-only request: defer to `maintain-skills-readme`
- bootstrap request: defer to `bootstrap-skills-plugin-repo`
- upstream docs changed materially: report dated findings before narrowing or applying fixes

Outputs:

- Markdown plus JSON with `run_context`, `findings`, `errors`
- Exact clean-run text: `No findings.`

### Workflow: `audit plus bounded fixes`

- Triggered when the user wants repo-wide guidance drift corrected after the audit.
- Variant workflow.
- `bounded-write`

Outputs:

- Same Markdown plus JSON report shape as `check-only`
- Exact clean-run text: `No findings.` when no issues and no errors remain
