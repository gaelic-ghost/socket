# Mixed AppKit And SwiftUI Composition

Use this reference when the request involves `NSHostingView`,
`NSHostingController`, SwiftUI hosted inside AppKit, AppKit exposed to SwiftUI,
or deciding which framework owns a mixed macOS app.

## Decision Rules

- Name the owner first: AppKit app, SwiftUI app, AppKit window, SwiftUI scene,
  AppKit controller, or SwiftUI view.
- If AppKit owns the app or window, SwiftUI content should usually be a hosted
  rendering and interaction surface with explicit inputs and callbacks.
- If SwiftUI owns the app or scene, AppKit views should usually be wrapped
  platform surfaces with limited responsibility.
- Put shared model state in one model owner and pass it across the hosting
  boundary.
- Keep menus, restoration, responder-chain actions, and window-controller
  behavior in AppKit when AppKit owns those behaviors.
- Keep SwiftUI environment, focus, preferences, scene storage, and view
  composition in SwiftUI when SwiftUI owns those behaviors.

## AppKit Hosting SwiftUI

- Use `NSHostingController` when a controller boundary fits the AppKit window or
  view-controller graph.
- Use `NSHostingView` for a view-level hosted SwiftUI surface.
- Pass models and commands in explicitly.
- Keep the AppKit owner responsible for window lifetime, menu validation,
  toolbar state, restoration, and app activation when those are AppKit-owned.

## SwiftUI Hosting AppKit

- Use SwiftUI representable bridges for focused AppKit views or controllers.
- Keep the AppKit wrapper's coordinator narrow: delegate bridging, target/action
  bridging, and platform-specific setup.
- Route broader app or scene decisions back to `swiftui-app-architecture-workflow`.

## Stop Conditions

- Stop if both frameworks can mutate the same state without a single owner.
- Stop if the bridge grows into a second app architecture hidden inside a view.

