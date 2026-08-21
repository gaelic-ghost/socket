# Release Workflow

The managed runtime supports one standard protected-main release workflow.
Run it only for an explicit release task and only through:

```text
just repo-release-prepare <version>
just repo-release-inspect <version>
just repo-release-advance <version>
```

Prepare validates, runs the optional root-owned `version-bump.fsx`, checks
release notes, commits, pushes, and opens or updates the release PR. Inspect
takes one bounded snapshot of identity, CI, reviews, and comments. Advance
rechecks the snapshot, merges only when every gate is clear, updates the owning
main worktree, tags, pushes, publishes, and performs branch accounting.

There is no polling mode. Pending remote state produces a continuation packet.
Never delete branches, worktrees, tags, or refs until reachability and branch
accounting prove the action safe.
