---
name: tipkit-workflow
description: Add, configure, present, style, test, and troubleshoot Apple TipKit tips in SwiftUI, UIKit, and AppKit using current Apple documentation. Use for Tip protocol definitions, Tips.configure, TipView inline tips, popoverTip tooltip popovers, TipUIView, TipUIPopoverViewController, TipNSView, TipNSPopover, rules, parameters, events and donations, actions, invalidation, display frequency, persistent datastores, testing overrides, and tips that do not appear or reappear correctly.
---

# TipKit Workflow

## Purpose

Implement Apple TipKit directly and predictably. Treat “tooltip” requests as a presentation decision: use TipKit for discoverable feature guidance and onboarding, then choose an inline tip or tip popover based on whether covering nearby controls is acceptable.

## When To Use

Use for adding, configuring, displaying, styling, testing, or diagnosing TipKit guidance in SwiftUI, UIKit, or AppKit.

## Single-Path Workflow

1. Apply the Apple docs gate through `explore-apple-swift-docs`. State the documented TipKit behavior being relied on before changing code.
2. Inspect the app entry point, deployment targets, highlighted control, existing presentation modifiers, and any existing TipKit configuration or tip types.
3. Classify the request:
   - inline SwiftUI guidance with `TipView`
   - SwiftUI tooltip popover with `popoverTip`
   - UIKit inline or popover presentation
   - AppKit inline or popover presentation
   - eligibility using parameters, events, rules, and options
   - lifecycle, persistence, testing, or troubleshooting
4. Read `references/presentation-and-platform-patterns.md` for presentation code and `references/eligibility-lifecycle-and-testing.md` for configuration, rules, persistence, invalidation, and diagnosis.
5. Define a small `Tip` type with stable identity and focused copy. Add `title`; add `message`, `image`, and `actions` only when they improve comprehension or provide a real next step.
6. Call `try Tips.configure(...)` once during app startup before tips need to become eligible. Handle configuration failure with a descriptive message that identifies TipKit initialization and the likely datastore or configuration cause.
7. Prefer inline `TipView` whenever layout can accommodate it. Use `popoverTip` when the tip must point at a compact control and temporary overlap is acceptable.
8. Encode real eligibility with `@Parameter`, `Tips.Event`, `#Rule`, and options. Donate events where the qualifying behavior actually happens; do not fake eligibility with unrelated view-local Boolean state.
9. Invalidate the tip when the highlighted feature is used or the guidance becomes permanently irrelevant. Do not confuse temporary dismissal with permanent invalidation.
10. Validate with deterministic TipKit testing controls, then run the applicable `xcode-build-run-workflow` and `xcode-testing-workflow` checks. Verify appearance, dismissal, action handling, persistence after relaunch, accessibility, and compact-window behavior on each supported platform.

## Inputs

- repository, app entry point, platform, and deployment targets
- feature or control to highlight
- inline or popover intent, or permission to choose
- eligibility, frequency, persistence, and invalidation requirements
- existing TipKit state and observed failure behavior

## Outputs

Return the documented Apple behavior, chosen presentation, configuration location, tip definition, eligibility and invalidation policy, changed files, validation performed, and any remaining platform limitation.

## Guards and Stop Conditions

- Do not use TipKit as a generic hover-help replacement without confirming that feature education is the intended behavior.
- Do not add a custom tooltip manager, coordinator, repository, or mirrored state layer around TipKit.
- Do not call `Tips.configure` repeatedly from feature views.
- Do not attach multiple competing popover presentations to the same control without checking composition and runtime behavior.
- Do not promise exact popover timing, simultaneous popovers, or imperative SwiftUI presentation control that TipKit does not expose.
- Do not reset the TipKit datastore or force all tips visible outside a deliberate debug, preview, or test path.
- Stop when Apple documentation and current code disagree, when a deployment target cannot support the required API, or when the request needs a custom always-available help surface instead of TipKit.

## Fallbacks and Handoffs

- Recommend `explore-apple-swift-docs` for current API or availability lookup.
- Recommend `swiftui-app-architecture-workflow` or `appkit-app-architecture-workflow` when ownership of the highlighted feature is unclear.
- Recommend `apple-ui-accessibility-workflow` for VoiceOver, Dynamic Type, contrast, focus, and alternative-access verification.
- Recommend `xcode-build-run-workflow` for execution.
- Recommend `xcode-testing-workflow` for automated validation.
- Use a native SwiftUI `help` modifier on macOS or a custom help presentation only when the product requirement is persistent contextual help rather than TipKit feature education; verify that API through Apple docs before implementing it.

## Customization

Use `references/customization-flow.md`. The first version has no runtime-enforced knobs; `scripts/customization_config.py` preserves the shared configuration contract.

## References

- `references/presentation-and-platform-patterns.md`
- `references/eligibility-lifecycle-and-testing.md`
- `references/customization-flow.md`
- Recommend `references/snippets/apple-xcode-project-core.md` when the app needs reusable repository policy alongside TipKit implementation guidance.
