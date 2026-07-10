---
name: sf-symbols-workflow
description: Guide SF Symbols selection, inspection, customization, rendering modes, variable color, symbol effects, animated symbols, custom symbols, accessibility semantics, availability checks, and Apple app integration. Use when a task mentions SF Symbols, the SF Symbols app, systemImage names, symbolRenderingMode, foregroundStyle palette or hierarchical color, multicolor symbols, variableValue, symbolEffect, custom symbol templates, symbol export, asset-catalog symbol resources, or choosing symbols for SwiftUI, AppKit, UIKit, or watchOS UI.
---

# SF Symbols Workflow

## Purpose

Use this skill to choose, inspect, customize, validate, and integrate SF Symbols in Apple app UI. The skill owns symbol selection, SF Symbols app inspection, rendering-mode decisions, custom-symbol workflow, symbol animation routing, and accessibility semantics.

It is not the app-icon workflow, not the generic SwiftUI animation workflow, and not the Xcode project execution workflow.

## When To Use

- Use this skill when the user asks about Apple's SF Symbols library or SF Symbols app.
- Use this skill when the task mentions built-in symbols, `Image(systemName:)`, `Label`, `UIImage(systemName:)`, `NSImage(systemSymbolName:)`, `symbolRenderingMode`, `symbolVariant`, `foregroundStyle`, `variableValue`, `symbolEffect`, `SymbolEffectTransition`, custom symbols, or symbol templates.
- Use this skill when a UI design needs a semantically correct icon, state variant, platform-available symbol, palette/multicolor rendering, variable color, or animated symbol effect.
- Use this skill when the user wants Codex to inspect the local SF Symbols app through Computer Use.
- Recommend `swiftui-animation-workflow` when the primary question is broader SwiftUI motion, transition design, state-driven animation, phase animation, keyframe animation, or reduce-motion behavior.
- Recommend `icon-composer-app-icon-workflow` when the work is an app icon rather than an in-app symbol.
- Recommend `apple-ui-accessibility-workflow` when the main issue is accessibility review beyond symbol labels and semantic meaning.
- Recommend `xcode-build-run-workflow` when the next honest step is asset-catalog integration, build, preview, simulator, or project-file validation.

## Single-Path Workflow

1. Classify the symbol job:
   - choose a built-in symbol
   - repair an incorrect or unavailable symbol name
   - choose a variant, such as fill, slash, circle, square, or badge
   - choose monochrome, hierarchical, palette, or multicolor rendering
   - apply variable color or variable draw behavior
   - apply a symbol effect or symbol transition
   - create, annotate, validate, or export a custom symbol
   - integrate an asset-catalog symbol into an app
2. Apply the Apple docs gate:
   - read the relevant Apple documentation first
   - state the documented behavior being relied on before recommending implementation
   - if Apple docs and the local SF Symbols app disagree, stop and surface the conflict
   - if no relevant Apple docs can be found, say that explicitly before proceeding
3. Inspect the local tool when current symbol-library behavior matters:
   - verify the SF Symbols app exists before promising GUI guidance
   - inspect the local app through Computer Use when the task needs category, rendering, animation, export, or custom-symbol evidence
   - use the app's sidebar and inspectors to verify symbol availability, variants, rendering support, variable behavior, and animation support
4. Choose the symbol path:
   - built-in SF Symbol when the semantic match and platform availability are good
   - built-in symbol plus variant when the state is a standard variant
   - rendering-mode or palette change when the shape is right and only color semantics need work
   - symbol effect when the motion is symbol-local and Apple documents the effect for the target platforms
   - custom symbol when the app needs a brand-specific or unavailable symbol while preserving SF Symbols metrics and template rules
   - ordinary SVG/vector artwork when the shape is not a symbol and does not benefit from SF Symbols behavior
5. Check implementation boundaries:
   - SwiftUI uses `Image`, `Label`, symbol modifiers, `foregroundStyle`, `symbolEffect`, and asset names when appropriate
   - UIKit and AppKit use image and symbol configuration APIs when appropriate
   - Xcode project and asset-catalog changes hand off to `xcode-build-run-workflow`
   - app-icon work hands off to `icon-composer-app-icon-workflow`
6. Return one recommendation path with:
   - the symbol source
   - rendering and animation choices
   - accessibility semantics
   - documentation behavior relied on
   - validation or handoff steps

## Local Tool Check

Use this check before live SF Symbols work:

