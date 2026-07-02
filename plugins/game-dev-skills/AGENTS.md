# AGENTS.md

This file is the Game Dev Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `game-dev-skills` is a monorepo-owned Socket child source for Codex game development workflow skills.
- The first shipped scope is Apple platform game development: SpriteKit, SceneKit, GameplayKit routing, Game Controller input, Core Haptics game feedback, and related Xcode validation handoffs.
- Root [`skills/`](./skills/) is the authored workflow surface.
- The repo root is the Codex plugin root through [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).

## Local Rules

- Keep Apple framework behavior grounded in Xcode-local docs, Dash Apple API Reference docsets, or official Apple Developer documentation before making framework-specific claims.
- Use `apple-dev-skills` for general Swift, SwiftUI, AppKit, UIKit, Xcode project integrity, simulator, signing, asset-catalog, DocC, and Apple docs-routing work.
- Use `swift-lang` for shared Swift language style, API design, concurrency, error handling, and source-organization guidance that is not game-specific.
- Use `reverse-engineering-skills` when the central input is a compiled game artifact, Unity build output, binary, symbol file, crash log, decompiler output, or disassembler output.
- Keep this plugin focused on game-specific authoring, maintenance, input, feedback, rendering-stack choice, profiling, and validation handoffs.
- Treat device feel, controller behavior, haptic sensation, frame pacing, latency, thermal behavior, and GPU timing as hardware-sensitive evidence. Do not claim those are verified unless they were observed on a suitable simulator, device, controller, trace, or local tool.

## Validation

```bash
uv run python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/<skill-name>
```

Run the root Socket metadata validator after plugin metadata, marketplace wiring, or root docs change:

```bash
uv run scripts/validate_socket_metadata.py
```
