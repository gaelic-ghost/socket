# socket

Mixed-model monorepo for Gale's Codex plugin and skills repositories.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Development](#development)
- [Verification](#verification)
- [Release Notes](#release-notes)
- [Current Status](#current-status)
- [Plugin Surfaces](#plugin-surfaces)
- [Marketplace Shape](#marketplace-shape)
- [Working In Socket](#working-in-socket)
- [Repository Layout](#repository-layout)

## Overview

`socket` is the superproject Gale uses to keep several Codex plugin and skills repositories under one Git root while OpenAI's documented Codex plugin system still lacks a better shared-parent scoping model.

### Status

`socket` is active. `apple-dev-skills` and `python-skills` are still subtree-managed child repositories. The other directories under [`plugins/`](./plugins/) are now treated as ordinary monorepo-owned nested directories.

### What This Project Is

This repository owns:

- the repo-root Codex marketplace at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json)
- the monorepo-owned nested plugin directories under [`plugins/`](./plugins/)
- the remaining subtree sync paths for `apple-dev-skills` and `python-skills`
- the root maintainer docs that explain how the mixed model works

### Motivation

It exists to keep the plugin and skills experiment workable under one repository without pretending Codex currently supports clean repo-private plugin packs, hidden repo-local install surfaces, or richer parent-level scoping than the documented marketplace model provides.

## Setup

Read the overview and marketplace sections first, then work from the mixed-monorepo rules in this repository's root docs and [AGENTS.md](./AGENTS.md).

If you need the root maintainer Python environment, sync it with:

```bash
uv sync --dev
```

Only `apple-dev-skills` and `python-skills` still use subtree sync workflows.

## Usage

Use `socket` when the task is about the superproject layer:

- root marketplace wiring
- mixed monorepo policy
- subtree sync flow for `apple-dev-skills` or `python-skills`
- cross-repo maintainer guidance

When the work is really about one child repository's own behavior, start from that child directory's docs instead.

## Development

### Setup

Work in the monorepo copy first. Use `plugins/<repo>/` for child-repository changes unless the task is explicitly about the root marketplace or root maintainer docs.

### Workflow

Keep root docs and marketplace wiring in sync with packaging changes in the same pass.

- For monorepo-owned child directories, edit `plugins/<repo>/` directly and commit in `socket`.
- For `apple-dev-skills` and `python-skills`, keep subtree sync operations explicit and isolated.
- Before removing or moving a plugin surface, verify whether the root marketplace or maintainer docs still reference it.

## Verification

There is no single heavy repo-wide build or test pipeline for `socket` yet.

The current validation surface is structural:

- keep [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json) valid JSON
- verify that every listed `source.path` matches the real child surface that the child repo treats as installable
- review child-repo docs when plugin packaging paths move
- run child-repo-specific validation from the relevant child repo when the change is really about that child repo

## Release Notes

Use Git history and GitHub releases for root-level superproject changes. Child repositories should continue to track their own shipped release notes inside their own surfaces.

## Current Status

The current plugin and skills directories under [`plugins/`](./plugins/) are:

- `agent-plugin-skills`
- `apple-dev-skills`
- `dotnet-skills`
- `productivity-skills`
- `python-skills`
- `rust-skills`
- `things-app`
- `web-dev-skills`

`apple-dev-skills` and `python-skills` are the only directories in that list that still keep live subtree relationships to separate upstream repositories.

## Plugin Surfaces

Treat `socket` as the canonical home for the monorepo-owned nested directories and as the subtree host for the remaining imported child repos.

- `agent-plugin-skills`, `dotnet-skills`, `productivity-skills`, `rust-skills`, `things-app`, and `web-dev-skills` are monorepo-owned here.
- `apple-dev-skills` and `python-skills` still preserve explicit subtree sync paths.
- Some child repos expose plugin packaging from the repo root, while others keep a nested packaged plugin root inside their own repository tree.

## Marketplace Shape

The repo-root marketplace lives at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json).

That marketplace points at the actual packaged surface each child repository treats as installable today:

- `./plugins/agent-plugin-skills`
- `./plugins/apple-dev-skills`
- `./plugins/dotnet-skills`
- `./plugins/productivity-skills`
- `./plugins/python-skills/plugins/python-skills`
- `./plugins/rust-skills`
- `./plugins/things-app`
- `./plugins/web-dev-skills`

The mixed shape is intentional for now. `socket` does not try to flatten those child repo packaging models into one fake uniform layout.

## Working In Socket

- Use the root docs when you need the mixed monorepo model, marketplace wiring, or subtree workflow.
- Use child-repo docs when you are changing a child repo's own skills, packaging, tests, or release guidance.
- For ordinary fixes in monorepo-owned child directories, edit the copy in `plugins/<name>/` directly.
- For `apple-dev-skills` and `python-skills`, keep subtree pull and push work explicit and separate from unrelated edits.
- Update the root marketplace and root docs whenever a child repo gains, moves, or removes plugin packaging.

## Repository Layout

```text
.
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── docs/
│   └── maintainers/
│       ├── plugin-alignment-plan.md
│       ├── plugin-packaging-strategy.md
│       ├── subtree-migration-plan.md
│       └── subtree-workflow.md
├── plugins/
│   ├── agent-plugin-skills/
│   ├── apple-dev-skills/
│   ├── dotnet-skills/
│   ├── productivity-skills/
│   ├── python-skills/
│   ├── rust-skills/
│   ├── things-app/
│   └── web-dev-skills/
├── AGENTS.md
├── README.md
├── ROADMAP.md
└── pyproject.toml
```
