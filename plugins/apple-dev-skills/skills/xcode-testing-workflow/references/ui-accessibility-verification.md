# UI Accessibility Verification

## Relationship to the accessibility skill

- `apple-ui-accessibility-workflow` owns semantic accessibility reasoning and framework-specific implementation guidance.
- `xcode-testing-workflow` owns runtime verification when the next honest step is proving accessibility behavior in a running app.

## What belongs here

- XCUITest follow-through for accessibility-sensitive flows
- `.xctestplan` matrices that vary launch arguments, locale, or content-size-category behavior
- screenshot and attachment capture for debugging accessibility regressions
- simulator or device validation when the UI needs repeated runtime coverage

## Expected runtime checks

- confirm the accessible flow still works when larger content sizes materially change layout
- confirm custom controls remain discoverable and actionable through their runtime UI state
- confirm focus movement and UI interruptions do not block the intended workflow
- capture evidence when the accessibility-sensitive state is hard to diagnose from code alone

## What does not belong here

- deciding the correct accessible label, trait, or representation in the first place
- broad accessibility review language that never turns into executable or manual runtime verification

## Handoff rules

- hand off to `apple-ui-accessibility-workflow` when the question is really about semantics, grouping, labels, traits, actions, or bridge behavior
- stay in `xcode-testing-workflow` when the problem is how to exercise and verify that behavior in a running app
