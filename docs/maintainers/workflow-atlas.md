# Maintainer Workflow Atlas

This document is maintainer-only. It is the repo-level workflow reference for every skill in this repository.

It diagrams real current workflows, captures their inputs and outputs, and describes the public Agent+Skill UX. Audit procedure, review criteria, and maintainer operating rules live in `docs/maintainers/reality-audit.md`.

## Packaging Context

- Root `skills/` is the canonical workflow-authoring surface.
- `plugins/productivity-skills/` is the plugin packaging root for Codex and Claude scaffolds.
- `.agents/skills` and `.claude/skills` mirror root `skills/` for local project discovery on macOS and Linux.
- `plugins/productivity-skills/skills` mirrors root `skills/` for local plugin packaging alignment.
- `.agents/plugins/marketplace.json` points local Codex plugin discovery at the plugin subtree rather than at the repository root.

## Repo-Wide Conventions

- `Workflow`: a logically grouped, user-meaningful path inside a skill.
- `Primary workflow`: the default path the skill should follow first.
- `Variant`: a subordinate branch inside the grouped skill, not a separate skill.
- `User-facing output`: what the end user sees from the Agent+Skill interaction.
- `Internal branch`: a decision point driven by mode, auth, config, missing input, or compatibility handling.
- `No findings.`, `blocked`, `created`, `updated`, `check-only`, `apply`, `duplicatePolicy`, `onUpdateWithoutToken`, `requireAbsoluteDateInConfirmation`, `outputStyle`, and `Executive Summary` use their current canonical repo meanings.

## Skill Index

| Skill | Canonical role | Workflows covered |
| --- | --- | --- |
| `bootstrap-skills-plugin-repo` | Repo bootstrap and structural alignment for skills/plugin repos | `check-only`, `apply`, scaffold creation, symlink mirror alignment |
| `explain-code-slice` | Canonical code-slice walkthrough explainer | `explain a slice`, `compare slices`, detail-level variants |
| `maintain-project-readme` | General README maintainer for ordinary software projects | `check-only`, `apply`, repo-profile detection, clean run, misroute rejection |
| `maintain-project-roadmap` | Checklist roadmap maintainer | `check-only`, `apply`, clean run, legacy migration |
| `maintain-skills-readme` | Specialized README maintainer for skills/plugin repos | audit-only, audit plus bounded fixes, clean run, error path |
| `sync-skills-repo-guidance` | Repo-wide guidance reconciler for skills/plugin repos | `check-only`, audit plus bounded fixes, upstream-doc refresh, misroute/defer handling |

## `bootstrap-skills-plugin-repo`

### Workflow: `check-only`

**Overview**

- Triggered when the user wants to audit or plan the structural bootstrap of a skills/plugin repository.
- Primary workflow.
- `read-only`

**Inputs**

- Required: `--repo-root <path>`
- Required: `--run-mode check-only`
- Optional: `--plugin-name <name>`
- Tool/script input: `scripts/bootstrap_skills_plugin_repo.py`

**Outputs**

- Markdown plus JSON with `run_context`, `findings`, `apply_actions`, `created_paths`, `errors`
- Exact clean-run text: `No findings.`

### Workflow: `apply`

**Overview**

- Triggered when the user wants missing repo structure created or aligned.
- Variant workflow.
- `bounded-write`

**Inputs**

- Required: `--repo-root <path>`
- Required: `--run-mode apply`
- Optional: `--plugin-name <name>`

**Outputs**

- Markdown plus JSON with `run_context`, `findings`, `apply_actions`, `created_paths`, `errors`
- Exact clean-run text: `No findings.` when no findings, no apply actions, and no errors remain

## `explain-code-slice`

### Workflow: `explain a slice`

**Overview**

- Triggered when the user wants one bounded end-to-end walkthrough of how part of a codebase works.
- Primary workflow.
- `read-only`

**Inputs**

- User intent selecting a slice explanation
- Required: a feature, request, event, job, datum, or code path to follow
- Optional: detail level (`quick`, `standard`, `thorough`)
- Optional: focus modifiers such as data-shape-heavy, branch-heavy, boundary-heavy, or debugging-oriented

**Outputs**

- Structured narrative with `Slice summary`, `Walkthrough`, `Diagram`, and `Notes`

## `maintain-project-readme`

### Workflow: `check-only`

**Overview**

- Triggered when the user wants deterministic auditing for an ordinary software-project `README.md`.
- Primary workflow.
- `read-only`

**Inputs**

