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

### Xcode 27 Beta

For Xcode 27 beta, add Socket through Xcode's official Plug-ins UI:

1. Open Xcode Settings.
2. Select Intelligence.
3. Open Plug-ins.
4. Choose Add Plug-in.
5. Choose Add from URL.
6. Enter:

```text
https://github.com/gaelic-ghost/socket.git
```

Xcode should enumerate the Socket child plug-ins from the public repository and let you import only the plug-ins you trust and need.

The Import from Codex path is still under evaluation for Xcode 27 beta. In current local testing, Xcode can see Codex-installed plug-ins, but it may select stale standalone or local-cache payloads when the same plug-in also exists outside the current Socket marketplace install. Prefer Add from URL for Socket until that beta behavior is better understood.

### Zed

For Zed's Codex external agent, install and update Socket through the normal Codex marketplace flow. Current local testing shows Zed's bundled `codex-acp` path inherits the user's normal Codex home by default, so Codex-in-Zed sees the same global `~/.codex` config, Socket marketplace cache, installed plug-ins, skills, and MCP servers as the regular Codex CLI and GUI unless Zed or the adapter is launched with an explicit `CODEX_HOME`.

Zed's own first-party Agent uses Zed-native skills and MCP configuration. Treat that as a separate compatibility surface from Codex running inside Zed through ACP.

## Usage

Use `socket` when you want one Codex catalog for focused agent workflow plugins.

Currently available from the catalog:

- `agent-portability-skills`
- `android-dev-skills`
- `apple-dev-skills`
- `cardhop-app`
- `cloud-deployment-skills`
- `codex-utilities`
- `dotnet-skills`
- `game-dev-skills`
- `productivity-skills`
- `python-skills`
- `reverse-engineering-skills`
- `server-side-jvm`
- `server-side-swift`
- `swift-lang`
- `rust-skills`
- `speak-swiftly`
- `swiftasb-skills`
- `things-app`
- `web-dev-skills`

## Plugin Status

Apple Dev Skills is Socket-owned under `plugins/apple-dev-skills` and keeps its public README because existing users can still arrive through the standalone compatibility marketplace. Other child planning now lives in [ROADMAP.md](./ROADMAP.md).

Current Socket catalog shape:

- `agent-portability-skills`: maintainer skills plus a source-bundled guidance-sync custom-agent definition for Socket-owned agent skill portability, Codex plugin surfaces, and host adapter guidance
- `android-dev-skills`: Android, Kotlin, Java, Gradle, Android Gradle Plugin, Compose/XML UI, testing, lint, emulator-aware validation handoff, and release-readiness workflow guidance
- `apple-dev-skills`: Apple, Swift, SwiftUI animation and architecture, Core Animation, Apple typography, SF Symbols, AppKit, Xcode, strict media type selection for AVFoundation, AVFAudio, Core Media, Core Audio, Audio Toolbox, Swift OpenAPI client, Safari, DocC workflows, and the source-bundled `swift-steward` custom-agent definition with its own roadmap
- `cardhop-app`: mixed skill plus bundled MCP server for Cardhop.app contact workflows
- `cloud-deployment-skills`: cloud provider deployment routing, official provider plugin selection, credential and mutation boundary checks, and AWS handoff to the official AWS Agent Toolkit rather than duplicated AWS MCP, CLI, or SAM setup
- `codex-utilities`: local Codex runtime utilities, starting with hooks that prefix generated Codex thread titles with the project directory name
- `dotnet-skills`: .NET, F#, and C# project-shape, bootstrap, implementation, test, package, diagnostics, ASP.NET Core, interop, CI, upgrade, and tooling guidance
- `game-dev-skills`: Apple platform game development workflows for SpriteKit, SceneKit, GameplayKit simulation, Game Controller input, Core Haptics feedback, Xcode game profiling, game-stack routing, and device-aware validation handoffs
- `productivity-skills`: general-purpose maintainer, documentation, Dice MCP job-search with bundled remote MCP config, Codex GUI worktree workflow, and automation-design workflows plus source-bundled docs-audit and code-tracing custom-agent definitions
- `python-skills`: Python runtime and tooling workflows for Python-based projects; see the [Python skills expansion plan](./docs/maintainers/python-skills-plugin-plan.md) for maintainer details
- `reverse-engineering-skills`: binary inspection, artifact triage, and reproducible reverse-engineering note workflows
- `server-side-jvm`: server-side JVM, Java, Scala, Gradle, Maven, SBT, and testing workflow guidance, with future Clojure support planned
- `server-side-swift`: server-side Swift bootstrap and guidance sync, Vapor, Hummingbird, hb Server/Lambda flows, persistence, OpenAPI/RPC, SwiftNIO, observability, auth, app sync, Docker, Apple Containerization, and Fly.io support plus the source-bundled `server-swift-steward` custom-agent definition
- `swift-lang`: shared Swift language, API style, error handling, functional pipelines, formatting, source organization, and modernization cleanup workflows
- `rust-skills`: Rust, Cargo, rustup, crate, workspace, CLI, library, package, CI, test, lint, and format workflow guidance
- `speak-swiftly`: Git-backed Speak Swiftly plugin from the standalone SpeakSwiftlyServer repository
- `swiftasb-skills`: SwiftASB companion guidance
- `things-app`: mixed skill plus bundled MCP server for Things.app workflows
- `web-dev-skills`: Expo SDK 56+ inline native modules, type generation, native-boundary inspection, and validation handoff guidance

Placeholder directories for future plugins (not available for install):

- `spotify`

## Development

For setup, local workflow, validation, review, release, and maintainer expectations, see [CONTRIBUTING.md](./CONTRIBUTING.md). For the consolidated child backlog, see [ROADMAP.md](./ROADMAP.md). For agent-facing repo rules, see [AGENTS.md](./AGENTS.md).

For Xcode 27 beta Markdown editing and repository browsing, open [`Socket.xcworkspace`](./Socket.xcworkspace). It is a browse-only workspace for docs, plugin payloads, scripts, and marketplace metadata; it is not a root build surface.

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
├── Socket.xcworkspace
└── ROADMAP.md
```

## Release Notes

Use GitHub releases and Git history for root `socket` changes. Child plugins may carry their own release notes and maintainer docs.

## License

The `socket` superproject, and all nested projects, are licensed under the Apache License 2.0. See [LICENSE](./LICENSE) and [NOTICE](./NOTICE).
