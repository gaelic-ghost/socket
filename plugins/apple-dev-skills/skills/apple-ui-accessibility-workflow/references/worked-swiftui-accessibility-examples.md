# Worked SwiftUI Accessibility Examples

## Example: synthetic chart summary

When a visual surface such as a custom chart is hard to read through the rendered tree alone, provide a synthetic accessibility representation that summarizes the same data in a user-facing structure.

```swift
struct WeeklyStepsChart: View {
    let entries: [(day: String, count: Int)]

    var body: some View {
        StepsBars(entries: entries)
            .accessibilityRepresentation {
                VStack(alignment: .leading) {
                    Text("Weekly steps")
                    ForEach(entries, id: \.day) { entry in
                        Text("\(entry.day): \(entry.count) steps")
                    }
                }
            }
    }
}
```

The rendered chart can stay visual, while the accessibility representation exposes a navigable textual summary.

## Example: custom rotor-friendly section heading

When a SwiftUI screen has clear structural sections, expose true headings instead of relying on larger fonts alone.

```swift
struct AccountSecuritySection: View {
    var body: some View {
        Section {
            Toggle("Face ID", isOn: .constant(true))
            Toggle("Require Passcode", isOn: .constant(true))
        } header: {
            Text("Account Security")
                .accessibilityAddTraits(.isHeader)
        }
    }
}
```

This lets assistive technologies treat the section title as structure, not just decoration.

## Example: representable bridge with UIKit semantics

When SwiftUI wraps a UIKit view, keep the accessibility contract authored in the UIKit layer when that is where the real role and state live.

```swift
struct ProgressRingView: UIViewRepresentable {
    let progress: Double

    func makeUIView(context: Context) -> RingView {
        RingView()
    }

    func updateUIView(_ uiView: RingView, context: Context) {
        uiView.progress = progress
        uiView.isAccessibilityElement = true
        uiView.accessibilityLabel = "Download progress"
        uiView.accessibilityValue = "\(Int(progress * 100)) percent"
    }
}
```

Here the wrapped UIKit view owns the accessible role and value because the rendered control itself lives there.
