# things-app

Canonical home for Gale's Things.app skills and bundled Things MCP server, with plugin-first packaging for Codex and Claude Code.

For maintainer policy and repository workflow expectations, see [AGENTS.md](./AGENTS.md).

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Development](#development)
- [Release Notes](#release-notes)
- [Verification](#verification)
- [License](#license)
- [Active Skills](#active-skills)
- [Bundled MCP Server](#bundled-mcp-server)
- [Packaging](#packaging)
- [Maintainer Python Tooling](#maintainer-python-tooling)
- [Repository Layout](#repository-layout)
- [Maintainer Notes](#maintainer-notes)

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

### Status

This repository is active and currently ships the Things-oriented skills, plugin packaging, and bundled MCP server surfaces described below.

### What This Project Is

This repository is the canonical home for Gale's Things-focused skills plus the bundled local MCP server they depend on.

### Motivation

It exists to keep Things-focused automation and integration work in a dedicated repo with explicit packaging and maintainer guidance.

## Setup

Start with the install and packaging guidance already documented here, then use the maintainer workflow and roadmap sections when changing the shipped skills, packaging, or MCP server surfaces.

## Usage

Use the skill, plugin, and MCP surfaces documented here that match the Things workflow you actually need, whether that is reminder management, digest generation, or local MCP automation.

## Development

### Setup

Install the documented local tooling, work from the canonical source surfaces in this repo, and keep packaging and docs aligned in the same pass.

### Workflow

Edit the canonical repo surfaces first, update docs and metadata together, and run the relevant validation commands for the plugin or MCP surface you changed.

## Verification

Run the documented tests and validation commands that match the Things plugin, skill, or MCP surfaces you changed, and keep the mixed-repo packaging story consistent across the root docs and the bundled server docs.

## Release Notes

Use Git history and GitHub releases to track shipped changes for this repository, especially when the skills, plugin packaging, and bundled MCP server move together.

## License

See [LICENSE](./LICENSE).

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
├── ROADMAP.md
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
- Track in-flight repo work in [ROADMAP.md](./ROADMAP.md).
