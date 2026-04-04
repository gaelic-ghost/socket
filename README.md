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
  - Current implementation: audit, install, update, uninstall, verify, repair, enable, disable, or promote an in-development Codex plugin at repo or personal scope with bounded marketplace merging and Codex config-state management.
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

This repo also tracks a repo-root Claude marketplace file at [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json) so the repository itself can be shared as a Git-backed Claude marketplace, while the actual plugin source of truth stays under [`plugins/agent-plugin-skills/`](./plugins/agent-plugin-skills/).

For local project discovery on macOS and Linux, including WSL 2 when Windows is involved, this repo uses POSIX symlink mirrors instead of duplicate skill trees:

- [`.agents/skills`](./.agents/skills) -> `../skills`
- [`.claude/skills`](./.claude/skills) -> `../skills`
- [`plugins/agent-plugin-skills/skills`](./plugins/agent-plugin-skills/skills) -> `../../skills`

Current packaging surfaces:

- [`plugins/agent-plugin-skills/.codex-plugin/plugin.json`](./plugins/agent-plugin-skills/.codex-plugin/plugin.json)
- [`plugins/agent-plugin-skills/.claude-plugin/plugin.json`](./plugins/agent-plugin-skills/.claude-plugin/plugin.json)
- [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json)
- [`plugins/agent-plugin-skills/hooks/hooks.json`](./plugins/agent-plugin-skills/hooks/hooks.json)
- [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json)

## What Belongs In Git

Official docs plus repo-maintainer judgment lead to a simple split:

- Track canonical plugin source trees and shared marketplace catalogs in git.
- Do not track consumer-side install copies, caches, or local-only runtime state.

In this repo shape, that means the tracked surfaces usually are:

- root [`skills/`](./skills/)
- tracked plugin package roots under [`plugins/`](./plugins/)
- repo-scoped Codex marketplace catalogs under [`.agents/plugins/`](./.agents/plugins/)
- repo-root Claude marketplace catalogs under [`.claude-plugin/`](./.claude-plugin/)
- shared plugin assets, hooks, MCP manifests, and app manifests that are part of the published plugin

Local-only or generated surfaces should stay out of git:

- personal Codex install copies under `~/.codex/plugins/`
- Codex installed cache state under `~/.codex/plugins/cache/`
- Claude local settings and other machine-local runtime state
- accidental in-repo local install copies or caches

This follows the current docs:

- Codex local plugins are loaded from a marketplace entry and then copied into the Codex cache, so the canonical source repo should track the source plugin and any repo-curated marketplace catalog, not the downstream cache copy.
- Claude plugin development uses `claude --plugin-dir` directly from source, while Claude marketplace distribution is Git-oriented and expects a tracked repo-root `.claude-plugin/marketplace.json` when you want the repository itself to be addable as a marketplace.

## Shared `.gitignore` Snippet

For skills and plugin development repos, merge this baseline snippet unless the repo already has stricter local-runtime ignores:

```gitignore
# Agent plugin repo local runtime state
.codex/plugins/
.codex/plugins/**
.claude/settings.local.json
.claude/local-settings.json
.claude/.local/
```

This snippet is intentionally narrow. It ignores accidental in-repo local install surfaces and Claude local-only settings, but it does not ignore tracked plugin manifests, marketplace catalogs, or canonical plugin source directories.

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

The installer accepts either the plugin root itself or a repo root that resolves to exactly one staged plugin under `plugins/`.

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

# Update the staged copied install after local source changes
uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py \
  --source-plugin-root plugins/agent-plugin-skills \
  --action update \
  --run-mode apply

# Remove the local Codex install surface for one plugin
uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py \
  --source-plugin-root plugins/agent-plugin-skills \
  --action uninstall \
  --run-mode apply

# Verify a wired install without mutating it
uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py \
  --source-plugin-root plugins/agent-plugin-skills \
  --action verify \
  --run-mode check-only \
  --print-md

# Repair a drifted repo-local install surface in one pass
uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py \
  --source-plugin-root plugins/agent-plugin-skills \
  --scope repo \
  --repo-root /path/to/target-repo \
  --action repair \
  --run-mode apply

# Enable or disable the plugin in Codex config
uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py \
  --source-plugin-root plugins/agent-plugin-skills \
  --action enable \
  --run-mode apply

uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py \
  --source-plugin-root plugins/agent-plugin-skills \
  --action disable \
  --run-mode apply

# Promote a repo-local install into personal scope
uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py \
  --source-plugin-root plugins/agent-plugin-skills \
  --scope repo \
  --repo-root /path/to/target-repo \
  --action promote \
  --run-mode apply
```

Troubleshooting:

- Fully restart Codex after repo-local marketplace changes. A still-open workspace can keep using the marketplace view it loaded before `install`, `update`, or `repair`.
- Repo scope only makes the plugin available in that repo. Use personal scope when the plugin should appear broadly across unrelated repos.
- If a staged repo-local plugin still does not appear after restart, check `~/.codex/log/codex-tui.log` for warnings like `skipping marketplace` or `local plugin source path must not be empty`.
- The Codex `/plugins` slash command list order may not be intuitive, so scan the whole list before concluding a plugin is missing.

### Claude Code Plugin

This repository also ships a Claude plugin manifest at [`plugins/agent-plugin-skills/.claude-plugin/plugin.json`](./plugins/agent-plugin-skills/.claude-plugin/plugin.json).

For Git-backed sharing, the repository also includes a tracked Claude marketplace catalog at [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json). That catalog points at the tracked plugin source under [`plugins/agent-plugin-skills/`](./plugins/agent-plugin-skills/), which matches Claude's documented relative-path marketplace model for plugins in the same repository.

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
├── .claude-plugin/
│   └── marketplace.json
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
