# Environment And Preferences

## Environment Boundary

- Use environment values for shared contextual scope that genuinely belongs to the surrounding hierarchy.
- Do not treat environment as a generic dependency container for unrelated services or view models.
- Apple documents `Scene.environment(_:_:)` as affecting that scene and its descendant views only, which makes scene-local environment shaping a real structural tool.

## Preference Boundary

- Use a preference key when a child view must publish information upward to an ancestor.
- Do not use a preference key as a general-purpose state bus.
- If the data naturally belongs in explicit parent-owned state, use explicit data flow instead.

## Practical Rules

- Prefer explicit initializer injection when the dependency is narrow and the ownership chain is clear.
- Prefer environment only when many descendants share the same contextual dependency and the surrounding hierarchy is the honest owner.
- Prefer a preference key only when the information is discovered in a descendant and must travel upward.
- Prefer focused values rather than environment when the state is about active scene or focused-subtree context for commands.
- Treat native environment actions like `dismiss`, `dismissWindow`, `openWindow`, and `openSettings` as presentation requests, not as general state transport.

## Worked Examples

### Example: Theme Policy Versus Editor Session

Use environment for:

- a theme policy, style policy, or other shared context that honestly belongs to the surrounding scene or app hierarchy

Use explicit injection for:

- an editor session, detail model, or narrow dependency that only a few descendants need

Why:

- shared contextual scope is what environment is for
- narrow ownership gets harder to explain once it is pushed into environment just for convenience

### Example: Child Layout Reporting

Use a preference key when:

- a child discovers layout-derived information that an ancestor must react to, such as a measured header height or anchor

Do not use a preference key when:

- the data is ordinary business state that could have been passed explicitly

Why:

- preference keys are for upward publication from descendants
- they are not a substitute for explicit state ownership

### Example: Command Context Is Not Environment

Bad shape:

- active editor selection or currently focused item is written into environment so commands can find it

Better shape:

- use focused values or scene-focused values for that active context

Why:

- active focus context is narrower and more truthful than broad environment propagation

### Example: Native Presentation Actions Are Not App Services

Use native environment actions for:

- requesting presentation or dismissal of a settings scene, supplemental window, current modal, or current window

Do not use environment actions as proof that:

- broad environment injection is the right tool for your own app services, stores, routers, or scene coordinators

Why:

- `openWindow`, `dismissWindow`, `dismiss`, and `openSettings` are documented system actions exposed through environment because presentation is contextual
- that does not imply your own business objects should also be pushed into environment just because they are convenient to reach

### Example: Inspector Visibility Belongs To The Owning Scene Or Detail Surface

Use explicit state or scene-owned state when:

- an inspector is part of the current scene's detail workflow and its visibility depends on current selection or scene mode

Do not use environment for:

- duplicating inspector-visible state across unrelated descendants that do not actually own inspector presentation

Why:

- inspector visibility is usually part of scene structure, not a broad ambient dependency
- once inspector state is ambient without a clear owner, sidebar, detail, toolbar, and commands all start mutating it from unclear directions

## References

- [Scene.environment(_:_:)](https://developer.apple.com/documentation/swiftui/scene/environment(_:_:))
- [EnvironmentValues.dismiss](https://developer.apple.com/documentation/swiftui/environmentvalues/dismiss)
- [EnvironmentValues.dismissWindow](https://developer.apple.com/documentation/swiftui/environmentvalues/dismisswindow)
- [EnvironmentValues.openWindow](https://developer.apple.com/documentation/swiftui/environmentvalues/openwindow)
- [EnvironmentValues.openSettings](https://developer.apple.com/documentation/swiftui/environmentvalues/opensettings)
