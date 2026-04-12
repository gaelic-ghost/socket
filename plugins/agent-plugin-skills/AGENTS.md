# AGENTS.md

## Repository Role

- This repository is the canonical home for maintainer skills that target skills-export and plugin-export repositories.
- Treat `productivity-skills` as the default baseline maintainer layer for general repo docs and workflow guidance; this repo is the narrower specialist layer for exported-skill and exported-plugin repo shapes.
- Root `skills/` is the canonical authored and exported surface.
- This repo ships source-repo plugin packaging at [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) and intentionally does not keep a repo-local Codex marketplace file for itself.

## Repo-specific Rules

- Keep Codex limitation wording blunt. When this repo discusses Codex plugin export boundaries, say plainly that repo-visible plugins come from the documented marketplace model rather than from a richer repo-private scoping system.
- Do not recreate nested staged plugin directories, repo-local installer workflows, or install-surface validation machinery in this repository unless Gale explicitly asks for that reversal.
- Keep repo-maintainer docs under [`docs/maintainers/`](./docs/maintainers/), and keep installed skills independent from those docs.
- Keep `docs/maintainers/reality-audit.md` and `docs/maintainers/workflow-atlas.md` aligned with the shipped maintainer-skill surface.
