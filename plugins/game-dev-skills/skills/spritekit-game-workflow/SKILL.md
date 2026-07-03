---
name: spritekit-game-workflow
description: Guide SpriteKit game implementation, repair, and maintenance. Use when Codex works on SKScene, SKView, SKNode, actions, particles, cameras, constraints, 2D physics, tile maps, SpriteKit resources, .sks files, SpriteKit and GameplayKit integration, or SpriteKit validation in Apple game projects.
---

# SpriteKit Game Workflow

## Overview

Use this skill for game-specific SpriteKit work after SpriteKit has been chosen as the rendering and scene framework. Keep generic Xcode project mechanics, signing, simulator operation, and Swift language cleanup with the Apple Dev and Swift Lang owner skills.

## Source Check

Use Xcode-local documentation, Dash Apple API Reference docsets, or official Apple documentation before making SpriteKit-specific claims:

- [SpriteKit](https://developer.apple.com/documentation/spritekit)
- [SKScene](https://developer.apple.com/documentation/spritekit/skscene)
- [SKNode](https://developer.apple.com/documentation/spritekit/sknode)
- [GameplayKit](https://developer.apple.com/documentation/gameplaykit)

Apple documentation describes SpriteKit as a high-performance 2D framework for games and graphics-intensive apps that integrates with GameplayKit and SceneKit. Use that boundary when deciding whether SpriteKit or another stack owns the work.

## Workflow

1. Inspect the SpriteKit surface:
   - `import SpriteKit`
   - `SKScene`, `SKView`, `SKNode`, `SKSpriteNode`, `SKCameraNode`, `SKAction`, `SKPhysicsWorld`, `SKPhysicsBody`, `SKEmitterNode`, `SKTileMapNode`
   - `.sks` files, texture atlases, particle files, tile sets, audio resources, and asset catalogs
   - scene loading, scene transitions, update loops, input event routing, and host SwiftUI/AppKit/UIKit views
2. Preserve scene ownership:
   - Keep simulation, rendering, input, and resource-loading responsibilities explicit.
   - Avoid hiding game state in arbitrary node names or untyped `userData` unless the existing project already owns that convention.
   - Use GameplayKit when entity-component modeling, state machines, pathfinding, agents, or randomization services are the real concern.
3. Implement narrowly:
   - Put per-frame behavior in the scene or a game-specific model layer the repo already owns.
   - Use `SKAction` for node-local animation when it fits.
   - Use SpriteKit physics for 2D collision and contact behavior when the project can express the gameplay in SpriteKit terms.
   - Keep host SwiftUI/AppKit/UIKit code thin when it only embeds an `SKView`.
4. Validate honestly:
   - Build and run through the repo's Xcode or SwiftPM workflow.
   - Use simulator or device evidence for visual behavior when possible.
   - Use device evidence for touch, controller, haptic, and frame-pacing claims that the local environment cannot prove.
   - Use Instruments or `xctrace` handoffs when the question is frame time, memory, CPU/GPU overlap, or stutter.

## Handoffs

- `choose-apple-game-stack` when the stack choice is still unclear.
- `gameplaykit-simulation-workflow` when entity-component modeling, state machines, pathfinding, agents, randomization, or simulation update order owns the work.
- `xcode-game-profiling-workflow` when SpriteKit frame pacing, stutter, texture/resource churn, physics cost, or per-frame update cost needs evidence.
- `game-controller-input-workflow` for physical controllers, virtual controllers, keyboard, or mouse input.
- `core-haptics-game-feedback-workflow` for custom haptics or controller rumble.
- `apple-dev-skills:xcode-build-run-workflow` for project membership, scheme, build, run, simulator, and Metal-toolchain-aware execution mechanics.
- `apple-dev-skills:xcode-testing-workflow` for XCTest, UI tests, Instruments, `xctrace`, or profiling evidence.
- `swift-lang` for non-game-specific Swift style, API, concurrency, or source cleanup.

## Output Shape

Return the SpriteKit owner, files changed or planned, scene/resource impact, GameplayKit handoff if relevant, validation path, and any manual visual or hardware checks still required.
