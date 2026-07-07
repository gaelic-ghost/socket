---
name: choose-apple-game-stack
description: Choose the right Apple platform game-development stack before implementation. Use when Codex needs to route a game task across SpriteKit, SceneKit, RealityKit, Metal, GameplayKit, Game Controller, Core Haptics, GameKit, SwiftUI/AppKit/UIKit host surfaces, assets, profiling, or Apple Dev Skills handoffs.
---

# Choose Apple Game Stack

## SwiftData And SwiftUI Rule

When a task combines SwiftData with SwiftUI, keep SwiftData directly coupled to SwiftUI through Apple's data-driven path: `modelContainer`, environment `modelContext`, `@Query`, SwiftData model objects, and bindings. Do not add repositories, stores, service layers, DTO mirrors, view-model caches, wrapper objects, or other abstraction layers between SwiftData and SwiftUI. If this skill is not the right owner for SwiftData-backed SwiftUI work, hand off to `apple-dev-skills:swiftui-app-architecture-workflow` instead of inventing an intermediate data layer.

## Overview

Use this skill before implementing Apple game work when the correct owner is not obvious. The goal is to choose the smallest game-specific stack that fits the project instead of turning a rendering, input, haptics, or profiling task into a generic Apple app change.

## Source Check

Use repo-local files, Xcode MCP `DocumentationSearch`, Xcode-local documentation, Dash Apple API Reference docsets, and readable official Apple documentation before making framework-specific claims. Generic no-JS web search/open results, snippets, metadata shells, or bare Apple Developer URLs are not enough evidence that Apple docs were read. Useful Apple anchors:

- [SpriteKit](https://developer.apple.com/documentation/spritekit)
- [SceneKit](https://developer.apple.com/documentation/scenekit)
- [GameplayKit](https://developer.apple.com/documentation/gameplaykit)
- [Game Controller](https://developer.apple.com/documentation/gamecontroller)
- [Core Haptics](https://developer.apple.com/documentation/corehaptics)
- [RealityKit game development](https://developer.apple.com/documentation/realitykit#Game-development)
- [Designing for games](https://developer.apple.com/design/human-interface-guidelines/designing-for-games)

State the documented behavior that changes the recommendation. If local docs and current code disagree, stop and surface that conflict.

## Classification Workflow

1. Inspect the repository shape:
   - Xcode project, workspace, XcodeGen `project.yml`, Swift package, or mixed app-plus-package layout
   - imports such as `SpriteKit`, `SceneKit`, `RealityKit`, `Metal`, `GameplayKit`, `GameController`, `CoreHaptics`, `GameKit`, `AVFAudio`, or `SwiftUI`
   - asset catalogs, `.sks`, `.scn`, `.scnassets`, `.usdz`, `.reality`, `.metal`, texture atlases, audio files, and controller or haptic code
   - tests, manual validation checklists, profiling traces, Instruments artifacts, and CI scripts
2. Identify the game job:
   - 2D scene, animation, physics, or particle work
   - 3D scene, camera, lighting, material, animation, or asset work
   - immersive RealityKit or visionOS game work
   - custom GPU rendering, shader, or Metal performance work
   - entity-component, state machine, pathfinding, agents, or procedural rules work
   - physical or virtual controller input, keyboard, mouse, or stylus game input
   - haptic, audio-haptic, or controller-rumble feedback
   - Game Center, achievements, leaderboard, multiplayer, or save-state work
   - profiling, frame pacing, latency, memory, thermal, or GPU timing work
3. Choose the owner:
   - SpriteKit for most 2D games, `SKScene`, nodes, actions, particles, 2D physics, tile maps, and SpriteKit resources.
   - SceneKit for existing 3D SceneKit projects, scene graphs, cameras, lights, materials, animations, and 3D physics where RealityKit is not the chosen migration target.
   - RealityKit for modern entity-component 3D, spatial, AR, or visionOS game work when project requirements and platform support fit.
   - Metal for custom rendering, shader pipelines, GPU-driven workloads, or performance questions that SpriteKit, SceneKit, and RealityKit do not own cleanly.
   - GameplayKit for game rules, state machines, entity-component modeling, pathfinding, agents, and randomization services that should not be buried in view code.
   - Game Controller for physical controllers, virtual controllers, keyboard/mouse game input, controller lifecycle, mappings, and controller haptics handoffs.
   - Core Haptics for custom haptic patterns and audio-haptic feedback when hardware support and device validation are explicit.
4. Route non-game work away:
   - Use `apple-dev-skills` for generic Xcode project integrity, signing, simulator, asset-catalog mechanics, SwiftUI/AppKit/UIKit host views, DocC, and Apple documentation exploration.
   - Use `swift-lang` for Swift API shape, concurrency, errors, formatting, and source structure when the issue is not game-specific.
   - Use `reverse-engineering-skills` for compiled game artifacts, Unity build outputs, binaries, crash logs, or decompiler/disassembler output.

## Validation Choice

Choose validation based on the claim being made:

- Build or project-integrity claims: use the relevant Xcode or SwiftPM validation workflow from `apple-dev-skills`.
- Rendering behavior: validate with a running app, preview, simulator, device, screenshot, or trace when possible.
- Controller input: validate with the relevant hardware, virtual controller, keyboard, mouse, or explicit fallback path.
- Haptics and physical feel: require device or controller evidence; otherwise report a manual validation gap.
- Performance and frame pacing: prefer Release builds and Instruments or `xctrace` evidence.

## Follow-Up Skill Routing

- Use `gameplaykit-simulation-workflow` when game rules, entity-component modeling, state machines, agents, pathfinding, randomization, or simulation update order own the problem.
- Use `xcode-game-profiling-workflow` when frame pacing, stutter, CPU/GPU overlap, memory pressure, thermal state, trace capture, or profiling evidence owns the problem.
- Keep Metal rendering and shader architecture as a future handoff when the work requires shader code, render-pass architecture, command encoding, resource layout, GPU counters, or Metal debugger workflow beyond profiling triage.

## Output Shape

Return:

1. `Chosen stack`: SpriteKit, SceneKit, RealityKit, Metal, GameplayKit, Game Controller, Core Haptics, GameKit, Apple Dev Skills handoff, or mixed.
2. `Game owner`: scene, renderer, simulation, input, haptics, assets, host app, profiling, or service boundary.
3. `Why`: the concrete framework behavior or project evidence that drove the choice.
4. `Handoffs`: next skill or plugin to use.
5. `Validation`: exact build, run, trace, hardware, or manual-check path.
6. `Open decisions`: only decisions that block a correct implementation.
