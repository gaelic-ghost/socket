# agent-plugin-skills

Installable maintainer skills for skills-export and plugin-export repositories.

## Overview

### Status

Active `socket` child plugin.

### What This Project Is

`agent-plugin-skills` provides compact maintainer workflows for repositories that author Codex skills or package those skills as Codex plugins.

It keeps local guidance limited to repo shape, discovery mirrors, packaging boundaries, and `socket` house policy. Current OpenAI Codex docs remain the source of truth for full plugin, skill, MCP, hooks, marketplace, and subagent behavior.

### Motivation

Skills and plugins are easy to over-document because the install surfaces, authoring surfaces, and runtime surfaces are close together on disk. This plugin keeps those concepts named consistently while avoiding old manual installer workflows.

## What It Provides

- `bootstrap-skills-plugin-repo`: bootstrap or align a skills-export repository around root `skills/`, discovery mirrors, and maintainer guidance
- `sync-skills-repo-guidance`: audit guidance drift across README, AGENTS, maintainer docs, and discovery mirrors

## Use It For

Use this plugin when the target repository is itself a Codex skill or plugin repository and the work is about repo shape, packaging boundaries, discovery mirrors, or cross-surface documentation alignment.

For general repository docs and maintainer workflow cleanup, start with `productivity-skills`.

## Codex Boundary

OpenAI's documented Codex plugin system exposes repo-visible plugins through marketplace catalogs and does not document a richer repo-private scoping model beyond that. In the Socket marketplace, the `agent-plugin-skills` entry points at `./plugins/agent-plugin-skills`.

Ordinary user installs should use Git-backed marketplace sources:

```bash
codex plugin marketplace add gaelic-ghost/socket
codex plugin marketplace upgrade socket
```

The plugin manifest points to bundled skills with `"skills": "./skills/"`. Only `plugin.json` belongs in `.codex-plugin/`; `skills/`, `.app.json`, `.mcp.json`, `hooks/`, and `assets/` belong at the plugin root.

## Maintenance

Declare the required dev dependencies in `pyproject.toml`. The maintainer baseline is `pytest`, `ruff`, and `mypy` through `uv`.

Before changing guidance about Codex Plugins, Skills, MCP, Hooks, marketplaces, or subagents, refresh the official OpenAI docs and keep this repository's own prose focused on the durable local policy.

## Socket Docs

- Install and update guidance: [Socket README](../../README.md)
- Shared contributor workflow: [Socket CONTRIBUTING](../../CONTRIBUTING.md)
- Consolidated backlog: [Socket TODO](../../TODO.md)
- Agent-facing local guidance: [AGENTS](./AGENTS.md)
