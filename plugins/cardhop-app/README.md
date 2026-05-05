# cardhop-app

Canonical home for Gale's Cardhop.app Codex skill, bundled local MCP server, and thin plugin packaging.

For maintainer policy and source-of-truth boundaries, see [AGENTS.md](./AGENTS.md). For contributor workflow, setup, and review expectations, see the Socket root [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Development](#development)
- [Repo Structure](#repo-structure)
- [Release Notes](#release-notes)
- [Active Skills](#active-skills)
- [Bundled MCP Server](#bundled-mcp-server)
- [Packaging](#packaging)

## Overview

`cardhop-app` ships three related surfaces in one repo:

- reusable Cardhop-oriented skills under [`skills/`](./skills/)
- a bundled FastMCP server under [`mcp/`](./mcp/)
- thin Codex plugin packaging metadata at the repo root

### Status

`cardhop-app` is active and currently maintained as a mixed skills-plus-server repository inside `socket`.

### What This Project Is

This repository is the canonical home for Gale's Cardhop.app automation workflows and the local MCP server those workflows depend on.

### Motivation

It keeps the Cardhop workflow surface, the bundled server implementation, and the Codex plugin packaging story aligned in one place instead of splitting those concerns across separate repositories.

## Quick Start

If you want to use the workflow guidance, start with the skills under [`skills/`](./skills/). If you want to work on the bundled server, go straight to [`mcp/README.md`](./mcp/README.md). If you are changing the repo itself, use the contributor workflow in the Socket root [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Usage

Use the surface that matches the job:

- root [`skills/`](./skills/) for Cardhop.app contact-capture and contact-update workflows
- root plugin metadata for Codex installation and discovery
- [`mcp/`](./mcp/) for the local FastMCP server, its tests, and its server-specific docs

The current active skill is intentionally narrow:

- `cardhop-contact-workflow` for adding, updating, and validating Cardhop contact actions through the bundled MCP server

## Development

### Setup

The bundled server lives under [`mcp/`](./mcp/) and uses `uv` for setup:

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

Run the bundled server checks from `mcp/`:

```bash
cd mcp
uv run pytest
uv run ruff check .
uv run mypy .
```

When the skill wording or packaging metadata changes, also review the root docs and plugin metadata together.

## Repo Structure

```text
.
├── .codex-plugin/
│   └── plugin.json
├── .mcp.json
├── AGENTS.md
├── README.md
├── ROADMAP.md
├── mcp/
└── skills/
    └── cardhop-contact-workflow/
```

## Release Notes

Use Git history and GitHub releases to track shipped changes, especially when skills, packaging metadata, and the bundled MCP server move together.

## Active Skills

- [`skills/cardhop-contact-workflow/`](./skills/cardhop-contact-workflow/): guided Cardhop.app contact add and update workflow over the bundled MCP server

## Bundled MCP Server

The former standalone `cardhop-mcp` project now lives directly under [`mcp/`](./mcp/), with its package metadata, tests, and server-specific docs kept together there.

The packaged Codex MCP entrypoint in [`.mcp.json`](./.mcp.json) launches that server with:

```json
{
  "mcpServers": {
    "cardhop_app_socket": {
      "command": "uv",
      "args": ["run", "python", "app/server.py"],
      "cwd": "../../mcp"
    }
  }
}
```

That relative `cwd` matters because the plugin packaging lives at repo root while the server stays self-contained inside the bundled package directory.

## Packaging

This repository keeps authored workflow content and packaging metadata separate on purpose.

- root `skills/` is the canonical workflow-authoring surface
- [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) points Codex at the root skill and bundled MCP config
- the bundled FastMCP server stays self-contained under [`mcp/`](./mcp/)

Helpful references:

- [OpenAI Codex Skills](https://developers.openai.com/codex/skills)
- [OpenAI Codex plugins](https://developers.openai.com/codex/plugins)
