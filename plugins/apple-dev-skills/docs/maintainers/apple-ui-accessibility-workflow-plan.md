# Apple UI Accessibility Workflow Plan

Date: 2026-04-16

## Purpose

Record the chosen direction for Milestone 37 so the new accessibility skill lands as a focused Apple UI accessibility workflow instead of dissolving into generic design review, a duplicate SwiftUI architecture surface, or a shadow Xcode testing skill.

## Decision

The first version should ship as `apple-ui-accessibility-workflow`.

It should be broad enough to remain the durable home for Apple UI accessibility work across SwiftUI, UIKit, and AppKit, but the first implementation slice should be SwiftUI-first.

That means the first version should:

- make SwiftUI accessibility implementation and review the primary path
- explain where UIKit and AppKit accessibility responsibilities differ from or map onto SwiftUI behavior
- hand off execution-heavy verification and UI automation work to `xcode-testing-workflow`
- hand off non-accessibility SwiftUI structure questions to `swiftui-app-architecture-workflow`

It should not become:

- a generic UX or visual-design review skill
- the primary owner of test execution, simulator control, or XCUITest mechanics
- a second Apple-docs router
- a dumping ground for every SwiftUI question that happens to mention a `View`

## Scope Boundary

### In Scope

- SwiftUI accessibility labels, values, hints, traits, headings, actions, hidden-state decisions, and input labels
- accessibility element grouping and tree shaping through `accessibilityElement(children:)`, `accessibilityChildren`, and `accessibilityRepresentation`
- practical SwiftUI review of lists, forms, custom controls, charts, and composite views where the default accessibility tree is not enough
- verification expectations for VoiceOver, focus order, rotor/navigation implications, Dynamic Type, contrast, and reduced-motion-sensitive UI behavior
- explicit comparison guidance for SwiftUI, UIKit, and AppKit accessibility surfaces
- bridging expectations for `UIViewRepresentable` and `NSViewRepresentable` wrappers
- accessibility-specific anti-pattern review for Apple UI code

### Out Of Scope

- replacing `explore-apple-swift-docs` for Apple documentation routing
- replacing `xcode-testing-workflow` for XCUITest execution, simulator control, or `.xctestplan` orchestration
- replacing `swiftui-app-architecture-workflow` for app, scene, command, or data-flow architecture questions that are not primarily accessibility questions
- absorbing generic component styling, animation, or visual-polish advice that is not tied to accessibility behavior

## Documentation Sources

The first version should anchor itself in current Apple accessibility APIs and guidance:

