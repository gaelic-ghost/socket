# apple-dev-skills

Apple, Swift, and Xcode workflow skills for Codex and Claude Code.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Development](#development)
- [Repo Structure](#repo-structure)
- [Active Skills](#active-skills)
- [Release Notes](#release-notes)
- [License](#license)

## Overview

### Status

This repository is active and available for maintainer use.

### What This Project Is

This repository is the canonical source of truth for Gale's Apple, Swift, and Xcode workflow skills. Treat `productivity-skills` as the default baseline layer for general repo-doc and maintenance work, and use `apple-dev-skills` when Apple-specific assumptions should actively shape the workflow.

### Motivation

It exists to keep Apple-platform workflow guidance in one dedicated repository with explicit requirements around Apple documentation, Xcode-safe workflows, and clear source-of-truth boundaries.

## Quick Start

This repository is primarily the authored source tree for the shipped Apple workflow skills rather than an end-user app with a separate getting-started path. If you want to understand what the repo currently ships, start with [Active Skills](#active-skills) and [`docs/maintainers/workflow-atlas.md`](./docs/maintainers/workflow-atlas.md). If you want to modify the repository, go to [Development](#development) and use [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the maintainer workflow.

## Usage

Use this repository's skills when the work is about:

- Swift or SwiftUI implementation
- Apple UI accessibility implementation or review
- SwiftUI app structure, focus design, scene ownership, or command architecture
- Xcode build, run, or test workflows
- DocC symbol comments, articles, catalog structure, or DocC-oriented review
- Swift source cleanup, file-header normalization, or source-organization policy
- Swift package bootstrap or validation
- Apple-project guidance sync
- Apple-platform documentation routing

Use [`CONTRIBUTING.md`](./CONTRIBUTING.md) for maintainer workflow details, and use [`ROADMAP.md`](./ROADMAP.md) for planned and completed milestone-level work.

## Development

### Setup

Sync the maintainer environment before editing skills, tests, or maintainer docs:

```bash
uv sync --dev
```

### Workflow

Treat root [`skills/`](./skills/) as the canonical authored surface. Keep shared reusable assets in [`shared/`](./shared/), maintainer docs in [`docs/`](./docs/), and install metadata in [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) and [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json).

Keep the repo honest about its Apple docs-first policy. When a skill changes, update the relevant tests and maintainer guidance in the same pass rather than letting the packaging or guidance drift. Use [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the normal contributor workflow and review expectations.

### Validation

Run the repository test suite for skill and metadata changes:

```bash
bash .github/scripts/validate_repo_docs.sh
uv run pytest
```

## Repo Structure

```text
.
├── .codex-plugin/
├── .claude-plugin/
├── AGENTS.md
├── CONTRIBUTING.md
├── README.md
├── ROADMAP.md
├── docs/maintainers/
├── shared/
├── skills/
└── tests/
```

## Active Skills

- `bootstrap-swift-package`
- `bootstrap-xcode-app-project`
- `author-swift-docc-docs`
- `explore-apple-swift-docs`
- `apple-ui-accessibility-workflow`
- `format-swift-sources`
- `structure-swift-sources`
- `swiftui-app-architecture-workflow`
- `swift-package-build-run-workflow`
- `swift-package-testing-workflow`
- `swift-package-workflow`
- `sync-swift-package-guidance`
- `sync-xcode-project-guidance`
- `xcode-app-project-workflow`
- `xcode-build-run-workflow`
- `xcode-testing-workflow`

## Release Notes

Use Git history and GitHub releases to track shipped changes for this repository.

## License

See [LICENSE](./LICENSE).
