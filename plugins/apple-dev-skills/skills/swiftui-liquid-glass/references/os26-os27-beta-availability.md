# OS 26 And OS 27 Beta Availability

The Xcode beta SwiftUI interface confirms that the core custom Liquid Glass surface remains the OS 26 baseline: `glassEffect`, `GlassEffectContainer`, `glassEffectID`, `glassEffectTransition`, `glassEffectUnion`, `Glass`, and glass button styles are not new OS 27-only APIs.

OS 27 beta adds toolbar composition controls that can affect system-provided glass presentation:

- `ToolbarItemVisibilityPriority` and `visibilityPriority(_:)` are available on iOS 27 and macOS 26.1 or later.
- iOS 27 adds `ToolbarOverflowMenu` and iOS-only toolbar placement options such as `bottomOrnament`.

Treat these as toolbar-layout and discoverability features, not reasons to wrap standard toolbar content in custom glass. Gate each new API independently, preserve the OS 26 toolbar shape, and visually validate normal, compact, overflow, and accessibility states on the beta destination. Beta API names and behavior can still change before release.
