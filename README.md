# things-app

Canonical home for Gale's Things.app skills and bundled Things MCP server, with plugin-first packaging for Codex and Claude Code.

For maintainer policy and repository workflow expectations, see [AGENTS.md](./AGENTS.md).

## Overview

This repository now bundles three closely related surfaces:

- reusable Things-oriented skills under [`skills/`](./skills/)
- the local FastMCP server under [`mcp/things-app-mcp/`](./mcp/things-app-mcp/)
- plugin packaging metadata under [`plugins/things-app/`](./plugins/things-app/)

The goal is to keep one canonical repository for:

- reminder-management workflows
- week-ahead digest generation
- the local MCP server those workflows rely on
- install surfaces for Codex and Claude Code

## Active Skills

- `things-reminders-manager`
  - Deterministic create and update workflows for Things reminders and scheduled todos.
- `things-digest-generator`
  - Week-ahead planning digests built from Things MCP reads or equivalent JSON exports.

## Bundled MCP Server

The repository now vendors the former standalone `things-app-mcp` project at [`mcp/things-app-mcp/`](./mcp/things-app-mcp/), preserving its history via `git subtree`.

That server remains a self-contained FastMCP package with its own:

- [`README.md`](./mcp/things-app-mcp/README.md)
- [`pyproject.toml`](./mcp/things-app-mcp/pyproject.toml)
- [`tests/`](./mcp/things-app-mcp/tests/)
- [`docs/`](./mcp/things-app-mcp/docs/)

Run its local checks from that directory:

```bash
cd mcp/things-app-mcp
uv sync
uv run pytest
```

## Packaging

This repository uses a plugin-first layout while keeping root [`skills/`](./skills/) as the canonical workflow-authoring surface.

Packaged plugin surfaces live under:

- [`plugins/things-app/.codex-plugin/plugin.json`](./plugins/things-app/.codex-plugin/plugin.json)
- [`plugins/things-app/.claude-plugin/plugin.json`](./plugins/things-app/.claude-plugin/plugin.json)
- [`plugins/things-app/.mcp.json`](./plugins/things-app/.mcp.json)
- [`plugins/things-app/skills`](./plugins/things-app/skills)
- [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json)
- [`.agents/skills`](./.agents/skills)
- [`.claude/skills`](./.claude/skills)

The packaging is intentionally conservative:

- keep reusable workflow logic in root `skills/`
- keep the MCP server self-contained under `mcp/`
- keep plugin manifests and marketplace wiring as install metadata rather than as the source of truth

Helpful references:

- OpenAI Codex Skills: <https://developers.openai.com/codex/skills>
- OpenAI Codex plugins: <https://developers.openai.com/codex/plugins>
- Claude Code Skills: <https://code.claude.com/docs/en/skills>
- Claude Code Plugins: <https://code.claude.com/docs/en/plugins>

## Maintainer Python Tooling

Repo-root Python tooling remains focused on the skill-side helper surface:

```bash
uv sync --dev
uv run pytest
```

That repo-root test run currently targets the Python-backed digest skill test surface.

## Repository Layout

```text
.
├── .agents/
│   ├── skills -> ../skills
│   └── plugins/
│       └── marketplace.json
├── .claude/
│   └── skills -> ../skills
├── AGENTS.md
├── README.md
├── mcp/
│   └── things-app-mcp/
├── plugins/
│   └── things-app/
│       ├── .codex-plugin/
│       ├── .claude-plugin/
│       ├── .mcp.json
│       └── skills -> ../../skills
├── pyproject.toml
└── skills/
    ├── things-digest-generator/
    └── things-reminders-manager/
```

## Maintainer Notes

- Keep active skill runtime assets self-contained inside each skill directory.
- Prefer `uv run pytest` for the Python-backed digest skill test surface.
- Treat `things-app` as the canonical repo home for the Things skills and bundled MCP server.
