---
name: app-intents-workflow
description: Design, implement, validate, and troubleshoot App Intents, App Entities, App Shortcuts, and system-surface integrations. Use when exposing a focused app action or content to Siri, Spotlight, Shortcuts, widgets, controls, Live Activities, or hardware interactions.
---

# App Intents Workflow

## Purpose

Expose the smallest useful action and content surface outside an app without turning system integration into a second app architecture. Apple documents App Intents as the bridge that makes app actions and data discoverable in system experiences; select real user-recognizable verbs and entities before adding an intent type.

## When To Use

- Use for `AppIntent`, `AppEntity`, `AppEnum`, `AppShortcutsProvider`, entity queries, result snippets, Spotlight indexing, widgets, controls, Live Activities, Siri, and Action button or Apple Pencil actions.
- Use when an app action needs an explicit deep-link or scene-opening handoff after system invocation.
- Hand off Xcode target, extension, build, simulator, and runtime inspection work to `xcode-build-run-workflow`; hand test plans and UI automation to `xcode-testing-workflow`.

## Single-Path Workflow

1. Apply the Apple docs gate through `explore-apple-swift-docs`. Confirm the framework, platform availability, and target system surface before changing code.
2. Define one user-recognizable verb and the minimum data it needs. Prefer an existing app domain type; do not invent a parallel intent-only repository, store, or DTO layer.
3. Classify the surface: direct action, parameterized action, entity lookup, App Shortcut, Spotlight result, widget/control action, Live Activity action, or hardware interaction.
4. Read `references/intent-entity-and-shortcut-shapes.md` for intent, entity, query, shortcut, and result patterns. Read `references/system-surfaces-and-validation.md` for indexing, extension boundaries, privacy, and validation.
5. Implement the narrow intent and make `perform()` call the existing domain action or explicit app handoff. Keep parameter confirmation, failures, and result output descriptive and user-facing.
6. Add `AppEntity` only when people need to select, search, or inspect app-owned content. Give entity display representations stable identifiers and use the appropriate query shape; do not expose private, transient, or unverifiable data.
7. Add App Shortcuts only for actions people plausibly invoke repeatedly. Use short, natural phrases and real parameter defaults rather than advertising every internal operation.
8. For widgets, controls, Live Activities, and Spotlight, validate the owning extension and system-surface contract rather than assuming the main app target alone is enough.
9. Validate discovery, parameter resolution, cancellation/failure behavior, app handoff, accessibility, and privacy on the intended platform. Record system-surface limitations separately from app behavior.

## Inputs

- app and target shape, deployment target, and intended system surface
- user-recognizable action or content entity
- authentication, confirmation, privacy, and app-handoff requirements
- existing domain operation, content identity, and validation evidence

## Outputs

- selected intent/entity/shortcut shape and the documented Apple behavior it relies on
- target or extension requirements and the narrowest app-handoff contract
- privacy and destructive-action boundary
- validation evidence for the actual system surface and any remaining limitation

## Guards and Stop Conditions

- Do not expose every app command just because the framework can describe it.
- Do not put network, persistence, or feature business logic into `perform()` when an existing domain operation owns it.
- Do not claim Siri, Spotlight, widget, control, or hardware availability without checking the current Apple documentation and deployment target.
- Do not use App Intents to bypass app authentication, confirmation, privacy policy, or destructive-action safeguards.
- Stop when the requested surface needs an unsupported entitlement, extension, capability, or system behavior that Apple documentation does not establish.

## Fallbacks and Handoffs

- Recommend `swiftui-app-architecture-workflow` for scene and deep-link ownership.
- Recommend `apple-ui-accessibility-workflow` for accessible labels, snippets, and alternate interaction verification.
- Recommend `xcode-build-run-workflow` for target setup, extensions, build, simulator, logs, and runtime execution.
- Recommend `xcode-testing-workflow` for deterministic testing and UI automation.
- Recommend `apple-developer-provisioning-workflow` only when documented capability or identifier provisioning becomes the actual blocker.

## Customization

Use `references/customization-flow.md`. The first version exposes no runtime-enforced knobs; it preserves the shared customization contract without allowing a configuration to bypass documentation, privacy, or validation requirements.

## References

- `references/intent-entity-and-shortcut-shapes.md`
- `references/system-surfaces-and-validation.md`
- `references/customization-flow.md`
- Recommend `references/snippets/apple-xcode-project-core.md` when the app needs reusable Xcode-project policy alongside App Intents integration.
- [App Intents](https://developer.apple.com/documentation/appintents) documents intents, entities, shortcuts, and system-surface integration.
- [Adopting App Intents to support system experiences](https://developer.apple.com/documentation/appintents/adopting-app-intents-to-support-system-experiences) documents discovery across system experiences.
