# things-app

Canonical home for Gale's Things.app skills, bundled local MCP server, and plugin packaging.

For maintainer policy and source-of-truth boundaries, see [AGENTS.md](./AGENTS.md).

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Development](#development)
- [Verification](#verification)
- [Release Notes](#release-notes)
- [License](#license)
- [Active Skills](#active-skills)
- [Bundled MCP Server](#bundled-mcp-server)
- [Packaging](#packaging)
- [Maintainer Python Tooling](#maintainer-python-tooling)
- [Repository Layout](#repository-layout)

## Overview

This repository ships three closely related surfaces:

- reusable Things-oriented skills under [`skills/`](./skills/)
- the bundled FastMCP server under [`mcp/things-app-mcp/`](./mcp/things-app-mcp/)
- plugin packaging metadata at the repo root for Codex and Claude Code

### Status

`things-app` is active and currently ships maintained Things-oriented skills, plugin packaging metadata, and the bundled MCP server described below.

### What This Project Is

This repository is the canonical home for Gale's Things-focused automation workflows and the local MCP server they depend on.

### Motivation

It exists to keep the Things workflow surface, the server implementation, and the plugin packaging story aligned in one place instead of spreading those pieces across separate repos.

## Setup

Start with the install and packaging guidance in this README, then use the server-specific docs inside [`mcp/things-app-mcp/`](./mcp/things-app-mcp/) when the work is really about the bundled FastMCP package.

## Usage

Use the surface that matches the job you are doing:

- root [`skills/`](./skills/) for Things workflow guidance
- root plugin manifests for Codex or Claude plugin installation
- [`mcp/things-app-mcp/`](./mcp/things-app-mcp/) for the bundled local MCP server package and its server-specific validation

## Development

### Setup

Work from the canonical source surfaces in this repository and keep docs, packaging metadata, and server guidance aligned in the same change.

### Workflow

Edit root skills first when changing workflow behavior. Edit the bundled MCP server in `mcp/things-app-mcp/` when the server behavior changes. Treat plugin manifests and marketplace wiring as install metadata rather than as the source of truth for workflow logic.

## Verification

Run the validation commands that match the surface you changed.

For the repo-root Python-backed skill surface:

```bash
uv sync --dev
uv run pytest
```

For the bundled MCP server package:

```bash
cd mcp/things-app-mcp
uv sync
uv run pytest
```

## Release Notes

Use Git history and GitHub releases to track shipped changes for this repository, especially when skills, packaging metadata, and the bundled MCP server move together.

## License

See [LICENSE](./LICENSE).

## Active Skills

- `things-reminders-manager`: deterministic create and update workflows for Things reminders and scheduled todos
- `things-digest-generator`: week-ahead planning digests built from Things MCP reads or equivalent JSON exports

## Bundled MCP Server

The former standalone `things-app-mcp` project now lives under [`mcp/things-app-mcp/`](./mcp/things-app-mcp/), with its own package metadata, tests, docs, and README.

Use its local docs and tests when the work is really about the server package rather than the root skill and plugin surfaces.

## Packaging

This repository keeps root workflow content and plugin metadata separate on purpose.

- root [`skills/`](./skills/) is the canonical workflow-authoring surface
- [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) and [`.claude-plugin/plugin.json`](./.claude-plugin/plugin.json) describe install metadata
- [`.agents/skills`](./.agents/skills) and [`.claude/skills`](./.claude/skills) are discovery mirrors into root `skills/`
- the bundled server stays self-contained under [`mcp/things-app-mcp/`](./mcp/things-app-mcp/)

Helpful references:

- [OpenAI Codex Skills](https://developers.openai.com/codex/skills)
- [OpenAI Codex plugins](https://developers.openai.com/codex/plugins)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Claude Code Plugins](https://code.claude.com/docs/en/plugins)

## Maintainer Python Tooling

Repo-root Python tooling is intentionally narrow and currently supports the Python-backed digest skill test surface:

```bash
uv sync --dev
uv run pytest
```

## Repository Layout

```text
.
├── .agents/
│   └── skills -> ../skills
├── .claude/
│   └── skills -> ../skills
├── .claude-plugin/
│   └── plugin.json
├── .codex-plugin/
│   └── plugin.json
├── AGENTS.md
├── LICENSE
├── README.md
├── ROADMAP.md
├── mcp/
│   └── things-app-mcp/
├── pyproject.toml
└── skills/
    ├── things-digest-generator/
    └── things-reminders-manager/
```
