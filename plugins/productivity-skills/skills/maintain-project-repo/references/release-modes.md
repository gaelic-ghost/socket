# Release Modes

## `standard`

Use this mode for an ordinary standalone repository whose release line is a protected `main` branch.

Run it from a feature branch or worktree. Do not run standard release mode from `main`; the script treats `main` as the protected integration branch that receives the release through a pull request.

- run local validation first
- require committed changes and a clean worktree
- run the repo-specific version bump hook at `scripts/repo-maintenance/version-bump.sh`
- commit the version bump as `release: bump versions for vX.Y.Z`
- push the branch
- open or update a pull request against `main`
- watch CI
- stop with a clear message if CI is not green so the maintainer can fix the branch, push, and rerun the same script
- check PR review state and comments after CI is green
- stop on requested changes or comments so the maintainer can address valid concerns, add out-of-scope concerns to `ROADMAP.md`, resolve the threads, push, and rerun the same script
- merge the PR with a merge commit once CI is green and the comment pass is clear
- fast-forward local `main` from `origin/main`
- create the annotated release tag locally from the reviewed local `main`
- push the tag
- create the GitHub release unless skipped
- prune stale remote tracking refs and delete local branches already merged into `main` where safe

Example:

```bash
bash scripts/repo-maintenance/release.sh --mode standard --version v1.2.0
```

When a release intentionally has no repo version surfaces, pass `--skip-version-bump`. When the PR comment pass has already been handled and only historical comments remain visible through GitHub, rerun with `--review-comments-addressed`.

## `submodule`

Use this mode when the current repository is checked out as a git submodule inside a larger parent repository:

- run local validation first
- require a clean worktree
- require an actual superproject relationship
- create the release tag locally
- push the branch and tag in the submodule repository
- create the GitHub release when `gh` is available
- leave the parent-repo pointer update as a separate explicit follow-up step

Example:

```bash
bash scripts/repo-maintenance/release.sh --mode submodule --version v1.2.0
```
