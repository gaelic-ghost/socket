---
name: swiftui-liquid-glass
description: Design, implement, review, and validate SwiftUI Liquid Glass interfaces across iOS and macOS. Use when choosing native glass effects, grouped glass surfaces, glass button styles, morphing transitions, availability fallbacks, or removing conflicting custom chrome.
---

# SwiftUI Liquid Glass

## Purpose

Use the platform's native glass system deliberately rather than reproducing it with custom blur, opaque fills, or ad hoc material layers. Liquid Glass is a visual-system contract: this workflow owns where it belongs, how related surfaces group, and how earlier systems retain a clear fallback; it does not own a feature's state or navigation architecture.

## When To Use

- Use for `glassEffect`, `GlassEffectContainer`, glass button styles, `glassEffectID`, interactive glass, shape/tint consistency, and iOS/macOS availability handling.
- Use when reviewing custom chrome, toolbar, sidebar, card, chip, or action surfaces that visually fight the current platform design.
- Hand off component ownership to `swiftui-app-architecture-workflow`, animation mechanics to `swiftui-animation-workflow`, and desktop/AppKit ownership to `appkit-app-architecture-workflow`.

## Single-Path Workflow

1. Apply the Apple docs gate through `explore-apple-swift-docs`. Confirm the current platform API, deployment target, and availability before selecting a glass treatment.
2. Inspect the existing hierarchy, materials, toolbars, controls, backgrounds, shapes, and interaction model. Identify the few semantic surfaces that need emphasis rather than applying glass to every container.
3. Classify the work: system-chrome cleanup, one glass surface, a related group of glass controls, interactive action, morphing transition, or cross-version fallback.
4. Read `references/glass-composition-and-fallbacks.md` for composition and availability patterns and `references/review-and-validation.md` for visual, accessibility, and performance review.
5. Prefer native controls, system materials, and standard toolbars before adding custom glass. Apply glass after the layout and visual modifiers that define the surface.
6. Use `GlassEffectContainer` only for genuinely related nearby glass elements. Keep shapes, spacing, and tint roles consistent; use interactive glass only for actual controls.
7. Use `glassEffectID` and a namespace only when the hierarchy changes and a morphing relationship makes the transition clearer. Do not introduce glass IDs as decorative animation noise.
8. Gate version-sensitive APIs and provide an intentional non-glass fallback that preserves hierarchy, affordance, contrast, and touch/keyboard access.
9. Read `references/os26-os27-beta-availability.md` before treating an OS 27 beta toolbar feature as a Liquid Glass API change. Core custom-glass APIs remain the OS 26 baseline; OS 27 beta toolbar composition features need their own availability gates and visual validation.
10. Validate in Light and Dark appearance, compact and regular windows where relevant, reduced-motion and accessibility settings, keyboard/pointer interaction, the oldest supported OS fallback, and OS 27 beta toolbar overflow/visibility behavior when used.

## Inputs

- target platform, deployment target, and current Apple API availability
- existing hierarchy, visual language, interaction model, and supported fallback systems
- target glass surfaces and any requested morphing relationship
- accessibility, appearance, and supported-window requirements

## Outputs

- documented glass decision, composition boundary, and fallback design
- modifier, container, interactivity, and shape guidance for the affected surface
- validation evidence for current-system glass and the oldest supported fallback
- one handoff when component ownership, animation, accessibility, or execution owns the remaining work

## Guards and Stop Conditions

- Do not substitute custom blur stacks for native Liquid Glass when native APIs fit the deployment target.
- Do not make an entire screen, sidebar, or scroll container glass by default; preserve readable content hierarchy and system chrome.
- Do not use interactive glass on a static label or use a glass button style for a non-action.
- Do not claim an availability fallback is acceptable until it preserves the feature's semantic action and accessibility behavior.
- Stop when current Apple documentation and the requested deployment target conflict, or when the product needs a deliberately non-system visual language that calls for a separate design decision.

## Fallbacks and Handoffs

- Recommend `swiftui-app-architecture-workflow` for ownership, navigation, scene, or component-boundary decisions.
- Recommend `swiftui-animation-workflow` for animation timing, transitions, or state-driven motion that exceeds the glass relationship.
- Recommend `apple-ui-accessibility-workflow` for contrast, VoiceOver, Dynamic Type, reduced motion, and alternate input review.
- Recommend `xcode-build-run-workflow` for previews, build, run, and visual validation.

## Customization

Use `references/customization-flow.md`. The first version has no runtime-enforced appearance knob because visual-system choices must remain tied to the app's deployment target, semantics, and current Apple documentation.

## References

- `references/glass-composition-and-fallbacks.md`
- `references/review-and-validation.md`
- `references/customization-flow.md`
- Recommend `references/snippets/apple-xcode-project-core.md` when the app needs reusable Xcode-project policy alongside Liquid Glass implementation.
- [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views) documents native glass composition and customization.
