# socket

*The macOS Marketplace for Codex*

![Socket neon banner with a glowing purple wordmark connected to a wall outlet.](./docs/media/socket-banner.jpg)

![Codex plugin directory filtered to the Socket marketplace, showing Productivity Skills featured above installable Socket child plugins.](./docs/media/codex-plugin-directory-socket-productivity-skills.png)

Promo audio: [Socket Codex Marketplace Promo](./docs/media/socket-codex-marketplace-promo.mp3)

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Plugin Status](#plugin-status)
- [Development](#development)
- [Repo Structure](#repo-structure)
- [Release Notes](#release-notes)
- [License](#license)

## Overview

### Status

`socket` is maintained by Gaelic Ghost.

### What This Project Is

Socket is a Marketplace of Plugins, Hooks, and MCP servers for Apple Platform Devs

### Motivation

Agents are great, but to do specialized work, they need specialized tools. Socket is a shared catalog for focused Codex plugins, hooks, skills, and MCP-backed workflows.

## Quick Start

Add the `socket` marketplace to Codex with:

```bash
codex plugin marketplace add gaelic-ghost/socket
```

After adding `socket`, restart your Codex, open the plugin directory, select `Socket`, and then install your choice of plugins.

When the marketplace changes, refresh it with:

```bash
codex plugin marketplace upgrade socket
```

Newly added plugins can be installed from the same plugin directory inside Codex.

## Usage

Use `socket` when you want one Codex catalog for focused agent workflow plugins.

Currently available from the catalog:

- `agent-plugin-skills`
- `apple-dev-skills`
- `cardhop-app`
- `dotnet-skills`
- `productivity-skills`
- `python-skills`
- `speak-swiftly`
- `swiftasb-skills`
- `things-app`

## Plugin Status

Apple Dev Skills keeps its own roadmap because it is the remaining subtree-managed child with a deeper standalone release surface. Other child planning now lives in [TODO.md](./TODO.md).

Current Socket catalog shape:

- `agent-plugin-skills`: maintainer skills for skills-export and plugin-export repositories
- `apple-dev-skills`: Apple, Swift, SwiftUI, Xcode, and DocC workflows with its own roadmap
- `cardhop-app`: mixed skill plus bundled MCP server for Cardhop.app contact workflows
- `dotnet-skills`: .NET, F#, and C# project-shape, bootstrap, implementation, test, package, diagnostics, ASP.NET Core, interop, CI, upgrade, and tooling guidance
- `productivity-skills`: general-purpose maintainer and documentation workflow baseline
- `python-skills`: Python, `uv`, project implementation, diagnostics, packaging, tooling, CI, upgrades, FastAPI, FastMCP, and pytest workflow plugin
- `speak-swiftly`: Git-backed Speak Swiftly plugin from the standalone SpeakSwiftlyServer repository
- `swiftasb-skills`: SwiftASB companion guidance
- `things-app`: mixed skill plus bundled MCP server for Things.app workflows

Placeholder directories for future plugins (not available for install):

- `rust-skills`
- `spotify`
- `web-dev-skills`

## Development

For setup, local workflow, validation, review, release, and maintainer expectations, see [CONTRIBUTING.md](./CONTRIBUTING.md). For the consolidated child backlog, see [TODO.md](./TODO.md). For agent-facing repo rules, see [AGENTS.md](./AGENTS.md).

## Repo Structure

```text
.
├── .agents/plugins/marketplace.json
├── docs/
│   ├── media/
│   └── maintainers/
├── plugins/
├── scripts/
├── AGENTS.md
├── CONTRIBUTING.md
├── README.md
├── TODO.md
└── ROADMAP.md
```

## Release Notes

Use GitHub releases and Git history for root `socket` changes. Child plugins may carry their own release notes and maintainer docs.

## License

The `socket` superproject, and all nested projects, are licensed under the Apache License 2.0. See [LICENSE](./LICENSE) and [NOTICE](./NOTICE).
