# AGENTS.md

## Repository Purpose

- This repository is the superproject for Gale's local Codex plugin and skills monorepo experiment.
- Use it to coordinate subtree-based imports of adjacent plugin and skills repositories into one repo root.
- Treat this as a conscious stopgap around Codex's current repo-scoped marketplace limits, not as proof that Codex has true shared-parent plugin scoping.

## Current Boundaries

- Do not import non-git directories as subtrees.
- Do not delete or rewrite the source repositories during early migration work.
- Prefer subtree imports over submodules here because preserving one Git root is the point of the experiment.
- Keep `plugins/` as the import surface for subtree-managed child repositories.
- Keep `.agents/plugins/marketplace.json` as the repo-root Codex marketplace catalog for this superproject.

## Source Of Truth

1. `docs/maintainers/subtree-migration-plan.md`
2. root repo files in this superproject
3. imported subtree directories under `plugins/`
