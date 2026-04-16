# App And Scene Structure

## Core Boundary

- `App` owns application entry and the top-level list of scenes.
- `Scene` is the lifecycle container the system manages.
- A scene is not just a visual grouping; it is the boundary for scene-specific lifecycle, presentation, and environment propagation.

## Primary Scene Types In Scope

- `WindowGroup`
  Use when the app should present multiple windows that share one structural template.
- `Window`
  Use when a distinct singleton-style window surface needs its own identity.
- `Settings`
  Use for a managed settings window in macOS-oriented SwiftUI apps.
- `DocumentGroup`
  Use for document-based applications instead of treating documents as ordinary windows.

## Documented Behaviors To Rely On

- Apple documents `Scene` as the part of the app interface with a lifecycle managed by the system.
- Apple documents `WindowGroup` as a scene whose windows maintain independent state.
- Apple documents `Settings` as a scene that SwiftUI manages for app settings rather than an arbitrary ordinary view.
- Apple documents `DocumentGroup` as the document-support scene rather than a stylistic alternative to `WindowGroup`.

## Structural Guidance

- Put app-wide responsibilities at the `App` boundary only when they truly apply across the whole app.
- Put scene-wide responsibilities at the scene boundary when they differ per window, per document, or per managed scene.
- Keep scene-local state scene-local when multiple windows can exist.
- Do not use one shared mutable object for every window just because the first draft happened to be single-window.
- Treat `NavigationSplitView` as a selection-driven scene root. Apple documents it as a view where selections in leading columns control presentations in subsequent columns.
- In a three-column split view, the sidebar typically owns the first selection, the content column typically owns the second selection, and the detail or inspector surface reacts to those selections.
- Prefer `List(selection:)` or similarly selection-honest containers in sidebar and content columns before inventing custom panel-coordination machinery.

## Worked Examples

### Example: Multiwindow Inspector State

Good shape:

- each `WindowGroup` window creates or receives its own scene-local inspector state
- commands or toolbars that operate on that state read it through scene-aware mechanisms

Why:

- Apple documents `WindowGroup` windows as maintaining independent state
- if one shared object is used for all windows, the design stops matching the documented scene boundary

### Example: Settings Stay In A Settings Scene

Good shape:

- the app declares a `Settings` scene and keeps settings presentation there
- views that need to open settings use the environment action for opening that scene

Why:

- settings are a managed scene surface, not just another arbitrary sheet or navigation destination
- keeping settings in the scene model preserves desktop-oriented app structure

### Example: Document Work Uses `DocumentGroup`

Good shape:

- document ownership and lifecycle live in `DocumentGroup`
- regular window structure stays for non-document surfaces

Why:

- document behavior is not just “a window with a file loaded into it”
- `DocumentGroup` is the documented document-support scene boundary

### Example: `NavigationSplitView` Owns Column Coordination

Good shape:

- the scene root is a `NavigationSplitView`
- the sidebar column uses `List(selection:)` or an equivalent selection-driven surface for the first level
- the content column reacts to the sidebar selection and exposes its own selection for the next level
- the detail view or inspector reacts to the current content selection rather than maintaining a second hidden copy of navigation state

Why:

- Apple documents `NavigationSplitView` as a view where selections in leading columns control subsequent columns
- this makes the split view itself the honest structural owner of master-content-detail flow
- ad hoc panel coordinators usually duplicate the same state in more obscure ways

### Example: Sidebar Rows Drive The Next Column

Good shape:

- sidebar rows use `NavigationLink(value:)` or explicit list selection to drive what the next column shows
- the content column presents the next level of navigation instead of the sidebar trying to mutate deep detail state directly

Why:

- Apple documents `NavigationSplitView` as coordinating with list selection, and it also supports `NavigationLink` with `NavigationStack` destinations inside columns
- this preserves a native, column-by-column navigation story instead of treating the sidebar like a button grid with hidden side effects

### Example: Settings And Auxiliary Windows Use Native Scene Actions

Good shape:

- use `openSettings` to present the app's `Settings` scene
- use `openWindow(id:)` or `openWindow(value:)` to present a declared `Window` or `WindowGroup`
- use `dismiss()` from inside a window hierarchy to close that window, unless the current presentation is a sheet or popover
- use `dismissWindow(id:)` when another view or command needs to close a known auxiliary window by identifier

Why:

- Apple documents `openSettings`, `openWindow`, `dismiss`, and `dismissWindow` as native scene and window actions
- these actions preserve system-managed window identity and behavior better than custom visibility registries
- using the native actions keeps ownership readable: scenes declare windows, and descendant views request system presentation or dismissal

## References

- [App](https://developer.apple.com/documentation/swiftui/app)
- [Scene](https://developer.apple.com/documentation/swiftui/scene)
- [Scenes](https://developer.apple.com/documentation/swiftui/scenes)
- [WindowGroup](https://developer.apple.com/documentation/swiftui/windowgroup)
- [Window](https://developer.apple.com/documentation/swiftui/window)
- [Settings](https://developer.apple.com/documentation/swiftui/settings)
- [DocumentGroup](https://developer.apple.com/documentation/swiftui/documentgroup)
- [NavigationSplitView](https://developer.apple.com/documentation/swiftui/navigationsplitview)
- [EnvironmentValues.openWindow](https://developer.apple.com/documentation/swiftui/environmentvalues/openwindow)
- [EnvironmentValues.dismiss](https://developer.apple.com/documentation/swiftui/environmentvalues/dismiss)
- [EnvironmentValues.dismissWindow](https://developer.apple.com/documentation/swiftui/environmentvalues/dismisswindow)
- [EnvironmentValues.openSettings](https://developer.apple.com/documentation/swiftui/environmentvalues/opensettings)
