# App Delegate And Lifecycle

Use this reference when the request is about `NSApplication`,
`NSApplicationDelegate`, activation policy, launch, termination, reopen, app-wide
resources, or whether an app-level model should exist.

## Decision Rules

- Let `NSApplication` and `NSApplicationDelegate` own app lifecycle callbacks,
  activation behavior, termination decisions, reopen behavior, and app-wide
  resource setup.
- Put app-wide model state in an explicit app model when many windows,
  controllers, or status-item surfaces need the same durable object.
- Keep window-local or document-local state out of the app delegate unless it is
  truly shared by the whole app.
- Prefer small delegate methods that call named model or controller operations
  over long lifecycle methods with mixed setup, UI construction, and persistence
  logic.
- Treat launch setup, restoration setup, menu setup, status-item setup, and
  runtime-service setup as separate responsibilities even when the app delegate
  triggers all of them.

## Common Shapes

- **Single-window app:** app delegate creates or restores one window controller
  and keeps app-wide services in an app model.
- **Multiwindow app:** app delegate owns app-wide services; each window
  controller owns one window's UI and selected model.
- **Menu bar app:** app delegate or status-item controller owns the status item,
  activation policy, and quit behavior; transient popovers or panels own their
  own view controllers.
- **Document app:** `NSDocumentController` and document objects own document
  lifetimes; the app delegate owns only app-wide setup and policy.

## Stop Conditions

- Stop if the proposed app model would secretly become a catch-all for unrelated
  window, document, menu, and persistence behavior.
- Stop if SwiftUI `App` or scene structure is already the real app lifecycle
  owner; route that decision to `swiftui-app-architecture-workflow`.

