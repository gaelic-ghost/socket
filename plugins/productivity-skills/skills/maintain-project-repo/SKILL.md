---
name: maintain-project-repo
description: Install or refresh a profile-aware local-first repo-maintenance toolkit for Swift, Xcode, and general repositories, including validate, sync, and release entrypoints plus thin CI and pre-commit samples. Use when a repo needs reusable maintainer scripts instead of ad hoc GitHub-only helpers.
license: MIT
metadata:
  semver: 0.1.2
---

# Maintain Project Repo

## Purpose

Install or refresh a reusable `scripts/repo-maintenance/` toolkit inside a general, SwiftPM, or Xcode repository so validation, shared-sync work, and release steps live in repo-owned local scripts rather than in CI-only glue. `scripts/run_workflow.py` is the runtime entrypoint, and `scripts/install_repo_maintenance_toolkit.py` applies the managed file set, writes `scripts/repo-maintenance/config/profile.env`, and keeps the installed toolkit profile explicit.

## When To Use

- Use this skill when a Swift or Xcode repo needs one local entrypoint for validation, shared sync work, and releases.
- Use this skill when a repo has GitHub Actions or local shell helpers that should become thin wrappers around repo-owned scripts.
- Use this skill when a repo needs a standard and a submodule-aware release flow.
- Use this skill when the user wants a local-first alternative to putting maintainer logic under `.github/scripts/`.
- Do not use this skill for app bootstrap, Swift package bootstrap, or AGENTS-only guidance sync by themselves.
- Recommend `bootstrap-swift-package` when the repo does not exist yet and package scaffold creation is still the primary task.
- Recommend `bootstrap-xcode-app-project` when the repo does not exist yet and native Apple app bootstrap is still the primary task.
- Recommend `sync-swift-package-guidance` or `sync-xcode-project-guidance` when the immediate task is AGENTS alignment rather than maintainer-toolkit installation.

## Single-Path Workflow

1. Collect the required inputs:
   - `repo_root`
   - optional `operation`
   - optional `skip_github_workflow`
   - optional `dry_run`
2. Classify the repo and profile:
   - prefer this toolkit for SwiftPM repos, Xcode app repos, mixed Apple repos, and general software repos that need local maintainer automation
   - choose `swift-package` for plain Swift package repos
   - choose `xcode-app` for native Apple app repos
   - choose `generic` when no stronger Swift or Xcode profile applies
   - stop if the requested path is not a repository root
3. Explain the architecture boundary before mutating anything:
   - this is a durable building-block change because it creates one repo-owned maintainer surface that bootstrap, sync, validation, CI, and release flows can all share
   - it removes the pain of CI-only helper scripts and scattered release glue
   - the simpler extension path considered first was leaving helper scripts under `.github/scripts/` and adding more workflow-specific wrappers, but that would keep local and CI behavior drifting apart
4. Run `scripts/run_workflow.py` to normalize the inputs and choose the installer path.
5. Apply the managed toolkit files:
   - install or refresh `scripts/repo-maintenance/`
   - install or refresh `scripts/repo-maintenance/config/profile.env` for the selected profile
   - install or refresh the thin workflow wrapper at `.github/workflows/validate-repo-maintenance.yml` unless disabled
   - preserve repo-specific scripts or files that are not part of the managed file set
6. Verify the installed toolkit:
   - `scripts/repo-maintenance/validate-all.sh`
   - `scripts/repo-maintenance/sync-shared.sh`
   - `scripts/repo-maintenance/release.sh`
   - `.github/workflows/validate-repo-maintenance.yml` when workflow installation is enabled
   - branch protection, when enabled, requires the GitHub Actions check context `validate`; do not require the display-style string `Validate Repo Maintenance / validate`
7. Hand off follow-on work cleanly:
   - use `scripts/repo-maintenance/validate-all.sh` for local validation
   - use `scripts/repo-maintenance/sync-shared.sh` for repo-local shared sync tasks
   - use `scripts/repo-maintenance/release.sh --mode standard` or `--mode submodule` for releases

## Inputs

- `repo_root`: optional absolute or relative path to the repository root; defaults to `.`
- `operation`: `install`, `refresh`, or `report-only`
- `profile`: `generic`, `swift-package`, or `xcode-app`
- `skip_github_workflow`: optional flag to skip `.github/workflows/validate-repo-maintenance.yml`
- `dry_run`: optional flag to report the managed actions without writing files
- Defaults:
  - runtime entrypoint: executable `scripts/run_workflow.py`
  - `repo_root=.` when omitted
  - `operation=install`
  - `profile=generic`
  - GitHub workflow installation is enabled unless explicitly skipped

## Outputs

- `status`
  - `success`: the toolkit is installed, refreshed, or reported successfully
  - `blocked`: the requested repo root or installer preconditions are invalid
  - `failed`: the installer started but did not complete successfully
- `path_type`
  - `primary`: the managed installer path completed
  - `fallback`: a non-mutating report-only result was returned
- `output`
  - resolved repo root
  - normalized inputs
  - selected profile
  - managed file list
  - planned or applied actions
  - one concise next step

## Guards and Stop Conditions

- Stop with `blocked` if the repo root does not exist.
- Stop with `blocked` if the repo root is not a directory.
- Stop with `blocked` if the managed target paths are blocked by non-regular files that cannot be updated safely.
- Stop with `blocked` if the requested operation is unsupported.

## Fallbacks and Handoffs

- `report-only` is the non-mutating fallback path.
- The installer preserves repo-specific extra files under `scripts/repo-maintenance/`, `.github/workflows/`, and adjacent surfaces when they are not part of the managed file set.
- The installer keeps the selected toolkit profile explicit via `scripts/repo-maintenance/config/profile.env`.
- The generated workflow's branch-protection check context is `validate`; GitHub exposes the job check run by that context, not by the workflow title plus job name.
- Recommend `bootstrap-swift-package` or `bootstrap-xcode-app-project` when the repo still needs to be created.
- Recommend `sync-swift-package-guidance` or `sync-xcode-project-guidance` when AGENTS alignment is still the missing baseline after the toolkit is present.

## Customization

- Use `references/customization-flow.md`.
- `scripts/customization_config.py` stores and reports customization state.
- The current customization surface is one policy-only default for release mode preference. Installation shape, profile selection, and managed file selection are explicit workflow behavior, not durable runtime customization.

## References

### Workflow References

- `references/repo-maintenance-layout.md`
- `references/release-modes.md`
- `references/pre-commit-vs-ci.md`

### Contract References

- `references/automation-prompts.md`
- `references/customization-flow.md`

### Support References

- `assets/repo-maintenance/`
- `assets/github/repo-maintenance-workflows/validate-repo-maintenance.yml`

### Script Inventory

- `scripts/run_workflow.py`
- `scripts/install_repo_maintenance_toolkit.py`
- `scripts/customization_config.py`
