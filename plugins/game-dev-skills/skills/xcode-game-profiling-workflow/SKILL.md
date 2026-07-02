---
name: xcode-game-profiling-workflow
description: Guide Apple game profiling and performance-evidence work in Xcode and Instruments. Use when Codex investigates frame pacing, stutter, FPS, CPU/GPU overlap, Time Profiler evidence, Game Performance or Game Memory templates, Metal Performance HUD routing, memory pressure, thermal state, trace capture, or profiling handoffs for SpriteKit, SceneKit, RealityKit, or Metal-backed games.
---

# Xcode Game Profiling Workflow

## Overview

Use this skill when the question is game performance evidence, not shader design. It helps agents choose the right Xcode or Instruments profiling path, interpret game-specific symptoms, and hand off Metal rendering or shader work without absorbing that future skill.

## Source Check

Use Xcode-local documentation, Dash Apple API Reference docsets, or official Apple documentation before making profiling-tool claims:

- [Analyzing the performance of your Metal app](https://developer.apple.com/documentation/xcode/analyzing-the-performance-of-your-metal-app)
- [Metal developer workflows](https://developer.apple.com/documentation/xcode/metal-developer-workflows)
- [Monitoring your Metal app's graphics performance](https://developer.apple.com/documentation/xcode/monitoring-your-metal-apps-graphics-performance)
- [Understanding the Metal Performance HUD metrics](https://developer.apple.com/documentation/xcode/understanding-the-metal-performance-hud-metrics)
- [Analyzing the memory usage of your Metal app](https://developer.apple.com/documentation/xcode/analyzing-the-memory-usage-of-your-metal-app)

Apple describes the Game Performance template as a way to profile frame time by combining threading, system-call, and Metal system trace information. Use that tool for evidence about smooth rendering, CPU/GPU overlap, stutters, memory pressure, display timing, and thermal state. Do not treat it as a substitute for a future Metal rendering or shader workflow.

## Workflow

1. Classify the symptom:
   - low FPS
   - intermittent stutter
   - long frame interval
   - CPU-bound update loop
   - GPU-bound rendering
   - poor CPU/GPU overlap
   - memory growth, texture pressure, or resource churn
   - thermal throttling
   - input-to-visual or input-to-haptic latency
2. Choose the evidence path:
   - Game Performance template for frame pacing, CPU/GPU overlap, display timing, Time Profiler, thermal state, GPU events, and Metal resource events.
   - Game Memory template for memory footprint, VM behavior, allocations, and Metal resource memory pressure.
   - Metal Performance HUD for live FPS, GPU time, frame interval, memory, thermal, Game Mode, and capture-scope discovery.
   - `xctrace` when the project needs repeatable CLI trace capture or shareable artifacts.
   - Xcode Metal capture or debugger only when the next question is a Metal workload, resource, pass, or shader question.
3. Preserve profiling integrity:
   - Prefer Release builds when optimization, frame time, inlining, specialization, ARC behavior, or GPU workload shape matters.
   - Record device, OS, Xcode, scheme, build configuration, display refresh rate, Game Mode state when relevant, and reproduction steps.
   - Keep trace artifacts, screenshots, or summary exports named by scenario and timestamp when the repo has a diagnostics location.
   - Do not claim haptic feel, physical controller latency, or thermal behavior without suitable device evidence.
4. Interpret cautiously:
   - CPU-heavy frames need call-tree or thread-state evidence before code changes.
   - GPU-heavy frames need GPU timeline, resource, pass, or shader evidence before shader conclusions.
   - Memory-heavy frames need allocation, VM, or Metal resource evidence before asset-pipeline changes.
   - If the trace suggests shader or render-pass design issues, hand off to future Metal rendering guidance or current Apple Dev Xcode execution skills rather than inventing shader architecture here.

## Handoffs

- `spritekit-game-workflow` when the fix is SpriteKit scene, action, physics, texture, or node behavior.
- `scenekit-game-workflow` when the fix is SceneKit scene graph, material, lighting, asset, or node behavior.
- `gameplaykit-simulation-workflow` when component systems, state machines, agents, pathfinding, or randomization are on the hot path.
- `apple-dev-skills:xcode-testing-workflow` for Instruments, `xctrace`, XCTest, UI test, or trace interpretation mechanics.
- `apple-dev-skills:xcode-build-run-workflow` for schemes, build configurations, run destinations, and project settings.
- Future `metal-game-rendering-workflow` when the fix requires shader code, render-pass architecture, Metal resource layout, command encoding, GPU counters, or Metal debugger workflow beyond profiling triage.

## Output Shape

Return the symptom, evidence path, build/run configuration, trace or HUD evidence collected, likely bottleneck class, recommended owner skill, and any manual device or profiling gaps.
