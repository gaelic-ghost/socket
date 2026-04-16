# Focus And Focused Context

## Why This Gets Its Own Reference

- Focus in SwiftUI is not just one modifier.
- It spans state, eligibility, movement, default placement, value publication, object publication, and scene-wide versus subtree-wide visibility.
- That makes it broad enough to deserve its own decision surface rather than being treated as a footnote under commands.

## Core Focus Layers

### Focus State

- Use `FocusState` when a view or scene needs to observe or drive focus placement.
- Prefer enum-backed or otherwise explicit focus identifiers when multiple focusable surfaces must be disambiguated cleanly.
- Avoid Boolean focus state when the real model has more than one meaningful focus target.

### Focus Eligibility And Interaction

- Use `focusable` when a view truly needs to participate in focus.
- Use `focusable(_:interactions:)` and `FocusInteractions` when the kind of focus-driven interaction matters.
- Do not mark large containers focusable unless they are genuinely part of the focus model.

### Focus Scope And Movement

- Use `focusScope` and `prefersDefaultFocus` when default-focus behavior needs an explicit boundary.
- Use `focusSection` when focus movement between regions needs spatial or sequential guidance.
- Treat focus-region design as part of app structure, not as a visual-only tweak.

## Focused Context Publication

### Value Types

- Use `focusedValue` when a focused subtree should publish value-typed context tied to the currently focused view hierarchy.
- Use `focusedSceneValue` when the context should stay visible anywhere within the active scene, regardless of where focus currently sits.
- Use `FocusedValue` or related focused-value readers in commands or toolbars that need the active focused context.

### Reference Types

- Use `focusedObject` when a focused subtree should publish a reference-typed observable object tied to the currently focused view hierarchy.
- Use `focusedSceneObject` when the reference-typed context should stay visible throughout the active scene.
- Do not reach for focused objects automatically just because a type is observable. First ask whether a focused value or explicit injection would be narrower and clearer.

## Ownership Rules

- Focus state belongs where focus movement is actually being driven.
- Focused context belongs at the narrowest level that still matches the behavior the command or UI surface needs.
- If a command should keep working anywhere in the active scene, prefer scene-wide focused context over subtree-only focused context.
- If the state is not really about active focus, do not force it through the focus system.

## Worked Examples

### Example: Enum-Backed `FocusState` For A Form

Good shape:

- a single enum-backed `FocusState` names the meaningful focus targets
- views bind against explicit enum cases instead of several unrelated Boolean flags

Why:

- once there are multiple meaningful focus destinations, enum-backed focus state makes ownership and transitions clearer
- this matches Apple’s documented guidance for richer focus-state modeling better than a pile of separate Booleans

### Example: `focusedValue` Versus `focusedSceneValue`

Use `focusedValue` when:

- the command or toolbar action should change with the currently focused subtree

Use `focusedSceneValue` when:

- the command should still work anywhere inside the active scene, even if focus shifts to another part of that scene

Why:

- subtree-scoped and scene-scoped focus publication are different ownership statements
- scene-wide publication is broader and should only be chosen when the behavior really needs that breadth

### Example: `focusedObject` Is Not Global State

Good shape:

- a focused object is published because the active focused subtree really owns the current reference-typed context

Bad shape:

- one large observable object is published as a focused object only because it is easy to reach from commands

Correction:

- first ask whether the command needs a narrow focused value, explicit injection, or scene-wide focused publication instead
- use focused objects when the object is genuinely the active focused context, not when it is just the easiest shared container

## Common Failure Shapes

- Boolean `FocusState` used where multiple focus targets actually exist
- scene-wide focused context used when subtree-only context would be more honest
- focused object used as a disguised global state channel
- focusable wrappers applied broadly just to make focus APIs easier to reach
- focus rules hidden in a modifier tangle that makes ownership impossible to explain

## References

- [Focus](https://developer.apple.com/documentation/swiftui/focus)
- [FocusState](https://developer.apple.com/documentation/swiftui/focusstate)
- [FocusedValues](https://developer.apple.com/documentation/swiftui/focusedvalues)
- [FocusedObject](https://developer.apple.com/documentation/swiftui/focusedobject)
- [FocusInteractions](https://developer.apple.com/documentation/swiftui/focusinteractions)
- [View.focusedValue(_:_:)](https://developer.apple.com/documentation/swiftui/view/focusedvalue(_:_:))
- [View.focusedSceneValue(_:_:)](https://developer.apple.com/documentation/swiftui/view/focusedscenevalue(_:_:))
- [View.focusedObject(_:)](https://developer.apple.com/documentation/swiftui/view/focusedobject(_:))
- [View.focusedSceneObject(_:)](https://developer.apple.com/documentation/swiftui/view/focusedsceneobject(_:))
- [View.focusable(_:interactions:)](https://developer.apple.com/documentation/swiftui/view/focusable(_:interactions:))
- [View.focusScope(_:)](https://developer.apple.com/documentation/swiftui/view/focusscope(_:))
- [View.focusSection()](https://developer.apple.com/documentation/swiftui/view/focussection())
