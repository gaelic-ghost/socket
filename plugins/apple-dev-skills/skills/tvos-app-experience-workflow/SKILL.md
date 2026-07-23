---
name: tvos-app-experience-workflow
description: Guide tvOS app-experience decisions for remote-first SwiftUI and UIKit interfaces, focus navigation, Large Text, Apple TV capability gates, and TVMLKit migration. Use when Apple TV interaction, focus geometry, large-screen accessibility, or a tvOS-specific framework boundary is the primary concern.
---

# tvOS App Experience Workflow

## Purpose

Guide the Apple TV-specific decisions that ordinary SwiftUI app architecture
does not own: indirect remote/controller input, visible focus movement,
large-screen layout, Large Text, hardware and SDK availability, and migration
away from TVMLKit. Keep SwiftUI as the primary UI path and use UIKit focus APIs
only for a demonstrated geometry or lifecycle constraint.

## When To Use

- Use this skill for a tvOS catalog, utility, education, fitness, game-adjacent,
  or media-browsing app whose main question is remote-first interaction or
  focus behavior.
- Use this skill for SwiftUI content shelves, lockups, hover effects,
  `focusSection()`, focused-item clipping, focus restoration, or large-screen
  layout decisions.
- Use this skill for `UIFocusGuide`, `UIFocusEnvironment`, preferred focus
  environments, focus-update diagnostics, or a UIKit/SwiftUI focus boundary.
- Use this skill for tvOS 27 Large Text/Dynamic Type adaptation, remote versus
  controller input, text-entry burden, Apple TV hardware/GPU capability gates,
  and beta-SDK availability questions.
- Use this skill to inventory a TVMLKit app and plan a migration to SwiftUI or
  UIKit; TVMLKit has been deprecated since tvOS 18.
- Recommend `tvos-media-playback-workflow` when playback UI, remote transport
  commands, Now Playing state, AVKit customization, HLS, or a custom player is
  the primary concern.
- Recommend `swiftui-app-architecture-workflow` when the tvOS constraints are
  understood and the remaining question is ordinary SwiftUI scene, state, or
  component ownership.
- Recommend `apple-ui-accessibility-workflow` when the main question is the
  accessibility tree or semantics beyond tvOS focus and Large Text.

## Single-Path Workflow

1. Classify the request:
   - SwiftUI-first content layout
   - focus routing or restoration
   - UIKit focus escape hatch
   - Large Text or accessibility adaptation
   - capability or beta-SDK gate
   - TVMLKit migration inventory
2. Apply the Apple docs gate:
   - use `explore-apple-swift-docs` to read current Apple documentation first
   - state the documented focus, input, availability, or deprecation behavior
     relied on before proposing a change
   - mark tvOS 27 claims as beta-specific with the checked SDK/build date until
     Apple ships the GM
3. Choose the smallest native UI surface:
   - SwiftUI `Button`, `focusSection()`, lockup, hover-effect, and scroll
     behavior for normal catalog layouts
   - normal focus geometry with enough room for scale and elevation
   - UIKit `UIFocusGuide` or preferred focus environments only when native
     geometry cannot produce the intended movement
4. Check the platform boundary:
   - Siri Remote, controller, voice, or companion-device input
   - focus, select, Menu/Back, and restoration behavior
   - text-entry alternative and remote friction
   - Apple TV generation, GPU family, simulator/device-only requirement, and
     unavailable framework
   - Large Text, RTL, VoiceOver order, and visual focus states
5. Return one recommendation with:
   - resolved request class
   - documented Apple behavior relied on
   - selected SwiftUI or UIKit surface
   - platform/beta availability result
   - validation matrix and one honest handoff

## Inputs

- `request`: optional free-text tvOS task.
- `scope`: optional explicit scope: `layout`, `focus`, `uikit-focus`,
  `large-text`, `capability`, `tvmlkit-migration`, or `review`.
- `framework_context`: optional `swiftui`, `uikit`, `mixed`, or `unknown`.
- `target_context`: optional Apple TV generation, tvOS deployment target,
  remote/controller requirement, and whether the request is beta-targeted.
- Defaults:
  - docs-first guidance always applies
  - SwiftUI is the primary implementation path
  - directional focus remains under user control
  - tvOS 27 behavior stays beta-qualified until reverified at GM

## Outputs

- `status`
  - `success`: an app-experience recommendation is ready
  - `handoff`: another skill owns the next step
  - `blocked`: capability, runtime, or current documentation evidence is too
    incomplete to make the requested claim
- `path_type`
  - `primary`: native SwiftUI focus/layout guidance is sufficient
  - `fallback`: a UIKit focus API, device evidence, or migration inventory is
    required
- `output`
  - request class
  - documented Apple behavior relied on
  - focus/layout or migration recommendation
  - platform and beta boundary
  - validation expectation and handoff

## Guards and Stop Conditions

- Do not treat Siri Remote movement as touchscreen coordinates or direct a
  focus move in a chosen direction; the focus system owns directional movement.
- Do not add a pointer-driven navigation model for ordinary tvOS menus.
- Do not let focused lockups clip, overlap controls, or lose their readable
  title when focus scaling and elevation occur.
- Do not make typing-heavy interaction the only path through a TV experience.
- Do not claim a framework, Apple Intelligence surface, GPU feature, controller
  behavior, or tvOS 27 beta behavior is available without current documentation
  and, when needed, device evidence.
- Do not extend TVMLKit for new features; inventory it and route a migration to
  SwiftUI or UIKit instead.
- Do not claim direct Core AI, `SystemLanguageModel`, or Foundation Models
  inference support on tvOS. Hand runtime selection to
  `model-lab-skills:choose-apple-model-runtime` with the current tvOS
  availability limitation explicit.

## Fallbacks and Handoffs

- Recommend `tvos-media-playback-workflow` for AVKit/player choice, remote
  transport commands, Now Playing, HLS/interstitials, or custom playback UI.
- Recommend `swiftui-app-architecture-workflow` for scene, environment, state,
  service, command, and ordinary component ownership.
- Recommend `apple-ui-accessibility-workflow` for semantic accessibility,
  accessibility-tree shaping, and broader assistive-technology review.
- Recommend `avfoundation-media-pipeline-workflow` for general AVFoundation
  assets, playback pipeline, capture, reader/writer, or export work.
- Recommend `xcode-build-run-workflow` for project, scheme, build, launch, and
  device follow-through; recommend `xcode-testing-workflow` for runtime UI
  verification and XCUITest planning.
- Recommend `explore-apple-swift-docs` when the real need is current Apple
  documentation rather than a design decision.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` preserves the shared customization-file
contract. This first version has no runtime-enforced knobs.

## References

### Workflow References

- `references/focus-layout-and-input.md`
- `references/platform-beta-and-migration.md`
- `references/validation-expectations.md`
- `references/customization-flow.md`

### Support References

- Recommend `explore-apple-swift-docs` for current Apple documentation before
  asserting framework or beta-platform availability.
- Recommend `apple-ui-accessibility-workflow` for user-facing semantic
  accessibility beyond this skill's tvOS focus and Large Text boundary.

### Script Inventory

- `scripts/customization_config.py`
