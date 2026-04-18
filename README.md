# socket

Mixed-model monorepo for Gale's Codex plugin and skills repositories.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Development](#development)
- [Repo Structure](#repo-structure)
- [Release Notes](#release-notes)
- [License](#license)
- [Repository Docs](#repository-docs)
- [Plugin Surfaces](#plugin-surfaces)
- [Marketplace Shape](#marketplace-shape)

## Overview

### Status

This repository is active and maintained as the superproject layer.

### What This Project Is

`socket` is the superproject Gale uses to keep several Codex plugin and skills repositories under one Git root while OpenAI's documented Codex plugin system still lacks a better shared-parent scoping model. It owns the repo-root Codex marketplace at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json), the monorepo-owned nested plugin directories under [`plugins/`](./plugins/), the remaining subtree sync paths for `apple-dev-skills`, `python-skills`, and `SpeakSwiftlyServer`, and the root maintainer docs that explain how the mixed model works.

### Motivation

It exists to keep the plugin and skills experiment workable under one repository without pretending Codex currently supports clean repo-private plugin packs, hidden repo-local install surfaces, or richer parent-level scoping than the documented marketplace model provides.

## Quick Start

Start here when the task is about the superproject layer rather than one child repository:

1. Read [`README.md`](./README.md), [`AGENTS.md`](./AGENTS.md), and [`docs/maintainers/subtree-workflow.md`](./docs/maintainers/subtree-workflow.md).
2. Confirm whether the work belongs at the root `socket` layer or inside a specific child repo under [`plugins/`](./plugins/).
3. If you need the root maintainer Python environment, sync it with:

```bash
uv sync --dev
```

4. Run the root validation path when the change touches marketplace wiring or the root metadata contract:

```bash
uv run scripts/validate_socket_metadata.py
```

## Usage

Use `socket` when the task is about the superproject layer:

- root marketplace wiring
- mixed monorepo policy
- subtree sync flow for `apple-dev-skills`, `python-skills`, or `SpeakSwiftlyServer`
- cross-repo maintainer guidance

When the work is really about one child repository's own behavior, start from that child directory's docs instead.

## Development

### Setup

Sync the root maintainer environment with:

```bash
uv sync --dev
```

Only `apple-dev-skills`, `python-skills`, and `SpeakSwiftlyServer` still use subtree sync workflows.

### Workflow

Treat Gale's local `socket` checkout as the normal day-to-day checkout on `main`. Work in the monorepo copy first, and use the relevant directory under [`plugins/`](./plugins/) for child-repository changes unless the task is explicitly about the root marketplace or root maintainer docs. Reach for a feature branch or a dedicated worktree only when the change needs extra isolation.

Keep root docs and marketplace wiring in sync with packaging changes in the same pass. For monorepo-owned child directories, edit the relevant directory under [`plugins/`](./plugins/) directly and commit in `socket`. For `apple-dev-skills`, `python-skills`, and `SpeakSwiftlyServer`, keep subtree sync operations explicit and isolated.

Use [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the maintainer workflow boundary and [`ROADMAP.md`](./ROADMAP.md) for root planning and historical notes.

### Validation

The current root validation surface is structural:

- keep [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json) valid JSON
- verify that every listed `source.path` matches the real child surface that the child repo treats as installable
- verify that every packaged plugin path still exposes a matching `.codex-plugin/plugin.json`
- review child-repo docs when plugin packaging paths move
- run child-repo-specific validation from the relevant child repo when the change is really about that child repo

Run the root validator locally with:

```bash
uv run scripts/validate_socket_metadata.py
```

## Repo Structure

```text
.
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── ACCESSIBILITY.md
├── CONTRIBUTING.md
├── docs/
│   └── maintainers/
│       ├── plugin-packaging-strategy.md
│       └── subtree-workflow.md
├── plugins/
├── scripts/
│   └── validate_socket_metadata.py
├── AGENTS.md
├── README.md
└── ROADMAP.md
```

## Release Notes

Use Git history and GitHub releases for root-level superproject changes. Child repositories should continue to track their own shipped release notes inside their own surfaces.

## License

The `socket` superproject is licensed under the Apache License 2.0. See [LICENSE](./LICENSE) for the full text and [NOTICE](./NOTICE) for the root superproject notice surface.

## Repository Docs

The root superproject docs are:

- [README.md](./README.md) for the superproject overview and root workflow
- [CONTRIBUTING.md](./CONTRIBUTING.md) for root contribution workflow expectations
- [AGENTS.md](./AGENTS.md) for root operating rules and repo-boundary guidance
- [ROADMAP.md](./ROADMAP.md) for root planning and milestone tracking
- [ACCESSIBILITY.md](./ACCESSIBILITY.md) for the root accessibility contract around docs, metadata, and maintainer automation
- [`docs/maintainers/`](./docs/maintainers/) for the deeper maintainer references behind the mixed-monorepo and subtree model

## Plugin Surfaces

Treat `socket` as the canonical home for the monorepo-owned nested directories and as the subtree host for the remaining imported child repos.

- `agent-plugin-skills`, `dotnet-skills`, `productivity-skills`, `rust-skills`, `things-app`, and `web-dev-skills` are monorepo-owned here.
- `apple-dev-skills`, `python-skills`, and `SpeakSwiftlyServer` preserve explicit subtree sync paths.
- Some child repos expose plugin packaging from the repo root, while others keep a nested packaged plugin root inside their own repository tree.

## Marketplace Shape

The repo-root marketplace lives at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json).

That marketplace points at the actual packaged surface each child repository treats as installable today:

- `./plugins/agent-plugin-skills`
- `./plugins/apple-dev-skills`
- `./plugins/dotnet-skills`
- `./plugins/productivity-skills`
- `./plugins/SpeakSwiftlyServer`
- `./plugins/python-skills/plugins/python-skills`
- `./plugins/rust-skills`
- `./plugins/things-app`
- `./plugins/web-dev-skills`

The mixed shape is intentional for now. `socket` does not try to flatten those child repo packaging models into one fake uniform layout.
