---
name: scenekit-game-workflow
description: Guide SceneKit game implementation, repair, and maintenance. Use when Codex works on SCNScene, SCNView, SCNNode, cameras, lights, materials, geometry, animation, 3D physics, .scn files, .scnassets, model assets, SceneKit and SwiftUI/AppKit/UIKit integration, or RealityKit migration handoffs.
---

# SceneKit Game Workflow

## Overview

Use this skill for game-specific SceneKit work after SceneKit has been chosen or when maintaining an existing SceneKit project. Keep generic Apple app lifecycle, project-integrity mechanics, and Swift source cleanup with their owner skills.

## Source Check

Use Xcode MCP `DocumentationSearch`, Xcode-local documentation, Dash Apple API Reference docsets, or readable official Apple documentation before making SceneKit-specific claims. Generic no-JS web search/open results, snippets, metadata shells, or bare Apple Developer URLs are not enough evidence that Apple docs were read:

- [SceneKit](https://developer.apple.com/documentation/scenekit)
- [SCNScene](https://developer.apple.com/documentation/scenekit/scnscene)
- [SCNNode](https://developer.apple.com/documentation/scenekit/scnnode)
- [Bringing your SceneKit projects to RealityKit](https://developer.apple.com/documentation/realitykit/bringing-your-scenekit-projects-to-realitykit)

When new work is really modern 3D, spatial, or visionOS game work, consider RealityKit before deepening SceneKit-specific architecture. When maintaining an existing SceneKit project, preserve SceneKit unless the user asks for a migration.

## Workflow

1. Inspect the SceneKit surface:
   - `import SceneKit`
   - `SCNScene`, `SCNView`, `SCNNode`, `SCNCamera`, `SCNLight`, `SCNMaterial`, `SCNGeometry`, `SCNPhysicsWorld`, `SCNPhysicsBody`, animation players, and delegates
   - `.scn`, `.scnassets`, `.dae`, `.obj`, `.usdz`, textures, normal maps, environment maps, and animation assets
   - host SwiftUI/AppKit/UIKit views and project-resource membership
2. Keep the scene graph readable:
   - Name node ownership explicitly.
   - Keep camera, lighting, physics, material, and asset-loading changes close to the scene or game subsystem that owns them.
   - Avoid opaque node-name lookups for core gameplay unless the existing project already uses them deliberately.
3. Choose migration posture:
   - Maintain SceneKit for existing projects when the request is repair, content, performance, or incremental gameplay work.
   - Consider RealityKit when the request is new spatial or visionOS-first work, entity-component design, or an explicit SceneKit-to-RealityKit migration.
   - Consider Metal only when the work needs custom rendering or shader-level ownership beyond SceneKit's model.
4. Validate honestly:
   - Build and run through the repo's Xcode workflow.
   - Inspect visual behavior in a running app, simulator, device, screenshot, or recording when possible.
   - Use Instruments or `xctrace` handoffs for frame pacing, CPU/GPU timing, memory, or asset-loading performance.

## Handoffs

- `choose-apple-game-stack` when SceneKit versus RealityKit versus Metal is still unclear.
- `gameplaykit-simulation-workflow` when entity-component modeling, state machines, pathfinding, agents, randomization, or simulation update order owns the work.
- `xcode-game-profiling-workflow` when SceneKit frame pacing, CPU/GPU overlap, material/asset cost, memory pressure, or trace evidence owns the work.
- `game-controller-input-workflow` for controller, keyboard, mouse, and virtual-controller input.
- `core-haptics-game-feedback-workflow` for haptic feedback.
- `apple-dev-skills:xcode-build-run-workflow` for project membership, schemes, build, run, resources, and simulator mechanics.
- `apple-dev-skills:xcode-testing-workflow` for XCTest, UI tests, Instruments, `xctrace`, and trace interpretation.

## Output Shape

Return the SceneKit owner, changed or planned scene/assets, migration posture, validation path, and any manual visual, hardware, or profiling checks still required.
