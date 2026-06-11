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
- `codex-utilities`
- `dotnet-skills`
- `productivity-skills`
- `python-skills`
- `server-side-swift`
- `rust-skills`
- `speak-swiftly`
- `swiftasb-skills`
- `things-app`
- `web-dev-skills`

## Plugin Status

Apple Dev Skills is Socket-owned under `plugins/apple-dev-skills` and keeps its public README because existing users can still arrive through the standalone compatibility marketplace. Other child planning now lives in [TODO.md](./TODO.md).

Current Socket catalog shape:

- `agent-plugin-skills`: maintainer skills plus a source-bundled guidance-sync custom-agent definition for skills-export and plugin-export repositories
- `apple-dev-skills`: Apple, Swift, SwiftUI, AppKit, Xcode, Swift OpenAPI client, Safari, DocC workflows, and the source-bundled `swift-steward` custom-agent definition with its own roadmap
- `cardhop-app`: mixed skill plus bundled MCP server for Cardhop.app contact workflows
- `codex-utilities`: local Codex runtime utilities, starting with hooks that prefix generated Codex thread titles with the project directory name
- `dotnet-skills`: .NET, F#, and C# project-shape, bootstrap, implementation, test, package, diagnostics, ASP.NET Core, interop, CI, upgrade, and tooling guidance
- `productivity-skills`: general-purpose maintainer, documentation, Codex GUI worktree workflow, and automation-design workflows plus source-bundled docs-audit and code-tracing custom-agent definitions
- `python-skills`: Python runtime and tooling workflows for Python-based projects; see the [Python skills expansion plan](./docs/maintainers/python-skills-plugin-plan.md) for maintainer details
- `server-side-swift`: server-side Swift support plus the source-bundled `server-swift-steward` custom-agent definition for services with frameworks like Vapor and Hummingbird
- `rust-skills`: Rust, Cargo, rustup, crate, workspace, CLI, library, package, CI, test, lint, and format workflow guidance
- `speak-swiftly`: Git-backed Speak Swiftly plugin from the standalone SpeakSwiftlyServer repository
- `swiftasb-skills`: SwiftASB companion guidance
- `things-app`: mixed skill plus bundled MCP server for Things.app workflows
- `web-dev-skills`: Expo SDK 56+ inline native modules, type generation, native-boundary inspection, and validation handoff guidance

Placeholder directories for future plugins (not available for install):

- `android-dev-skills`
- `spotify`

## Development

For setup, local workflow, validation, review, release, and maintainer expectations, see [CONTRIBUTING.md](./CONTRIBUTING.md). For the consolidated child backlog, see [TODO.md](./TODO.md). For agent-facing repo rules, see [AGENTS.md](./AGENTS.md).

## Repo Structure

```text
.
├── .agents/
│   ├── plugins/marketplace.json
│   └── socket-steward/
├── docs/
│   ├── agents/
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

The `socket` superproject, and all nested projects, are licensed under the PolyForm Noncommercial License 1.0.0 for future public versions. See [LICENSE](./LICENSE), [NOTICE](./NOTICE), and [COMMERCIAL-USE.md](./COMMERCIAL-USE.md).

Commercial use requires a separate written commercial license from Gale. For commercial licensing, contact Gale W at <mail@galewilliams.com>.

Socket versions published before the PolyForm Noncommercial change remain available under the license terms that applied to those versions. The historical Apache License 2.0 text is preserved in [LICENSE-HISTORICAL-APACHE-2.0](./LICENSE-HISTORICAL-APACHE-2.0).
