# Release Modes

## `standard`

Use this mode for an ordinary standalone repository:

- run local validation first
- require a clean worktree
- create the release tag locally
- push the branch and tag
- create the GitHub release when `gh` is available

Example:

```bash
bash scripts/repo-maintenance/release.sh --mode standard --version v1.2.0
```

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
