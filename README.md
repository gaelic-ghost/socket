# agent-plugin-skills

Canonical repo-maintainer skills for building, aligning, and evolving agent-skills and agent-plugin repositories.

For maintainer policy, source-of-truth order, and standards references, see [AGENTS.md](./AGENTS.md).

## Active Skills

- `maintain-plugin-docs`
  - Current implementation: audit and bounded fixes for `README.md`, `ROADMAP.md`, or both in stack-specific skills and plugin repositories.
  - Intended scope: become the combined docs maintainer for plugin-development repos here, pairing the current specialized README maintenance with the same checklist-style roadmap maintenance model used by `maintain-project-roadmap`.
  - Install guidance should prioritize Codex local plugin installs and Claude Code plugin usage first, with `npx skills` per-skill and `--all` installs treated as secondary.
- `bootstrap-skills-plugin-repo`
  - Use when creating or structurally aligning a skills or plugin repository to the shared plugin-first layout.
- `install-plugin-to-socket`
  - Current implementation: audit, install, refresh, or detach an in-development Codex plugin at repo or personal scope with bounded marketplace merging.
  - It follows the documented Codex local-plugin flow: local plugin directory plus marketplace wiring, then restart and verification.
  - It is also the repair surface for drifted local installs, such as missing staged plugin paths, stale marketplace entries, or the wrong staged materialization mode.
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
uv tool install ruff
uv tool install mypy
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

For Codex local installs, the documented staged paths are:

- personal scope: `~/.codex/plugins/agent-plugin-skills` with `~/.agents/plugins/marketplace.json`
- repo scope: `$REPO_ROOT/plugins/agent-plugin-skills` with `$REPO_ROOT/.agents/plugins/marketplace.json`

Use `install-plugin-to-socket` to merge the marketplace entry safely and stage a copied plugin tree at those paths. Personal scope is the default recommendation unless a repository explicitly needs repo-local plugin wiring.

You can persist that default preference through:

- repo profile: `.codex/profiles/install-plugin-to-socket/customization.yaml`
- global profile: `~/.config/gaelic-ghost/agent-plugin-skills/install-plugin-to-socket/customization.yaml`

Example:

```yaml
schemaVersion: 1
profile: personal-first
isCustomized: true
defaultInstallScope: personal
```

Common workflows:

```bash
# Install into personal scope using the default resolution chain
uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py \
  --source-plugin-root plugins/agent-plugin-skills \
  --action install \
  --run-mode apply

# Refresh the staged copied install after local source changes
uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py \
  --source-plugin-root plugins/agent-plugin-skills \
  --action refresh \
  --run-mode apply

# Remove the local Codex install surface for one plugin
uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py \
  --source-plugin-root plugins/agent-plugin-skills \
  --action detach \
  --run-mode apply
```

### Claude Code Plugin

This repository also ships a Claude plugin manifest at [`plugins/agent-plugin-skills/.claude-plugin/plugin.json`](./plugins/agent-plugin-skills/.claude-plugin/plugin.json).

For local Claude Code development, test the plugin directly from the source repo with `claude --plugin-dir /absolute/path/to/plugins/agent-plugin-skills`. The repo-local [`.claude/skills`](./.claude/skills) mirror remains here for standalone project discovery, but the Codex installer skill in this repo does not manage Claude install surfaces.

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
