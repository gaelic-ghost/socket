# Architecture Decision Rules

## Choose The Ownership Boundary First

- If the responsibility belongs to the whole app, keep it at the app boundary.
- If it varies per window, per document, or per managed scene, keep it scene-local.
- If it only affects one subtree, keep it in that subtree.
- If it only affects one view, keep it local.
- If the behavior is native scene or window presentation, keep the source of truth in scene declarations and use the documented environment action to request the presentation change.

## Choose The Transport Second

- Use explicit initializer injection when the dependency chain is short and readable.
- Use `Binding` when a child needs a focused writable projection of parent-owned state.
- Use environment values for shared contextual scope, not for arbitrary service dumping.
- Use focused values or scene-focused values for command and active-scene context.
- Use preference keys for child-to-ancestor publication, not as a hidden state channel.
- Use native environment presentation actions for opening or dismissing windows and settings, rather than inventing a parallel router when the scene model already names the target.

## Prefer The Narrowest Honest Mechanism

- If explicit flow is still clear, use it before introducing a broader implicit channel.
- If the broader channel hides ownership, it is probably the wrong tool.
- If the mechanism makes it harder to explain who owns the data and who changes it next, step back and choose a simpler one.

## Split View Decision Rules

- If the UI is fundamentally sidebar-content-detail, prefer `NavigationSplitView` as the scene root instead of a hand-built `HStack` plus several manually synchronized panels.
- In a split view, let leading-column selection drive subsequent columns the way Apple documents, instead of letting sidebar buttons mutate deep detail state directly.
- Prefer `List(selection:)` or similarly selection-honest containers in sidebar and content columns before inventing custom row coordinators.
- Let detail and inspector surfaces react to current content selection instead of storing a second hidden navigation model just for those surfaces.
