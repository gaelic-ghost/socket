---
name: game-controller-input-workflow
description: Guide Apple Game Controller framework input work for games. Use when Codex works on GCController, GCDevice, extended gamepad mappings, virtual controllers, keyboard and mouse game input, controller connection lifecycle, controller haptics handoffs, input evidence, accessibility alternatives, or device-aware validation.
---

# Game Controller Input Workflow

## Overview

Use this skill for game input that belongs to the Game Controller framework or to controller-adjacent keyboard and mouse game controls. Keep rendering work in SpriteKit, SceneKit, RealityKit, or Metal owner skills.

## Source Check

Use Xcode MCP `DocumentationSearch`, Xcode-local documentation, Dash Apple API Reference docsets, or readable official Apple documentation before making Game Controller-specific claims. Generic no-JS web search/open results, snippets, metadata shells, or bare Apple Developer URLs are not enough evidence that Apple docs were read:

- [Game Controller](https://developer.apple.com/documentation/gamecontroller)
- [Supporting Game Controllers](https://developer.apple.com/documentation/gamecontroller/supporting-game-controllers)
- [GCController](https://developer.apple.com/documentation/gamecontroller/gccontroller)
- [GCKeyboard](https://developer.apple.com/documentation/gamecontroller/gckeyboard)
- [GCMouse](https://developer.apple.com/documentation/gamecontroller/gcmouse)

## Workflow

1. Inspect input ownership:
   - `import GameController`
   - `GCController`, `GCDevice`, `GCExtendedGamepad`, `GCMicroGamepad`, `GCKeyboard`, `GCMouse`, `GCVirtualController`, `GCDeviceHaptics`
   - controller connection and disconnection notifications
   - polling, value-changed handlers, input snapshots, or custom input abstraction
   - renderer-specific input bridges in SpriteKit, SceneKit, RealityKit, or host views
2. Preserve evidence shape:
   - Keep button press/release, analog values, directional values, repeat state, timestamps, modifiers, and device identity visible where the project needs diagnostics.
   - Do not normalize discrete keyboard events into fake continuous geometry.
   - Do not claim hardware behavior was verified without the relevant controller, keyboard, mouse, Siri Remote, or virtual-controller evidence.
3. Design mappings:
   - Keep gameplay actions separate from raw controller elements.
   - Provide keyboard or touch alternatives when controller input is optional.
   - Make remapping, dead zones, inversion, and accessibility choices explicit when they are part of the requested work.
4. Validate:
   - Verify compile/build through the Apple Dev execution workflow.
   - Run a manual or automated input checklist on the relevant hardware or simulator surface.
   - Record missing hardware as a validation gap instead of pretending the sandbox proved controller feel.

## Handoffs

- `core-haptics-game-feedback-workflow` for haptics, rumble, audio-haptic patterns, and capability checks.
- `spritekit-game-workflow` or `scenekit-game-workflow` when the work becomes scene or gameplay integration.
- `apple-dev-skills:xcode-build-run-workflow` for build, run, simulator, and project membership mechanics.
- `apple-dev-skills:apple-ui-accessibility-workflow` for broader accessibility review when control alternatives, labels, focus, or assistive interaction become central.

## Output Shape

Return the input devices, raw input owner, gameplay-action mapping, accessibility alternatives, validation hardware or simulator path, and missing evidence.
