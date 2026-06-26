# apple-dev-skills

Apple, Swift, SwiftUI, AppKit, Icon Composer app icons, Safari, Xcode, Swift OpenAPI client, DocC, and `Dash.app` workflows for Codex.

![Codex plugin directory filtered to the Socket marketplace, showing Apple Dev Skills listed alongside companion plugins below a Productivity Skills suggestion.](./docs/media/codex-plugin-directory-socket-apple-dev-skills.png)

Promo audio: [Apple Dev Skills Codex Workflows Promo](./docs/media/apple-dev-skills-codex-workflows-promo.mp3)

The Socket marketplace is the easiest way to install Apple Dev Skills alongside the companion Productivity Skills workflows.

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

`apple-dev-skills` is maintained and supported by Gale as a key component of the Socket Marketplace.

### What This Project Is

Apple development work has sharp edges around framework behavior, Xcode project state, documentation, accessibility, and build tooling. This plugin keeps helps agents move *swiftly* through a challenging landscape, instead of fumbling over mountains of implicit behavior.

This repository is the canonical source of truth for Gale's Apple, Swift, and Xcode workflow skills.

### Motivation

I wanted to build stuff faster, but agents were struggling with Swift, declarative frameworks, Xcode and `.pbxproj`, the `swift build` `xcodebuild` split, etc. I figured I could improve that a bit. it's gone pretty well, so far~

## Quick Start

The easiest way to install Apple Dev Skills with its companion workflows is through Gale's Socket marketplace:

```bash
codex plugin marketplace add gaelic-ghost/socket
```

Restart Codex, open the plugin directory, choose `Socket`, and install or enable `apple-dev-skills`. Install `productivity-skills` from the same marketplace too if you want the Apple bootstrap and guidance-sync workflows.

When the Socket marketplace changes, refresh it:

```bash
codex plugin marketplace upgrade socket
```

## Usage

Use Apple Dev Skills when an agent is helping with:

- AVFAudio session, route, interruption, permission, and app-audio policy repair
- AVAudioEngine graph, format, rendering, tap, and real-time callback repair
- AVFoundation capture, playback, async asset loading, reader, writer, and export workflows
- Core Media timing, sample-buffer, format-description, and synchronization diagnostics
- Core Audio and Audio Toolbox modernization or legacy repair
- Swift and SwiftUI implementation
- AppKit and mixed AppKit/SwiftUI architecture
- Xcode build, run, test, and project workflows
- Xcode coding intelligence, Xcode-hosted agents, and external-agent MCP setup
- Icon Composer app icon design, preview, and Xcode handoff
- Safari extension and SafariServices integration choices
- Swift OpenAPI client generation and `URLSession` transport integration
- Swift package bootstrap, build, and testing
- Apple UI accessibility work
- DocC comments, articles, and documentation catalogs
- Swift source formatting and file organization, with shared language cleanup routed to `swift-lang` when installed through Socket
- Apple docs lookup before design or code changes
- Apple-specific repo guidance setup or refresh

Most Apple Dev Skills workflows are useful as a standalone plugin. Bootstrap and guidance-sync workflows also need `productivity-skills`, because that companion plugin owns the reusable repo-maintenance workflow that Apple Dev Skills applies to Swift packages and Xcode apps.

Treat `productivity-skills` as the default baseline layer for general repo-doc and maintenance work, and use Apple Dev Skills when Apple-specific behavior should shape the workflow.

The [`socket`](https://github.com/gaelic-ghost/socket) repository is Gale's plugin superproject and marketplace catalog.

If you only want the Apple plugin without the rest of Socket, the standalone marketplace remains supported:

```bash
codex plugin marketplace add gaelic-ghost/apple-dev-skills
codex plugin marketplace upgrade apple-dev-skills
```

When installed as a Codex plugin, Apple Dev Skills also registers Xcode's built-in MCP bridge through `xcrun mcpbridge`. Users still need to allow external agents in Xcode's Intelligence settings and keep the relevant project open in Xcode before external Codex sessions can use Xcode-provided tools.

## Development

Treat root [`skills/`](./skills/) as the canonical authored surface. Keep shared reusable assets in [`shared/`](./shared/) and tests in [`tests/`](./tests/).

Use [`CONTRIBUTING.md`](./CONTRIBUTING.md) for maintainer workflow details, and use [AGENTS.md](./AGENTS.md) for agent-facing repo rules.

Run the repository test suite for skill and metadata changes:

```bash
bash .github/scripts/validate_repo_docs.sh
uv run pytest
```

## Repo Structure

```text
.
├── .codex-plugin/
├── .mcp.json
├── docs/
├── shared/
├── skills/
├── tests/
├── AGENTS.md
├── CONTRIBUTING.md
├── README.md
└── ROADMAP.md
```

## Active Skills

- `apple-ui-accessibility-workflow`
- `appkit-app-architecture-workflow`
- `author-swift-docc-docs`
- `avaudio-engine-workflow`
- `avfaudio-session-workflow`
- `avfoundation-media-pipeline-workflow`
- `bootstrap-swift-package`
- `bootstrap-xcode-app-project`
- `coreaudio-modernization-repair-workflow`
- `coremedia-timing-samplebuffer-workflow`
- `explore-apple-swift-docs`
- `format-swift-sources`
- `icon-composer-app-icon-workflow`
- `safari-extension-control-workflow`
- `structure-swift-sources`
- `swift-openapi-client-workflow`
- `swift-package-build-run-workflow`
- `swift-package-testing-workflow`
- `swift-package-workflow`
- `swiftui-app-architecture-workflow`
- `sync-swift-package-guidance`
- `sync-xcode-project-guidance`
- `xcode-app-project-workflow`
- `xcode-build-run-workflow`
- `xcode-coding-intelligence-workflow`
- `xcode-testing-workflow`

## Release Notes

Use GitHub releases and Git history to track shipped changes for this repository.

## License

This repository is licensed under the PolyForm Noncommercial License 1.0.0. See [LICENSE](./LICENSE).

Commercial use requires a separate written commercial license from Gale. For commercial licensing, contact Gale W at <mail@galewilliams.com>. See the Socket root [COMMERCIAL-USE.md](../../COMMERCIAL-USE.md) for the current commercial-use policy.
