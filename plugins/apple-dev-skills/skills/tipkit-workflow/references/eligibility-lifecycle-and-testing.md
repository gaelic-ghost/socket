# Eligibility, Lifecycle, and Testing

## Configure Once at Startup

Configure TipKit before tips need to display, normally in the app initializer:

```swift
import SwiftUI
import TipKit

@main
struct ExampleApp: App {
    init() {
        do {
            try Tips.configure()
        } catch {
            assertionFailure(
                "TipKit configuration failed before the app created its first scene. " +
                "Check the configured datastore location and TipKit options. Underlying error: \(error)"
            )
        }
    }

    var body: some Scene {
        WindowGroup { ContentView() }
    }
}
```

Use configuration options deliberately:

- `displayFrequency(_:)` controls the minimum cadence used when determining tip eligibility.
- `datastoreLocation(_:)` changes persistent storage. Apple documents Application Support as the default on iOS, macOS, watchOS, and visionOS, and a caches/UserDefaults arrangement on tvOS.
- `cloudKitContainer(_:)` enables cross-device TipKit datastore sync. Apple recommends a separate CloudKit container for tips and requires the app’s iCloud and remote-notification background capabilities. TipKit does not sync through CloudKit by default.
- A group-container datastore requires a correctly configured App Group entitlement.

Do not move configuration into individual feature views and do not silently swallow errors.

## Define Stable Eligibility

Use a parameter rule for persistent app state:

```swift
struct FavoriteTip: Tip {
    @Parameter
    static var hasFavorites = false

    var title: Text { Text("Save a favorite") }

    var rules: [Rule] {
        #Rule(Self.$hasFavorites) { $0 == false }
    }
}
```

Use an event rule for repeated behavior:

```swift
struct SearchTip: Tip {
    static let openedLibrary = Tips.Event(id: "opened-library")

    var title: Text { Text("Search your library") }

    var rules: [Rule] {
        #Rule(Self.openedLibrary) {
            $0.donations.donatedWithin(.week).count >= 3
        }
    }
}
```

Donate where the real product event occurs. Decide whether an “open” means a navigation entry, scene/session activation, or some other boundary; do not blindly count SwiftUI `onAppear` or `.task` reruns as separate user events.

```swift
Task {
    await SearchTip.openedLibrary.donate()
}
```

Current Xcode documentation exposes async `donate()` / `donate(_:)` methods and callback-based `sendDonation(_:)` / `sendDonation(_:_:)` alternatives. Prefer structured-concurrency `donate` from async-aware code; use `sendDonation` only when the callback form fits the existing boundary better.

Multiple entries in `rules` combine with logical AND. Keep parameter and event identifiers stable after release because persisted eligibility depends on identity and history.

When several tips compete for one presentation surface, use `TipGroup` to select one eligible tip at a time instead of attaching multiple independent popovers. Choose the group priority deliberately and render its current eligible tip through the appropriate presentation API.

Use tip options such as maximum display count or display-frequency overrides only when the product behavior requires them. Confirm current option names and availability through Xcode docs before coding.

## Dismissal and Invalidation

Closing a tip dismisses the current presentation. Calling `invalidate(reason:)` permanently invalidates that tip for the persisted datastore. Invalidate at the feature’s success point, using the reason that matches what happened, such as `.actionPerformed` when the person used the highlighted feature.

Do not invalidate on view appearance, unrelated navigation, or an action that merely opens more information unless the tip’s job is actually complete.

## Deterministic Debugging and Tests

TipKit persists display history, so “the code is correct but nothing appears” often means configuration, eligibility, frequency, or prior invalidation is controlling the result.

Use TipKit’s testing APIs only in deliberate debug, preview, or test setup:

```swift
#if DEBUG
try? Tips.resetDatastore()
Tips.showAllTipsForTesting()
#endif
```

Call `Tips.resetDatastore()` before `Tips.configure()`. Apple documents that reset removes existing tip, event, and parameter records and must run before configuration. Apply force-visible or force-hidden testing overrides in the same deliberate startup test path, then configure TipKit once.

Apple also provides `hideAllTipsForTesting()` for deterministic hidden-state checks. Verify exact signatures and throwing behavior in the active Xcode documentation before committing test helpers, because these controls can evolve with the SDK.

Never leave unconditional datastore resets or force-visible overrides in production startup.

## Troubleshooting Order

1. Confirm `Tips.configure` completed before presentation.
2. Confirm the running OS supports the chosen TipKit API.
3. Confirm the tip instance is attached to the intended live view or control.
4. Inspect every parameter and event rule; remember multiple rules AND together.
5. Confirm event donations occur on the actual runtime path.
6. Check display-frequency and max-display-count options.
7. Check whether the tip was dismissed or permanently invalidated in the current datastore.
8. Temporarily force visibility in a debug/test path to separate content/presentation problems from eligibility problems.
9. Reset the datastore only when losing local TipKit history is acceptable.
10. For UIKit or AppKit, confirm the status-observation task is alive, main-actor UI updates occur, and presentation objects are retained.
11. For SwiftUI toolbar controls, check toolbar overflow, menus, sheets, alerts, other popovers, competing tips, and compact geometry for presentation conflicts.

Test the normal path again without force-visible overrides. Relaunch the app to verify persistence and test the smallest supported window or device size to expose popover collisions.
