# AGENTS.md

## Repository Scope

- `socket` is Gale's local Codex plugin and skills superproject.
- Use it to coordinate the child repositories under [`plugins/`](./plugins/), the repo-root marketplace at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json), and the root maintainer docs.
- Treat this repository as a conscious stopgap around OpenAI's current documented Codex plugin-scoping limits, not as proof that Codex supports richer shared-parent or repo-private plugin scoping than the documented marketplace model.

## Shared Repo Defaults

- These defaults apply across the nested plugin and skills repositories unless a closer `AGENTS.md` narrows them.
- Treat managed production installs such as `~/.agents/skills` as read-only deployment artifacts while working in these development repositories.
- When a repository ships reusable skills, treat the top-level authored surface such as `skills/`, `mcps/`, or `apps/` as the source of truth. Treat plugin manifests, marketplace files, and nested packaged plugin roots as packaging metadata unless a nearer `AGENTS.md` explicitly says otherwise.
- Keep installed skills independent from repo-level docs under `docs/`.
- Prefer POSIX symlink discovery mirrors over duplicate or hardlinked skill trees when a repo exposes `.agents/skills` or `.claude/skills`.
- Do not track consumer-side install copies, cache directories, or machine-local runtime state in git.
- Keep the same names for the same concepts across `SKILL.md`, `agents/openai.yaml`, docs, automation prompts, scripts, and marketplace metadata.
- If docs and scripts disagree, fix the script or narrow the documented contract so they match.
- When shipped behavior, active skill inventory, packaging roots, or validation commands change, update the relevant docs and `ROADMAP.md` in the same pass unless Gale explicitly says not to.
- For Python-backed skill repositories, prefer `uv sync --dev`, `uv run pytest`, and uv-managed maintainer tools such as `ruff` and `mypy`.
- When OpenAI or Claude product behavior matters, prefer official docs first. When describing Codex plugin boundaries, say plainly that repo-visible plugins come from the documented marketplace model and that OpenAI does not currently document a richer repo-private scoping model.
- Use these terms consistently:
  - `skill`: reusable workflow-authoring unit
  - `plugin`: installable distribution bundle
  - `subagent`: delegated runtime worker with its own context and tool policy

## Monorepo Rules

- Keep `plugins/` as the import surface for both monorepo-owned nested directories and the remaining subtree-managed child repositories.
- `apple-dev-skills`, `python-skills`, and `SpeakSwiftlyServer` are the child repositories here that still keep explicit upstream subtree sync paths.
- Do not import non-git directories as subtrees.
- Do not hand-edit subtree history to make imported child repos look monorepo-native.
- Do not re-vendor one child plugin repo inside another nested directory when the top-level copy already exists in `socket`.
- Keep socket-level docs grounded in the real packaged plugin roots that exist inside the child repos. Do not assume every child surface exposes `.codex-plugin/plugin.json` at its directory root.
- When a child repo uses nested plugin packaging such as `plugins/<plugin-name>/`, point the root marketplace at that real packaged root instead of inventing a second packaging layer at the superproject root.

## Working Here

- Start from the root docs when the task is about the mixed monorepo model, root marketplace wiring, subtree sync for `apple-dev-skills`, `python-skills`, or `SpeakSwiftlyServer`, or superproject release flow.
- Start from the child repo docs when the task is really about one child repo's own behavior.
- When a child repository already exists under `plugins/`, do the work in the monorepo copy first unless Gale explicitly asks for a separate checkout, worktree, or direct child-repo workflow.
- For ordinary fixes in monorepo-owned child directories, edit `plugins/<repo-name>/` directly in `socket`.
- For `apple-dev-skills`, `python-skills`, and `SpeakSwiftlyServer`, keep subtree sync operations explicit:
  - `git subtree pull --prefix=plugins/<repo-name> <remote> <branch>`
  - `git subtree push --prefix=plugins/<repo-name> <remote> <branch>`
- When importing or reintroducing a subtree-managed child repo later, add or update the named git remote first, then use `git subtree add --prefix=plugins/<repo-name> <remote> <branch>` in a dedicated commit.
- When a child repo gains, removes, or moves plugin packaging, update [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json), [README.md](./README.md), and the root maintainer docs in the same pass.

## Source Of Truth

1. [README.md](./README.md)
2. [docs/maintainers/subtree-workflow.md](./docs/maintainers/subtree-workflow.md)
3. [docs/maintainers/subtree-migration-plan.md](./docs/maintainers/subtree-migration-plan.md)
4. [docs/maintainers/plugin-alignment-plan.md](./docs/maintainers/plugin-alignment-plan.md)
5. [docs/maintainers/plugin-packaging-strategy.md](./docs/maintainers/plugin-packaging-strategy.md)
6. root repo files in this superproject
7. nested directories under [`plugins/`](./plugins/)

## Local Overrides

- Nested `AGENTS.md` files under `plugins/` refine this root guidance for their own repo shapes, domain rules, validation paths, and packaging boundaries.
