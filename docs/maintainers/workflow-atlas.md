# Maintainer Workflow Atlas

This document is maintainer-only. It is the repo-level workflow reference for every skill in this repository.

It diagrams real current workflows, captures their inputs and outputs, and describes the public Agent+Skill UX. Audit procedure, review criteria, and maintainer operating rules live in `docs/maintainers/reality-audit.md`.

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
| `code-slice-explainer` | Canonical code-slice walkthrough explainer | `explain a slice`, `compare slices`, detail-level variants |
| `maintain-project-readme` | General README maintainer for ordinary software projects | `check-only`, `apply`, repo-profile detection, clean run, misroute rejection |
| `maintain-project-roadmap` | Checklist roadmap maintainer | `check-only`, `apply`, clean run, legacy migration |
| `maintain-skills-readme` | Specialized README maintainer for skills/plugin repos | audit-only, audit plus bounded fixes, clean run, error path |
| `project-workspace-cleaner` | Read-only cleanup audit | findings path, clean run, partial-results branch |
| `things-digest-generator` | Things planning digest builder | MCP-first, JSON fallback, executive output, clean run, missing-input failure |
| `things-reminders-manager` | Things reminder mutation workflow | create, update, `duplicatePolicy=ask-first`, `onUpdateWithoutToken` variants, blocked/disambiguation |

## `code-slice-explainer`

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

## `project-workspace-cleaner`

### Workflow: read-only scan with findings

**Overview**

- Triggered when the user wants cleanup findings across a workspace.
- Primary workflow.
- `read-only`

## `things-digest-generator`

### Workflow: planning digest generation

**Overview**

- Triggered when the user wants a week-ahead planning digest from Things data.
- Primary workflow.

## `things-reminders-manager`

### Workflow: reminder mutation

**Overview**

- Triggered when the user wants deterministic reminder creation or update handling for Things.
- Primary workflow.
