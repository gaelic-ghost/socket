---
name: swiftui-performance-audit
description: Diagnose SwiftUI rendering, scrolling, update, CPU, memory, image, layout, and animation performance from code and evidence. Use when a SwiftUI feature is slow, janky, broadly invalidating, memory-heavy, or needs a code-first audit before Instruments capture.
---

# SwiftUI Performance Audit

## Purpose

Make performance work evidence-led: inspect the smallest relevant SwiftUI data-flow and view slice first, name code-level suspicion separately from runtime proof, then hand trace capture to the existing Xcode or SwiftPM testing workflow.

## When To Use

- Use for slow rendering, dropped frames, broad view updates, unstable list identity, expensive body work, layout churn, image pressure, broad animation, high CPU, or memory growth in SwiftUI.
- Do not use this skill as a generic style review, a replacement for Instruments, or a reason to introduce caches, view models, stores, or coordinators.

## Single-Path Workflow

1. Apply the Apple docs gate through `explore-apple-swift-docs`. Confirm current Observation and SwiftUI behavior before proposing a performance change.
2. Collect the target view, reproduction steps, data flow, device/simulator, build configuration, and the observed symptom.
3. Classify the symptom as invalidation, identity churn, body computation, layout, image, animation, CPU, or retained-memory pressure.
4. Read `references/code-smells-and-remediation.md` and identify only code-backed suspicions. Mark each finding as suspected until a capture proves it.
5. Prefer narrow ownership, stable identity, precomputation outside `body`, downsampled images, localized state, and reduced layout complexity. Do not use `equatable()` or `@State` as an unmeasured cache.
6. When code inspection is insufficient, hand trace capture to `xcode-testing-workflow` for scheme/destination work or `swift-package-testing-workflow` for package-first workloads.
7. Compare the same reproduction before and after the change. Report CPU, frame behavior, allocations, and view-update evidence only when captured.

## Inputs

- target view/feature, smallest reproduction, and symptom
- state/observation/data-flow slice and relevant identities
- platform, device or simulator, build configuration, and any existing trace

## Outputs

- findings labeled as code-level suspicion or trace-backed evidence
- smallest remediation proposal with ownership and behavior preserved
- profiling handoff or before/after validation result

## Guards and Stop Conditions

- Do not claim a view is the performance root cause without code evidence or a trace.
- Do not add a ViewModel, repository, service wrapper, or arbitrary `@State` cache merely to quiet a symptom.
- Do not compare Debug and Release captures as if they are the same measurement.
- Stop when the reproduction is not defined well enough to distinguish a product behavior from a performance regression.

## Fallbacks and Handoffs

- Recommend `xcode-testing-workflow` for Instruments, `xctrace`, schemes, destinations, and trace interpretation.
- Recommend `swift-package-testing-workflow` for package-first signposts and profiling workloads.
- Recommend `swiftui-app-architecture-workflow` or `swiftui-component-audit-workflow` only when the evidence shows a real component-ownership issue.

## Customization

Use `references/customization-flow.md`. The workflow has no knobs that can weaken the distinction between a code suspicion and trace-backed performance evidence.

## References

- `references/code-smells-and-remediation.md`
- `references/customization-flow.md`
- Recommend `references/snippets/apple-xcode-project-core.md` when the app needs reusable Xcode-project policy alongside profiling work.
- [Understanding and improving SwiftUI performance](https://developer.apple.com/documentation/xcode/understanding-and-improving-swiftui-performance) documents SwiftUI performance analysis in Xcode.
