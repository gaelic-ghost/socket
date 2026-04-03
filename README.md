# agent-plugin-skills

Canonical repo-maintainer skills for building, aligning, and evolving agent-skills and agent-plugin repositories.

For maintainer policy, source-of-truth order, and standards references, see [AGENTS.md](./AGENTS.md).

## Active Skills

- `maintain-skills-readme`
  - Current scope: audit and bounded fixes for `README.md` in stack-specific skills and plugin repositories.
  - Planned direction: evolve into a broader stack-specific docs maintainer skill, likely `maintain-plugin-docs`, while preserving a clean boundary from repo-wide guidance sync.
- `bootstrap-skills-plugin-repo`
  - Use when creating or structurally aligning a skills or plugin repository to the shared plugin-first layout.
- `sync-skills-repo-guidance`
  - Current scope: ongoing maintenance and alignment of agent-skills and plugin-development guidance, maintainer docs, discovery mirrors, and related docs links for this repo pattern.
  - Current automation is narrower than the long-term intent: the script audits local guidance snippets and symlink mirrors, while broader link and policy reconciliation is still maintainer-driven.

## Repo Purpose

This repository is intentionally stack-specific.

It is for maintainers working on repositories that package agent capabilities such as:

- skills
- plugins
- MCP server packaging
- OpenAI or MCP apps
- marketplace metadata
- cross-ecosystem docs and guidance drift

It is not meant to be a general productivity helper pack. That boundary keeps this repo coherent and makes global install intent clearer.

## Packaging And Discovery

Root [`skills/`](./skills/) is the canonical authored skill surface. In repo-policy shorthand, keep root `skills/` as the canonical authoring surface.

Plugin, marketplace, MCP, app, and hook manifests stay under [`plugins/`](./plugins/) and [`.agents/plugins/`](./.agents/plugins/).

For local project discovery on macOS and Linux, including WSL 2 when Windows is involved, this repo uses POSIX symlink mirrors instead of duplicate skill trees:

- [`.agents/skills`](./.agents/skills) -> `../skills`
- [`.claude/skills`](./.claude/skills) -> `../skills`
- [`plugins/agent-plugin-skills/skills`](./plugins/agent-plugin-skills/skills) -> `../../skills`

Current packaging surfaces:

- [`plugins/agent-plugin-skills/.codex-plugin/plugin.json`](./plugins/agent-plugin-skills/.codex-plugin/plugin.json)
- [`plugins/agent-plugin-skills/.claude-plugin/plugin.json`](./plugins/agent-plugin-skills/.claude-plugin/plugin.json)
- [`plugins/agent-plugin-skills/hooks/hooks.json`](./plugins/agent-plugin-skills/hooks/hooks.json)
- [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json)

## Standards And Docs

This repo aims for full applicable coverage across the open Agent Skills standard and platform-specific overlays.

Key references:

- Agent Skills Standard: [agentskills.io/home](https://agentskills.io/home)
- Vercel guidance: [vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context](https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context)
- OpenAI Codex Skills: [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills)
- OpenAI Codex Plugins: [developers.openai.com/codex/plugins](https://developers.openai.com/codex/plugins)
- OpenAI Codex Plugin authoring: [developers.openai.com/codex/plugins/build](https://developers.openai.com/codex/plugins/build)
- Claude Code Skills: [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)
- Claude Code Plugins: [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins)
- Anthropic Agent Skills Best Practices: [platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

## Maintainer Python Tooling

```bash
uv sync --dev
uv run --group dev pytest
```

Quick validation examples:

```bash
uv run --group dev python /Users/galew/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/maintain-skills-readme
uv run --group dev python /Users/galew/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/bootstrap-skills-plugin-repo
uv run --group dev python /Users/galew/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/sync-skills-repo-guidance
```

## Install

Install one skill through the Vercel `skills` CLI:

```bash
npx skills add gaelic-ghost/agent-plugin-skills --skill maintain-skills-readme
```

Install all active skills:

```bash
npx skills add gaelic-ghost/agent-plugin-skills --all
```

Common starting points:

- README-only maintenance:
  `npx skills add gaelic-ghost/agent-plugin-skills --skill maintain-skills-readme`
- repo bootstrap or structural alignment:
  `npx skills add gaelic-ghost/agent-plugin-skills --skill bootstrap-skills-plugin-repo`
- repo-wide guidance sync:
  `npx skills add gaelic-ghost/agent-plugin-skills --skill sync-skills-repo-guidance`

## Repository Layout

```text
.
├── .agents/
│   ├── skills -> ../skills
│   └── plugins/
│       └── marketplace.json
├── .claude/
│   └── skills -> ../skills
├── README.md
├── AGENTS.md
├── plugins/
│   └── agent-plugin-skills/
│       ├── .codex-plugin/
│       ├── .claude-plugin/
│       ├── assets/
│       ├── bin/
│       ├── hooks/
│       └── skills -> ../../skills
├── skills/
│   ├── bootstrap-skills-plugin-repo/
│   ├── maintain-skills-readme/
│   └── sync-skills-repo-guidance/
├── docs/
│   └── maintainers/
├── ROADMAP.md
└── pyproject.toml
```

## License

Apache License 2.0. See [LICENSE](./LICENSE).
