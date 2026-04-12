# AGENTS.md

## Repository Purpose

- This repository is the superproject for Gale's local Codex plugin and skills monorepo experiment.
- Use it to coordinate Gale's plugin and skills directories under one repo root, with `apple-dev-skills` and `python-skills` as the remaining subtree-managed child repositories.
- Treat this as a conscious stopgap around Codex's current repo-scoped marketplace limits, not as proof that Codex has true shared-parent plugin scoping.
- Treat `socket` as the canonical home for all monorepo-owned nested directories under `plugins/`, plus the repo-root marketplace wiring, release flow, and cross-repo maintainer guidance.
- Treat `plugins/apple-dev-skills/` and `plugins/python-skills/` as the child repositories that still keep upstream subtree sync paths.

## Current Boundaries

- Do not import non-git directories as subtrees.
- Keep `plugins/` as the import surface for both monorepo-owned nested directories and the remaining subtree-managed child repositories.
- Keep `.agents/plugins/marketplace.json` as the repo-root Codex marketplace catalog for this superproject.
- Keep socket-level docs grounded in the actual packaged plugin roots that exist inside the nested directories under `plugins/`. Do not assume every child surface exposes `.codex-plugin/plugin.json` at the directory root.
- When a child repo uses nested plugin packaging such as `plugins/<plugin-name>/`, point the socket marketplace at that actual packaged root instead of inventing a second packaging layer at the superproject root.
- Do not hand-edit or rewrite `apple-dev-skills` or `python-skills` subtree history to make them look monorepo-native. Use explicit subtree sync operations there.
- Do not re-vendor one child plugin repository inside another nested directory when the top-level directory already exists in `socket`. Keep one surviving copy at the superproject layer.

## Working In The Monorepo

- Start from the root docs when the task is about the mixed monorepo model, root marketplace wiring, subtree sync for `apple-dev-skills` or `python-skills`, or monorepo release flow.
- Start from the child repo docs when the task is really about one nested directory's own behavior.
- When a child repository already exists under `plugins/`, do the work in the monorepo copy first unless Gale explicitly asks for a separate checkout, worktree, or direct child-repo workflow.
- For ordinary fixes in monorepo-owned child directories, edit `plugins/<repo-name>/` directly and commit in `socket`. Do not assume an upstream child remote exists.
- For `apple-dev-skills` and `python-skills`, keep the subtree workflow explicit: sync with `git subtree pull --prefix=plugins/<repo-name> <remote> <branch>` or publish back with `git subtree push --prefix=plugins/<repo-name> <remote> <branch>` in dedicated commits.
- When importing or reintroducing a subtree-managed child repository later, add or update the matching named git remote first, then use `git subtree add --prefix=plugins/<repo-name> <remote> <branch>` in a dedicated commit.
- When a child repo gains, removes, or moves plugin packaging, update `.agents/plugins/marketplace.json`, `README.md`, and the maintainer docs in the same pass.
- Keep superproject commits focused on one kind of change at a time: subtree work, nested-directory packaging work, marketplace wiring, docs alignment, or release.
- Before removing a nested directory, a subtree, or changing its packaging path, verify whether the socket marketplace or root docs still reference it.

## Source Of Truth

1. `README.md`
2. `docs/maintainers/subtree-workflow.md`
3. `docs/maintainers/subtree-migration-plan.md`
4. `docs/maintainers/plugin-alignment-plan.md`
5. `docs/maintainers/plugin-packaging-strategy.md`
6. root repo files in this superproject
7. nested directories under `plugins/`
