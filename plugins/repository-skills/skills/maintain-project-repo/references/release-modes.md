# Release Modes

Use these modes only when the current task is actually a release, publish, merge, tag, or protected-main release preparation task. They are not the default completion path for ordinary questions, investigations, local edits, documentation maintenance, or targeted validation.

## `standard`

Use this mode for an ordinary standalone repository whose release line is a protected `main` branch.

Run it from a feature branch or worktree. Do not run standard release mode from `main`; the script treats `main` as the protected integration branch that receives the release through a pull request.

- run `--operation prepare` for local validation, the version bump, branch push, PR creation, one remote snapshot, and a continuation packet
- require committed changes and a clean worktree
- run the repo-specific version bump hook at the selected profile root:
  `scripts/repo-maintenance/version-bump.sh` for `generic` or
  `Scripts/repo-maintenance/version-bump.sh` for `xcode-workspace`
- commit the version bump as `release: bump versions for vX.Y.Z`
- push the branch
- perform one immediate branch-visibility re-read; if it is not visible, emit a continuation packet instead of polling
- open or update a pull request against `main`
- use `--operation inspect` for one PR/check/review snapshot; it emits a continuation packet for unknown or pending remote state
- create one host-native continuation no sooner than five minutes later, then reuse that same matching scheduler item while the gate stays pending and healthy; do not delete/recreate it after an unchanged snapshot. Codex uses heartbeat, Hermes uses an updated continuable `cronjob` with `deliver="origin"` and `attach_to_session=true`
- on wakeup run `inspect` first, then use `--operation advance` only if the packet's branch, commit, PR, and tag identities still match
- stop with a clear message if CI fails, changes are requested, or unresolved comments remain; an explicit CodeRabbit quota, usage, rate, or review-limit diagnostic is non-blocking because it produced no review, but all other CodeRabbit contexts and comments still block
- stop on requested changes or comments so the maintainer can address valid concerns, add out-of-scope concerns to `ROADMAP.md`, resolve the threads, push, and rerun the same script
- merge the PR with a merge commit once CI is green and the comment pass is clear
- fast-forward local `main` from `origin/main`
- create the annotated release tag locally from the reviewed local `main`
- push the tag
- perform one immediate tag-visibility re-read; if it is not visible, emit a continuation packet instead of polling
- create the GitHub release unless skipped, preferring `docs/releases/vX.Y.Z.md` and then `docs/releases/X.Y.Z.md` as its checked-in body; when neither exists, log the fallback and use GitHub-generated notes. Pass `--prerelease` for SemVer prerelease tags such as `vX.Y.Z-alpha.N`, `vX.Y.Z-beta.N`, `vX.Y.Z-rc.N`, or preview-style suffixes
- perform one immediate GitHub-release re-read; if it is not readable, emit a continuation packet instead of polling
- verify the GitHub release object's prerelease metadata matches the release tag before calling release publication complete
- verify `git log origin/main..main` or the repository's equivalent base/remote comparison is empty before claiming the local base branch is synchronized
- enumerate every local branch still not contained by `main` and account for each branch as already preserved elsewhere, intentionally still in progress, newly archived, newly merged, or safe to delete
- prune stale remote tracking refs and delete only local branches already merged into `main` after branch accounting proves they are safe

Treat branch accounting as a hard completion gate, not optional cleanup. Use `git branch --no-merged <base>` or the repository's equivalent branch inventory before cleanup, and do not say a release, publish, merge, or cleanup step is done until every local branch not contained by the local base branch has been accounted for. Do not say work is on `main`, merged, recovered, preserved, or safe to clean up until commit reachability has been verified in the exact local repository and remote that statement refers to. Do not delete local branches, remote branches, worktrees, archive refs, or temporary rescue refs until branch accounting is complete and any non-base history is either merged or preserved on an explicit archive ref.

Example:

```bash
bash scripts/repo-maintenance/release.sh --mode standard --version v1.2.0 --operation prepare
```

When a release intentionally has no repo version surfaces, pass `--skip-version-bump`. When the PR comment pass has already been handled and only historical comments remain visible through GitHub, rerun with `--review-comments-addressed`.

Remote waiting is never a release-script operation. `prepare`, `inspect`, and `advance` each take one bounded snapshot and either make an immediate safe transition or emit a continuation packet. Agents create one host-native wakeup no sooner than five minutes later, reuse that same matching scheduler item while the gate remains pending and healthy, and pause/delete it only on resolution, failure, cancellation, or identity drift. Create/update a replacement only after the prior item fires or becomes stale. Resume with `inspect`, and use `advance` only after packet identities match. Do not use shell `sleep`, `gh pr checks --watch`, timer loops, or one-to-four-minute rechecks.

## `submodule`

Use this mode when the current repository is checked out as a git submodule inside a larger parent repository:

- run local validation first
- require a clean worktree
- require an actual superproject relationship
- create the release tag locally
- push the branch and tag in the submodule repository
- perform one immediate branch and tag visibility re-read; if either is absent, create or reuse the matching host-native continuation no sooner than five minutes later, then inspect before another release action rather than polling
- create the GitHub release when `gh` is available, passing `--prerelease` for SemVer prerelease tags such as `vX.Y.Z-alpha.N`, `vX.Y.Z-beta.N`, `vX.Y.Z-rc.N`, or preview-style suffixes
- perform one immediate GitHub release re-read after creation; if it is absent, create or reuse the matching host-native continuation no sooner than five minutes later, then inspect before another release action rather than polling
- verify the GitHub release object's prerelease metadata matches the release tag before calling release publication complete
- verify the submodule branch and tag are visible on the intended remote before calling that work preserved or released
- leave the parent-repo pointer update as a separate explicit follow-up step

Example:

```bash
bash scripts/repo-maintenance/release.sh --mode submodule --version v1.2.0
```
