---
name: gameplaykit-simulation-workflow
description: Guide GameplayKit simulation and gameplay-architecture work. Use when Codex works on GKEntity, GKComponent, GKComponentSystem, GKState, GKStateMachine, GKGraph, GKAgent, GKGoal, GKBehavior, GKRandom, SpriteKit or SceneKit integration, pathfinding, agents, state machines, reusable gameplay logic, or game simulation validation.
---

# GameplayKit Simulation Workflow

## Overview

Use this skill when the problem is gameplay logic rather than rendering. GameplayKit is the owner when entities, components, systems, states, agents, pathfinding, or reproducible gameplay services need to stay separate from SpriteKit, SceneKit, RealityKit, SwiftUI, or ad hoc view code.

## Source Check

Use Xcode-local documentation, Dash Apple API Reference docsets, or official Apple documentation before making GameplayKit-specific claims:

- [GameplayKit](https://developer.apple.com/documentation/gameplaykit)
- [GameplayKit entities and components](https://developer.apple.com/documentation/gameplaykit#Entities-and-Components)
- [GameplayKit state machines](https://developer.apple.com/documentation/gameplaykit#State-Machines)
- [GameplayKit agents, goals, and behaviors](https://developer.apple.com/documentation/gameplaykit#Agents-Goals-and-Behaviors)
- [GKScene](https://developer.apple.com/documentation/gameplaykit/gkscene)
- [GKComponentSystem](https://developer.apple.com/documentation/gameplaykit/gkcomponentsystem)

Apple documents GameplayKit as a framework for organizing game logic and providing reusable gameplay features such as random number generation, AI, pathfinding, and agent behavior. Use that boundary to keep simulation out of renderer-specific code unless the project intentionally couples them.

## Workflow

1. Inspect the gameplay model:
   - `import GameplayKit`
   - `GKEntity`, `GKComponent`, `GKComponentSystem`
   - `GKState`, `GKStateMachine`
   - `GKGraph`, `GKGraphNode`, `GKGridGraph`
   - `GKAgent`, `GKAgent2D`, `GKAgent3D`, `GKGoal`, `GKBehavior`, `GKPath`
   - `GKRandomSource`, `GKRandomDistribution`, `GKRuleSystem`
   - `GKScene`, `GKSKNodeComponent`, and SpriteKit scene-editor integration
2. Choose the GameplayKit surface:
   - Use entities and components when several gameplay objects need reusable behaviors without deep inheritance.
   - Use component systems when components need ordered per-frame updates across many entities.
   - Use state machines when the game or object behavior has explicit state transitions and invalid transitions should be prevented.
   - Use graphs and pathfinding when navigation rules are more important than renderer-specific movement.
   - Use agents, goals, and behaviors when autonomous movement should be expressed as goals and constraints.
   - Use GameplayKit random sources when reproducibility, seeded behavior, or distribution shape matters.
3. Keep renderers thin:
   - SpriteKit and SceneKit nodes can present gameplay state, but they should not become the only source of gameplay truth unless the project already owns that pattern.
   - Use `GKSKNodeComponent` or explicit adapter components when SpriteKit nodes and GameplayKit entities need to stay synchronized.
   - For SceneKit, keep 3D node synchronization explicit rather than burying game rules in node lookup code.
4. Validate simulation honestly:
   - Unit-test pure gameplay rules where practical.
   - Test state-machine transitions, seeded random behavior, pathfinding outcomes, and component update order without requiring a rendered scene when possible.
   - Use renderer or device validation only for integration behavior that pure tests cannot prove.

## Handoffs

- `spritekit-game-workflow` when SpriteKit scene, node, action, physics, or `.sks` behavior owns the work.
- `scenekit-game-workflow` when SceneKit scene graph, assets, camera, lighting, or 3D physics owns the work.
- `xcode-game-profiling-workflow` when per-frame component updates, pathfinding, agents, or renderer synchronization become performance-sensitive.
- `swift-lang` for general Swift API design, concurrency, error handling, source organization, or test style that is not game-specific.
- `apple-dev-skills:xcode-testing-workflow` for Xcode test plans, UI tests, Instruments, `xctrace`, or test execution mechanics.

## Output Shape

Return the GameplayKit owner, selected GameplayKit surface, renderer synchronization boundary, files or systems changed, pure-test path, integration validation path, and remaining open gameplay decisions.
