# Architecture Decision Rules

Use this reference when choosing between AppKit, SwiftUI, or a mixed app shape,
or when the request needs a concise recommendation rather than a topic-specific
reference.

## Framework Choice

- Choose AppKit when the behavior is naturally owned by app delegates, status
  items, responder-chain menus, window controllers, view controllers, documents,
  panels, inspectors, AppKit restoration, target/action, or AppKit bindings.
- Choose SwiftUI when the behavior is naturally owned by SwiftUI `App`, scenes,
  `WindowGroup`, `Window`, `Settings`, `DocumentGroup`, commands, focus,
  environment, preferences, or reusable view composition.
- Choose mixed composition when one framework owns the app or window shape and
  the other framework provides a focused view, control, or content surface.

## Ownership Choice

- Put app-wide behavior at the app delegate or app model boundary.
- Put menu bar behavior at the status-item controller boundary.
- Put active-window behavior at the window-controller boundary.
- Put document behavior at the document or document-controller boundary.
- Put pane, selection, and local UI behavior at the view-controller boundary.
- Put durable state in a model or persistence surface.
- Put hosted SwiftUI behavior behind an explicit hosting boundary.

## Transport Choice

- Prefer direct injection for required collaborators.
- Prefer target/action for user commands from AppKit controls and menus.
- Prefer responder-chain actions when the active responder should decide.
- Prefer delegate methods where AppKit already offers a delegate contract.
- Prefer explicit model methods for mutations.
- Prefer persistence payloads only when the data must survive process or window
  lifetime.

## Recommendation Shape

Return one path:

1. "The owner should be ..."
2. "The transport should be ..."
3. "The Apple behavior this relies on is ..."
4. "The tradeoff is ..."
5. "The next step is ..."

