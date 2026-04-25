# Release Modes

This document names the release modes used by `socket` so maintainer work follows the same local-first shape as `productivity-skills:maintain-project-repo` while still respecting `socket`'s mixed monorepo and subtree responsibilities.

## Mode Summary

Use `standard` when the release belongs only to the `socket` superproject. Use `subtrees` when the release also needs explicit accounting for subtree-managed child repositories.

Both modes treat `socket` as the release owner for the umbrella repository:

1. make the intended commits
2. validate the changed surface
3. publish through a branch and pull request when the change is not already on `main`
4. check CI and fix failures before continuing
5. check PR comments and requested changes before continuing
6. merge to `main`
7. fast-forward local `main`
8. create the `socket` tag locally from the reviewed `main`
9. push the tag
10. create the GitHub release from the existing tag
11. verify `git log origin/main..main` is empty
12. account for every local branch not contained by `main`

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

After a version bump lands on `main`, create the matching `vX.Y.Z` tag from `main`, push it, and create the GitHub release with `gh release create --verify-tag`.

## Subtrees Mode

Use `subtrees` when a `socket` release also changes, imports, refreshes, or depends on one of the remaining subtree-managed child repositories.

Subtrees mode is standard mode plus this extra gate:

1. identify each subtree-managed child touched by the release
2. classify each touched child as `pull-only`, `push-out`, or `no subtree action`
3. run the required subtree pull or push before tagging `socket`, or record why no subtree action is correct
4. rerun root validation after any subtree operation
5. re-check `git log origin/main..main` and `git branch --no-merged main` before cleanup or final status

This mode is not the same as `maintain-project-repo`'s `submodule` mode. `socket` is still the umbrella repository being released, not a child checkout waiting for a parent pointer update.

## Current Subtree Policy

| Child | Prefix | Remote | Direction | Rule |
| --- | --- | --- | --- | --- |
| `apple-dev-skills` | `plugins/apple-dev-skills` | `apple-dev-skills` | pull and push | Work may start in `socket`; push back with `git subtree push` when the child repo should receive the socket-authored change. |
| `SpeakSwiftlyServer` | `plugins/SpeakSwiftlyServer` | `speak-swiftly-server` | pull-only | Build, validate, tag, release, and live-refresh in the standalone SpeakSwiftlyServer checkout, then pull the merged child state into `socket`. Do not subtree-push SpeakSwiftlyServer from `socket` unless Gale explicitly overrides this rule. |

## Subtrees Mode Checklist

Before opening or merging the `socket` release PR:

- verify which subtree-managed children are touched
- for `SpeakSwiftlyServer`, verify the standalone checkout already owns the child release or say plainly that the socket sync is intentionally deferred
- for `apple-dev-skills`, decide whether the socket commit must be pushed back to the child remote before the umbrella release
- keep subtree sync commits isolated from unrelated docs, marketplace, or version-bump commits

Before tagging `socket`:

- confirm the subtree policy table above was followed
- run `uv run scripts/validate_socket_metadata.py`
- confirm local `main` is fast-forwarded to `origin/main`
- confirm `git log origin/main..main` is empty
- enumerate every local branch not contained by `main` and account for each one

After tagging:

- push the `socket` tag
- create the GitHub release from the existing tag
- verify the release object exists on GitHub
- if a child release landed outside `socket`, verify `socket` either contains that child state or explicitly records why the sync is deferred
