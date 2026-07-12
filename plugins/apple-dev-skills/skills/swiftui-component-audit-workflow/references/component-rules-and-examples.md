# Declarative Component Rules And Examples

SwiftUI is declarative UI, closer to React, F# Fabulous, and Elm than to AppKit or UIKit. A reusable `View` describes what it renders from state; it does not receive an imperative collaborator that tells it how to operate.

## Bad: Injected Collaborators

```swift
struct GEAItemRow: View {
    let viewModel: GEAItemRowViewModel
    let analytics: GEAAnalyticsService
}
```

This hides rendering state, mutation ownership, and side effects behind objects that the component does not own.

## Good: Values And Intent

```swift
struct GEAItemRow: View {
    let title: String
    let isComplete: Bool
    let onToggle: () -> Void
}
```

The memberwise initializer is sufficient. The parent owns the larger workflow; the row describes its state and reports its intent.

## Good: Private Composition

```swift
struct GEAItemEditor: View {
    @State private var draft = GEAItemDraft()

    var body: some View {
        GEAItemEditorFields(draft: $draft)
    }
}

private struct GEAItemEditorFields: View {
    @Binding var draft: GEAItemDraft
}
```

Private implementation views may receive the enclosing component's values, bindings, and actions.

## Good: Framework-Owned Hierarchy Context

```swift
struct GEAItemList: View {
    @Environment(\.modelContext) private var modelContext
    @Query private var items: [GEAItemModel]
}
```

Use existing environment actions such as `dismiss`, `openWindow`, and `openSettings` before inventing equivalents. Add a custom environment value/action only for a real hierarchy-wide capability; otherwise keep the action local.
