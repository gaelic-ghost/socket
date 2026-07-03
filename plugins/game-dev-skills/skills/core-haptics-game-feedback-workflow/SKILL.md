---
name: core-haptics-game-feedback-workflow
description: Guide Core Haptics and game feedback work for Apple games. Use when Codex designs, implements, repairs, or validates CHHapticEngine, CHHapticPattern, audio-haptic feedback, controller haptics, capability checks, fallback behavior, accessibility-sensitive feedback, or physical-device haptic validation.
---

# Core Haptics Game Feedback Workflow

## Overview

Use this skill when game feedback depends on haptics, audio-haptic patterns, or controller rumble. Keep physical sensation claims behind real device or controller evidence.

## Source Check

Use Xcode-local documentation, Dash Apple API Reference docsets, or official Apple documentation before making Core Haptics or controller-haptics claims:

- [Core Haptics](https://developer.apple.com/documentation/corehaptics)
- [Playing Haptics on Game Controllers](https://developer.apple.com/documentation/corehaptics/playing-haptics-on-game-controllers)
- [Game Controller haptics](https://developer.apple.com/documentation/gamecontroller/gcdevicehaptics)
- [Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)

Apple sample guidance for controller haptics requires a physical device and Bluetooth-connected controller. Treat that as the evidence standard for controller haptic validation.

## Workflow

1. Inspect feedback ownership:
   - `import CoreHaptics`
   - `CHHapticEngine`, `CHHapticPattern`, `CHHapticEvent`, `CHHapticParameter`, `CHHapticAdvancedPatternPlayer`
   - `GCDeviceHaptics`, controller localities, and Game Controller integration
   - audio-session, audio-engine, or sound-effect code that must synchronize with feedback
2. Check capabilities before design commitments:
   - Device haptic support
   - Controller haptic localities
   - Audio-haptic needs
   - Interruptions, engine reset, app lifecycle, and background behavior
   - Accessibility, reduced motion, user settings, and alternate feedback paths
3. Design patterns from gameplay meaning:
   - Impact, charge, rhythm, confirmation, warning, surface texture, failure, and reward feedback should be named by gameplay purpose.
   - Keep haptic pattern creation testable and data-driven when a game has many feedback events.
   - Avoid firing haptics from hidden side effects that make input or gameplay hard to reason about.
4. Validate honestly:
   - Compile and run with the relevant Apple Dev execution workflow.
   - Use physical iPhone, iPad, Mac trackpad, or game controller evidence for sensation claims.
   - Report simulator-only or unsupported-device checks as compile/API validation, not physical haptic validation.

## Handoffs

- `game-controller-input-workflow` when controller lifecycle, mappings, or input events own the issue.
- `apple-dev-skills:avfaudio-session-workflow` when audio session configuration owns the failure.
- `apple-dev-skills:avaudio-engine-workflow` when AVAudioEngine graph behavior owns synchronized audio.
- `apple-dev-skills:xcode-build-run-workflow` for project membership, build, run, and device execution mechanics.

## Output Shape

Return the gameplay feedback purpose, haptic owner, capability checks, fallback or accessibility path, validation device/controller, and any sensation evidence that remains manual.
