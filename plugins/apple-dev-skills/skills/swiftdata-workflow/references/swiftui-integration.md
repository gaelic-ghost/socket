# SwiftUI Integration

- Attach the container with SwiftUI's `modelContainer` integration.
- Read the environment `modelContext`, use `@Query` for live collections, and pass SwiftData model objects or narrow bindings through the view tree.
- Do not put a repository, store, service mirror, DTO mirror, or view-model cache between SwiftData and SwiftUI.
- A view may own local presentation state with `@State` and a view-local `@Observable` type when needed, but it must not mirror or cache SwiftData merely to avoid the framework's direct integration.
- Hand component extraction and view naming to `swiftui-app-architecture-workflow`.
