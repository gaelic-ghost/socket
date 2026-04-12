# productivity-skills

Useful productivity skills plus durable template skills that downstream language- and stack-specific repos can adapt.

For maintainer guidance, standards references, and cross-ecosystem packaging policy, see [AGENTS.md](./AGENTS.md).

## Overview

This plugin is active and maintained.

This repository is the general-purpose baseline layer in Gale's skills ecosystem. It ships broadly reusable workflow skills directly from root `skills/`, while narrower repo-maintainer and plugin-maintainer workflows now live in the sibling [`agent-plugin-skills`](../agent-plugin-skills) repository.

Active skills:

- [`explain-code-slice`](./skills/explain-code-slice/SKILL.md)
- [`maintain-project-readme`](./skills/maintain-project-readme/SKILL.md)
- [`maintain-project-agents`](./skills/maintain-project-agents/SKILL.md)
- [`maintain-project-contributing`](./skills/maintain-project-contributing/SKILL.md)
- [`maintain-project-roadmap`](./skills/maintain-project-roadmap/SKILL.md)
- [`maintain-project-repo`](./skills/maintain-project-repo/SKILL.md)

The goal is to keep this repo focused on portable, generally useful workflow help instead of absorbing language-, framework-, or repository-specific specialization.

## Install

Install one skill:

```bash
npx skills add gaelic-ghost/productivity-skills --skill explain-code-slice
```

Install all shipped skills:

```bash
npx skills add gaelic-ghost/productivity-skills --all
```

For local authoring and testing in this repo, the canonical source tree remains [`skills/`](./skills/), with thin discovery mirrors and marketplace metadata pointing back to the same authored skill surface.

## Packaging And Discovery

Discovery and install surfaces in this repository are intentionally thin. Root [`skills/`](./skills/) remains the canonical authored surface, while local discovery mirrors and marketplace catalogs expose that same skill tree directly:

- [`.agents/skills`](./.agents/skills)
- [`.claude/skills`](./.claude/skills)
- [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json)
- [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json)

Helpful references:

- [OpenAI Codex Skills](https://developers.openai.com/codex/skills)
- [OpenAI Codex customization](https://developers.openai.com/codex/concepts/customization/)
- [OpenAI Codex plugins overview](https://developers.openai.com/codex/plugins)
- [OpenAI Codex plugin authoring](https://developers.openai.com/codex/plugins/build)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Claude Code Plugins](https://code.claude.com/docs/en/plugins)

## Development

This repository standardizes maintainer-side Python tooling around `uv`.

```bash
uv sync --dev
uv tool install ruff
uv tool install mypy
uv run --group dev pytest
```

For maintainer workflow guidance, source-of-truth rules, and cross-ecosystem packaging policy, use:

- [AGENTS.md](./AGENTS.md)
- [docs/maintainers/workflow-atlas.md](./docs/maintainers/workflow-atlas.md)
- [docs/maintainers/reality-audit.md](./docs/maintainers/reality-audit.md)

Keep root [`skills/`](./skills/) as the canonical workflow-authoring surface. Treat `.agents/skills` and `.claude/skills` as discovery mirrors, and keep the repo-local marketplace catalogs aligned directly to the same source tree instead of staging nested packaged plugin copies.

When a workflow becomes meaningfully stack-, language-, or repo-specific, prefer moving that stronger specialization into a dedicated adjacent plugin instead of weakening the shared productivity-skills baseline.

Run focused maintainer checks before shipping changes:

```bash
uv run --group dev pytest
```

## Repo Structure

```text
.
├── .agents/
│   ├── skills -> ../skills
│   └── plugins/
│       └── marketplace.json
├── .claude/
│   └── skills -> ../skills
├── .claude-plugin/
│   └── marketplace.json
├── AGENTS.md
├── README.md
├── ROADMAP.md
├── docs/
│   └── maintainers/
├── skills/
│   ├── explain-code-slice/
│   ├── maintain-project-agents/
│   ├── maintain-project-contributing/
│   ├── maintain-project-readme/
│   ├── maintain-project-roadmap/
│   └── maintain-project-repo/
└── pyproject.toml
```

Track in-flight maintainer planning in [ROADMAP.md](./ROADMAP.md) and use Git history plus GitHub releases for shipped release notes.

## License

Apache License 2.0. See [LICENSE](./LICENSE).
