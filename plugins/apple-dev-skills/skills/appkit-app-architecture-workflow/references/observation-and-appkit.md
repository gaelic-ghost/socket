# Observation And AppKit

Use this reference when the request involves Swift Observation, `@Observable`,
AppKit controls, controllers, delegates, hosted SwiftUI views, or main-actor UI
updates.

## Decision Rules

- Treat an `@Observable` model as a model object, not as a SwiftUI-only view
  model by default.
- Keep AppKit UI updates on the main actor.
- Use Observation to make model changes visible to SwiftUI hosted content or to
  explicit AppKit update code that reads the model.
- Do not assume AppKit controls automatically re-render just because an
  `@Observable` model changed. Name the bridge that updates the control,
  controller, hosted SwiftUI view, or binding.
- Keep one owner for mutable state. If AppKit owns the model, hosted SwiftUI
  views should receive and mutate that model through explicit inputs. If SwiftUI
  owns the state, AppKit should act as a hosted platform surface rather than a
  competing owner.

## Bridge Choices

- **Hosted SwiftUI content:** pass the observable model into
  `NSHostingController` or `NSHostingView`.
- **AppKit controller update:** observe or refresh from model changes through a
  deliberate controller method, task, notification, or other app-approved
  bridge.
- **Control value editing:** route edits through target/action, delegate, or
  binding so the model owner stays clear.
- **Long-running work:** keep background work separate from UI updates and hop
  back to the main actor before touching AppKit controls.

## Anti-Patterns

- Do not duplicate the same model as both an AppKit controller property and an
  independent SwiftUI state object.
- Do not describe Observation as a replacement for AppKit's responder chain,
  target/action, or menu validation.
- Do not hide main-actor requirements inside detached tasks.

