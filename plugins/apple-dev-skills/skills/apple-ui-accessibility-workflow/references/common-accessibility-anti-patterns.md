# Common Accessibility Anti-Patterns

## Accessibility identifiers treated as accessibility semantics

- `accessibilityIdentifier` helps automation and testing.
- It does not replace a user-facing label, value, hint, or role.

## Modifier spam without a semantic reason

- Repeating visible text as an explicit accessibility label can make announcements noisier without making them clearer.
- Add explicit modifiers only when they fix a real semantic problem.

## Decorative hiding that removes meaning

- Hiding content from accessibility is only safe when the meaning is truly decorative or already represented elsewhere.
- If the user loses information by hiding the view, the design still has an accessibility bug.

## Custom controls without the right action model

- A view that looks tappable or adjustable but does not expose a matching accessibility action or role is misleading.
- The accessible role should match the real interaction model.

## Claims of completion without runtime validation

- A code review can show likely correctness or likely bugs.
- It cannot honestly prove the live VoiceOver or focus experience without a runtime pass.
