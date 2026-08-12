---
name: git-workflow
description: "Safely inspect and perform everyday Git work: branches, focused commits, history, integration, conflicts, worktrees, and recovery. Use for local version-control tasks that are not GitHub settings or release publication."
---

# Git Workflow

## Purpose

Handle ordinary local Git work with enough evidence to preserve uncommitted
work, branch reachability, and worktree ownership. This workflow does not own
GitHub settings or protected-main releases.

## Workflow

1. Read the closest `AGENTS.md`; inspect `git status --short --branch`,
   `git worktree list`, and the relevant history/diff before a mutation.
2. Inspect the effective Git configuration before an operation depends on fetch,
   pull, or tracking-branch behavior. On Gale-managed machines, expect
   `fetch.prune=true`, `pull.ff=only`, and `branch.autoSetupRebase=always`;
   report any local or worktree override rather than silently changing it. See
   `references/gale-git-baseline.md`.
3. Classify the operation:
   - inspection: status, diff, log, blame, or reachability;
   - focused change: create/switch a branch, stage intentional files, commit;
   - integration: fetch, compare, rebase or merge, resolve conflicts;
   - recovery: reflog, lost commit investigation, or safe restoration plan.
4. Preserve the current work before an operation that rewrites, discards, or
   moves it. Explain the exact target and recovery path before using reset,
   clean, rebase, force push, or branch/worktree deletion.
5. For branch work, use a feature branch and separate worktree when required by
   repository guidance. Never keep the same branch live in two worktrees except
   as a short recovery step.
6. Make focused commits with the repository's required subject format. Review
   staged changes and commit reachability after each shared Git mutation.
7. For integration, fetch first. The normal Gale baseline prunes stale refs and
   refuses pull-created merge commits; newly tracking branches rebase on pull.
   Choose a merge or rebase only when repository policy and the branch's
   publication state justify it. Resolve each conflict from source intent, run
   proportionate validation, and inspect the resulting diff.
8. Before deleting a branch, worktree, ref, or archive, verify reachability and
   complete any repository-required branch accounting.

## Boundaries

- Route GitHub pull requests, reviews, issues, and CI collaboration to
  `github-collaboration-workflow`.
- Route tags, publishing, GitHub releases, and protected-main release cleanup
  to `maintain-project-repo`.
- Route GitHub settings, rulesets, and security configuration to
  `maintain-github-repository`.
- Push, force push, merge, tag, and destructive recovery actions require clear
  user authority or an existing repository-owned release contract.
- Do not encode Gale's machine-level Git baseline as repository-local config in
  a generated template or existing repository.

## Hermes Notes

This is portable guidance. Verify that `git` is installed, the target is a Git
worktree, and the active identity/remotes are the intended ones. Hermes gains
no Git credentials or mutation authority from this skill.
