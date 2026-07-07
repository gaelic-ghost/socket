---
name: core-animation-layer-workflow
description: Guide Core Animation layer-backed rendering and animation decisions for Apple apps, including CALayer trees, layer-backed AppKit and UIKit views, SwiftUI bridges, implicit and explicit CAAnimation, CATransaction, CAMediaTiming, model versus presentation layers, shape, gradient, replicator, emitter, text, tiled, and metal layers, performance diagnosis, and Xcode or Instruments validation handoffs. Use when a task mentions Core Animation, QuartzCore, CALayer, CAAnimation, CATransaction, CAShapeLayer, CAGradientLayer, CATextLayer, CAReplicatorLayer, modelLayer, presentationLayer, layerClass, wantsLayer, or layer-backed animation repair.
---

# Core Animation Layer Workflow

## SwiftData And SwiftUI Rule

When a task combines SwiftData with SwiftUI, keep SwiftData directly coupled to SwiftUI through Apple's data-driven path: `modelContainer`, environment `modelContext`, `@Query`, SwiftData model objects, and bindings. Do not add repositories, stores, service layers, DTO mirrors, view-model caches, wrapper objects, or other abstraction layers between SwiftData and SwiftUI. If this skill is not the right owner for SwiftData-backed SwiftUI work, hand off to `apple-dev-skills:swiftui-app-architecture-workflow` instead of inventing an intermediate data layer.

## Purpose

Use this skill to decide when Core Animation is the right layer-backed rendering or animation surface, then guide implementation, repair, and validation without confusing layer ownership with SwiftUI, AppKit, or UIKit view ownership.

It is not the default path for ordinary SwiftUI motion, AppKit/UIKit control animation, app architecture, or Xcode execution.

## When To Use

- Use this skill when the task mentions Core Animation, QuartzCore, `CALayer`, `CAAnimation`, `CABasicAnimation`, `CAKeyframeAnimation`, `CAAnimationGroup`, `CATransaction`, `CAMediaTiming`, `presentationLayer`, `modelLayer`, or layer trees.
- Use this skill when the task mentions layer-backed AppKit views, `wantsLayer`, `UIView.layer`, `layerClass`, custom `CALayer` subclasses, shape layers, gradient layers, text layers, tiled layers, emitter layers, replicator layers, or transform layers.
- Use this skill when the work needs model-layer versus presentation-layer reasoning, implicit-animation repair, explicit-animation timing, hit-testing during animation, layer-content scaling, or layer-backed performance diagnosis.
- Recommend `swiftui-animation-workflow` when SwiftUI-native state animation, transitions, phase/keyframe animation, or reduce-motion behavior is enough.
- Recommend `appkit-app-architecture-workflow` or `swiftui-app-architecture-workflow` when the real issue is ownership, view structure, scene structure, or lifecycle.
- Recommend `xcode-build-run-workflow` when the next step is build, preview, simulator, screenshot, runtime diagnostics, Instruments handoff, or project-file validation.

## Single-Path Workflow

1. Classify the layer job:
   - view backing layer
   - custom layer drawing
   - implicit property animation
   - explicit `CAAnimation`
   - layer tree composition
   - model/presentation mismatch
   - layer bridge from SwiftUI, AppKit, or UIKit
   - performance or rendering artifact diagnosis
2. Apply the Apple docs gate:
   - read the relevant Apple documentation first
   - state the documented behavior being relied on before recommending implementation
   - if Apple docs and the current code disagree, stop and surface the conflict
   - if no relevant Apple docs can be found, say that explicitly before proceeding
3. Decide whether Core Animation is justified:
   - stay in SwiftUI, AppKit, or UIKit when their animation helpers cover the behavior clearly
   - use Core Animation when the task needs layer tree composition, presentation-layer inspection, custom layer subclasses, specialized layer types, or lower-level timing
   - consider SpriteKit, SceneKit, Metal, AVFoundation, or Canvas when the task is really game, 3D, GPU rendering, video, or SwiftUI drawing work
4. Choose the layer ownership boundary:
   - UIKit view backing layer
   - AppKit layer-backed view
   - standalone sublayer tree owned by a view/controller/representable
   - custom layer class with explicit inputs
   - SwiftUI bridge via representable or hosting boundary
