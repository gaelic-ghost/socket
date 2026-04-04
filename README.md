# agent-plugin-skills

Canonical repo-maintainer skills for building, aligning, and evolving agent-skills and agent-plugin repositories.

For maintainer policy, source-of-truth order, and standards references, see [AGENTS.md](./AGENTS.md).

## Active Skills

- `maintain-plugin-docs`
  - Current implementation: audit and bounded fixes for `README.md`, `ROADMAP.md`, or both in stack-specific skills and plugin repositories.
  - Intended scope: become the combined docs maintainer for plugin-development repos here, pairing the current specialized README maintenance with the same checklist-style roadmap maintenance model used by `maintain-project-roadmap`.
  - Install guidance should prioritize Codex Plugin and Claude Code Plugin setup first, with `npx skills` per-skill and `--all` installs treated as secondary.
- `bootstrap-skills-plugin-repo`
  - Use when creating or structurally aligning a skills or plugin repository to the shared plugin-first layout.
- `install-plugin-to-socket`
  - Current implementation: audit, install, refresh, or detach an in-development Codex plugin at repo or personal scope with bounded marketplace merging.
  - It follows the documented Codex local-plugin flow: local plugin directory plus marketplace wiring, then restart and verification.
  - It stays honest about scope and does not claim undocumented control over Codex's installed-plugin cache internals.
- `sync-skills-repo-guidance`
  - Current scope: ongoing maintenance and alignment of agent-skills and plugin-development guidance, maintainer docs, discovery mirrors, and related docs links for this repo pattern.
  - Current automation is narrower than the long-term intent: the script audits local guidance snippets and symlink mirrors, while broader link and policy reconciliation is still maintainer-driven.
- `validate-plugin-install-surfaces`
  - Current implementation: audit-only validation for skill metadata overlays, plugin manifests, marketplace wiring, discovery mirrors, and README install examples.
  - It treats root `skills/` as canonical and reports structural drift without mutating the repo.

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

These skills are meant to be installed repo-locally into a repository where an agent-skills plugin is being developed. They are designed to support Gale or another coding agent working inside that target repo, including automation and subagent-style maintenance passes.

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
uv run --group dev python /Users/galew/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/maintain-plugin-docs
uv run --group dev python /Users/galew/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/bootstrap-skills-plugin-repo
uv run --group dev python /Users/galew/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/install-plugin-to-socket
uv run --group dev python /Users/galew/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/sync-skills-repo-guidance
uv run --group dev python /Users/galew/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/validate-plugin-install-surfaces
```

## Install

### Codex Plugin

This repository ships a Codex plugin package at [`plugins/agent-plugin-skills/.codex-plugin/plugin.json`](./plugins/agent-plugin-skills/.codex-plugin/plugin.json), with the local marketplace entry already wired in [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json).

For local development, the primary Codex install path is the plugin surface rooted at [`plugins/agent-plugin-skills`](./plugins/agent-plugin-skills). To mirror that plugin into another repo-scoped or personal Codex install surface, use the `install-plugin-to-socket` skill from this repo.

### Claude Code Plugin

This repository also ships a Claude plugin manifest at [`plugins/agent-plugin-skills/.claude-plugin/plugin.json`](./plugins/agent-plugin-skills/.claude-plugin/plugin.json), and keeps the canonical authored skills mirrored into [`.claude/skills`](./.claude/skills) for Claude Code discovery.

Use those plugin and discovery surfaces as the primary Claude Code installation path for this repo family before reaching for secondary distribution channels.

### Vercel `skills` CLI

Install one skill through the Vercel `skills` CLI:

```bash
npx skills add gaelic-ghost/agent-plugin-skills --skill maintain-plugin-docs
```

Install all active skills:

```bash
npx skills add gaelic-ghost/agent-plugin-skills --all
```

Common starting points:

- plugin-docs maintenance:
  `npx skills add gaelic-ghost/agent-plugin-skills --skill maintain-plugin-docs`
- repo bootstrap or structural alignment:
  `npx skills add gaelic-ghost/agent-plugin-skills --skill bootstrap-skills-plugin-repo`
- local Codex plugin wiring for repo or personal scope:
  `npx skills add gaelic-ghost/agent-plugin-skills --skill install-plugin-to-socket`
- repo-wide guidance sync:
  `npx skills add gaelic-ghost/agent-plugin-skills --skill sync-skills-repo-guidance`
- install-surface and metadata validation:
  `npx skills add gaelic-ghost/agent-plugin-skills --skill validate-plugin-install-surfaces`

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
│   ├── install-plugin-to-socket/
│   ├── maintain-plugin-docs/
│   ├── sync-skills-repo-guidance/
│   └── validate-plugin-install-surfaces/
├── docs/
│   └── maintainers/
├── ROADMAP.md
└── pyproject.toml
```

## License

Apache License 2.0. See [LICENSE](./LICENSE).
