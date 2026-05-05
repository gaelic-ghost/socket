# things-app

Canonical home for Gale's Things.app skills, bundled local MCP server, and plugin packaging.

For maintainer policy and source-of-truth boundaries, see [AGENTS.md](./AGENTS.md). For contributor workflow, setup, and review expectations, see the Socket root [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Development](#development)
- [Repo Structure](#repo-structure)
- [Release Notes](#release-notes)
- [License](#license)
- [Active Skills](#active-skills)
- [Bundled MCP Server](#bundled-mcp-server)
- [Packaging](#packaging)

## Overview

`things-app` ships three related surfaces in one repo:

- reusable Things-oriented skills under [`skills/`](./skills/)
- a bundled FastMCP server under [`mcp/`](./mcp/)
- thin Codex plugin packaging metadata at the repo root

### Status

`things-app` is active and currently maintained as a mixed skills-plus-server repository.

### What This Project Is

This repository is the canonical home for Gale's Things-focused automation workflows and the local MCP server those workflows depend on.

### Motivation

It keeps the Things workflow surface, the bundled server implementation, and the plugin packaging story aligned in one place instead of splitting those concerns across separate repositories.

## Quick Start

This repo is primarily a maintainer and power-user surface rather than an end-user app with a single quick-start flow.

If you want to use the workflow guidance, start with the skills under [`skills/`](./skills/). If you want to work on the bundled server, go straight to [`mcp/README.md`](./mcp/README.md). If you are changing the repo itself, use the contributor workflow in the Socket root [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Usage

Use the surface that matches the job:

- root [`skills/`](./skills/) for Things reminder and planning workflows
- root plugin metadata for Codex installation and discovery
- [`mcp/`](./mcp/) for the local FastMCP server, its docs, and its server-specific checks

The current active skills are intentionally narrow:

- `things-reminders-manager` for deterministic create and update flows around Things reminders and scheduled to-dos
- `things-digest-generator` for week-ahead planning digests built from Things reads or equivalent JSON exports

## Development

### Setup

The repo has two distinct Python environments:

- repo root for the digest-skill maintainer tooling and tests
- `mcp/` for the bundled server package and its lint, typecheck, and smoke flows

Root setup:

```bash
uv sync --dev
```

Bundled server setup:

```bash
cd mcp
uv sync
```

### Workflow

Keep the source-of-truth boundaries straight:

- edit root [`skills/`](./skills/) when workflow behavior changes
- edit [`mcp/`](./mcp/) when server behavior changes
- treat [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) and [`.mcp.json`](./.mcp.json) as install metadata, not as the source of truth for workflow logic

When a change touches more than one surface, update the nearby docs in the same pass so the mixed-repo model stays explicit and accurate.

### Validation

Run the checks that match the surface you changed.

Repo-root skill validation:

```bash
uv run pytest
```

Bundled server validation:

```bash
cd mcp
uv run pytest
uv run ruff check .
uv run mypy .
```

For local HTTP smoke checks while working on the bundled server:

```bash
cd mcp
make smoke-http
make smoke-json
```

## Repo Structure

```text
.
├── .codex-plugin/
│   └── plugin.json
├── .mcp.json
├── AGENTS.md
├── README.md
├── mcp/
├── pyproject.toml
└── skills/
    ├── things-digest-generator/
    └── things-reminders-manager/
```

## Release Notes

Use Git history and GitHub releases to track shipped changes, especially when skills, packaging metadata, and the bundled MCP server move together.

## License

See the Socket root [LICENSE](../../LICENSE).

## Active Skills

- [`skills/things-reminders-manager/`](./skills/things-reminders-manager/): deterministic create and update workflows for Things reminders and scheduled to-dos
- [`skills/things-digest-generator/`](./skills/things-digest-generator/): week-ahead planning digests built from Things MCP reads or equivalent JSON exports

## Bundled MCP Server

The former standalone `things-app-mcp` project now lives directly under [`mcp/`](./mcp/), with its own package metadata, helper commands, tests, and server-specific docs.

The packaged Codex MCP entrypoint in [`.mcp.json`](./.mcp.json) launches that server with:

```json
{
  "things-app": {
    "command": "uv",
    "args": ["run", "python", "app/server.py"],
    "cwd": "../../mcp"
  }
}
```

That relative `cwd` matters because the plugin packaging lives at repo root while the server stays self-contained inside the bundled package directory.

## Packaging

This repository keeps authored workflow content and packaging metadata separate on purpose.

- root `skills/` is the canonical workflow-authoring surface
- [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) points Codex at the root skills and bundled MCP config
- the bundled FastMCP server stays self-contained under [`mcp/`](./mcp/)

Helpful references:

- [OpenAI Codex Skills](https://developers.openai.com/codex/skills)
- [OpenAI Codex plugins](https://developers.openai.com/codex/plugins)
