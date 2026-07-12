# SwiftUI Component Audit Checklist

For every view, verify:

- It is independently understandable and previewable when reusable.
- Its public stored properties are values, narrow bindings, or action closures rather than collaborator objects.
- It owns presentation state at the narrowest honest boundary using `@State`, derived values, and local helpers.
- A local `@Observable` type, if present, is created and retained by the owning view with `@State`.
- It uses existing environment values/actions first; custom environment values/actions are reserved for dynamic or broadly shared hierarchy context.
- Preferences only publish descendant-derived information upward.
- Focused values and commands model active command context rather than broad shared mutable state.
- SwiftData flows directly through `modelContainer`, `modelContext`, `@Query`, model objects, and narrow bindings.
- Its initializer is synthesized unless explicit initialization has a real invariant or transformation.
- It contains no imperative router, coordinator, controller, or cache that duplicates SwiftUI ownership.
- Every feature service provides one direct capability or cohesive related group, has a named lifecycle owner, and reaches its real boundary without an umbrella-service or forwarding chain.
- A service is in environment only when independent descendants need direct invocation or observable state; reusable leaf views still expose values, bindings, and actions.
