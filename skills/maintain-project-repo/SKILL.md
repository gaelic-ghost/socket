---
name: maintain-project-repo
description: Install or refresh deterministic FSX repository maintenance, maintain all four canonical project documents, validate and synchronize repository assets, and operate protected-main releases.
license: Apache-2.0
metadata:
  semver: 1.0.0
---

# Maintain Project Repo

## Purpose

Install one repo-owned F# script runtime behind a small `just` interface. The
runtime owns repository validation, shared-asset synchronization, canonical
documentation, and bounded protected-main release operations.

## Required Interface

Run repository work through `just`. Documentation has exactly two public
commands and both always process README.md, CONTRIBUTING.md, AGENTS.md, and
ROADMAP.md as one transaction:

```text
just docs-check
just docs-apply
```

The remaining managed commands are:

```text
just repo-validate
just repo-sync
just repo-release-prepare <version>
just repo-release-inspect <version>
just repo-release-advance <version>
```

Never add per-document recipes, direct operator-facing script commands, Python
or shell implementations, compatibility wrappers, or alternate documentation
modes.

## Installation Workflow

1. Confirm the target is the repository root and select `generic` or
   `xcode-workspace` explicitly.
2. Use `scripts/maintain-project-repo.fsx` from this skill for `install`,
   `refresh`, or `report-only`.
3. Install the fixed manifest under `scripts/repo-maintenance/`, the managed
   Just import, and the GitHub validation workflow.
4. Install or refresh the four documentation contracts and templates.
5. Run the full documentation transaction: apply for install/refresh and check
   for report-only.
6. Run the target repository's `just repo-validate` after mutation.

The installer preserves repo-owned files outside the managed manifest. It does
not infer profiles, accept project-local schemas, or expose skip-docs behavior.

## Documentation Contract

The four document-owner skills provide fixed JSON contracts and Markdown
templates. `maintain-project-docs.fsx` loads all four in a fixed order, audits
responsibility boundaries, plans every change before writing, applies writes
atomically, and verifies the result. Apply is idempotent.

Customization is intentionally narrow: repositories supply their substantive
project content inside the canonical sections. They cannot customize document
names, required headings, aliases, ordering, status vocabulary, normalization,
or fix policy.

## Managed Layout

```text
scripts/repo-maintenance/
  maintain-project-docs.fsx
  repo-maintenance.fsx
  repo-maintenance.just
  managed-assets.json
  docs/
  validations/
  syncing/
  version-bump.fsx             # optional repo-owned release hook
.github/workflows/
  validate-repo-maintenance.yml
```

Ordered validation and synchronization hooks are `.fsx` files. The runtime
discovers them lexically and invokes them through `dotnet fsi`. Hook filenames
and arguments are the extension boundary; there is no persistent policy file.

## Validation and Synchronization

- `just repo-validate` verifies the managed manifest and Just import, then runs
  every root-owned validation hook.
- `just repo-sync` runs every root-owned synchronization hook and then validates.
- CI calls `just repo-validate`; it does not duplicate repository policy.
- End-to-end tests live only at the target repository root. Do not install or
  retain nested test suites inside skills or managed directories.

## Release Workflow

Use the standard protected-main path only when the user asks to release:

1. `repo-release-prepare` validates, performs the repo-owned version bump,
   checks release notes, commits the release branch, pushes it, and creates or
   updates its PR.
2. `repo-release-inspect` checks the saved branch, commit, PR, checks, reviews,
   comments, base branch, and tag identities without polling.
3. `repo-release-advance` repeats identity checks, merges only when every gate
   passes, updates the owning main worktree, tags, pushes, creates the GitHub
   release, and performs branch accounting.

Prerelease SemVer tags create GitHub prereleases. Checked-in notes under
`docs/releases/` are preferred. Never delete branches, worktrees, refs, or
release state until every unmerged branch is explicitly accounted for.

## Guards

- Treat repository-skills 10.0.2 as the migration baseline; do not copy behavior
  from an earlier installed version.
- Stop when a managed target is not a regular file or when both legacy and
  canonical toolkit roots exist.
- Stop on unsupported profiles, operations, hook extensions, release states,
  or document contract violations.
- Do not write repository-local Git defaults.
- Do not add Python, shell, YAML customization, per-file documentation commands,
  nested tests, or transitional duplicate paths.

## References

- `references/document-boundaries.md`
- `references/repo-maintenance-layout.md`
- `references/release-modes.md`
- `references/pre-commit-vs-ci.md`
- `references/automation-prompts.md`
- `references/project-docs-maintenance-automation-prompts.md`

## Script Inventory

- `scripts/maintain-project-repo.fsx`
- `scripts/maintain-project-docs.fsx`
