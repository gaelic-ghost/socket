# apple-dev-skills

Apple, Swift, image and video processing, Vision and Core ML recognition, camera and depth capture, ARKit spatial sensing, Photos, audio and media pipelines, SwiftUI animation and architecture, Core Animation, Apple typography, SF Symbols, AppKit, Apple Developer provisioning, CloudKit, Icon Composer app icons, Safari, DeviceCheck, App Attest, Xcode, Swift OpenAPI client, DocC, and `Dash.app` workflows for Codex.

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

- Strict Apple media type and framework selection across AVFoundation, AVFAudio, Core Media, Core Audio, and Audio Toolbox work
- AVFAudio session, route, interruption, permission, and app-audio policy repair
- AVAudioEngine graph, format, rendering, tap, and real-time callback repair
- AVFoundation capture, playback, async asset loading, reader, writer, and export workflows
- Core Media timing, sample-buffer, format-description, and synchronization diagnostics
- Core Audio and Audio Toolbox modernization or legacy repair
- Core Image filter graphs, RAW development, color management, HDR rendering, custom kernels, and performance repair
- Image I/O decoding, encoding, metadata, thumbnails, auxiliary data, and AppKit/UIKit/Core Graphics representation bridging
- Apple Vision text, barcode, face, landmark, pose, segmentation, tracking, feature-print, coordinate, and live-frame analysis
- Custom Core ML image classification, object detection, semantic segmentation, model provenance, evaluation, and performance integration through Vision
- AVFoundation camera discovery, controls, rotation, photo capture, depth, calibration, synchronized outputs, mattes, and computational-capture diagnostics
- ARKit world tracking, planes, ray casting, scene depth, LiDAR reconstruction, meshes, maps, relocalization, and visionOS provider guidance
- ARKit TrueDepth face geometry, blend shapes, eye transforms, body anchors, skeletons, scale estimation, privacy, and authentication boundaries
- VideoToolbox compression/decompression, Core Video pixel buffers and pools, Core Media compressed samples, hardware capability, color/HDR, and codec diagnostics
- Privacy-preserving PhotosUI selection and PhotoKit authorization, assets, resources, iCloud delivery, changes, creation, albums, and nondestructive editing
- Swift and SwiftUI implementation
- SwiftUI animation, transitions, symbol effects, phase/keyframe motion, and reduce-motion behavior
- Core Animation layer-backed rendering, `CALayer` ownership, `CAAnimation` timing, and model/presentation repair
- Apple typography, San Francisco and New York system designs, Dynamic Type, custom fonts, and font asset boundaries
- SF Symbols selection, rendering, custom symbols, variable color, symbol effects, and app integration
- AppKit and mixed AppKit/SwiftUI architecture
- Xcode build, run, test, and project workflows
- XcodeGen migration and modernization for existing Xcode app projects
- Xcode coding intelligence, Xcode-hosted agents, and external-agent MCP setup
- Xcode String Catalog localization, translator context, plural/device variants, XLIFF handoff, and locale-aware validation
- New Xcode app bootstrap with a default `Sources/Resources/Localizable.xcstrings` catalog, plus guidance-sync audits that require project-aware catalog membership
- Icon Composer app icon design, preview, and Xcode handoff
- Safari extension and SafariServices integration choices
- DeviceCheck per-device state and App Attest app-integrity flow planning
- Safe official App Store Connect provisioning and CloudKit automation planning, with explicit Apple Developer Portal fallbacks
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

When installed as a Codex plugin, Apple Dev Skills declares two Xcode-selected MCP commands: `xcrun mcpbridge` for Xcode's active project and debugging-session tools, plus experimental `xcrun lldb-mcp` for LLDB's standalone MCP bridge. Users still need to allow external agents in Xcode's Intelligence settings and keep the relevant project open before external Codex sessions can use Xcode-provided tools. Xcode 27.0 Beta 3 resolves but does not start `lldb-mcp`, so use the working `mcpbridge` path and Xcode's active debugger session until a later Xcode release starts the standalone bridge normally.

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
- `apple-image-representation-workflow`
- `arkit-face-body-tracking-workflow`
- `arkit-spatial-sensing-workflow`
- `appkit-app-architecture-workflow`
- `app-intents-workflow`
- `author-swift-docc-docs`
- `avaudio-engine-workflow`
- `avfaudio-session-workflow`
- `avfoundation-media-pipeline-workflow`
- `bootstrap-swift-package`
- `bootstrap-xcode-app-project`
- `camera-capture-depth-workflow`
- `apple-typography-workflow`
- `coreaudio-modernization-repair-workflow`
- `core-image-processing-workflow`
- `core-animation-layer-workflow`
- `coremedia-timing-samplebuffer-workflow`
- `devicecheck-app-attest-workflow`
- `apple-developer-provisioning-workflow`
- `apple-runtime-telemetry-workflow`
- `explore-apple-swift-docs`
- `format-swift-sources`
- `icon-composer-app-icon-workflow`
- `ios-runtime-forensics-workflow`
- `macos-distribution-workflow`
- `macos-window-management-workflow`
- `migrate-xcode-project-to-xcodegen`
- `photos-library-editing-workflow`
- `safari-extension-control-workflow`
- `sf-symbols-workflow`
- `structure-swift-sources`
- `swiftdata-workflow`
- `tipkit-workflow`
- `tips-helpviewer-workflow`
- `vision-coreml-recognition-workflow`
- `vision-image-analysis-workflow`
- `video-codec-processing-workflow`
- `swift-openapi-client-workflow`
- `swift-package-build-run-workflow`
- `swift-package-testing-workflow`
- `swift-package-workflow`
- `swiftui-animation-workflow`
- `swiftui-app-architecture-workflow`
- `swiftui-component-audit-workflow`
- `swiftui-liquid-glass`
- `swiftui-performance-audit`
- `sync-swift-package-guidance`
- `sync-xcode-project-guidance`
- `xcode-app-project-workflow`
- `xcode-build-run-workflow`
- `xcode-coding-intelligence-workflow`
- `xcode-debugger-mcp-workflow`
- `xcode-device-hub-workflow`
- `xcode-localization-workflow`
- `xcode-testing-workflow`

## Release Notes

Use GitHub releases and Git history to track shipped changes for this repository.

## License

This repository is licensed under the Apache License 2.0. See [LICENSE](./LICENSE).
