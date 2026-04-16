# SwiftUI Accessibility Tree Shaping

## Default tree versus accessibility tree

- The accessibility tree does not have to match the visual tree one-for-one.
- SwiftUI lets you combine, contain, ignore, replace, or synthesize accessibility elements when the raw visual structure is not the right user-facing semantic structure.

## Key tools

- `accessibilityElement(children:)`
  Use this to choose whether child elements combine, stay contained, or are ignored from the new parent accessibility element.
- `accessibilityChildren`
  Use this when one or more synthetic accessibility children should replace the raw child structure.
- `accessibilityRepresentation`
  Use this when the accessible presentation should act like a different semantic view tree than the rendered implementation.
- `accessibilityHidden`
  Use this only when the hidden content is truly decorative or duplicated meaning that is better expressed elsewhere.

## When reshaping is justified

- A composed card visually contains several texts and icons but should behave as one actionable element.
- A custom visualization needs a synthetic accessible summary or child breakdown because the rendered implementation is not readable to assistive technologies.
- Decorative content duplicates meaning that is already carried by a better accessible label or representation.

## Worked example: combine a tappable settings card

When a card is visually made of multiple child views but acts like one button, combine the children so assistive technologies do not announce each decorative fragment separately.

```swift
struct SettingsCard: View {
    let title: String
    let subtitle: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 12) {
                Image(systemName: "bell.badge")
                VStack(alignment: .leading) {
                    Text(title)
                    Text(subtitle)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
                Spacer()
                Image(systemName: "chevron.right")
            }
        }
        .accessibilityElement(children: .combine)
    }
}
```

The combined element still behaves like one button instead of sounding like a list of icons and text fragments.

## Review questions

- Should this content be one accessible element or many?
- If many children are announced, is that actually useful or just noisy?
- If content is hidden from accessibility, where does the meaning go instead?
- If a synthetic representation is used, does it still match the real interaction model?
