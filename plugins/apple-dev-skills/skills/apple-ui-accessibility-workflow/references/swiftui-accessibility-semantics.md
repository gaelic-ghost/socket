# SwiftUI Accessibility Semantics

## Baseline model

- SwiftUI already exposes baseline accessibility behavior for standard controls such as buttons, toggles, text fields, sliders, lists, and navigation surfaces.
- Start by confirming what the default semantics already provide before adding explicit accessibility modifiers.
- Prefer explicit accessibility modifiers only when the default semantic output is incomplete, misleading, noisy, or structurally wrong for assistive technologies.

## Description surfaces

- Use `accessibilityLabel(_:)` when the user-facing accessible name needs to differ from what SwiftUI would otherwise infer.
- Use `accessibilityValue(_:)` when the control or content has a stateful value that assistive technologies need to announce.
- Use `accessibilityHint(_:)` only when the next action or consequence is not already clear from the role, label, and surrounding context.
- Use `accessibilityInputLabels(_:)` when alternate spoken or input names materially help users target the element.

## Roles, traits, and structure

- Use `accessibilityAddTraits(_:)` and `accessibilityRemoveTraits(_:)` when the semantic role needs to be refined explicitly.
- Prefer semantic correctness over decorative verbosity. A custom card that behaves like a button should expose button semantics; it should not sound like a pile of unrelated text.
- Use heading semantics where the content truly acts as a structural section heading for navigation.

## Actions

- Use `accessibilityAction` or `accessibilityActions` when assistive technologies need an explicit action surface that is not already represented by the default control behavior.
- Use adjustable or scroll actions only when the control really behaves as an adjustable value or scrollable surface from an assistive-technology perspective.

## Worked example: custom favorite toggle

When a custom control renders as an icon plus styled text, make sure the accessible name and value describe the state instead of making VoiceOver infer meaning from presentation details.

```swift
struct FavoriteButton: View {
    let isFavorite: Bool
    let toggle: () -> Void

    var body: some View {
        Button(action: toggle) {
            Label(isFavorite ? "Favorite" : "Mark Favorite", systemImage: isFavorite ? "star.fill" : "star")
        }
        .accessibilityLabel("Favorite")
        .accessibilityValue(isFavorite ? "On" : "Off")
    }
}
```

This keeps the accessible name stable while exposing the changing state through the value.

## Review questions

- What would VoiceOver call this element?
- What would VoiceOver say the element does?
- Is the accessible name derived from meaningful content or from implementation noise?
- Does the announced role match the interaction model the user actually gets?
