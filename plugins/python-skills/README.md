# python-skills

Python workflow skills for uv bootstrapping, FastAPI and FastMCP scaffolding, integration work, and pytest setup.

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

`python-skills` bundles reusable Python-focused workflows centered on `uv`, FastAPI, FastMCP, and pytest-oriented repo setup.

### Status

This repository is active and currently ships authored Python skills, repo-local tests, and a nested packaged plugin root for Codex installation.

### What This Project Is

This repository is the canonical source of truth for Gale's Python workflow skills. Root [`skills/`](./skills/) is the authored surface, while the nested packaged plugin root under [`plugins/python-skills/`](./plugins/python-skills/) exists for Codex packaging. Treat `productivity-skills` as the default baseline layer for general repo-doc and maintenance work, and use `python-skills` when Python-, `uv`-, FastAPI-, or FastMCP-specific behavior should shape the workflow.

### Motivation

It exists to keep Python-specific workflow guidance in one place while preserving a thin packaging layer instead of duplicating the skill tree per platform.

## Setup

Sync the repo-local maintainer environment before running tests:

```bash
uv sync --dev
```

## Usage

Use this repository when the work is about:

- bootstrapping uv-managed Python projects or workspaces
- scaffolding FastAPI or FastMCP services
- integrating FastAPI and FastMCP in one codebase
- setting up or troubleshooting pytest in uv-managed repos

## Development

### Setup

Treat root [`skills/`](./skills/) as the canonical authored surface. Keep the nested packaged plugin root under [`plugins/python-skills/`](./plugins/python-skills/) as install metadata only.

### Workflow

Update the root skill content first, then keep the nested packaged plugin root, marketplace metadata, and tests aligned in the same pass.

## Verification

Run the repository test suite before landing metadata or documentation changes:

```bash
uv sync --dev
uv run pytest
```

## Release Notes

Use Git history and GitHub releases to track shipped changes for this repository.

## License

See [LICENSE](./LICENSE).

## Active Skills

- `bootstrap-python-mcp-service`
- `bootstrap-python-service`
- `bootstrap-uv-python-workspace`
- `integrate-fastapi-fastmcp`
- `uv-pytest-unit-testing`

## Packaging

This repository intentionally separates the authored surface from the packaged plugin root.

- root [`skills/`](./skills/) is the canonical authored workflow surface
- [`plugins/python-skills/`](./plugins/python-skills/) is the packaged Codex plugin root used by the `socket` marketplace
- [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json) carries the Claude-side marketplace metadata

## Repository Layout

```text
.
├── .claude-plugin/
│   └── marketplace.json
├── AGENTS.md
├── LICENSE
├── README.md
├── ROADMAP.md
├── docs/
├── plugins/
│   └── python-skills/
│       ├── .claude-plugin/
│       ├── .codex-plugin/
│       └── skills -> ../../skills
├── pyproject.toml
├── skills/
├── tests/
└── uv.lock
```