- [SwiftUI Accessibility fundamentals](https://developer.apple.com/documentation/swiftui/accessibility-fundamentals)
- [SwiftUI accessibility modifiers](https://developer.apple.com/documentation/swiftui/view-accessibility)
- [AccessibilityChildBehavior](https://developer.apple.com/documentation/swiftui/accessibilitychildbehavior)
- [AccessibilityTraits](https://developer.apple.com/documentation/swiftui/accessibilitytraits)
- [UIAccessibility](https://developer.apple.com/documentation/uikit/uiaccessibility)
- [NSAccessibility](https://developer.apple.com/documentation/appkit/nsaccessibility)
- [XCTest](https://developer.apple.com/documentation/xctest)
- [Handling UI Interruptions](https://developer.apple.com/documentation/xctest/handling-ui-interruptions)
- [Accessibility in the Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/accessibility)

The skill should make a few documented behaviors explicit and foundational:

- SwiftUI already exposes baseline accessibility behavior for common system controls, so custom modifiers should respond to a real gap instead of blindly restating visible text
- the accessibility tree is not always identical to the visual tree, and SwiftUI provides explicit APIs to combine, contain, ignore, replace, or synthesize accessibility elements
- representable wrappers must preserve or recreate underlying UIKit or AppKit accessibility information when SwiftUI cannot infer it automatically
- accessibility verification is partly semantic review and partly runtime validation, so the skill must stay honest about when the next step belongs to XCUITest or manual VoiceOver follow-through

## Core Questions The Skill Should Answer

- Does this control or composite view already expose the right accessibility semantics, or does it need explicit labels, values, actions, or traits?
- Should this view remain multiple child elements, become one combined element, or expose a synthetic accessibility representation?
- What accessibility information should come from visible content versus an explicit accessibility modifier?
- When a custom SwiftUI control wraps UIKit or AppKit behavior, where does the accessibility contract need to cross the bridge?
- What verification steps are actually needed before claiming the UI is accessible?

## Workflow Shape

The first version should stay single-path and practical:

1. Classify the request:
   - SwiftUI implementation
   - SwiftUI review
   - UIKit/AppKit comparison or bridge guidance
   - verification planning
2. Apply the Apple docs gate:
   - gather the relevant Apple accessibility references first
   - state the documented behavior being relied on before recommending changes
3. Decide the accessibility surface:
   - default semantic behavior is sufficient
   - explicit description is needed
   - explicit traits or actions are needed
   - explicit tree reshaping is needed
   - bridge-specific UIKit or AppKit accessibility work is needed
4. Check common anti-patterns:
   - duplicative labels that repeat visible context badly
   - hiding meaningful content from accessibility without a replacement
   - custom controls that look interactive but do not expose the right role or action
   - accessibility identifiers treated as if they solve user-facing accessibility
   - focus or navigation order that only works visually
5. Return one recommendation path with:
   - documented Apple behavior relied on
   - the recommended accessibility surface
   - any framework-specific bridge warning
   - one verification expectation
   - one handoff when the next honest step is docs lookup, Xcode test execution, or broader SwiftUI architecture work

## Reference File Plan

The initial reference set should be small and explicit:

- `references/swiftui-accessibility-semantics.md`
  Covers labels, values, hints, traits, headings, actions, and tree-shaping semantics in SwiftUI.
- `references/swiftui-accessibility-tree-shaping.md`
  Covers `accessibilityElement(children:)`, `accessibilityChildren`, `accessibilityRepresentation`, hiding, grouping, and synthetic elements.
- `references/framework-bridging-uikit-appkit.md`
  Covers where SwiftUI wraps UIKit or AppKit and where platform-native accessibility properties still matter.
- `references/worked-swiftui-accessibility-examples.md`
  Covers concrete SwiftUI examples for stable labels and values, tree reshaping, synthetic representations, headings, and representable-wrapper accessibility.
- `references/verification-expectations.md`
  Covers VoiceOver, focus order, Dynamic Type, contrast, reduced motion, simulator or device checks, and the explicit handoff to Xcode testing.
- `references/common-accessibility-anti-patterns.md`
  Names the failure modes directly and explains the likely correction path.

## Repo File Plan

The first implementation slice should add:

- `skills/apple-ui-accessibility-workflow/SKILL.md`
- `skills/apple-ui-accessibility-workflow/agents/openai.yaml`
- `skills/apple-ui-accessibility-workflow/references/swiftui-accessibility-semantics.md`
- `skills/apple-ui-accessibility-workflow/references/swiftui-accessibility-tree-shaping.md`
- `skills/apple-ui-accessibility-workflow/references/framework-bridging-uikit-appkit.md`
- `skills/apple-ui-accessibility-workflow/references/worked-swiftui-accessibility-examples.md`
- `skills/apple-ui-accessibility-workflow/references/verification-expectations.md`
- `skills/apple-ui-accessibility-workflow/references/common-accessibility-anti-patterns.md`

The first slice should also update:

- `skills/xcode-testing-workflow`
- `skills/swift-package-testing-workflow`
- `docs/maintainers/workflow-atlas.md`
- `README.md`
- `ROADMAP.md`

## Why Keep Testing Separate

Accessibility design and accessibility verification overlap, but they are not the same workflow.

This skill should own the semantic and framework-level reasoning. `xcode-testing-workflow` should own runtime UI automation details such as interruption monitors, test-plan matrices, launch arguments, screenshots, attachments, and simulator follow-through. `swift-package-testing-workflow` should stay lighter and only cover package-side semantic testing or handoff conditions.

## Adjacent Skill Boundaries

- `explore-apple-swift-docs`
  Owns Apple-docs source selection and direct documentation lookup.
- `swiftui-app-architecture-workflow`
  Owns app, scene, command, focus, environment, and view-composition architecture outside the accessibility-specific boundary.
- `xcode-testing-workflow`
  Owns XCUITest execution, `.xctestplan` execution, UI automation mechanics, and test-specific runtime verification.
- `swift-package-testing-workflow`
  Owns package-first test organization and semantic-test guidance, with handoff to Xcode testing when runtime UI accessibility verification matters.

## Quality Expectations

The skill should improve:

- user-facing semantic accuracy
- honesty about what assistive technologies will perceive
- bridge correctness between SwiftUI and UIKit or AppKit
- verification discipline before accessibility claims are treated as done

The skill should avoid rewarding:

- modifier spam without a clear semantic reason
- accessibility identifiers used as a substitute for user-facing accessibility
- generic design review language that does not connect to Apple accessibility behavior
- claims of verification without a runtime or manual accessibility pass

## First Implementation Slice

The first implementation slice should:

- create the new `apple-ui-accessibility-workflow` skill surface
- lock the skill boundary in `SKILL.md`
- add the initial reference set listed above
- update the testing workflows so Xcode owns deep runtime accessibility verification and SwiftPM hands off clearly
- expand Xcode testing guidance around `.xctestplan`, XCUITest, XCUIAutomation, and accessibility verification expectations

## Deferred Follow-Up

These can wait until the first version proves useful:

- a richer UIKit-only or AppKit-only deep-dive reference set
- worked examples for charts, canvas-heavy views, or fully custom controls
- runtime helpers or deterministic checklists beyond documentation and handoff guidance
- stronger downstream AGENTS sync once the accessibility surface stabilizes

## Concerns And Risks

- The biggest risk is letting the new skill become a second SwiftUI architecture surface.
- The second risk is letting testing details dominate the skill so heavily that it stops being about accessibility semantics.
- The third risk is writing broad “be accessible” guidance without enough Apple-specific behavior to make the skill actionable.

## Recommended Roadmap Interpretation

Milestone 37 should now be read as:

- phase one: `apple-ui-accessibility-workflow` as a SwiftUI-first Apple accessibility implementation and review skill, with explicit UIKit/AppKit bridge guidance
- phase one in parallel: deeper `.xctestplan`, XCUITest, XCUIAutomation, and accessibility-verification guidance in `xcode-testing-workflow`
- later follow-up: broader worked examples and deeper framework-specific expansion once the first accessibility surface proves useful
