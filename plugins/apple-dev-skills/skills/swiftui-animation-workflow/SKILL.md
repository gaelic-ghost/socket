---
name: swiftui-animation-workflow
description: Guide SwiftUI animation design, implementation, repair, and validation across withAnimation, animation(_:value:), transactions, transitions, content transitions, matchedGeometryEffect, navigation transitions, PhaseAnimator, KeyframeAnimator, TimelineView, symbol effects, reduce-motion behavior, previews, and performance-aware handoffs. Use when a task mentions SwiftUI animation, motion, transition design, animated state changes, hero transitions, phase or keyframe animation, symbolEffect in SwiftUI, reduce motion, or repairing confusing or over-broad animation behavior.
---

# SwiftUI Animation Workflow

## Purpose

Use this skill to design, implement, repair, and validate SwiftUI motion that stays state-driven, accessible, and grounded in Apple documentation. The skill owns SwiftUI animation selection, transition decisions, phase/keyframe motion, symbol-effect routing, reduce-motion checks, and preview or runtime validation handoffs.

It is not the SwiftUI app architecture workflow, not the SF Symbols selection workflow, and not the Core Animation layer workflow.

## When To Use

- Use this skill when the user asks for SwiftUI animation, motion, transition, symbol-effect, or animated state-change guidance.
- Use this skill when code uses `withAnimation`, `animation(_:value:)`, binding animation, `transaction`, `transition`, `contentTransition`, `matchedGeometryEffect`, `navigationTransition`, `PhaseAnimator`, `KeyframeAnimator`, `TimelineView`, `Canvas`, or `symbolEffect`.
- Use this skill when an animation is too broad, triggers unexpectedly, does not animate, ignores reduce-motion expectations, performs poorly, or mixes state ownership with side-effectful motion code.
- Use this skill when the user wants a design choice between simple state animation, transition, matched geometry, phase animation, keyframes, timeline-driven rendering, or a handoff to lower-level rendering.
- Recommend `swiftui-app-architecture-workflow` when the primary issue is ownership, scene structure, environment, focus, commands, or view composition rather than motion behavior.
- Recommend `sf-symbols-workflow` when the primary issue is choosing, coloring, validating, or customizing the symbol itself.
- Recommend `xcode-build-run-workflow` when the next step is preview, build, run, simulator, screenshot, or project-file validation.

## Single-Path Workflow

1. Classify the motion job:
   - simple state transition
   - insertion or removal transition
   - content transition inside a stable view
   - matched geometry or navigation transition
   - phase-based animation
   - keyframe animation
   - symbol effect
   - timeline or continuously updating drawing
   - performance or accessibility repair
2. Apply the Apple docs gate:
   - read the relevant SwiftUI documentation first
   - state the documented behavior being relied on before recommending implementation
   - if Apple docs and the current code disagree, stop and surface the conflict
   - if no relevant Apple docs can be found, say that explicitly before proceeding
3. Choose the smallest motion primitive that fits the job:
   - `withAnimation` for one user action where all dependent changes should share a transaction
   - `animation(_:value:)` for a specific view subtree reacting to a specific value
   - binding animation when the control binding is the intended animation boundary
   - `transaction` when the task needs to override or disable animation in a subtree
   - `transition` for view insertion or removal
   - `contentTransition` for content changes inside an existing view
   - `matchedGeometryEffect` or navigation transition when identity and geometry continuity matter
   - `PhaseAnimator` for discrete phase sequences
   - `KeyframeAnimator` for coordinated values with explicit timing
   - `TimelineView` or lower-level rendering only when the motion is genuinely time-driven
4. Keep the data flow honest:
   - make animation derive from explicit state
   - avoid hidden timers, global animation state, and side effects inside frequently called animation closures
   - keep expensive work out of per-frame keyframe or timeline closures
   - keep architecture cleanup separate from motion cleanup unless the animation bug is caused by ownership confusion
5. Check accessibility and comfort:
   - verify whether reduce-motion behavior should disable, simplify, or replace motion
   - preserve meaning without relying on motion alone
   - avoid repeated decorative motion unless the user or product explicitly wants it