- Required: `--project-root <path>`
- Required: `--run-mode check-only`
- Optional: `--readme-path <path>`
- Tool/script input: `scripts/maintain_project_readme.py`

**Branch Conditions**

- Skills/plugin repo detected: reject and redirect to `maintain-skills-readme`
- Multiple repo profiles match: report ambiguity while selecting the conservative valid profile
- README already sound: exact clean-run text

**Outputs**

- Markdown plus JSON with `run_context`, `profile_assignment`, `schema_violations`, `command_integrity_issues`, `content_quality_issues`, `fixes_applied`, `post_fix_status`, `errors`
- Exact clean-run text: `No findings.`

### Workflow: `apply`

**Overview**

- Triggered when the user wants bounded README-only normalization or repair for an ordinary software-project `README.md`.
- Variant workflow.
- `bounded-write`

**Inputs**

- Required: `--project-root <path>`
- Required: `--run-mode apply`
- Optional: `--readme-path <path>`

**Outputs**

- Markdown plus JSON with `run_context`, `profile_assignment`, `schema_violations`, `command_integrity_issues`, `content_quality_issues`, `fixes_applied`, `post_fix_status`, `errors`
- Exact clean-run text: `No findings.` when no issues and no errors remain after the post-fix audit

## `maintain-project-roadmap`

### Workflow: `check-only`

**Overview**

- Triggered when the user wants checklist roadmap validation without edits.
- Primary workflow.
- `read-only`

**Inputs**

- Required: `--project-root <path>`
- Required: `--run-mode check-only`
- Optional: `--roadmap-path <path>`
- Tool/script input: `scripts/maintain_project_roadmap.py`

**Outputs**

- Markdown plus JSON with `run_context`, `findings`, `apply_actions`, `errors`
- Exact clean-run text: `No findings.`

### Workflow: `apply`

**Overview**

- Triggered when the user wants bounded roadmap normalization or creation.
- Variant workflow.
- `bounded-write`

**Inputs**

- Required: `--project-root <path>`
- Required: `--run-mode apply`
- Optional: `--roadmap-path <path>`

**Outputs**

- Markdown plus JSON with `run_context`, `findings`, `apply_actions`, `errors`
- Exact clean-run text: `No findings.` when no findings, no apply actions, and no errors remain

## `maintain-skills-readme`

### Workflow: audit-only

**Overview**

- Triggered when the user wants `README.md` maintenance for a skills/plugin repository without applying fixes.
- Primary workflow.
- `read-only`

**Inputs**

- Required: `--workspace <path>`
- Optional: `--repo-glob <glob>`
- Optional: repeatable `--exclude <path>`
- Tool/script input: `scripts/maintain_skills_readme.py`

**Outputs**

- Markdown plus JSON with `run_context`, `repos_scanned`, `profile_assignments`, `schema_violations`, `command_integrity_issues`, `fixes_applied`, `post_fix_status`, `errors`
- Exact clean-run text: `No findings.`

### Workflow: audit plus bounded fixes

**Overview**

- Triggered when the user wants README fixes for a skills/plugin repository.
- Variant workflow.
- `bounded-write`

**Inputs**

- Same inputs as audit-only
- Explicit write trigger: `--apply-fixes`

**Outputs**

- Same Markdown plus JSON report shape as audit-only
- Exact clean-run text: `No findings.` when no issues and no errors remain

## `sync-skills-repo-guidance`

### Workflow: `check-only`

**Overview**

- Triggered when the user wants a repo-wide guidance audit for an existing skills/plugin repository.
- Primary workflow.
- `read-only`

**Inputs**

- Required: `--repo-root <path>`
- Required: `--run-mode check-only`
- Optional: `--plugin-name <name>`
- Tool/script input: `scripts/sync_skills_repo_guidance.py`

**Branch Conditions**

- README-only request: defer to `maintain-skills-readme`
- roadmap-only request: defer to `maintain-project-roadmap`
- upstream docs changed materially: report dated findings before narrowing or applying fixes

**Outputs**

- Markdown plus JSON with `run_context`, `findings`, `errors`
- Exact clean-run text: `No findings.`

### Workflow: `audit plus bounded fixes`

**Overview**

- Triggered when the user wants repo-wide guidance drift corrected after the audit.
- Variant workflow.
- `bounded-write`

**Inputs**

- Same inputs as `check-only`
- Requires official-doc refresh before applying repo-wide guidance changes

**Outputs**

- Same Markdown plus JSON report shape as `check-only`
- Exact clean-run text: `No findings.` when no issues and no errors remain
