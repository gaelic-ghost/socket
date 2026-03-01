# private-skills Roadmap

Last updated: 2026-03-01

## Scope

This roadmap tracks planned enhancements for the `github-repo-defaults` skill.

## Current State

- Completed: one-command defaults script, description/topic inference, baseline repo settings policy alignment.
- Next focus: advanced creation controls, branch governance, sync/audit mode, and automation-ready outputs.

## Milestone 1: Creation Controls

### Goal

Improve initial repository creation ergonomics and consistency.

### Planned Enhancements

- Add `--template` support for creating repositories from a template source.
- Add `--default-branch` support to set the initial default branch explicitly.

### Acceptance Criteria

- Script accepts `--template <owner/name>` and applies it during repo creation.
- Script accepts `--default-branch <branch>` and configures the repository default branch.
- Dry-run output shows both settings clearly when provided.

## Milestone 2: Default Branch Protection Bootstrap

### Goal

Make secure default-branch protection easy and repeatable.

### Planned Enhancements

- Add optional `--protect-default-branch` mode.
- Configure branch protection for PR-based changes, status checks, and linear history in bootstrap mode.

### Acceptance Criteria

- Protection setup runs only when explicitly requested.
- Dry-run explains every protection rule that would be applied.
- Script exits with clear error messages when required API permissions are missing.

## Milestone 3: Pull Request Settings Baseline

### Goal

Standardize PR behavior and merge conventions beyond current merge-method defaults.

### Planned Enhancements

- Configure squash commit title/message behavior consistently.
- Optionally enable auto-merge based on a flag and policy profile.

### Acceptance Criteria

- New options are documented with safe defaults.
- API updates are idempotent and do not fail when rerun.
- Verification output includes effective PR/merge settings.

## Milestone 4: Repository Classification Profiles

### Goal

Support smart defaults based on repository type.

### Planned Enhancements

- Add `--profile` with initial values: `library`, `service`, `mcp-server`.
- Profile adjusts topics, description style hints, and selected defaults.

### Acceptance Criteria

- `--profile` affects behavior deterministically and is visible in dry-run output.
- Unknown profiles fail fast with clear help text.
- Base defaults remain unchanged when profile is not provided.

## Milestone 5: Safe Sync Mode

### Goal

Allow policy re-application to existing repositories without unintended destructive changes.

### Planned Enhancements

- Add `--sync` mode to compare current repository settings with desired policy.
- Add human-readable diff preview before applying sync changes.

### Acceptance Criteria

- Sync output distinguishes no-op, add/update, and skipped actions.
- Sync mode avoids deleting unrelated settings unless explicitly requested.
- Dry-run and apply modes produce consistent planned-change summaries.

## Milestone 6: CI and Governance Seed Hooks

### Goal

Bootstrap common quality and governance files during first publish.

### Planned Enhancements

- Add optional seeding for `.github/workflows` baseline checks.
- Add optional template creation for `CODEOWNERS`, `SECURITY.md`, and `CONTRIBUTING.md`.

### Acceptance Criteria

- Seeding is opt-in and never overwrites existing files by default.
- Generated files are deterministic and documented.
- Summary reports which files were created, skipped, or already present.

## Milestone 7: Machine-Readable Output

### Goal

Make script output automation-friendly.

### Planned Enhancements

- Add `--json` mode for structured run summaries.
- Include normalized fields for repo target, actions, settings, and topics.

### Acceptance Criteria

- JSON output is valid and stable across reruns.
- Human-readable output remains default behavior.
- Dry-run JSON includes planned actions without side effects.

## Milestone 8: Public Visibility Guardrails

### Goal

Reduce accidental public publication and enforce readiness checks.

### Planned Enhancements

- Require explicit `--confirm-public` when `--visibility public` is used.
- Add optional checks for README/license presence before public creation.

### Acceptance Criteria

- Public creation fails fast without explicit confirmation.
- Guardrail checks can run in dry-run and apply modes with clear status reporting.
- Help output documents all public-safety flags.

## Backlog Quality Gate

- Keep script POSIX-safe.
- Keep defaults aligned with `/Users/galew/.codex/AGENTS.md`.
- Add tests for argument parsing and dry-run plans as enhancements ship.
