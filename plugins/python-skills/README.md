# python-skills

Python workflow skills for `uv` bootstrapping, FastAPI and FastMCP scaffolding, integration work, and pytest setup.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Development](#development)
- [Verification](#verification)
- [Release Notes](#release-notes)
- [License](#license)
- [Active Skills](#active-skills)
- [Packaging](#packaging)
- [Repository Layout](#repository-layout)

## Overview

`python-skills` is the Python-specific workflow plugin in Gale's skills ecosystem.

### Status

This directory is active as normal monorepo-owned content inside `socket` and currently ships a focused set of Python workflow skills.

### What This Project Is

This directory is the canonical home for Gale's Python-oriented skill authoring inside `socket`. Root [`skills/`](./skills/) is the authored surface, and the directory root is also the Codex plugin root through [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).

### Motivation

It exists to keep Python-specific workflow guidance in one place without mixing it into the broader general-purpose maintainer layer owned by `productivity-skills`.

## Setup

Use the repo-local maintainer environment when you want to inspect, test, or edit this repository:

```bash
uv sync --dev
```

Keep the maintainer toolchain declared in this repository instead of assuming machine-global Python tools. When the repo's validation surface uses them, declare `pytest`, `ruff`, and `mypy` in the repo-local dev dependency group and run them through `uv`.

If you are trying to contribute changes instead of just consume the shipped skills, use the Socket root [CONTRIBUTING.md](../../CONTRIBUTING.md) for the maintainer workflow.

## Usage

Use `python-skills` when the work is specifically about:

- bootstrapping `uv`-managed Python projects or workspaces
- scaffolding FastAPI services
- scaffolding FastMCP services
- integrating FastAPI and FastMCP in one codebase
- setting up or troubleshooting pytest in `uv`-managed repositories

### Direct Skill Installation

The canonical authored surface is [`skills/`](./skills/). This repository supports direct skill installation from that shared tree into standard Codex skill locations when you want one skill or a small subset instead of the whole packaged plugin.

### Packaged Plugin Installation

The Codex plugin root is this repository root. In parent repositories such as `socket`, marketplace entries should point at the child repo root rather than a second nested packaged copy.

### Install-Surface Map

For Codex, keep these surfaces distinct:

- marketplace catalog: a repo marketplace such as `socket/.agents/plugins/marketplace.json` or a personal marketplace at `~/.agents/plugins/marketplace.json`
- staged plugin directory: this repo root, which is the local plugin payload directory the marketplace entry should point at
- installed plugin cache: `~/.codex/plugins/cache/$MARKETPLACE_NAME/python-skills/local/`
- enabled-state config: `~/.codex/config.toml`

### Codex Limitation Warning

OpenAI's documented Codex plugin system supports repo marketplaces, personal marketplaces, staged plugin directories, installed plugin caches, and enabled-state config, but it does not provide proper repo-private plugin scoping beyond that marketplace model.

## Development

### Setup

Treat root [`skills/`](./skills/) as the source of truth for shipped workflow content. Treat [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) as install-surface metadata and discovery wiring, not as a second authored tree.

### Workflow

Keep the public docs, maintainer guidance, and packaging metadata aligned in the same pass when the shipped skill surface changes. Use this repository for Python-, `uv`-, FastAPI-, FastMCP-, and pytest-specific workflow behavior. Use `productivity-skills` for broader general-purpose maintainer workflows that should stay stack-neutral.

Use the Socket root [CONTRIBUTING.md](../../CONTRIBUTING.md) for the contributor contract and [`AGENTS.md`](./AGENTS.md) for durable child-specific guidance.

## Verification

Run the repo validation path before landing documentation, metadata, or packaging changes:

```bash
uv sync --dev
uv run scripts/validate_repo_metadata.py
uv run pytest
uv run ruff check .
uv run mypy .
```

## Release Notes

Use `socket` Git history and GitHub releases to track shipped changes for this directory.

`python-skills` follows the shared `socket` semantic version. Version inventory and version bumps must run through the root [`scripts/release.sh`](../../scripts/release.sh) workflow, not through an independent `python-skills` release path.

## License

See the Socket root [LICENSE](../../LICENSE).

## Active Skills

- `bootstrap-python-mcp-service`
- `bootstrap-python-service`
- `bootstrap-uv-python-workspace`
- `integrate-fastapi-fastmcp`
- `uv-pytest-unit-testing`

## Packaging

This repository intentionally keeps authored content and plugin metadata separate.

- root [`skills/`](./skills/) is the canonical authored workflow surface
- [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) defines the Codex plugin metadata at the repo root

## Repository Layout

```text
.
├── .codex-plugin/
│   └── plugin.json
├── AGENTS.md
├── README.md
├── ROADMAP.md
├── pyproject.toml
├── scripts/
│   └── validate_repo_metadata.py
├── skills/
├── tests/
└── uv.lock
```
