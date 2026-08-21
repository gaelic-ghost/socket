---
name: repository-operations-workflow
description: Route repository work to focused Git, GitHub, documentation, worktree, settings, or release workflows. Use first when a request spans several repository operations or the correct owner is unclear.
---

# Repository Operations Workflow

## Purpose

Provide one entry point for `repository-skills` without turning it into a
catch-all implementation surface. Classify the request, inspect only the state
needed for that classification, then hand work to the narrowest owner.

## Routing

1. Read the closest `AGENTS.md`, inspect `git status --short --branch`, and
   identify the repository root and remote only when the request needs them.
2. Route by the primary outcome:

   | Outcome | Owner |
   | --- | --- |
   | Status, branch, commit, history, rebase, conflict, recovery, or Git-default alignment | `git-workflow` |
   | Pull request, review, issue, CI, or collaboration handoff | `github-collaboration-workflow` |
   | Codex worktree mode, local environment, or app-owned worktree behavior | `codex-gui-worktree-workflow` |
   | Parallel worker branch, worktree, write, or integration ownership | `coordinate-worktrees-and-threads` |
   | GitHub settings, rulesets, security automation, or repository policy | `maintain-github-repository` |
   | README, CONTRIBUTING, AGENTS, or ROADMAP maintenance | The matching `maintain-project-*` document workflow |
   | Coordinated repository-document sweep | `maintain-project-docs` |
   | Version bump, tag, release, publication, or branch-accounting cleanup | `maintain-project-repo` |
3. When the request crosses multiple outcomes, name the sequence and keep each
   mutation with its owning workflow. For example: select a worktree, make a
   focused Git change, prepare a PR, then use the release workflow only after a
   release is explicitly requested.
4. Report the selected owner, observed repository state, required authority,
   and one next action.

## Guardrails

- Do not use a release workflow for ordinary local edits or a GitHub settings
  workflow for pull-request collaboration.
- Do not infer permission to push, merge, tag, delete, publish, or change
  GitHub settings from a read-only request.
- Keep branch/worktree ownership explicit before parallel work; a branch does
  not grant permission to mutate shared repository state.
- Treat Gale's fetch-prune, fast-forward-only pull, and tracking-branch rebase
  preferences as machine-level defaults. Route their inspection and any
  repository-specific override to `git-workflow`; do not install them as
  repository-local configuration.
- On Hermes or another non-Codex host, treat Codex GUI worktree association as
  unavailable and use ordinary Git worktree guidance instead.
