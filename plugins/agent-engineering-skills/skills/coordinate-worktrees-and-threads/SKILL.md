---
name: coordinate-worktrees-and-threads
description: Assign worktree, branch, thread, artifact, write, validation, integration, and cleanup ownership before parallel repository work. Use when launching or resuming a worker that will inspect or modify repository state outside the coordinator's single worktree.
---

# Coordinate Worktrees And Threads

Establish repository ownership before a worker begins. A thread is not a
worktree, and a branch is not permission to make shared Git mutations.

## Launch Record

For every worker, record the worker/task identity, coordinator, repository and
base commit, worktree path, branch, read/write scope, allowed Git operations,
validation lane, output/merge target, final report route, and retention or
cleanup decision.

## Rules

- Give parallel writers disjoint files or directories and separate worktrees.
- Serialize Git operations that change shared repository state. A worker must
  not assume it owns tags, merges, release branches, deletion, or cleanup.
- Serialize heavy build and test lanes unless the environment explicitly proves
  they are independent and safe.
- Keep final integration, conflict resolution, release, branch accounting, and
  cleanup with the coordinator unless the user explicitly assigns them.
- When a worker returns, report branch/worktree state, commits, validation,
  uncommitted changes, artifacts, and the recommended integration action.

## Completion

The coordinator explicitly chooses whether to retain the worker thread or
worktree for follow-up, merge/preserve its result, archive it, or remove it
after branch accounting. Never delete a worktree or branch merely because a
worker says it is done.
