# productivity-skills

Broadly useful workflow and maintainer skills for Codex and Claude Code.

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

`productivity-skills` bundles general-purpose workflows for documentation maintenance, roadmap work, repository hygiene, and plain-language code explanation.

### Status

This repository is active and currently ships a small set of broadly reusable maintainer and explanation skills.

### What This Project Is

This repository is the canonical home for Gale's general-purpose productivity workflow families that are meant to stay useful across many repos instead of collapsing into one stack-specific plugin.

### Motivation

It exists to keep the baseline versions of common maintainer workflows in one focused repository, while leaving stronger stack-specific variants to dedicated plugins.

## Setup

Sync the repo-local maintainer environment before running tests:

```bash
uv sync --dev
```

## Usage

Use this repository when the work is about:

- explaining code paths in plain language
- maintaining README, AGENTS, CONTRIBUTING, ACCESSIBILITY, or ROADMAP docs
- keeping a general-purpose repository-maintenance baseline aligned

## Development

### Setup

Treat root [`skills/`](./skills/) as the canonical authored surface. Keep install metadata in [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) and [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json), and keep maintainer docs under [`docs/`](./docs/).

### Workflow

When a skill changes, update its tests and any repo-level maintainer guidance in the same pass. Keep the repo focused on general-purpose workflows instead of quietly growing stack-specific assumptions.

## Verification

Run the repo-local test suite for documentation and metadata changes:

```bash
uv sync --dev
uv run pytest
```

## Release Notes

Use Git history and GitHub releases to track shipped changes for this repository.

## License

See [LICENSE](./LICENSE).

## Active Skills

- `explain-code-slice`
- `maintain-project-agents`
- `maintain-project-accessibility`
- `maintain-project-contributing`
- `maintain-project-readme`
- `maintain-project-repo`
- `maintain-project-roadmap`

## Repository Layout

```text
.
├── .claude-plugin/
│   └── marketplace.json
├── .codex-plugin/
│   └── plugin.json
├── AGENTS.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── ROADMAP.md
├── docs/
├── pyproject.toml
├── skills/
└── uv.lock
```
