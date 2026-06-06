# Menus, Responder Chain, And Validation

Use this reference when the request involves the main menu, context menus,
toolbar actions, keyboard shortcuts, target/action, the responder chain, or menu
validation.

## Decision Rules

- Use target/action for concrete UI commands when the action has a natural
  controller or responder owner.
- Use the responder chain when the active window, document, or view controller
  should decide whether an action is valid.
- Use menu validation to reflect real state such as selected document, active
  window, pending operation, missing permission, or unsupported mode.
- Keep command handlers close to the owner of the state they mutate.
- Prefer direct AppKit action methods over broad command buses unless the app
  already has a real command model that multiple surfaces share.

## Ownership Guide

- **App-wide command:** app delegate or app controller.
- **Active document command:** document, document window controller, or active
  responder.
- **Active window command:** window controller or selected view controller.
- **Selection command:** view controller that owns the selection.
- **Toolbar command:** same owner as the equivalent menu command.

## Validation Guide

- Disable commands when there is no owner, no selection, blocked permissions, or
  an active operation that cannot overlap.
- Update labels only when the command truly changes meaning.
- Keep validation human-readable in code: name the missing state or blocked
  operation rather than returning false with no explanation in adjacent logs.

## Mixed AppKit/SwiftUI

- SwiftUI commands belong in `swiftui-app-architecture-workflow` when the app is
  SwiftUI-owned.
- In AppKit-owned apps, hosted SwiftUI views should call explicit model or
  controller inputs rather than inventing a parallel command system that bypasses
  menu validation.
