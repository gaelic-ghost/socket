# AppKit MVC, Target Action, And Bindings

Use this reference when the request involves AppKit MVC, controller lifetime,
delegates, target/action, AppKit bindings, or how models should change from UI.

## Decision Rules

- Keep models independent from AppKit controls when practical. Models carry
  domain state and operations; controllers translate UI events into model
  changes.
- Use target/action for user commands that originate in controls, menus,
  toolbars, or keyboard shortcuts.
- Use delegates for owner-to-collaborator decisions where AppKit already
  exposes a delegate model.
- Use AppKit bindings only when the binding is simpler and clearer than explicit
  controller updates, and when the key-value observing shape is appropriate for
  the model.
- Keep view controllers focused on view hierarchy and local UI coordination.
- Keep window controllers focused on window chrome, toolbar/menu participation,
  restoration, and root-controller wiring.

## Practical Ownership

- The model should answer "what state or operation is this?"
- The view controller should answer "how does this view show and edit it?"
- The window controller should answer "which window owns this surface?"
- The app delegate or app controller should answer "what applies to the whole
  app?"

## Anti-Patterns

- Do not make a controller a dumping ground for persistence, network calls,
  window restoration, app preferences, menu validation, and rendering.
- Do not create a new coordinator when an existing delegate, target/action, or
  responder-chain path already names the owner clearly.
- Do not let bindings hide important side effects or validation.
