# Commands And Focus

## Core Boundary

- Commands belong where the command's responsibility belongs.
- Scene-sensitive commands should read from the active scene context rather than from a broad global object.
- Focused context is often the bridge that commands consume, but command ownership and focused-context design are not the same question.

## Practical Guidance

- Use `CommandMenu` and `CommandGroup` when the app needs menu-bar or keyboard-command structure.
- Use focused-context tools only after deciding that a command is actually scene-sensitive or focus-sensitive.
- Let the dedicated focus reference own the detailed choice between `focusedValue`, `focusedSceneValue`, `focusedObject`, `focusedSceneObject`, `FocusState`, and focusable interactions.
- Prefer native sidebar and inspector command surfaces over custom toggle commands with private duplicated state.
- When SwiftUI or the platform already exposes a native command or toolbar affordance for a sidebar or inspector, align custom commands around that existing surface instead of shadowing it with parallel terminology.

## Ownership Rules

- App-level commands belong in the app command surface.
- Scene-sensitive commands should not be routed through unrelated leaf views or global environment objects when focused values give a narrower, more honest path.
- Leaf views may publish focused values, but they should not become the hidden owner of app-wide command policy.

## Worked Examples

### Example: Sidebar Filter Command

Good shape:

- the command surface owns the `CommandMenu`
- the sidebar publishes a scene-focused action or value that the command consumes

Why:

- the command belongs to the app command surface
- the active scene provides the context the command needs
- the sidebar does not become the hidden owner of menu policy

### Example: Global Quit-Adjacent Behavior

Good shape:

- truly app-wide commands stay app-wide and do not depend on focused context

Why:

- not every command problem is a focus problem
- if a command does not vary by active scene or focused subtree, adding focused context only makes ownership harder to read

### Example: Native Sidebar And Inspector Commands Stay Native

Good shape:

- the app keeps native sidebar behavior attached to the split-view scene model
- inspector presentation stays tied to the detail or scene state that actually owns it
- custom menu commands augment native behavior instead of inventing a second command vocabulary for showing and hiding core chrome

Why:

- desktop SwiftUI already carries expectations around sidebar and inspector behavior
- when the app creates parallel custom toggles with different state names, command ownership becomes harder to follow and the UI becomes less native

### Example: Close An Auxiliary Window From A Command

Good shape:

- a command uses `dismissWindow(id:)` when it needs to close a specific auxiliary window declared by the app
- the command uses `dismiss()` only when the command is running from within the hierarchy that owns the current presentation

Why:

- Apple documents `dismissWindow` as the environment action for dismissing a known window by identifier
- Apple documents `dismiss()` as context-sensitive; inside a modal it dismisses the modal rather than the enclosing window
- choosing the right action keeps the command tied to the actual presentation boundary it intends to affect

### Example: Open Settings Or A Supplemental Window Without A Router Layer

Good shape:

- a command or toolbar action calls `openSettings()`, `openWindow(id:)`, or `openWindow(value:)`
- the app scene declarations remain the source of truth for what can be opened

Why:

- these are already native environment actions with system-managed semantics
- a custom router or window registry usually duplicates scene declarations while making behavior less obvious

## References

- [CommandGroup](https://developer.apple.com/documentation/swiftui/commandgroup)
- [Scenes: Setting commands](https://developer.apple.com/documentation/swiftui/scene#Setting-commands)
- [EnvironmentValues.dismissWindow](https://developer.apple.com/documentation/swiftui/environmentvalues/dismisswindow)
- [EnvironmentValues.openWindow](https://developer.apple.com/documentation/swiftui/environmentvalues/openwindow)
- [EnvironmentValues.openSettings](https://developer.apple.com/documentation/swiftui/environmentvalues/opensettings)
