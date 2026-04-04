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
| `maintain-plugin-docs` | Current plugin-docs maintainer for stack-specific skills and plugin repos | README audit/apply, ROADMAP audit/apply, combined docs passes |
| `sync-skills-repo-guidance` | Current guidance-alignment owner for skills and plugin repos | `check-only` script audit, maintainer-driven guidance reconciliation, misroute and defer handling |

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

## `maintain-plugin-docs`

Current-state note:

- This skill is the current stack-specific docs-maintenance surface for plugin-development repos in this family.
- The implemented automation owns `README.md`, `ROADMAP.md`, and combined docs passes through `--doc-scope`.
- The intended scope is broader in policy and refinement, but the checklist-style `ROADMAP.md` maintenance path now exists in the same skill surface.
- For repo guidance, Codex local plugin install guidance and Claude Code plugin usage guidance should be treated as the primary documented surfaces, with Vercel `skills` CLI installs as the secondary surface.

### Workflow: audit-only

- Triggered when the user wants plugin-repo docs maintenance and the current request is still `README.md`-only or README-first.
- Primary workflow.
- `read-only`

Inputs:

- Required: `--workspace <path>`
- Optional: `--doc-scope <readme|roadmap|all>`
- Optional: `--repo-glob <glob>`
- Optional: repeatable `--exclude <path>`
- Tool or script input: `scripts/maintain_plugin_docs.py`

Outputs:

- Markdown plus JSON with `run_context`, `repos_scanned`, `profile_assignments`, `readme_findings`, `roadmap_findings`, `cross_doc_findings`, `fixes_applied`, `post_fix_status`, `errors`
- Exact clean-run text: `No findings.`

### Workflow: audit plus bounded fixes

- Triggered when the user wants README fixes for a skills or plugin repository.
- Variant workflow.
- `bounded-write`

Outputs:

- Same Markdown plus JSON report shape as audit-only
- Exact clean-run text: `No findings.` when no issues and no errors remain

### Workflow: ROADMAP audit/apply

- Triggered when the user wants checklist-style `ROADMAP.md` maintenance in a plugin-development repo.
- Supports `check-only` and bounded `apply` behavior through `--doc-scope roadmap`.
- In combined runs, `--doc-scope all` audits both surfaces and reports cross-doc drift.

## `sync-skills-repo-guidance`

Current-state note:

- This skill currently owns ongoing guidance alignment for this repo pattern.
- Its script coverage is narrower than the full maintainer workflow.
- The current script audits local guidance snippets and discovery mirrors. Broader docs-link maintenance, policy wording changes, and cross-doc reconciliation are still maintainer-driven.

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

- README-only request: defer to `maintain-plugin-docs`
- bootstrap request: defer to `bootstrap-skills-plugin-repo`
- upstream docs changed materially: report dated findings before narrowing or changing repo guidance

Outputs:

- Markdown plus JSON with `run_context`, `findings`, `errors`
- Exact clean-run text: `No findings.`

### Workflow: maintainer-driven guidance fixes

- Triggered when the user wants repo-wide guidance drift corrected after the audit.
- Variant workflow.
- `bounded-write`

Outputs:

- The script still emits the same JSON report shape as `check-only`.
- Actual doc fixes are currently applied by the maintainer after interpreting the audit and broader repo context.
