# Release Modes

This document names the release modes used by `socket` so maintainer work follows the same local-first shape as `productivity-skills:maintain-project-repo` while still respecting `socket`'s mixed monorepo and subtree responsibilities.

## Mode Summary

Use `standard` when the release belongs only to the `socket` superproject. Use `subtrees` when the release also needs explicit accounting for subtree-managed child repositories.

Both modes treat `socket` as the release owner for the umbrella repository. Prepare implementation changes in a branch-backed worktree by default, then use the clean `main` checkout for reviewed release verification after merge:

1. make the intended commits
2. validate the changed surface
3. publish through a branch and pull request unless Gale explicitly approved direct-main release work
4. check CI and fix failures before continuing
5. check PR comments and requested changes before continuing
6. merge to `main`
7. fast-forward local `main`
8. run the `release-ready` gate
9. capture release evidence from the reviewed `main` commit with `scripts/release.sh release-evidence`
10. generate the release-note draft with `scripts/release.sh release-notes X.Y.Z`
11. create the `socket` tag locally from the reviewed `main`
12. push the tag
13. create the GitHub release from the existing tag
14. verify the GitHub release object exists
15. verify `git log origin/main..main` is empty
16. account for every local branch not contained by `main`
17. refresh the local Codex marketplace cache with `codex plugin marketplace upgrade socket`

The marketplace cache refreshes are always the final release steps. Never run
them before the GitHub release exists and has been verified, subtree accounting
is complete, and branch accounting has been recorded.

The difference is that `subtrees` adds a child-repository sync gate before tagging or before claiming the release is done.

## Standard Mode

Use `standard` for root docs, root marketplace metadata, root validation scripts, monorepo-owned child directories, and shared version bumps that do not need child-repository subtree synchronization.

Standard mode should feel like the protected-main flow from `maintain-project-repo`: changes land through the normal `socket` branch and worktree path unless Gale explicitly approved direct-main release work, CI and review comments are cleared before tagging, local `main` is fast-forwarded after merge, and the tag is created from the reviewed `main` commit.

The root version helper remains a version-surface tool, not the full release driver:

```bash
scripts/release.sh inventory
scripts/release.sh patch
scripts/release.sh minor
scripts/release.sh major
scripts/release.sh custom 1.2.3
```

Trusted maintainers can use the patch-refresh helper when the intended release
is the standard patch-only Socket refresh described above:

```bash
scripts/release.sh patch-refresh
```

`patch-refresh` is the main direct-main exception. It bumps the shared patch version, validates root marketplace
metadata, commits and pushes `main`, pushes any required subtree split, runs the
`release-ready` gate, captures commit-bound marketplace and Dependabot evidence,
tags `main`, publishes and verifies the GitHub release with that evidence in the
release notes, verifies branch accounting, and refreshes the local Socket
marketplace cache. The helper tries `codex plugin marketplace upgrade socket`
with a 45-second outer guard first. If the current Codex CLI still fails with
its internal 30-second Git clone timeout and `fatal: early EOF`, the helper
fast-forwards the existing configured Socket marketplace cache from the same Git
source instead of leaving the release half-finished at the final local-refresh
step.
If local branches are not contained by `main`, the helper stops during its
branch-accounting preflight before it bumps the version; after accounting for
those branches explicitly, a trusted maintainer may rerun with:

```bash
scripts/release.sh patch-refresh --allow-unmerged-branches
```

After a version bump lands on `main`, run the executable pre-tag gate:

```bash
scripts/release.sh release-ready X.Y.Z
```

Then capture evidence from that exact commit and generate the release-note
draft:

```bash
scripts/release.sh release-evidence
scripts/release.sh release-notes X.Y.Z > /private/tmp/socket-vX.Y.Z-notes.md
```

The ignored `.socket-release-evidence.json` artifact records the commit,
timestamp, isolated marketplace add/remove result, direct Dependabot API
result, and open-alert details. `release-notes` refuses evidence captured from
a different commit. Re-run `release-evidence` after any commit change.

Only after that gate passes, create the matching `vX.Y.Z` tag from `main`, push
it, create the GitHub release with `gh release create --verify-tag`, verify the
release object, complete branch accounting, run `codex plugin marketplace
upgrade socket`.

## Subtrees Mode

Use `subtrees` when a `socket` release also changes, imports, refreshes, or depends on a currently subtree-managed child repository.

Subtrees mode is standard mode plus this extra gate:

1. identify each subtree-managed child touched by the release
2. classify each touched child as `pull`, `push`, or `no subtree action`
3. run the required subtree pull or push before tagging `socket`, or record why no subtree action is correct
4. rerun root validation after any subtree operation
5. re-check `git log origin/main..main` and `git branch --no-merged main` before cleanup or final status

Shared-version-only edits under a subtree-managed child count as `no subtree action` when every touched child file is one of the maintained version surfaces updated by the root version helper, including adjacent `uv.lock` self-version entries. Any other touched file under the child remains substantive and must still pass the subtree accounting gate before tagging.

This mode is not the same as `maintain-project-repo`'s `submodule` mode. `socket` is still the umbrella repository being released, not a child checkout waiting for a parent pointer update.

## Current Subtree Policy

| Child | Prefix | Remote | Direction | Rule |
| --- | --- | --- | --- | --- |
| None | n/a | n/a | n/a | No child plugin currently requires a Socket release-time subtree pull or push. |

`plugins/apple-dev-skills` is now the canonical Socket-hosted Apple Dev Skills payload. The standalone `gaelic-ghost/apple-dev-skills` repository is a compatibility marketplace and README pointer that redirects to Socket, so Socket release tooling must not push the payload subtree back into that compatibility repo unless a future migration explicitly restores that workflow.

## Subtrees Mode Checklist

Before opening or merging the `socket` release PR:

- verify which subtree-managed children are touched
- for `apple-dev-skills`, record `no subtree action` while the standalone repository remains only the compatibility redirect to Socket
- keep subtree sync commits isolated from unrelated docs, marketplace, or version-bump commits

Before tagging `socket`:

- confirm the subtree policy table above was followed
- run `uv run scripts/validate_socket_metadata.py`
- confirm local `main` is fast-forwarded to `origin/main`
- run `scripts/release.sh release-ready X.Y.Z`
- run `scripts/release.sh release-evidence`
- prepare the GitHub release notes with `scripts/release.sh release-notes X.Y.Z`
- confirm `git log origin/main..main` is empty
- enumerate every local branch not contained by `main` and account for each one

After tagging:

- push the `socket` tag
- create the GitHub release from the existing tag
- verify the release object exists on GitHub
- if a child release landed outside `socket`, verify `socket` either contains that child state or explicitly records why the sync is deferred. For Speak Swiftly, the Socket catalog follows `gaelic-ghost/SpeakSwiftlyServer` directly, so standalone SpeakSwiftlyServer releases normally require no local subtree sync.
- confirm `git log origin/main..main` is empty
- enumerate every local branch not contained by `main` and account for each one
- run the Socket marketplace cache refresh so Gale's local Codex install sees the released marketplace state; this must not happen earlier. `patch-refresh` owns the supported retry/fallback path for the known Codex 30-second Git clone timeout.