1. Locate the app. Gale's current local path observed on 2026-06-28 is `/Applications/SF Symbols.app`.
2. Read the app version from `Contents/Info.plist` when current library behavior matters.
3. Open or inspect the app when the user asks for GUI guidance, custom symbol validation, export behavior, or visual comparison.
4. Treat SF Symbols app state as evidence, not as a source file to mutate. Ask before saving, overwriting, exporting into a repo, or changing user-owned collections.

Current local evidence from 2026-06-28: SF Symbols 7.2 build 119 exposes an accessibility-visible sidebar with categories such as What's New, Draw, Variable, Multicolor, Custom Symbols, and inspectors for Info, Format, and Animation.

## Inputs

- `request`: optional free-text task description used to classify the symbol job.
- `target_framework`: optional framework emphasis such as `swiftui`, `uikit`, `appkit`, or `mixed`.
- `target_platforms`: optional platform list such as `ios`, `macos`, `watchos`, `visionos`, or `mixed-apple`.
- `symbol_name`: optional existing symbol name or custom symbol asset name.
- `visual_goal`: optional desired semantic meaning, state, brand shape, or interaction feedback.
- Defaults:
  - Apple docs-first guidance always applies
  - built-in SF Symbols are preferred when they match the semantics and platform targets
  - accessibility semantics are part of the symbol choice, not a cleanup step

## Outputs

- `status`
  - `success`: the request belongs to this workflow and a symbol recommendation is ready
  - `handoff`: another skill owns the next step after symbol-aware classification
  - `blocked`: current docs, app evidence, or project context is insufficient for an honest recommendation
- `path_type`
  - `built-in-symbol`
  - `custom-symbol`
  - `rendering-repair`
  - `animation-repair`
  - `fallback-artwork`
- `output`
  - requested symbol job class
  - chosen symbol or custom-symbol path
  - rendering, variant, variable, or effect choice
  - accessibility label and semantic notes
  - documented Apple behavior relied on
  - validation or handoff step

## Guards and Stop Conditions

- Do not invent symbol names. Verify names in Apple docs, the SF Symbols app, or the project before using them.
- Do not assume a symbol supports a variant, multicolor rendering, variable color, or animation just because a similar symbol does.
- Do not use color alone to communicate state. Pair color with shape, text, label, or state context when meaning matters.
- Do not treat SF Symbols as app icons. Use `icon-composer-app-icon-workflow` for app-icon work.
- Do not copy, modify, or redistribute Apple symbol assets outside documented app-development use without surfacing the licensing or redistribution boundary once.
- Do not save, export, overwrite, or modify local SF Symbols app collections through Computer Use without explicit user confirmation.
- Stop with `blocked` when the target OS/platform range is unknown and the symbol choice depends on availability.

## Fallbacks and Handoffs

- Recommend `swiftui-animation-workflow` when symbol effects are only one piece of broader view motion.
- Recommend `apple-ui-accessibility-workflow` when the work needs a broader accessibility audit, VoiceOver behavior review, or assistive-technology validation.
- Recommend `icon-composer-app-icon-workflow` when the output is an app icon or marketing icon rather than an in-app symbol.
- Recommend `xcode-build-run-workflow` when the next step is adding asset-catalog resources, updating an Xcode project, previewing, building, or validating simulator/device behavior.
- Recommend `explore-apple-swift-docs` when the user primarily needs raw Apple documentation lookup.
- Recommend `references/snippets/apple-xcode-project-core.md` when repo policy or Xcode project-integrity guidance is needed before applying symbol resources.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` exists to preserve the repo-wide customization-file contract, but the first version of this skill defines no runtime-enforced knobs.

Keep the first release focused on symbol selection, app inspection, rendering behavior, accessibility semantics, and Xcode handoffs. If future iterations add deterministic export or validation helpers, document those helpers before relying on them.

## References

### Workflow References

- `references/symbol-selection-and-rendering.md`
- `references/custom-symbols-and-app-inspection.md`
- `references/customization-flow.md`

### Support References

- Recommend `explore-apple-swift-docs` when the user needs direct Apple-docs lookup instead of SF Symbols workflow guidance.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Xcode project policy before applying symbol assets.
- Apple documentation anchors to verify include SF Symbols in the Human Interface Guidelines, Configuring and displaying symbol images in your UI, Creating custom symbol images for your app, SwiftUI Images symbol rendering, and SwiftUI symbol effects.

### Script Inventory

- `scripts/customization_config.py`
