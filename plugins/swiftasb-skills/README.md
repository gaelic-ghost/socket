# swiftasb-skills

Codex skills for explaining [SwiftASB](https://github.com/gaelic-ghost/SwiftASB) and building Swift apps or packages on top of it.

## Table of Contents

- [Overview](#overview)
- [Usage](#usage)
- [Development](#development)
- [Verification](#verification)
- [Release Notes](#release-notes)
- [License](#license)
- [Active Skills](#active-skills)
- [Packaging](#packaging)
- [Repository Layout](#repository-layout)

## Overview

`swiftasb-skills` is the SwiftASB companion guidance plugin in Gale's skills ecosystem.

### Status

This directory is active as normal monorepo-owned content inside `socket` and ships the SwiftASB companion workflow set.

### What This Project Is

This plugin helps Codex agents explain SwiftASB, choose an integration shape, implement SwiftUI-facing, AppKit-facing, and package-author SwiftASB work, and diagnose integration failures. SwiftASB itself remains the source of truth for the Swift package, public API, DocC, release notes, generated wire maintenance, and licensing.

### Motivation

SwiftASB users need agents to make good adoption and integration decisions before code changes start. This plugin gives agents a Codex-visible workflow surface for that work without requiring SwiftPM dependency checkouts to act as plugin roots.

## Usage

Use `swiftasb-skills` when the work is specifically about:

- explaining what SwiftASB does and whether it fits a user's Swift project
- choosing between SwiftUI, AppKit, command-line, helper-service, or package-author integration shapes
- building SwiftUI state around SwiftASB's `CodexAppServer`, `CodexThread`, `CodexTurnHandle`, and observable companions
- diagnosing SwiftASB integration failures across runtime discovery, app-server startup, threads, turns, approvals, diagnostics, MCP status, history reads, and live-test isolation

Use `apple-dev-skills` for Apple framework rules, Xcode workflow selection, SwiftUI/AppKit lifecycle behavior, DocC, build, and test execution.

## Development

Treat root [`skills/`](./skills/) as the source of truth for shipped workflow content. Treat [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) as install-surface metadata.

Before changing exact SwiftASB API guidance, verify the current SwiftASB package state through the local checkout or [GitHub repository](https://github.com/gaelic-ghost/SwiftASB). The first supported public API baseline is `v1.0.0`; the current released baseline is `v1.0.1`, and the local package may be under active development.

## Verification

From the Socket root, run:

```bash
uv run scripts/validate_socket_metadata.py
```

Also review changed skills for stale SwiftASB symbol names and source-of-truth links.

## Release Notes

Use `socket` Git history and GitHub releases to track shipped changes for this directory.

`swiftasb-skills` follows the shared `socket` semantic version. Version inventory and version bumps must run through the root [`scripts/release.sh`](../../scripts/release.sh) workflow.

## License

See [LICENSE](../../LICENSE) for the Socket superproject license. SwiftASB package licensing is documented in the [SwiftASB repository](https://github.com/gaelic-ghost/SwiftASB).

## Active Skills

- `explain-swiftasb`
- `choose-integration-shape`
- `build-swiftui-app`
- `build-appkit-app`
- `build-swift-package`
- `diagnose-integration`

## Packaging

This repository intentionally keeps authored content and plugin metadata separate.

- root [`skills/`](./skills/) is the canonical authored workflow surface
- [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) defines the Codex plugin metadata at the repo root
- the Socket marketplace entry points at `./plugins/swiftasb-skills`

## Repository Layout

```text
.
├── .codex-plugin/
│   └── plugin.json
├── AGENTS.md
├── README.md
└── skills/
```
