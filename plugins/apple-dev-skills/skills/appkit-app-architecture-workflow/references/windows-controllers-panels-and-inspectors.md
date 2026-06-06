# Windows, Controllers, Panels, And Inspectors

Use this reference when the request involves `NSWindow`, `NSWindowController`,
`NSViewController`, panels, inspectors, sidebars, sheets, tabbed windows, or
multiwindow ownership.

## Decision Rules

- Let `NSWindowController` own one window's lifetime, restoration identity,
  toolbar, window-level commands, and root view-controller wiring.
- Let `NSViewController` own one view hierarchy, view lifecycle, selection UI,
  and local control wiring.
- Put durable domain state in model objects, documents, or workspace objects,
  not in `NSView` subclasses.
- Use panels and inspectors for secondary surfaces that inspect or adjust a
  selected model; do not let them become hidden owners of the primary document or
  workspace.
- Keep sheets tied to the window whose operation they confirm, block, or edit.

## Common Shapes

- **Document window:** document owns file-backed state; window controller owns
  window chrome and controller graph; view controllers render and edit document
  state.
- **Workspace window:** workspace model owns reopenable project state; window
  controller owns one workspace window; view controllers own panes.
- **Inspector panel:** inspector controller observes current selection and sends
  explicit edits back to the selected model owner.
- **Utility panel:** app-level or window-level controller owns the panel,
  depending on whether the panel applies globally or to the active window.

## Stop Conditions

- Stop if a view controller starts owning app-wide services, global menu state,
  persistence migrations, and selected model state at the same time.
- Stop if a panel writes to a model without a clear selected owner or undo path.

