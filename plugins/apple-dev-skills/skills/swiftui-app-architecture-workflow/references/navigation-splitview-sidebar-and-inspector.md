# NavigationSplitView, Sidebar, And Inspector

## Core Boundary

- Treat `NavigationSplitView` as a scene-structure primitive, not as a cosmetic container.
- Apple documents it as a view where selections in leading columns control presentations in subsequent columns.
- Sidebar, content, detail, and inspector behavior should follow that selection model before introducing custom coordination layers.

## Documented Behaviors To Rely On

- Apple documents `NavigationSplitView` as a two- or three-column container where leading-column selection drives later columns.
- Apple documents that `NavigationSplitView` typically acts as a root view in a scene.
- Apple documents that a split view coordinates directly with `List(selection:)`, including programmatic selection updates.
- Apple documents that `NavigationLink(value:)` can coordinate with list selection inside `NavigationSplitView`.
- Apple documents a built-in `sidebarToggle` toolbar item for `NavigationSplitView` on supported platforms.
- Apple documents `InspectorCommands` as the built-in commands surface for toggling an inspector.

## Structural Guidance

- Use `NavigationSplitView` when the app is genuinely sidebar-content-detail or sidebar-detail in structure.
- Prefer `List(selection:)` or another honest selection container in the sidebar and content columns.
- Let sidebar selection drive the content column, and let content selection drive detail or inspector state.
- Keep the split-view selection model as the primary navigation truth instead of storing a second parallel panel-routing model.
- If a column needs deeper push-style navigation inside itself, embed a `NavigationStack` in that column rather than teaching the sidebar to mutate deep destinations directly.

## Sidebar Guidance

- A native sidebar usually behaves like a selection surface, not a grid of imperative buttons.
- Prefer rows that use `NavigationLink(value:)` or participate in `List(selection:)` so selection and navigation stay coordinated.
- Do not make sidebar cells directly rewrite deep detail state, inspector state, and unrelated scene mode all at once.
- If the sidebar chooses a category, collection, document, or top-level entity, make that selection the input to the next column rather than a hidden side effect.

## Content And Detail Guidance

- The content column should usually refine the current sidebar selection rather than act as an unrelated second root.
- The detail column should react to the current content selection or navigation path rather than carrying a separate hidden copy of that same state.
- When no meaningful selection exists yet, use an explicit placeholder such as “Select an item” rather than forcing fake detail state.

## Inspector Guidance

- Treat an inspector as a detail-adjacent surface owned by the current scene or detail workflow.
- Inspector visibility should usually be driven by scene-owned or detail-owned state, not by a broad global environment object.
- If inspector content depends on the current selection, let that selection feed the inspector directly instead of introducing another intermediate coordinator solely to mirror it.
- Use `InspectorCommands()` when the app wants the native inspector toggle command surface instead of inventing a parallel custom command.

## Native Command And Toolbar Guidance

- Keep the built-in sidebar toggle when it matches the app structure; do not remove it just to replace it with a custom duplicate.
- If the app needs custom commands around inspector presentation, prefer augmenting `InspectorCommands` rather than shadowing it with unrelated terminology.
- When the app truly needs programmatic column visibility changes, keep that state near the split-view scene root with `NavigationSplitViewVisibility`.

## Worked Examples

### Example: Sidebar Selection Drives Content Selection Space

Good shape:

- the sidebar is a `List(selection:)` of top-level entities
- the content column reads the current sidebar selection and presents the next-level list for that entity
- the content column owns its own selection for the next step

Why:

- this matches Apple’s documented three-column coordination model
- each column owns the selection that is native to that level instead of one global object pretending to own every level at once

### Example: Sidebar Cells Use `NavigationLink(value:)`

Good shape:

- rows in a selectable sidebar list use `NavigationLink(value:)`
- the list and navigation logic coordinate through the same selection value

Why:

- Apple documents that `NavigationLink(value:)` can coordinate with list selection in `NavigationSplitView`
- that keeps visual selection and navigation destination in sync without extra glue code

### Example: Content Selection Drives Detail And Inspector

Good shape:

- the content column owns the active item selection
- the detail pane reads that selection to show the main detail surface
- the inspector reads that same current selection and scene-owned inspector visibility state

Why:

- the detail and inspector are both downstream consequences of the active content selection
- introducing a second mirrored “current detail item” usually just creates drift and extra invalidation paths

### Example: Native Sidebar And Inspector Commands Stay Native

Good shape:

- the split-view scene keeps the native sidebar toggle behavior
- the scene opts into `InspectorCommands()` when it offers an inspector
- custom commands add domain behavior around the current selection without replacing the native command vocabulary

Why:

- Apple already provides built-in desktop command surfaces for these controls
- keeping those native surfaces intact makes the app easier to reason about and more consistent with platform expectations

### Example: Programmatic Column Visibility Stays At The Scene Root

Good shape:

- the scene root owns `NavigationSplitViewVisibility`
- commands or toolbars that need to change column visibility mutate that state through the scene owner

Why:

- column visibility is part of split-view scene structure, not leaf-view rendering detail
- storing it at the scene root keeps ownership aligned with the view actually using the binding

## Common Failure Shapes

- sidebar buttons that directly rewrite deep detail state and inspector state at the same time
- one global observable object that stores every sidebar, content, detail, and inspector selection together
- removing native sidebar or inspector controls only to re-add weaker custom versions
- using the detail column as a second root instead of a downstream consequence of earlier-column selection
- duplicating the current selection into a second “active item” property just for the inspector

## References

- [NavigationSplitView](https://developer.apple.com/documentation/swiftui/navigationsplitview)
- [NavigationSplitViewVisibility](https://developer.apple.com/documentation/swiftui/navigationsplitviewvisibility)
- [NavigationLink](https://developer.apple.com/documentation/swiftui/navigationlink)
- [List](https://developer.apple.com/documentation/swiftui/list)
- [ToolbarDefaultItemKind.sidebarToggle](https://developer.apple.com/documentation/swiftui/toolbardefaultitemkind/sidebartoggle)
- [InspectorCommands](https://developer.apple.com/documentation/swiftui/inspectorcommands)
- [View.navigationSplitViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewstyle(_:))
- [View.navigationSplitViewColumnWidth(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewcolumnwidth(_:))
- [View.navigationSplitViewColumnWidth(min:ideal:max:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewcolumnwidth(min:ideal:max:))