5. Choose the animation path:
   - implicit animation through property changes and transactions
   - explicit animation object when timing, repeat, key path, fill behavior, or presentation continuity requires it
   - disabled actions when layout or data updates must not animate
   - framework-level animation when Core Animation is unnecessary
6. Check model and presentation behavior:
   - update the model layer to the intended final value
   - use presentation layer only for in-flight visual state, hit testing, or diagnostics
   - avoid leaving animations that visually finish but snap because the model layer was not updated
7. Return one recommendation path with:
   - the layer ownership boundary
   - chosen layer or animation primitive
   - documented behavior relied on
   - artifact, timing, or performance risk
   - validation or handoff step

## Inputs

- `request`: optional free-text task description used to classify the Core Animation question.
- `target_framework`: optional framework emphasis such as `swiftui`, `appkit`, `uikit`, or `mixed`.
- `target_platforms`: optional platform list such as `ios`, `macos`, `tvos`, `visionos`, or `mixed-apple`.
- `current_code`: optional relevant files or snippets.
- `symptom`: optional issue such as snap-back, flicker, blurry contents, wrong timing, missed hit test, or performance drop.
- Defaults:
  - Apple docs-first guidance always applies
  - higher-level Apple UI framework animation is preferred unless Core Animation solves a concrete problem
  - Xcode or Instruments validation is reported as a handoff unless actually run

## Outputs

- `status`
  - `success`: the request belongs to this workflow and a layer recommendation is ready
  - `handoff`: another skill owns the next step after Core Animation-aware classification
  - `blocked`: docs, target platform, code, or validation context is insufficient for an honest recommendation
- `path_type`
  - `layer-ownership`
  - `implicit-animation`
  - `explicit-animation`
  - `model-presentation-repair`
  - `performance-diagnosis`
  - `handoff`
- `output`
  - classified layer job
  - chosen ownership boundary
  - chosen layer or animation primitive
  - model/presentation behavior to preserve
  - documented Apple behavior relied on
  - validation or handoff step

## Guards and Stop Conditions

- Do not drop into Core Animation when SwiftUI, AppKit, or UIKit animation APIs solve the problem cleanly.
- Do not change a UIKit view's backing layer delegate; Apple documents that the view is the layer's delegate.
- Do not use presentation-layer values as durable model state.
- Do not rely on removed layers, stale presentation layers, or animations that leave the model layer at the old value.
- Do not add timers for animation timing when `CAAnimation`, `CATransaction`, display links, or framework primitives fit.
- Do not claim performance, frame pacing, or Instruments evidence unless the relevant validation actually ran.
- Stop with `blocked` when the issue depends on visual artifacts, timing, or device behavior that cannot be inspected in the current environment.

## Fallbacks and Handoffs

- Recommend `swiftui-animation-workflow` for SwiftUI-native state animation, transitions, phase/keyframe animation, symbol effects, or reduce-motion behavior.
- Recommend `swiftui-app-architecture-workflow` or `appkit-app-architecture-workflow` when view/lifecycle ownership is the real blocker.
- Recommend `apple-ui-accessibility-workflow` when animation or visual effects need broader accessibility review.
- Recommend `xcode-build-run-workflow` for build, run, preview, simulator, screenshot, runtime diagnostics, or Instruments handoff.
- Recommend `explore-apple-swift-docs` when the user primarily needs raw Apple documentation lookup.
- Recommend `references/snippets/apple-xcode-project-core.md` when repo policy or Xcode project-integrity guidance is needed before applying layer-backed changes.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` exists to preserve the repo-wide customization-file contract, but the first version of this skill defines no runtime-enforced knobs.

Keep the first release focused on layer classification, model/presentation repair, animation primitive choice, and validation handoffs. If future iterations add deterministic layer-tree diagnostics, document those helpers before relying on them.

## References

### Workflow References

- `references/layer-ownership-and-animation-rules.md`
- `references/model-presentation-and-performance.md`
- `references/customization-flow.md`

### Support References

- Recommend `explore-apple-swift-docs` when the user needs direct Apple-docs lookup instead of Core Animation workflow guidance.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Xcode project policy before validating layer-backed app changes.
- Apple documentation anchors to verify include Core Animation Support, `UIView.layer`, `UIView.layerClass`, `NSView.layer`, `NSImage` layer contents, `CALayer`, `CAAnimation`, `CATransaction`, and Core Animation specialized layer types.

### Script Inventory

- `scripts/customization_config.py`
