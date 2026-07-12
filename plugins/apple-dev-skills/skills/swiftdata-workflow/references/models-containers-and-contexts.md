# Models, Containers, And Contexts

- Use `GEAWhateverModel` only for a SwiftData persistence representation and keep the declaration in `GEAWhateverModel.swift`.
- Use `GEAWhatever` for the corresponding runtime/domain value when one is needed. Do not create a duplicate domain representation automatically.
- Define relationships, delete behavior, uniqueness, defaults, and optionality deliberately from documented SwiftData behavior.
- Place `ModelContainer` ownership at the app or scene boundary that owns the persistent lifetime.
- Keep each `ModelContext` on its intended actor and make cross-context or background work explicit.
- Keep `GEAApp.swift` as the lifecycle-entry naming exception. Do not create `GEAAppService` as a runtime/domain wrapper; add a direct concrete service only for a real app capability.
