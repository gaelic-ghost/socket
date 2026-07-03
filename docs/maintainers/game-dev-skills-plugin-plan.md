# Game Dev Skills Plugin Plan

This plan records the first durable shape for a Socket-hosted game development skills plugin.

## Intent

The `game-dev-skills` plugin should help agents choose and maintain game-specific project surfaces without turning `apple-dev-skills` into a catch-all for rendering, input, haptics, asset pipelines, profiling, and gameplay architecture.

The first release is Apple-platform-first. It covers SpriteKit, SceneKit, GameplayKit simulation, Game Controller input, Core Haptics feedback, Xcode game profiling, and rendering-stack choice across SpriteKit, SceneKit, RealityKit, Metal, and existing Apple app workflows.

This is a companion guidance plugin, not a runtime plugin. The first version does not bundle a game engine, template feed, asset pipeline, simulator wrapper, profiler automation, MCP server, or local game runtime.

## Packaging Direction

Package the guidance as an independent child plugin under:

```text
plugins/game-dev-skills/
```

The child plugin owns its Codex-facing guidance surface:

- `.codex-plugin/plugin.json`
- `skills/`
- plugin metadata, skill metadata, `AGENTS.md`, and maintainer notes that explain the plugin's role
- any validation scripts needed for the plugin's own authored guidance

The root Socket marketplace lists `game-dev-skills` as installable now that first-slice skill content exists. If the plugin ever loses its exported skill content, switch the marketplace entry back to `NOT_AVAILABLE` in the same pass.

## Boundaries With Existing Plugins

- Use `game-dev-skills` for game-specific authoring, input, haptics, rendering-stack choice, frame pacing, game-loop shape, gameplay architecture, and game profiling handoffs.
- Use `apple-dev-skills` for general Swift, SwiftUI, AppKit, UIKit, Xcode project integrity, simulator, signing, asset-catalog integration, Apple docs routing, DocC, and Apple-platform validation mechanics.
- Use `swift-lang` for Swift language style, API shape, concurrency, error handling, source layout, and non-game-specific cleanup.
- Use `reverse-engineering-skills` when the central input is a compiled artifact, binary, Unity build output, symbol file, crash log, decompiled output, or disassembler output.
- Use future engine-specific skills only when Unity, Godot, Unreal, or another engine-authoring workflow earns a dedicated owner.

Unity belongs here when the task is authoring, maintaining, profiling, or packaging a Unity project. Unity compiled-artifact analysis stays with `reverse-engineering-skills`.

## Documentation And Tool Sources

Use local Xcode documentation, Dash Apple API Reference docsets, and official Apple documentation before making framework-specific claims. Current first-slice source anchors include:

- [SpriteKit](https://developer.apple.com/documentation/spritekit)
- [SceneKit](https://developer.apple.com/documentation/scenekit)
- [GameplayKit](https://developer.apple.com/documentation/gameplaykit)
- [Game Controller](https://developer.apple.com/documentation/gamecontroller)
- [Core Haptics](https://developer.apple.com/documentation/corehaptics)
- [RealityKit game development](https://developer.apple.com/documentation/realitykit#Game-development)
- [Metal developer workflows](https://developer.apple.com/documentation/xcode/metal-developer-workflows)
- [Designing for games](https://developer.apple.com/design/human-interface-guidelines/designing-for-games)

Translate documentation into the concrete project, framework, validation, or handoff decision it changes.

## Shipped Skill Inventory

### `game-dev-skills:choose-apple-game-stack`

Choose the smallest correct Apple game-development shape before implementation. This skill routes between SpriteKit, SceneKit, RealityKit, Metal, SwiftUI/AppKit/UIKit host surfaces, Game Controller input, Core Haptics feedback, GameKit/Game Center, and existing Apple Dev Skills workflows.

### `game-dev-skills:spritekit-game-workflow`

Guide SpriteKit scene, node, action, physics, camera, resource, GameplayKit integration, and Xcode validation work.

### `game-dev-skills:scenekit-game-workflow`

Guide SceneKit scene, node graph, camera, lighting, material, animation, physics, asset, RealityKit migration, and Xcode validation work.

### `game-dev-skills:gameplaykit-simulation-workflow`

Guide GameplayKit entities, components, component systems, state machines, pathfinding, agents, randomization, renderer synchronization, and simulation validation.

### `game-dev-skills:game-controller-input-workflow`

Guide Game Controller framework work for physical controllers, virtual controllers, keyboard and mouse game input, mappings, connection lifecycle, haptics handoffs, and device-aware validation.

### `game-dev-skills:core-haptics-game-feedback-workflow`

Guide Core Haptics and game-controller haptic feedback design, capability checks, pattern ownership, audio-haptic boundaries, fallback behavior, accessibility, and physical-device validation.

### `game-dev-skills:xcode-game-profiling-workflow`

Guide Apple game profiling across frame pacing, stutter, CPU/GPU overlap, Game Performance and Game Memory templates, Metal Performance HUD routing, `xctrace`, trace evidence, and handoffs to rendering or shader work.

## Proposed Follow-Up Skill Inventory

- `game-dev-skills:metal-game-rendering-workflow`
- `game-dev-skills:game-asset-pipeline-workflow`
- `game-dev-skills:gamekit-game-center-workflow`
- `game-dev-skills:unity-authoring-workflow`

## First Slice

- [x] Create `plugins/game-dev-skills/` with `.codex-plugin/plugin.json` and `AGENTS.md`.
- [x] Add this maintainer plan.
- [x] Add first-slice Apple game-development workflow skills.
- [x] Add `gameplaykit-simulation-workflow` and `xcode-game-profiling-workflow` as the second Apple game-development skill slice.
- [x] Wire `game-dev-skills` into the root Socket marketplace as installable.
- [x] Update README and ROADMAP so users understand the new plugin surface.
- [x] Run skill-folder validation and plugin-manifest validation for the new child plugin.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.

## Open Questions

- What concrete scope should `metal-game-rendering-workflow` own beyond profiling triage: shader code, render-pass architecture, command encoding, resource layout, Metal debugger workflow, GPU counters, or all of those?
- Should Unity authoring live in this plugin, or should a later engine-specific plugin own Unity once the authoring scope is concrete?
