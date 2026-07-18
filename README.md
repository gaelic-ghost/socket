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

### Hermes Agent

Socket publishes an explicit Hermes compatibility surface for portable skills
and translated MCP configuration:

```bash
hermes skills tap add gaelic-ghost/socket
hermes skills install gaelic-ghost/socket/hermes-agent-compatibility
```

Codex plugin bundles remain host-specific. See the
[Hermes compatibility guide](./docs/maintainers/hermes-compatibility.md) for
the available skill tap, MCP translations, and the cases that need a native
Hermes plugin.

### Claude Code and Cowork

Socket also publishes a Claude marketplace. In Claude Code, add it with:

```bash
claude plugin marketplace add gaelic-ghost/socket
```

Then install the individual Socket plugins you want. Cowork users can add the
same GitHub marketplace from **Customize → Plugins**. Socket skills work in
both hosts; local Mac integrations such as Xcode, Cardhop, and Things are
Claude Code-only. Speak Swiftly remains unavailable in this catalog until its
standalone payload has a Claude-native hook boundary. See the
[Claude compatibility guide](./docs/maintainers/claude-compatibility.md) for
the full support boundary and update flow.

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
- `apple-creator-studio-skills`
- `apple-dev-skills`
- `cardhop-app`
- `cloud-deployment-skills`
- `cloud-inference-skills`
- `cybersecurity-skills`
- `messaging-collaboration-skills`
- `agentdeck`
- `dotnet-skills`
- `game-dev-skills`
- `network-protocol-skills`
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
- `apple-creator-studio-skills`: source-preserving Final Cut Pro editing, Motion template, Compressor delivery, Logic Pro production, MainStage concert, and GarageBand project workflows with local Help Viewer discovery, explicit Computer Use safeguards, and artifact or rehearsal verification
- `apple-dev-skills`: Apple, Swift, Core Image and Image I/O, Vision and Core ML recognition, AVFoundation camera and depth capture, ARKit spatial sensing, VideoToolbox and Core Video codecs, PhotosUI and PhotoKit, AVFAudio, Core Media, Core Audio, SwiftUI, AppKit, Xcode, Safari, OpenAPI, and DocC workflows, plus the source-bundled `swift-steward` custom-agent definition with its own roadmap
- `cardhop-app`: mixed skill plus bundled MCP server for Cardhop.app contact workflows
- `cloud-deployment-skills`: cloud provider deployment routing, official provider plugin selection, credential and mutation boundary checks, and AWS handoff to the official AWS Agent Toolkit rather than duplicated AWS MCP, CLI, or SAM setup
- `cloud-inference-skills`: cloud AI inference, training, model conversion, and GPU infrastructure routing for Runpod, Hugging Face, AWS, Vast.ai, CoreWeave, and similar providers, with bundled Runpod MCP server configuration, upstream Runpod skill mirrors, and first-party Hugging Face/AWS handoffs
- `cybersecurity-skills`: suspicious-content triage, evidence preservation, malware analysis, isolation, agentic security-tool controls, macOS investigation and defense, vulnerability validation, authorized web/API and network testing, incident response, threat hunting, detection content, and clear non-specialist advice
- `messaging-collaboration-skills`: chat-app, bot, business-messaging, meeting-collaboration, iMessage collaboration, Communication Notifications, Push to Talk, VoIP/SIP, documented iOS/iPadOS default communication roles, and app-owned macOS client workflows for Discord, Telegram, Slack, Teams, WhatsApp Business, SMS/MMS/RCS, Google Meet, and Apple communication surfaces, with explicit Signal and Mac operator-automation boundaries
- `agentdeck`: local Codex runtime utilities, starting with hooks that prefix generated Codex thread titles with the project directory name
- `dotnet-skills`: .NET, F#, and C# project-shape, bootstrap, implementation, test, package, diagnostics, ASP.NET Core, interop, CI, upgrade, and tooling guidance
- `game-dev-skills`: Apple platform game development workflows for native Metal and Metal 4 renderers, GPTK 3/4 routing, MetalFX, GPU asset streaming, experimental neural rendering, SpriteKit, SceneKit, GameplayKit simulation, Game Controller input, Core Haptics feedback, Xcode profiling, game-stack routing, and device-aware validation handoffs
- `network-protocol-skills`: modern networking and application-protocol workflows for transport selection, HTTP/3 and QUIC planning, Media over QUIC draft-aware guidance, WebRTC signaling/media/data-channel work, and protocol diagnostics with stack-plugin handoffs
- `productivity-skills`: general-purpose maintainer, documentation, Dice MCP job-search with bundled remote MCP config, Codex GUI worktree workflow, and automation-design workflows plus source-bundled docs-audit and code-tracing custom-agent definitions
- `python-skills`: Python runtime and tooling workflows for Python-based projects; see the [Python skills expansion plan](./docs/maintainers/python-skills-plugin-plan.md) for maintainer details
- `reverse-engineering-skills`: artifact triage, preservation, exact-build comparison, decompiler review, Apple Mach-O/runtime/signing/Apple Silicon/dyld/dynamic/kernel research, Cutter/Rizin, Malimite, Ghidra, Hopper, .NET, Unity and IL2CPP, and reproducible security evidence workflows
- `server-side-jvm`: server-side JVM, Java, Scala, Gradle, Maven, SBT, and testing workflow guidance, with future Clojure support planned
- `server-side-swift`: server-side Swift bootstrap and guidance sync, Vapor, Hummingbird, hb Server/Lambda flows, persistence, OpenAPI/RPC, SwiftNIO, observability, auth, app sync, Docker, Apple Containerization, and Fly.io support plus the source-bundled `server-swift-steward` custom-agent definition
- `swift-lang`: shared Swift language, API style, error handling, functional pipelines, formatting, source organization, SwiftSyntax transformation, compiler inspection, SourceKit semantics and indexing, SourceKit-LSP diagnosis, Swiftly/Xcode toolchain routing, and modernization cleanup workflows
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
