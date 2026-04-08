# Maintainer Workflow Atlas

This document is maintainer-only. It is the repo-level workflow reference for every skill in this repository.

Audit procedure, review criteria, and maintainer operating rules live in `docs/maintainers/reality-audit.md`.

## Packaging Context

- Root `skills/` is the canonical workflow-authoring surface.
- `plugins/agent-plugin-skills/` is the plugin packaging root for Codex and Claude scaffolds.
- `.agents/skills` and `.claude/skills` mirror root `skills/` for local project discovery on macOS and Linux.
- `plugins/agent-plugin-skills/skills/` is a bundled plugin directory kept in sync with root `skills/` for shipped plugin packaging.
- `.agents/plugins/marketplace.json` points local Codex plugin discovery at the plugin subtree.
- `.claude-plugin/marketplace.json` is the Git-backed Claude marketplace catalog for sharing this repo's tracked plugin sources.
- Canonical plugin source trees and shared marketplace catalogs belong in git. Downstream install copies, caches, and local-only runtime state do not.

## Skill Index

| Skill | Canonical role | Workflows covered |
| --- | --- | --- |
| `bootstrap-skills-plugin-repo` | Repo bootstrap and structural alignment for skills and plugin repos | `check-only`, `apply`, scaffold creation, discovery-mirror alignment, bundled plugin skills sync |
| `install-plugin-to-socket` | Bounded local Codex plugin install wiring for plugin-development repos | `check-only`, `apply`, install, update, uninstall, scope-resolution from profile defaults |
| `maintain-plugin-repo` | Repo-level maintainer orchestrator for plugin-development repos | `audit-only`, `apply-safe-fixes`, validator-plus-docs synthesis, optional install-repair routing |
| `maintain-plugin-docs` | Current plugin-docs maintainer for stack-specific skills and plugin repos | README audit/apply, ROADMAP audit/apply, combined docs passes |
| `sync-skills-repo-guidance` | Current guidance-alignment owner for skills and plugin repos | `check-only` script audit, maintainer-driven guidance reconciliation, misroute and defer handling |
| `validate-plugin-install-surfaces` | Audit-only validator for plugin metadata, marketplace wiring, install docs, discovery mirrors, and bundled plugin skills | audit-only validation, grouped findings, no mutation |

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

## `maintain-plugin-repo`

Current-state note:

- This skill is the current repo-level maintainer orchestrator for plugin-development repos in this family.
- It does not replace the existing specialists. It coordinates them.
- Version 1 always runs `validate-plugin-install-surfaces` first, always runs `maintain-plugin-docs`, and only routes install-surface repair into `install-plugin-to-socket` when explicit install inputs are supplied.

### Workflow: `audit-only`

- Triggered when the user wants one bounded plugin-repo health pass without mutating the repo.
- Primary workflow.
- `read-only`

Inputs:

- Required: `--repo-root <path>`
- Optional: `--plugin-name <name>`
- Optional: `--doc-scope <readme|roadmap|all>`
- Optional: `--source-plugin-root <path>`
- Optional: `--install-scope <personal|repo>`
- Optional: `--target-repo-root <path>`
- Optional: `--install-mode <copy|symlink>`
- Tool or script input: `scripts/maintain_plugin_repo.py`

Outputs:

- Markdown plus JSON with `run_context`, `repo_root`, `workflow`, `owner_assignments`, `validation_findings`, `docs_findings`, `install_findings`, `fixes_applied`, `deferred_findings`, `post_fix_status`, and `errors`
- Exact clean-run text: `No findings.`

### Workflow: `apply-safe-fixes`

- Triggered when the user wants one bounded repo-maintenance pass that applies safe docs fixes and, when explicitly requested, local Codex install-surface repairs.
- Variant workflow.
- `bounded-write`

Branch conditions:

- validation findings always shape the owner routing and deferred-work report
- docs maintenance is always routed through `maintain-plugin-docs`
- install repair is only attempted when `--source-plugin-root` is supplied and install repair is explicitly enabled
- broader manifest or packaging rewrites outside the existing specialist owners must be deferred instead of guessed

Outputs:

- Same Markdown plus JSON report shape as `audit-only`
- Exact clean-run text: `No findings.` when the post-fix pass finishes without remaining findings, deferred work, or errors

## `install-plugin-to-socket`

Current-state note:

- This skill is the current bounded local Codex plugin installer for this repo family.
- It supports personal-scope and repo-scope installs, persistent default-scope preferences, staged-copy updates, bounded uninstalls, audit-style verify runs, Codex config-state enable or disable actions, and repo-to-personal promote behavior.
- It does not manage Claude install surfaces.

### Workflow: audit-only

- Triggered when the user wants to inspect local Codex plugin wiring before applying changes.
- Primary workflow.
- `read-only`

Inputs:

- Required: `--source-plugin-root <path>`
- Required: `--action <install|update|uninstall|verify|enable|disable|promote>`
- Required: `--run-mode check-only`
- Optional: `--scope <personal|repo>`
- Optional: `--repo-root <path>`
- Optional: `--config <path>`
- Optional: `--codex-config-path <path>`
- Optional: `--install-mode <copy|symlink>`
- Tool or script input: `scripts/install_plugin_to_socket.py`

Outputs:

- JSON report with `run_context`, `scope`, `action`, `install_mode`, `source_plugin`, `target_plugin_root`, `marketplace_path`, `codex_config_path`, `plugin_config_key`, `findings`, `apply_actions`, `restart_required`, `verification_steps`, and `errors`
- Exact clean-run text: `No findings.` when the script is called with `--print-md` and there are no findings, apply actions, or errors

### Workflow: apply

- Triggered when the user wants local Codex plugin wiring created, updated, or removed.
- Variant workflow.
- `bounded-write`

Outputs:

- Same JSON report shape as audit-only
- Exact clean-run text: `No findings.` when no findings, no apply actions, and no errors remain

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

## `validate-plugin-install-surfaces`

Current-state note:

- This skill is the current audit-only validator for install surfaces, plugin manifests, and metadata overlays in this repo family.
- It intentionally reports drift without mutating files.

### Workflow: audit-only

- Triggered when the user wants one bounded validation pass over plugin manifests, marketplace wiring, README install docs, and discovery mirrors.
- Primary workflow.
- `read-only`

Inputs:

- Required: `--repo-root <path>`
- Optional: `--plugin-name <name>`
- Optional: `--print-md`
- Optional: `--print-json`
- Optional: `--md-out <path>`
- Optional: `--json-out <path>`
- Optional: `--fail-on-findings`
- Tool or script input: `scripts/validate_plugin_install_surfaces.py`

Outputs:

- Markdown plus JSON with `run_context`, `canonical_skill_dirs`, `plugin_roots`, `metadata_findings`, `install_surface_findings`, `mirror_findings`, and `errors`
- Exact clean-run text: `No findings.`
