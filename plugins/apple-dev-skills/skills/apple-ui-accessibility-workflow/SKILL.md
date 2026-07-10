---
name: apple-ui-accessibility-workflow
description: Guide Apple UI accessibility implementation and review for SwiftUI-first code, with UIKit and AppKit bridge guidance plus explicit verification expectations and testing handoffs. Use when the user wants help making Apple UI accessible, reviewing accessibility semantics, shaping the accessibility tree, or planning Apple-platform accessibility verification without collapsing the work into generic design review or Xcode test execution.
---

# Apple UI Accessibility Workflow

## Purpose

Provide a docs-first workflow for Apple UI accessibility implementation and review. Keep the first version SwiftUI-first while still covering the UIKit and AppKit bridge surface when SwiftUI code wraps platform-native views or when an accessibility behavior only makes sense in those underlying frameworks.

It is not the Apple-docs router, not the SwiftUI app-structure workflow, and not the Xcode execution workflow.

## When To Use

- Use this skill when the user wants help making a SwiftUI view, control, list, form, chart, or composite UI more accessible.
- Use this skill when the user wants help reviewing Apple UI semantics such as labels, values, hints, roles, traits, actions, headings, or grouping behavior.
- Use this skill when the user wants help deciding whether the default accessibility tree is sufficient or whether a view needs explicit accessibility modifiers.
- Use this skill when the user wants help shaping the accessibility tree with `accessibilityElement(children:)`, `accessibilityChildren`, `accessibilityRepresentation`, hiding rules, or synthetic accessibility content.
- Use this skill when the user wants help understanding where SwiftUI accessibility stops and UIKit or AppKit accessibility responsibilities begin.
- Use this skill when the user wants accessibility-specific verification expectations for VoiceOver, focus order, Dynamic Type, contrast, reduced motion, or related Apple platform settings.
- Recommend `explore-apple-swift-docs` when the user primarily needs Apple or Swift documentation lookup rather than accessibility guidance.
- Recommend `xcode-testing-workflow` when the work becomes XCUITest execution, simulator or device automation, `.xctestplan` configuration, or runtime UI verification.
- Recommend `swiftui-app-architecture-workflow` when the question is really about SwiftUI app structure, scene ownership, command ownership, or general data flow rather than accessibility semantics.

## Single-Path Workflow

1. Classify the request:
   - SwiftUI implementation
   - SwiftUI review
   - UIKit/AppKit bridge guidance
   - accessibility verification planning
2. Apply the Apple docs gate before recommending changes:
   - read the relevant Apple accessibility documentation first
   - state the documented behavior being relied on before giving accessibility guidance
   - if Apple docs and the current code disagree, stop and surface that conflict
   - if no relevant Apple docs can be found, say that explicitly before proceeding
3. Choose the accessibility surface:
   - default semantics are already sufficient
   - explicit description is needed
   - explicit traits or actions are needed
   - accessibility tree reshaping is needed
   - UIKit/AppKit bridge work is needed
4. Check the anti-patterns before finalizing guidance:
   - accessibility identifiers treated as if they solve user-facing accessibility
   - labels that redundantly repeat surrounding visible context
   - meaningful content hidden from accessibility without a replacement
   - custom controls that look interactive but do not expose the right role or action
   - visual order that does not produce a sane assistive-technology reading order
   - verification claims made without a runtime or manual accessibility pass
5. Return one recommendation path with:
   - the documented Apple behavior being relied on
   - the chosen accessibility surface
   - any SwiftUI versus UIKit/AppKit bridge warning when relevant
   - one verification expectation
   - one handoff when the next honest step is docs lookup, Xcode testing, or broader SwiftUI architecture work

## Inputs

- `request`: optional free-text task description used to classify the accessibility question.
- `scope`: optional explicit scope such as `swiftui-semantics`, `tree-shaping`, `bridge-guidance`, `review`, or `verification`.
- `platform_context`: optional platform emphasis such as `ios`, `ipados`, `macos`, `watchos`, `tvos`, or `mixed-apple`.
- `framework_context`: optional explicit framework emphasis such as `swiftui`, `uikit`, `appkit`, or `swiftui-with-bridge`.
- Defaults:
  - docs-first guidance always applies
  - SwiftUI is the primary path in the first version
  - UIKit and AppKit stay in scope when they materially affect accessibility behavior or representable-wrapper correctness

## Outputs

- `status`
  - `success`: the request belongs to this workflow and an accessibility recommendation is ready
  - `handoff`: the request belongs to another skill after accessibility-aware classification
  - `blocked`: the request lacks enough context to recommend an accessibility change honestly
- `path_type`
  - `primary`: the recommendation comes from a directly supported accessibility path
  - `fallback`: the recommendation depends on limited framework or platform context because the request shape is underspecified
- `output`
  - resolved request class
  - chosen accessibility surface
  - documented Apple behavior relied on
  - bridge findings when relevant
  - verification expectation
  - recommended skill when handing off
  - one concise next step

## Guards and Stop Conditions

- Do not treat accessibility identifiers as the same thing as user-facing accessibility semantics.
- Do not recommend accessibility modifiers that simply restate visible content unless the explicit semantic override is actually needed.
- Do not hide meaningful content from accessibility without documenting what replaces that information.
- Do not silently absorb XCUITest execution, simulator control, or `.xctestplan` work that belongs to `xcode-testing-workflow`.
- Do not silently absorb broader SwiftUI app-structure work that belongs to `swiftui-app-architecture-workflow`.
- Stop with `blocked` when the request is too vague to tell whether the problem is semantic content, tree shape, bridge behavior, or verification follow-through.

## Fallbacks and Handoffs

- Prefer explicit scope and framework context when the user provides them.
- Fall back to request-text inference when the platform or framework shape is unclear.
- Recommend `explore-apple-swift-docs` when the real need is broader Apple or Swift docs lookup.
- Recommend `xcode-testing-workflow` when the next honest step is runtime UI verification, XCUITest mechanics, simulator or device flow, XCUI interruption handling, screenshots, or `.xctestplan` orchestration.
- Recommend `swiftui-app-architecture-workflow` when the next honest step is app, scene, command, focus, environment, or dependency-flow architecture rather than accessibility semantics.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` exists to preserve the repo-wide customization-file contract, but the first version of this skill defines no runtime-enforced knobs.

Keep the first release focused on the decision model, the documented accessibility boundary, and explicit verification expectations. If future iterations add a real deterministic need for runtime knobs, document them explicitly before letting runtime behavior depend on them.

## References

### Workflow References

- `references/swiftui-accessibility-semantics.md`
- `references/swiftui-accessibility-tree-shaping.md`
- `references/framework-bridging-uikit-appkit.md`
- `references/worked-swiftui-accessibility-examples.md`
- `references/verification-expectations.md`
- `references/common-accessibility-anti-patterns.md`
- `references/customization-flow.md`

### Support References

- Recommend `explore-apple-swift-docs` when the user needs direct Apple-docs lookup instead of accessibility guidance.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Apple-project baseline policy rather than a one-off accessibility recommendation.

### Script Inventory

- `scripts/customization_config.py`
