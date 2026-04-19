# Release Workflow

## Purpose

This document is the maintainer-facing release contract for the standalone `SpeakSwiftlyServer` repository.

Historical release notes and release checklists live under [`docs/releases`](../releases/). Keep this file focused on the current release process rather than per-release records.

The release surface is intentionally split by checkout authority:

- use `release-prepare.sh` from a feature branch or worktree when the job is "validate this release candidate, push it, open or update the PR, and queue auto-merge"
- use `release-publish.sh` from the release branch when the job is "cut the actual tag and GitHub release from the merged branch tip"

That split keeps branch and worktree automation convenient without letting an unmerged feature branch publish a release tag accidentally.

One practical rule follows from that split: if the commits you want to release are not already on `origin/main`, you are still on the prepare side of the workflow even if those commits currently live in a local `main` checkout. Protected-branch policy and `release-publish.sh` both assume the release tip has already been merged and synced back down to local `main`.

## Context Rules

### Local `main`

Run:

```bash
scripts/repo-maintenance/release-publish.sh --version vX.Y.Z --skip-live-service-refresh
```

That path is the only supported tagged-release publisher. It syncs local `main` with `origin/main`, validates the repo unless told not to, stages the release artifact, creates the annotated tag, pushes the branch and tag, creates the GitHub release, and optionally refreshes the local LaunchAgent-backed live service.

If local `main` is ahead of `origin/main`, stop there. Do not try to force the publish path through that unsynced checkout. Put those commits on a feature branch if needed, run `release-prepare.sh`, merge the PR, fast-forward local `main`, and only then return to `release-publish.sh`.

### Local Feature Branch

Run:

```bash
scripts/repo-maintenance/release-prepare.sh --version vX.Y.Z
```

That path validates the repo unless told not to, stages the candidate artifact under `.release-artifacts/<tag>`, pushes the current branch, opens or updates the pull request, and enables auto-merge by default.

It does **not** create the release tag or GitHub release object.

### Local Worktree

Treat a regular `git worktree` checkout and a Worktrunk-created worktree the same way.

If the worktree is checked out on a feature branch, use `release-prepare.sh`.

If the worktree is checked out on the configured release branch, use `release-publish.sh`.

The worktree manager does not materially change the release semantics. The deciding factor is the checked-out branch and whether that branch is the configured release branch.

## Script Inventory

### `scripts/repo-maintenance/release-prepare.sh`

Purpose:

- branch and worktree release preparation
- branch push
- pull request creation or refresh
- auto-merge enablement

Key flags:

- `--version vX.Y.Z`
- `--base-branch <branch>`
- `--skip-validate`
- `--no-auto-merge`
- `--merge-method <merge|rebase|squash>`
- `--wait-for-merge`
- `--title <text>`
- `--body-file <path>`
- `--draft`
- `--dry-run`

### `scripts/repo-maintenance/release-publish.sh`

Purpose:

- final tagged release cut from the release branch
- tag push
- GitHub release creation
- optional live-service refresh

Key flags:

- `--version vX.Y.Z`
- `--mode <standard|submodule>`
- `--skip-validate`
- `--skip-gh-release`
- `--refresh-live-service`
- `--skip-live-service-refresh`
- `--live-service-config-file <path>`
- `--dry-run`

### `scripts/repo-maintenance/release.sh`

Purpose:

- compatibility dispatcher

Behavior:

- `release.sh prepare ...` dispatches to `release-prepare.sh`
- `release.sh publish ...` dispatches to `release-publish.sh`
- `release.sh ...` without a subcommand defaults to the publish path and refuses to run from a non-release branch

## Expected Flow

### Branch Or Worktree Prepare

1. finish the release candidate work on a feature branch
2. keep the worktree clean
3. run `release-prepare.sh --version vX.Y.Z`
4. let GitHub checks run
5. let auto-merge land the PR

If you accidentally made the release-candidate commits directly on local `main`, branch from that tip before continuing so the rest of the workflow still goes through `release-prepare.sh` and a normal PR merge.

### Main Publish

1. switch to `main`
2. ensure the checkout is clean
3. run `release-publish.sh --version vX.Y.Z`
4. run the current transport smoke gate or equivalent post-publish health verification

The current opt-in live E2E gate is:

```bash
SPEAKSWIFTLYSERVER_E2E=1 xcrun swift test --filter ServerTransportE2ETests
```

Use that smoke suite when you want one repo-owned proof that the shipped server can still boot the published runtime and answer over both HTTP and MCP. For the full maintainer verification path, pair it with the staged healthcheck and any live-service refresh steps documented in [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Defaults

The release defaults live in `scripts/repo-maintenance/config/release.env`.

Current defaults:

- release remote: `origin`
- release branch: `main`
- prepare auto-merge method: `merge`
- live-service refresh: enabled by default for publish

## Safety Properties

- `release-prepare.sh` refuses to run from the configured release branch
- `release-publish.sh` refuses to run from any branch other than the configured release branch
- `release-publish.sh` syncs the local release branch with the remote before tagging
- `release-publish.sh` refuses to publish if local release-branch commits are ahead of the remote
- protected `main` policies are expected to force release-candidate commits through a PR before publish
- both flows require a clean worktree
