# Menu Bar Status Item And Activation

Use this reference when the request involves a menu bar app, status item,
popover, floating panel, activation policy, dock visibility, reopen behavior, or
quit behavior.

## Decision Rules

- Treat an `NSStatusItem` as an app-level surface. It usually lives as long as
  the app, not as long as a popover, panel, or hosted view.
- Keep status-item setup in an app delegate, app controller, or dedicated
  status-item controller with a clear lifetime.
- Put transient UI in an `NSPopover`, `NSPanel`, or window controller; do not let
  the transient view own the status item itself.
- Make activation policy a deliberate app-level decision. A menu bar utility
  may hide the Dock icon, while a hybrid app may need normal activation.
- Keep quit behavior explicit. Menu bar apps need a discoverable quit command,
  and long-running work should either finish, cancel, or make background
  behavior clear before termination.

## AppKit And SwiftUI Mix

- SwiftUI `MenuBarExtra` can be the right owner for SwiftUI-first menu bar apps.
- Use AppKit status items when the app needs AppKit-specific menu validation,
  panels, responder-chain behavior, custom windows, app activation control, or
  mixed AppKit/SwiftUI ownership.
- If AppKit owns the status item and SwiftUI renders the popover content, pass a
  model into `NSHostingController` instead of making the SwiftUI view create the
  status item.

## Anti-Patterns

- Do not recreate the status item every time popover content changes.
- Do not hide quit, preferences, or diagnostics only inside a transient popover
  that may fail to open.
- Do not put global status-item authority inside a SwiftUI leaf view hosted by a
  popover.