6. Return one recommendation path with:
   - the motion job class
   - chosen SwiftUI primitive
   - state trigger and animation boundary
   - accessibility behavior
   - documented SwiftUI behavior relied on
   - validation or handoff step

## Inputs

- `request`: optional free-text task description used to classify the animation question.
- `target_platforms`: optional platform list such as `ios`, `macos`, `watchos`, `visionos`, or `mixed-apple`.
- `motion_goal`: optional desired effect such as feedback, transition, attention, loading, progress, delight, or continuity.
- `current_code`: optional relevant SwiftUI code or file paths.
- `validation_surface`: optional validation preference such as preview, simulator, unit snapshot, device, or manual review.
- Defaults:
  - Apple docs-first guidance always applies
  - state-driven SwiftUI animation is preferred before lower-level rendering
  - reduce-motion behavior must be considered for user-facing animation

## Outputs

- `status`
  - `success`: the request belongs to this workflow and a motion recommendation is ready
  - `handoff`: another skill owns the next step after SwiftUI animation-aware classification
  - `blocked`: current docs, code, platform, or validation context is insufficient for an honest recommendation
- `path_type`
  - `state-animation`
  - `transition`
  - `matched-geometry`
  - `phase-animation`
  - `keyframe-animation`
  - `timeline-rendering`
  - `repair`
  - `handoff`
- `output`
  - requested motion job class
  - chosen SwiftUI primitive
  - state trigger and animation boundary
  - accessibility and reduce-motion behavior
  - documented Apple behavior relied on
  - validation or handoff step

## Guards and Stop Conditions

- Do not use broad implicit animation when a value-scoped animation fits.
- Do not hide app, scene, or view ownership problems behind animation wrappers.
- Do not perform expensive work in `KeyframeAnimator`, timeline, or per-frame content closures.
- Do not use motion as the only signal for important state.
- Do not route ordinary SwiftUI animation into Core Animation unless a concrete framework limitation, host-view bridge, or layer-backed need requires it.
- Do not claim preview, simulator, or reduce-motion behavior has been verified unless that validation actually ran.
- Stop with `blocked` when the target OS/platform range is unknown and the chosen animation API depends on availability.

## Fallbacks and Handoffs

- Recommend `swiftui-app-architecture-workflow` when state ownership, scene ownership, focus, command, environment, or composition decisions are the real blocker.
- Recommend `sf-symbols-workflow` when the work is primarily symbol selection, rendering mode, variable color, custom symbols, or symbol availability.
- Recommend `apple-ui-accessibility-workflow` when the work needs a broader accessibility implementation or review beyond reduce-motion and non-motion fallback behavior.
- Recommend `xcode-build-run-workflow` when the next step is Xcode preview, simulator, screenshot, runtime diagnostics, or project-integrity follow-through.
- Recommend `explore-apple-swift-docs` when the user primarily needs raw Apple documentation lookup.
- Recommend `references/snippets/apple-xcode-project-core.md` when repo policy or Xcode project-integrity guidance is needed before validating animation in an app project.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` exists to preserve the repo-wide customization-file contract, but the first version of this skill defines no runtime-enforced knobs.

Keep the first release focused on motion classification, SwiftUI primitive choice, reduce-motion behavior, and validation handoffs. If future iterations add deterministic preview or screenshot helpers, document those helpers before relying on them.

## References

### Workflow References

- `references/animation-decision-rules.md`
- `references/transitions-effects-and-accessibility.md`
- `references/customization-flow.md`

### Support References

- Recommend `explore-apple-swift-docs` when the user needs direct Apple-docs lookup instead of SwiftUI animation workflow guidance.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Xcode project policy before previewing or validating animation changes.
- Apple documentation anchors to verify include SwiftUI Animations, Managing user interface state, Controlling the timing and movements of your animations, Unifying your app's animations, SwiftUI symbol effects, and Human Interface Guidelines Motion.

### Script Inventory

- `scripts/customization_config.py`
