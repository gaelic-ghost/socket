# Release Modes

This document names the release modes used by `socket` so maintainer work follows the same local-first shape as `productivity-skills:maintain-project-repo` while still respecting `socket`'s mixed monorepo and subtree responsibilities.

## Mode Summary

Use `standard` when the release belongs only to the `socket` superproject. Use `subtrees` when the release also needs explicit accounting for subtree-managed child repositories.

Both modes treat `socket` as the release owner for the umbrella repository:

1. make the intended commits
2. validate the changed surface
3. run the relevant temporary `CODEX_HOME` smoke check from [`plugin-install-testing.md`](./plugin-install-testing.md)
4. publish through a branch and pull request when the change is not already on `main`
5. check CI and fix failures before continuing
6. check PR comments and requested changes before continuing
7. merge to `main`
8. fast-forward local `main`
9. create the `socket` tag locally from the reviewed `main`
10. push the tag
11. create the GitHub release from the existing tag
12. verify the GitHub release object exists
13. verify `git log origin/main..main` is empty
14. account for every local branch not contained by `main`
15. refresh the local Codex marketplace cache with `codex plugin marketplace upgrade socket`
16. refresh the Mac mini Codex marketplace cache over SSH when it is reachable

The marketplace cache refreshes are always the final release steps. Never run
them before the GitHub release exists and has been verified, subtree accounting
is complete, and branch accounting has been recorded. The Mac mini refresh is
best-effort and should report clearly when the remote host is unavailable.

The difference is that `subtrees` adds a child-repository sync gate before tagging or before claiming the release is done.

## Standard Mode

Use `standard` for root docs, root marketplace metadata, root validation scripts, monorepo-owned child directories, and shared version bumps that do not need child-repository subtree synchronization.

Standard mode should feel like the protected-main flow from `maintain-project-repo`: changes land through the normal `socket` branch or local-main path, CI and review comments are cleared before tagging, local `main` is fast-forwarded after merge, and the tag is created from the reviewed `main` commit.

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

`patch-refresh` bumps the shared patch version, validates root marketplace
metadata, commits and pushes `main`, pushes any required subtree split, runs the
`release-ready` gate, tags `main`, publishes and verifies the GitHub release,
verifies branch accounting, runs `codex plugin marketplace upgrade socket`, and
then tries a best-effort Mac mini refresh over SSH. If local branches are not
contained by `main`, the helper stops during its branch-accounting preflight
before it bumps the version; after accounting for those branches explicitly, a
trusted maintainer may rerun with:

```bash
scripts/release.sh patch-refresh --allow-unmerged-branches
```

After a version bump lands on `main`, run the executable pre-tag gate:

```bash
scripts/release.sh release-ready X.Y.Z
```

Only after that gate passes, create the matching `vX.Y.Z` tag from `main`, push
it, create the GitHub release with `gh release create --verify-tag`, verify the
release object, complete branch accounting, run `codex plugin marketplace
upgrade socket`, and refresh the Mac mini marketplace cache over SSH when it is
reachable.

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
- run the relevant temporary `CODEX_HOME` smoke check from [`plugin-install-testing.md`](./plugin-install-testing.md)
- confirm local `main` is fast-forwarded to `origin/main`
- run `scripts/release.sh release-ready X.Y.Z`
- confirm `git log origin/main..main` is empty
- enumerate every local branch not contained by `main` and account for each one

After tagging:

- push the `socket` tag
- create the GitHub release from the existing tag
- verify the release object exists on GitHub
- if a child release landed outside `socket`, verify `socket` either contains that child state or explicitly records why the sync is deferred. For Speak Swiftly, the Socket catalog follows `gaelic-ghost/SpeakSwiftlyServer` directly, so standalone SpeakSwiftlyServer releases normally require no local subtree sync.
- confirm `git log origin/main..main` is empty
- enumerate every local branch not contained by `main` and account for each one
- run `codex plugin marketplace upgrade socket` so Gale's local Codex install sees the released marketplace state; this must not happen earlier
- refresh the Mac mini marketplace cache over SSH when it is reachable; report the remote failure clearly when it is not
