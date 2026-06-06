# Archiving, Persistence, And Migration

Use this reference when the request involves object archiving, secure coding,
restorable payloads, user defaults, files, `Codable`, Core Data, SwiftData, or
migration.

## Decision Rules

- Name the state first: preference, restoration hint, document content,
  workspace record, cache, local history, or domain model.
- Use user defaults for small user preferences, not complex document or
  workspace content.
- Use `Codable` and files for explicit app-owned records when the schema can
  evolve cleanly and the app controls the read/write path.
- Use `NSSecureCoding` or `NSKeyedArchiver` when an AppKit or Foundation API
  expects archived objects, when preserving Objective-C object graph semantics,
  or when interacting with existing archived data.
- Use Core Data or SwiftData when identity, relationships, queries, undo,
  migration, or persistent model coordination matter.
- Always name the migration boundary when persisted data may outlive the current
  app version.

## Secure Coding Boundary

- Prefer secure coding for archived object data.
- Keep archived classes narrow and intentional.
- Validate restored objects before trusting them as live model state.
- Keep archive failures human-readable: say which archive, class, or schema
  could not be read and what fallback is safe.

## Restoration Versus Persistence

- Restoration can point to durable state.
- Persistence stores durable state.
- A restoration archive should not become the only copy of user data unless the
  user-visible contract truly says the state is transient.
