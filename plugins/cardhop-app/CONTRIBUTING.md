# Contributing to cardhop-app

Use this guide when preparing changes so `cardhop-app` stays understandable, runnable, and reviewable for the next maintainer.

## Overview

This guide is for contributors working on the `cardhop-app` child repository inside `socket`: the root skill, the bundled MCP server under [`mcp/`](./mcp/), and the thin packaging metadata at repo root.

Before you start, read [README.md](./README.md) and [AGENTS.md](./AGENTS.md), then confirm which surface actually changed.

## Contribution Workflow

Use the root repository for work about:

- repo-root Codex packaging metadata in [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json)
- bundled MCP wiring in [`.mcp.json`](./.mcp.json)
- the Cardhop workflow guidance under [`skills/`](./skills/)
- the bundled FastMCP server under [`mcp/`](./mcp/)

Keep changes bounded to one coherent concern at a time. If a server behavior change also changes the workflow guidance or packaging story, update those docs in the same pass.

## Local Setup

Sync the bundled server environment with:

```bash
cd mcp
uv sync
```

## Development Expectations

Keep terminology aligned across docs, skill wording, server tools, and packaging metadata:

- `skill` means the reusable workflow-authoring surface under `skills/`
- `plugin` means the installable Codex bundle at repo root
- `bundled MCP server` means the local FastMCP package under `mcp/`

## Verification

Run the bundled server validation commands from `mcp/`:

```bash
cd mcp
uv run pytest
uv run ruff check .
uv run mypy .
```

When editing docs, also review the rendered Markdown structure and cross-links for the files you changed.

## Pull Request Expectations

A good PR should make the changed surface obvious. Include:

- what changed
- why the change belongs in `cardhop-app`
- any docs or packaging metadata updated to keep the repo honest
- the verification you ran
