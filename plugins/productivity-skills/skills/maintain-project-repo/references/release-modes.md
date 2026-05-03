# Release Modes

## `standard`

Use this mode for an ordinary standalone repository whose release line is a protected `main` branch.

Run it from a feature branch or worktree. Do not run standard release mode from `main`; the script treats `main` as the protected integration branch that receives the release through a pull request.

- run local validation first
- require committed changes and a clean worktree
- run the repo-specific version bump hook at `scripts/repo-maintenance/version-bump.sh`
- commit the version bump as `release: bump versions for vX.Y.Z`
- push the branch
- wait for the pushed branch to become visible on the remote before creating or updating the PR
- open or update a pull request against `main`
- wait for GitHub to report initial PR checks before treating missing checks as a failure
- watch CI
- stop with a clear message if CI is not green so the maintainer can fix the branch, push, and rerun the same script
- wait for PR review/comment state to be readable before making the review-comment gate decision
- check PR review state and comments after CI is green
- stop on requested changes or comments so the maintainer can address valid concerns, add out-of-scope concerns to `ROADMAP.md`, resolve the threads, push, and rerun the same script
- merge the PR with a merge commit once CI is green and the comment pass is clear
- fast-forward local `main` from `origin/main`
- create the annotated release tag locally from the reviewed local `main`
- push the tag
- wait for the pushed tag to become visible on the remote before creating the GitHub release
- create the GitHub release unless skipped
- wait for the GitHub release object to become readable after creation
- prune stale remote tracking refs and delete local branches already merged into `main` where safe

Example:

```bash
bash scripts/repo-maintenance/release.sh --mode standard --version v1.2.0
```

When a release intentionally has no repo version surfaces, pass `--skip-version-bump`. When the PR comment pass has already been handled and only historical comments remain visible through GitHub, rerun with `--review-comments-addressed`.

GitHub visibility waits default to `REPO_MAINTENANCE_GH_WAIT_TIMEOUT_SECONDS=120` and `REPO_MAINTENANCE_GH_WAIT_POLL_SECONDS=5`. More specific overrides such as `REPO_MAINTENANCE_INITIAL_CHECK_TIMEOUT_SECONDS`, `REPO_MAINTENANCE_PR_REVIEW_TIMEOUT_SECONDS`, `REPO_MAINTENANCE_REMOTE_BRANCH_TIMEOUT_SECONDS`, `REPO_MAINTENANCE_REMOTE_TAG_TIMEOUT_SECONDS`, and `REPO_MAINTENANCE_GH_RELEASE_TIMEOUT_SECONDS` can narrow individual gates without editing the script. Timeout failures should name the delayed surface and the last observed state so maintainers can tell indexing lag apart from real CI, review, branch, tag, or release failures.

## `submodule`

Use this mode when the current repository is checked out as a git submodule inside a larger parent repository:

- run local validation first
- require a clean worktree
- require an actual superproject relationship
- create the release tag locally
- push the branch and tag in the submodule repository
- wait for the pushed branch and tag to become visible on the remote
- create the GitHub release when `gh` is available
- wait for the GitHub release object to become readable after creation
- leave the parent-repo pointer update as a separate explicit follow-up step

Example:

```bash
bash scripts/repo-maintenance/release.sh --mode submodule --version v1.2.0
```
