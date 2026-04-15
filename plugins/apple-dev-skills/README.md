# apple-dev-skills

Apple, Swift, and Xcode workflow skills for Codex and Claude Code.

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

`apple-dev-skills` bundles reusable workflows for Apple-platform development work across Swift, SwiftUI, Xcode, SwiftPM, testing, formatting, and repo-guidance maintenance.

### Status

This repository is active and currently ships Apple-platform development skills plus shared maintainer resources and tests.

Recent work strengthened two of the more infrastructure-heavy surfaces:

- `structure-swift-sources` now has a clearer structural-cleanup contract, stronger file-header guidance, and a user-facing header inventory template.
- `explore-apple-swift-docs` now teaches direct Xcode MCP and Dash lookup paths first, with Dash localhost HTTP documented as the direct machine-readable fallback.

### What This Project Is

This repository is the canonical source of truth for Gale's Apple, Swift, and Xcode workflow skills. Treat `productivity-skills` as the default baseline layer for general repo-doc and maintenance work, and use `apple-dev-skills` when Apple-specific assumptions should actively shape the workflow.

### Motivation

It exists to keep Apple-platform workflow guidance in one dedicated repository with explicit requirements around Apple documentation, Xcode-safe workflows, and clear source-of-truth boundaries.

## Setup

Sync the maintainer environment before running repo-local validation:

```bash
uv sync --dev
```

## Usage

Use this repository's skills when the work is about:

- Swift or SwiftUI implementation
- Xcode build, run, or test workflows
- DocC symbol comments, articles, catalog structure, or DocC-oriented review
- Swift source cleanup, file-header normalization, or source-organization policy
- Swift package bootstrap or validation
- Apple-project guidance sync
- Apple-platform documentation routing

## Development

### Setup

Treat root [`skills/`](./skills/) as the canonical authored surface. Keep shared reusable assets in [`shared/`](./shared/), maintainer docs in [`docs/`](./docs/), and install metadata in [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) and [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json).

### Workflow

Keep the repo honest about its Apple docs-first policy. When a skill changes, update the relevant tests and maintainer guidance in the same pass rather than letting the packaging or guidance drift.

## Verification

Run the repository test suite for skill and metadata changes:

```bash
uv sync --dev
uv run pytest
```

## Release Notes

Use Git history and GitHub releases to track shipped changes for this repository.

## License

See [LICENSE](./LICENSE).

## Active Skills

- `bootstrap-swift-package`
- `bootstrap-xcode-app-project`
- `author-swift-docc-docs`
- `explore-apple-swift-docs`
- `format-swift-sources`
- `structure-swift-sources`
- `swift-package-build-run-workflow`
- `swift-package-testing-workflow`
- `swift-package-workflow`
- `sync-swift-package-guidance`
- `sync-xcode-project-guidance`
- `xcode-app-project-workflow`
- `xcode-build-run-workflow`
- `xcode-testing-workflow`

## Repository Layout

```text
.
├── .claude-plugin/
│   └── marketplace.json
├── .codex-plugin/
│   └── plugin.json
├── AGENTS.md
├── LICENSE
├── README.md
├── ROADMAP.md
├── docs/
├── pyproject.toml
├── shared/
├── skills/
├── tests/
└── uv.lock
```
