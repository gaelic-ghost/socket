# Architecture Decision Rules

## Choose The Ownership Boundary First

- If the responsibility belongs to the whole app, keep it at the app boundary.
- If it varies per window, per document, or per managed scene, keep it scene-local.
- If it only affects one subtree, keep it in that subtree.
- If it only affects one view, keep it local.
- If the behavior is native scene or window presentation, keep the source of truth in scene declarations and use the documented environment action to request the presentation change.

## Choose The Transport Second

- Use plain values, `Binding`, and action closures for a reusable component's explicit interface. This is declarative composition, not dependency injection.
- Use `Binding` when a child needs a focused writable projection of parent-owned state.
- Use existing environment values and actions for the framework behavior they already own. Add a custom environment value or action when many independent components share a genuinely app- or scene-wide capability, or when that capability must vary dynamically by hierarchy.
- Use a direct concrete feature service when a capability needs operations or observable state beyond local presentation state. Create it at the app or scene boundary that owns its lifecycle; install it in environment only when independent descendants need to invoke it or observe it directly.
- Keep a custom action local to the component that owns it, or to its enclosing component when only private child views use it.
- Use focused values or scene-focused values for command and active-scene context.
- Use preference keys for child-to-ancestor publication, not as a hidden state channel.
- Use native environment presentation actions for opening or dismissing windows and settings, rather than inventing a parallel router when the scene model already names the target.

## Prefer The Narrowest Honest Mechanism

- If explicit flow is still clear, use it before introducing a broader implicit channel.
- If the broader channel hides ownership, it is probably the wrong tool.
- If the mechanism makes it harder to explain who owns the data and who changes it next, step back and choose a simpler one.
- Do not pass a ViewModel, store, service, coordinator, manager, or other collaborating object from one reusable view into another. Make the component's values and intent explicit instead.
- Do not create an `AppService`, service facade, repository stack, or protocol-and-adapter chain merely to forward work between the UI and the real capability boundary. A surviving service must directly provide one capability or cohesive group of related operations.
- Prefer Swift's synthesized memberwise initializer. An explicit initializer must earn its existence by doing more than assigning stored properties.

## Split View Decision Rules

- If the UI is fundamentally sidebar-content-detail, prefer `NavigationSplitView` as the scene root instead of a hand-built `HStack` plus several manually synchronized panels.
- In a split view, let leading-column selection drive subsequent columns the way Apple documents, instead of letting sidebar buttons mutate deep detail state directly.
- Prefer `List(selection:)` or similarly selection-honest containers in sidebar and content columns before inventing custom row coordinators.
- Let detail and inspector surfaces react to current content selection instead of storing a second hidden navigation model just for those surfaces.
