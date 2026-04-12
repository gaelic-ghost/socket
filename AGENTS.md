# AGENTS.md

## Repository Purpose

- This repository is the superproject for Gale's local Codex plugin and skills monorepo experiment.
- Use it to coordinate subtree-based imports of adjacent plugin and skills repositories into one repo root.
- Treat this as a conscious stopgap around Codex's current repo-scoped marketplace limits, not as proof that Codex has true shared-parent plugin scoping.
- Treat `socket` as the canonical home for superproject concerns only: subtree imports, repo-root marketplace wiring, release flow, and cross-repo maintainer guidance.
- Treat each imported child repository under `plugins/` as the canonical home for its own skills, plugin manifests, tests, release notes, and repository-local maintainer docs unless the task is explicitly about the superproject layer.

## Current Boundaries

- Do not import non-git directories as subtrees.
- Do not delete or rewrite the source repositories during early migration work.
- Prefer subtree imports over submodules here because preserving one Git root is the point of the experiment.
- Keep `plugins/` as the import surface for subtree-managed child repositories.
- Keep `.agents/plugins/marketplace.json` as the repo-root Codex marketplace catalog for this superproject.
- Keep socket-level docs grounded in the actual packaged plugin roots that exist inside imported subtrees. Do not assume every child repo exposes `.codex-plugin/plugin.json` at the subtree root.
- When a child repo uses nested plugin packaging such as `plugins/<plugin-name>/`, point the socket marketplace at that actual packaged root instead of inventing a second packaging layer at the superproject root.
- Do not import or retain private child repositories in this public `socket` superproject. Keep private repos excluded from both `plugins/` and the root marketplace.
- Do not hand-edit or rewrite imported child repo history to make it look monorepo-native. Use subtree sync operations and explicit commits instead.
- Do not re-vendor one child plugin repository inside another imported subtree when the top-level subtree already exists in `socket`. Keep one surviving copy at the superproject layer.

## Working In The Monorepo

- Start from the root docs when the task is about subtree imports, root marketplace wiring, or monorepo release flow.
- Start from the child repo docs when the task is really about one imported repo's own behavior.
- When a child repository already exists under `plugins/`, do the work in the monorepo copy first unless Gale explicitly asks for a separate checkout, worktree, or direct child-repo workflow.
- For ordinary child-repo fixes that should publish back to the source repository, prefer this sequence: edit `plugins/<repo-name>/`, commit in `socket`, then use `git subtree push --prefix=plugins/<repo-name> <remote> <branch>` instead of cloning a temporary standalone checkout.
- When importing a new child repository, add or update the matching named git remote first, then use `git subtree add --prefix=plugins/<repo-name> <remote> <branch>` in a dedicated commit.
- When syncing an existing child repository, use `git subtree pull --prefix=plugins/<repo-name> <remote> <branch>` in a dedicated commit and re-check any affected socket docs or marketplace paths immediately afterward.
- When a child repo gains, removes, or moves plugin packaging, update `.agents/plugins/marketplace.json`, `README.md`, and the maintainer docs in the same pass.
- Keep superproject commits focused on one kind of change at a time: subtree import or sync, marketplace wiring, docs alignment, or release.
- Before removing an imported subtree or changing its packaging path, verify whether the socket marketplace or root docs still reference it.

## Source Of Truth

1. `docs/maintainers/subtree-migration-plan.md`
2. `docs/maintainers/subtree-workflow.md`
3. `docs/maintainers/plugin-alignment-plan.md`
4. `docs/maintainers/plugin-packaging-strategy.md`
5. root repo files in this superproject
6. imported subtree directories under `plugins/`
