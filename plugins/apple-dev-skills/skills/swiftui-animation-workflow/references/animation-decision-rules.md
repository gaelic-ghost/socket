# Animation Decision Rules

Use this reference when choosing or repairing the SwiftUI animation primitive.

## Primitive Choice

- Use `withAnimation` when one user action should animate all dependent view changes inside one transaction.
- Use `animation(_:value:)` when one view subtree should animate only when a specific value changes.
- Use binding animation when the control binding is the intended animation boundary.
- Use `transaction` to override, disable, or inspect animation behavior in a subtree.
- Use `transition` when a view enters or leaves the hierarchy.
- Use `contentTransition` when the view remains stable but its displayed content changes.
- Use `matchedGeometryEffect` when continuity between two views depends on shared identity and geometry.
- Use navigation transitions when the motion belongs to navigation and Apple documents support for the target platform.
- Use `PhaseAnimator` for discrete stages such as idle, pressed, confirmed, and settled.
- Use `KeyframeAnimator` for coordinated properties with explicit timing tracks.
- Use `TimelineView`, `Canvas`, or lower-level rendering only when the visual state genuinely depends on time or custom drawing.

## State and Ownership Rules

- Make animation depend on explicit state.
- Keep the state trigger near the interaction or model state that actually changes.
- Avoid global animation state unless the animation is truly app-wide.
- Keep effects declarative when possible.
- Avoid timers for ordinary state transitions.
- Avoid doing expensive work in closures that SwiftUI can call every frame.

## Repair Heuristics

- If too much animates, narrow the boundary from `withAnimation` to `animation(_:value:)`, or isolate subtrees with `transaction`.
- If nothing animates, verify the value is animatable, the view identity is stable, and the state change happens in the intended animation transaction.
- If insertion/removal snaps, verify the transition is on the inserted or removed view and the hierarchy identity is stable.
- If a matched geometry effect jumps, verify shared namespace, stable IDs, source/destination identity, and layout timing.
- If keyframes stutter, remove expensive closure work and simplify tracks.
- If timeline-driven animation drains resources, check whether the effect can be state-driven or event-driven instead.

## Handoff Boundaries

- Use `swiftui-app-architecture-workflow` when unclear ownership or scattered state causes the animation bug.
- Use `sf-symbols-workflow` when the behavior depends on symbol availability, rendering, variable value, or symbol-specific effects.
- Use future Core Animation guidance when a layer-backed host view, presentation layer, or explicit `CAAnimation` is the real surface.
- Use `xcode-build-run-workflow` for previews, builds, simulator checks, screenshots, and project integrity.
