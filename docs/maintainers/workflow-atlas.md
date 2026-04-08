# Maintainer Workflow Atlas

This document is maintainer-only. It is the repo-level workflow reference for every skill in this repository.

It diagrams real current workflows, captures their inputs and outputs, and describes the public Agent+Skill UX. Audit procedure, review criteria, and maintainer operating rules live in `docs/maintainers/reality-audit.md`.

## Packaging Context

- Root `skills/` is the canonical workflow-authoring surface.
- `plugins/productivity-skills/` is the plugin packaging root for Codex and Claude plugin metadata.
- `.agents/skills` and `.claude/skills` mirror root `skills/` for local project discovery on macOS and Linux.
- `plugins/productivity-skills/skills` mirrors root `skills/` for local plugin packaging alignment.
- `.agents/plugins/marketplace.json` points local Codex plugin discovery at the plugin subtree rather than at the repository root.
- `.claude-plugin/marketplace.json` is the repo-root Claude marketplace catalog for Git-backed sharing, while direct local Claude development still uses `claude --plugin-dir`.

## Product Direction

- This repository now optimizes for globally useful skills that make sense to install broadly.
- This repository is also the canonical general-purpose baseline layer for workflow families that may later narrow into stack-specific plugins.
- Dedicated language-, stack-, or repository-specific bundles should increasingly live in separate plugins intended for project-level or repo-level install.
- Those narrower plugins should refine or extend the workflows here when stronger assumptions improve the result, rather than turning this repo into a passive router.
- Agent-skills and agent-plugin repository maintenance now has a dedicated sibling repo at `/Users/galew/Workspace/agent-plugin-skills`.
- Those agent-stack maintainer skills are now out of this repo's active inventory and belong in the sibling repo instead.

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
| `explain-code-slice` | Canonical code-slice walkthrough explainer | `explain a slice`, `compare slices`, detail-level variants |
| `maintain-project-readme` | General README maintainer for ordinary software projects | `check-only`, `apply`, repo-profile detection, clean run, misroute rejection |
| `maintain-project-contributing` | General CONTRIBUTING maintainer for ordinary software projects | `check-only`, `apply`, repo-profile detection, clean run |
| `maintain-project-roadmap` | Checklist roadmap maintainer | `check-only`, `apply`, clean run, legacy migration |
| `maintain-project-repo` | Local-first repo maintainer toolkit installer | `install`, `refresh`, `report-only`, thin CI wrapper setup |

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

- Skills/plugin repo detected: reject and redirect to the dedicated `maintain-skills-readme` skill in `/Users/galew/Workspace/agent-plugin-skills`
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

## `maintain-project-contributing`

### Workflow: `check-only`

**Overview**

- Triggered when the user wants deterministic auditing for an ordinary software-project `CONTRIBUTING.md`.
- Primary workflow.
- `read-only`

**Inputs**

- Required: `--project-root <path>`
- Required: `--run-mode check-only`
- Optional: `--contributing-path <path>`
- Tool/script input: `scripts/maintain_project_contributing.py`

**Branch Conditions**

- Multiple repo profiles match: report ambiguity while selecting the conservative valid profile
- Contribution guide already sound: exact clean-run text

**Outputs**

- Markdown plus JSON with `run_context`, `profile_assignment`, `schema_violations`, `command_integrity_issues`, `content_quality_issues`, `fixes_applied`, `post_fix_status`, `errors`
- Exact clean-run text: `No findings.`

### Workflow: `apply`

**Overview**

- Triggered when the user wants bounded `CONTRIBUTING.md` normalization, repair, or creation.
- Variant workflow.
- `bounded-write`

**Inputs**

- Required: `--project-root <path>`
- Required: `--run-mode apply`
- Optional: `--contributing-path <path>`

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

## `maintain-project-repo`

### Workflow: `install` / `refresh`

**Overview**

- Triggered when the user wants reusable local maintainer scripts instead of CI-only helper glue.
- Primary workflow.
- `bounded-write`

**Inputs**

- Required: `--repo-root <path>`
- Optional: `--operation install|refresh`
- Optional: `--profile generic|swift-package|xcode-app`
- Optional: `--skip-github-workflow`
- Optional: `--dry-run`
- Tool/script input: `scripts/run_workflow.py`

**Branch Conditions**

- Managed path conflict: block when a required managed path cannot be updated safely
- GitHub workflow skip: keep toolkit install but omit the thin workflow wrapper

**Outputs**

- JSON with `status`, `path_type`, `output`, `profile`, `managed_files`, `applied_actions`, `next_step`

### Workflow: `report-only`

**Overview**

- Triggered when the user wants the planned toolkit file set without mutating the repo.
- Variant workflow.
- `read-only`

**Inputs**

- Required: `--repo-root <path>`
- Required: `--operation report-only`
- Optional: `--skip-github-workflow`

**Outputs**

- JSON with `status`, `path_type`, `output`, `managed_files`, `planned_actions`, `next_step`

## Related External Skills

The following workflows were incubated here but now live in `/Users/galew/Workspace/agent-plugin-skills`:

- `maintain-skills-readme`
- `bootstrap-skills-plugin-repo`
- `sync-skills-repo-guidance`
