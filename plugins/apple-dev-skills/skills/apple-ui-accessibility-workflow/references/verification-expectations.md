# Verification Expectations

## What this skill can verify directly

- semantic design intent
- likely accessibility-tree problems in the code
- whether the chosen SwiftUI or bridge APIs fit the documented Apple behavior

## What still needs runtime follow-through

- VoiceOver reading order and announcements
- focus movement and action discoverability in a running app
- Dynamic Type layout behavior under larger content sizes
- contrast-sensitive or reduced motion-sensitive behavior that only appears when the app runs
- XCUITest or simulator verification for repeated regression coverage

## Expected verification passes

- manually review the target flow with VoiceOver when the UI is materially user-facing
- review focus order and whether the accessible element grouping matches the intended interaction model
- review Dynamic Type or content-size-category behavior when text-heavy or control-dense layouts are involved
- review contrast or reduced motion-sensitive behavior when animation, overlays, or visual emphasis change the user experience

## Testing handoff

- Hand off to `xcode-testing-workflow` when the next honest step is XCUITest execution, simulator or device follow-through, `.xctestplan` configuration, launch arguments, locale or content-size-category matrices, screenshot capture, attachments, or XCUI interruption handling.
- Keep `swift-package-testing-workflow` limited to package-first semantic testing and handoff conditions rather than runtime UI accessibility automation.
