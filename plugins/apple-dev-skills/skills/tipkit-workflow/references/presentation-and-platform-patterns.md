# Presentation and Platform Patterns

## Choose the Presentation

Prefer an inline tip whenever practical. Apple documents that inline tips change layout to make room but avoid obscuring interactive UI. A popover tip overlays the current layout and can obscure controls, so reserve it for a compact feature that benefits from a visual pointer.

Keep a stable tip instance in the owning view. Define the content separately from presentation and feature behavior.

```swift
import SwiftUI
import TipKit

struct FavoriteTip: Tip {
    var title: Text { Text("Save a favorite") }
    var message: Text? { Text("Favorites stay at the top of your library.") }
    var image: Image? { Image(systemName: "star") }
}

struct LibraryView: View {
    private let favoriteTip = FavoriteTip()

    var body: some View {
        VStack {
            TipView(favoriteTip, arrowEdge: .bottom)

            Button("Favorite", systemImage: "star") {
                saveFavorite()
                favoriteTip.invalidate(reason: .actionPerformed)
            }
        }
    }
}
```

For a SwiftUI tip popover, attach `popoverTip` to the exact feature being explained:

```swift
Button("Favorite", systemImage: "star") {
    saveFavorite()
    favoriteTip.invalidate(reason: .actionPerformed)
}
.popoverTip(favoriteTip, arrowEdge: .top)
```

Treat the arrow edge as a preference whose visual result must be checked in the real window or device geometry. Avoid imagery in a compact popover when the pointer already makes the target clear.

## Actions

Define `actions` on the tip, then route by stable action identifiers in the presentation callback. An action is not automatically the same as completing the highlighted feature; invalidate only when the action makes the tip permanently irrelevant.

```swift
struct ExportTip: Tip {
    var title: Text { Text("Export your project") }

    var actions: [Action] {
        Action(id: "learn-more", title: "Learn More")
    }
}

TipView(ExportTip()) { action in
    guard action.id == "learn-more" else { return }
    openExportHelp()
}
```

## Styling

Use `tipViewStyle(_:)` and a focused `TipViewStyle` only when the system style cannot meet the app’s visual requirements. Preserve title, message, image, actions, dismissal, Dynamic Type, contrast, and accessibility semantics. Do not build a second presentation system merely to restyle tips.

## UIKit

Use `TipUIView` for inline UIKit content and `TipUIPopoverViewController` for a popover. Observe `shouldDisplayUpdates` or `statusUpdates` to add, present, remove, and dismiss the UIKit object as eligibility changes. Own the observation task in the view controller, run UI work on the main actor, and cancel the task when the view leaves its active lifecycle.

## AppKit

Use `TipNSView` for inline AppKit content and `TipNSPopover` for a popover. Observe `shouldDisplayUpdates` or `statusUpdates`, keep the presentation object alive while shown, update views on the main actor, and cancel the observation task when the owning controller disappears.

## Platform Verification

Check the exact API availability in Xcode documentation against every deployment target before editing. Build each affected platform because SwiftUI modifiers and framework bridges can differ even when the `Tip` content is shared.
