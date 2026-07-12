---
name: swiftui-component-audit-workflow
description: Audit and repair SwiftUI code toward self-contained declarative components, local reactive state, framework-native data flow, and simple reusable view interfaces. Use when an existing SwiftUI feature has external ViewModels, injected collaborators, imperative coordination, duplicated state, environment dumping, or unclear component ownership.
---

# SwiftUI Component Audit Workflow

## Purpose

Audit or repair a SwiftUI feature without importing AppKit, UIKit, or generic imperative architecture into a declarative view tree. SwiftUI components stand on their own: they render from explicit values and framework state, own local presentation state, and express user intent through narrow actions.

## When To Use

- Use for a SwiftUI architecture review, component audit, repair, or refactor.
- Use when reusable views receive ViewModels, stores, services, managers, coordinators, or other collaborating objects.
- Use when state is duplicated, a router or coordinator shadows SwiftUI navigation, or an environment becomes a dependency dump.
- Use when a team needs concrete good/bad SwiftUI examples before implementing a feature.
- Hand SwiftData persistence decisions to `swiftdata-workflow`, app and scene ownership to `swiftui-app-architecture-workflow`, and execution to the Xcode build or testing workflows.

## Single-Path Workflow

1. Read the relevant Apple documentation through `explore-apple-swift-docs` before proposing a repair.
2. Inventory each view's stored properties, local state, environment reads, preferences, focus, commands, and outward actions.
3. Classify every dependency:
   - component input: value, narrow binding, or action closure
   - component-local state: `@State`, derived value, or locally owned `@Observable` state
   - hierarchy context: existing or custom environment value/action
   - upward layout or presentation fact: preference key
   - active command context: focus or focused value
   - direct persistence state: `ModelContainer`, `modelContext`, `@Query`, model object, or narrow binding
   - non-SwiftUI boundary: networking, import/export, migration, testing, or server sync
4. Report a finding for every reusable view that accepts an external ViewModel, store, coordinator, manager, service, or observable collaborator.
5. Repair from the narrowest honest mechanism outward:
   - replace collaborators with values, bindings, and actions
   - move local presentation state into the owning view
   - use an existing environment action before adding a custom action
   - add a custom environment value or action only for a dynamic or broadly reused hierarchy capability
   - use preferences only for descendant-to-ancestor publication
   - restore direct SwiftData integration when persistence is being mirrored
6. Remove explicit initializers that only duplicate the synthesized memberwise initializer.
7. Re-audit the changed component boundaries and hand off for build, preview, or tests.

## Inputs

- `repository`: target repository or feature path.
- `mode`: `audit` for findings only, or `repair` for implementation.
- `scope`: optional files, feature, scene, or component name.
- `platform_context`: optional iOS, iPadOS, macOS, or mixed context.

## Outputs

- component inventory and declared ownership boundary
- findings ordered by severity with the violated component rule
- a before/after state-flow description
- exact repair plan or completed edits
- documented SwiftUI behavior relied on
- validation and handoff path

## Guards and Stop Conditions

- Do not recommend external ViewModels as a SwiftUI component shape.
- Do not treat values, bindings, and action closures as dependency injection; they are a declarative component interface.
- Do not pass collaborating objects between reusable views.
- Do not replace a documented SwiftUI environment action with an application router or coordinator.
- Do not add a custom environment action when a local action is sufficient; do add one when a dynamic or broadly shared hierarchy capability honestly needs it.
- Do not use preference keys as a general state bus.
- Do not insert repositories, stores, DTO mirrors, service mirrors, or view-model caches between SwiftData and SwiftUI.
- Prefer memberwise initializers; an explicit initializer needs real behavior beyond stored-property assignment.
- Stop and surface a broader app, scene, persistence, or navigation ownership decision rather than hiding it in a local refactor.

## Fallbacks and Handoffs

- Recommend `swiftui-app-architecture-workflow` for app, scene, command, focus, environment, or navigation ownership decisions.
- Recommend `swiftdata-workflow` for persistence integration or migration decisions.
- Recommend `explore-apple-swift-docs` for primary documentation lookup.
- Recommend `xcode-build-run-workflow` for previews, build, run, project membership, or guarded mutations.
- Recommend `xcode-testing-workflow` for Swift Testing, XCTest, XCUITest, or test diagnosis.

## Customization

Use `references/customization-flow.md`. This workflow has no runtime-enforced knobs; keep audits grounded in the repository and Apple documentation.

## References

- `references/component-rules-and-examples.md`
- `references/audit-checklist.md`
- `references/customization-flow.md`
- Recommend `swiftui-app-architecture-workflow/references/snippets/apple-xcode-project-core.md` when the target repo needs durable Apple project policy.

### Script Inventory

- `scripts/customization_config.py`
