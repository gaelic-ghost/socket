# agent-plugin-skills

Maintainer-skill repository for skills-export and plugin-export repos.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Development](#development)
- [Verification](#verification)
- [Release Notes](#release-notes)
- [License](#license)
- [Active Skills](#active-skills)
- [Repository Layout](#repository-layout)

## Overview

`agent-plugin-skills` packages maintainer-oriented skills for repositories that ship reusable skills or plugins.

### Status

This repository is active and currently ships maintainer workflows for bootstrapping and syncing skills-export repository guidance.

### What This Project Is

This repository is the canonical home for maintainer skills that help Gale keep skills-export repositories honest about packaging, discovery, and documentation boundaries.

### Motivation

It exists so repo-maintenance guidance for skill and plugin repositories can live in one focused place instead of being duplicated across unrelated plugin repos.

## Setup

Sync the repo-local maintainer environment when you want to run tests for the Python-backed maintainer tooling:

```bash
uv sync --dev
```

## Usage

Use these skills when the target repository is itself a skills-export or plugin-export repository and the job is about repo structure, packaging guidance, or cross-surface documentation alignment.

For general repository doc and maintenance workflows, treat `productivity-skills` as the default baseline layer first. Reach for `agent-plugin-skills` only when that broader baseline is not specific enough for a repo that exports skills or plugins as its actual shipped surface.

This repo is deliberately blunt about a core limitation: OpenAI's documented Codex plugin system still exposes repo-visible plugins through the documented marketplace model rather than through a richer private repo-scoping system.

## Development

### Setup

Treat root [`skills/`](./skills/) as the canonical authored surface. Keep maintainer docs under [`docs/`](./docs/) and plugin metadata under [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).

### Workflow

When you update a skill here, keep the surrounding maintainer guidance and tests aligned in the same pass. Do not invent hidden install surfaces or overstate Codex plugin scoping behavior.

## Verification

Run the repo-local maintainer tests before landing changes that touch skill behavior or metadata:

```bash
uv sync --dev
uv run pytest
```

## Release Notes

Use Git history and GitHub releases to track shipped changes to the maintainer-skill surface.

## License

See [LICENSE](./LICENSE).

## Active Skills

- `bootstrap-skills-plugin-repo`: bootstrap or align a skills-export repository around root `skills/`, discovery mirrors, and maintainer guidance
- `sync-skills-repo-guidance`: audit guidance drift across README, AGENTS, maintainer docs, and discovery mirrors in an existing skills-export repository

## Repository Layout

```text
.
├── .codex-plugin/
│   └── plugin.json
├── AGENTS.md
├── LICENSE
├── README.md
├── ROADMAP.md
├── docs/
├── pyproject.toml
├── skills/
└── uv.lock
```
