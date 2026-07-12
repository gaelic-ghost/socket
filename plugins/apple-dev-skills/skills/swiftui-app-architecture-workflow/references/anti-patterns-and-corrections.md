# Anti-Patterns And Corrections

## Environment Dumping Ground

Bad shape:

- every dependency gets pushed into environment values or environment objects because it is convenient

Correction:

- keep narrow dependencies explicit
- reserve environment for shared contextual scope that honestly belongs to the hierarchy

## Giant Root View

Bad shape:

- one root view owns app lifecycle concerns, scene wiring, command wiring, transient UI state, and leaf rendering details

Correction:

- split by responsibility
- keep app and scene boundaries explicit
- keep leaf rendering concerns local to smaller composable views

## Grouped SwiftUI View Files

Bad shape:

- multiple SwiftUI `View` component types are grouped into one Swift file because they are small, related, private, or currently used by one parent

Correction:

- split each SwiftUI `View` component into its own `<Name>.swift` file
- keep that component's Xcode SwiftUI preview in the same file as the component
- keep component-local state inside the component or extract only a genuinely reusable modifier such as `GEAWhateverViewModifier.swift`

## External SwiftUI View Models And Collaborators

Bad shape:

- a reusable view receives a ViewModel, store, coordinator, manager, service, or observable object from another view
- a parent creates a view-specific object only to pass it through the component tree
- a component writes an explicit initializer that only repeats its stored-property assignments

Correction:

- make reusable views self-contained declarative components with value, binding, and action inputs
- own complex local presentation state inside the component with `@State` and a view-local `@Observable` type only when direct state is no longer readable
- use the memberwise initializer unless a real transformation, validation, or invariant requires explicit initialization
- use environment, focus, preferences, commands, SwiftData model objects, or a non-SwiftUI boundary only when each matches its actual framework or ownership boundary

### Bad And Good Component Interfaces

Bad:

```swift
struct GEAItemRow: View {
    let viewModel: GEAItemRowViewModel
    let coordinator: GEAItemCoordinator
}
```

Good:

```swift
struct GEAItemRow: View {
    let title: String
    let isComplete: Bool
    let onToggle: () -> Void
}
```

Private implementation views may accept the enclosing component's local values, bindings, and actions. That is ordinary composition, not cross-component dependency injection.

## Wrapper-Heavy Architecture

Bad shape:

- extra coordinators, wrappers, and controller layers are added only to look architectural

Correction:

- prefer direct SwiftUI structure until a concrete ownership or lifecycle problem demands a layer
- make every extra type justify a real boundary

## Preference Keys As A State Bus

Bad shape:

- preference keys are used for ordinary state propagation or service access

Correction:

- use them only for upward publication from descendants to ancestors
- otherwise use explicit state flow or another narrower mechanism

## Hidden Control Flow In Modifiers

Bad shape:

- important app or scene behavior is buried in modifier chains so ownership becomes hard to explain

Correction:

- keep ownership and action flow obvious
- extract structure when needed, but do not hide the real owner

## Leaf Views Owning App Commands

Bad shape:

- command policy and app-level actions are effectively owned by one leaf view

Correction:

- let the command surface own commands
- let leaf views publish focused context when commands need it
