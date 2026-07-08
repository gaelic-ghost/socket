---
name: swiftui-app-architecture-workflow
description: Guide SwiftUI app-structure decisions for Apple apps across `App`, scenes, commands, focus, environment, preferences, window and document coordination, and reusable view composition. Use when the user wants help deciding where ownership belongs in a SwiftUI app, which data-flow mechanism fits a responsibility, or how to correct wrapper-heavy and state-scattering SwiftUI shapes without drifting into generic styling or execution work.
---

# SwiftUI App Architecture Workflow

## SwiftData And SwiftUI Rule

When a task combines SwiftData with SwiftUI, keep SwiftData directly coupled to SwiftUI through Apple's data-driven path: `modelContainer`, environment `modelContext`, `@Query`, SwiftData model objects, and bindings. Do not add repositories, stores, service layers, DTO mirrors, view-model caches, wrapper objects, or other abstraction layers between SwiftData and SwiftUI. If this skill is not the right owner for SwiftData-backed SwiftUI work, hand off to `apple-dev-skills:swiftui-app-architecture-workflow` instead of inventing an intermediate data layer.

## Purpose

Provide a docs-first workflow for SwiftUI app-structure decisions in Apple apps. This skill owns ownership-boundary guidance, transport-choice guidance, focused-context guidance, and anti-pattern correction for SwiftUI app composition across scenes, commands, focus, environment, preferences, and reusable view structure.

It is not the Apple-docs router, not the accessibility workflow, and not the Xcode execution workflow.

## SwiftUI View File Rule

Each SwiftUI `View` component must live in its own Swift file named for that view, and that file must carry the view's own Xcode SwiftUI preview. Do not group multiple `View` component types in one file, even when the views are small, related, nested, or currently used only by one parent. Split them into separate files so Xcode previews remain discoverable, isolated, and reliable.

SwiftUI view models are always per-view, with no exceptions. If a SwiftUI view has a view model, that model belongs to exactly that `View` component and must live beside the matching view in the matching `<ViewFileName>+Model.swift` file. Do not share a SwiftUI view model across multiple views, view families, screens, flows, or view clusters, and do not place multiple SwiftUI view models in one shared model file.

Keep supporting code in explicit paired files instead of bundling extra view types together: use `<ViewFileName>+Model.swift` for that view's model, `<ViewFileName>+Modifier.swift` for view-specific modifiers, and other narrowly named support files when needed. A file may contain private helper values or small non-`View` helpers for that one component, but it must not contain another SwiftUI `View` component.

For Xcode app projects, use strict Apple-app MVVM source layout: `Sources/Views/Shared`, `Sources/Views/macOS`, and `Sources/Views/iOS` own UI, `Sources/Models` owns persistence and transfer shapes, and `Sources/Services/Consumed`, `Sources/Services/Internal`, and `Sources/Services/Provided` own app services by direction. App-wide `@Observable` state lives beside the app entry point in `<AppName>App+ViewModel.swift`, containing `@Observable final class <AppName>AppViewModel`. UIKit and AppKit view-controller support lives beside the matching view as `<ViewName>+Controller.swift`; do not introduce a root `Controllers/` directory.

## When To Use

- Use this skill when the user wants help structuring a SwiftUI app across `App`, `Scene`, `WindowGroup`, `Window`, `Settings`, or `DocumentGroup`.
- Use this skill when the user wants help deciding where app-level, scene-level, and view-level responsibilities belong.
- Use this skill when the user wants help choosing between explicit dependency injection, environment values, focused values, scene-focused values, preference keys, bindings, or local state.
- Use this skill when a SwiftUI app uses SwiftData and the agent needs to keep SwiftData directly driving SwiftUI through Apple's data-driven UI integration instead of adding repositories, stores, mirrored state, or view-model cache layers.
- Use this skill when the user wants help with `FocusState`, `focusable`, focus scopes, focus sections, default focus, focused objects, or other focused-context design that changes ownership or data-flow choices.
- Use this skill when the user wants help with command ownership, command menus, command groups, focused command handling, or desktop-oriented SwiftUI command surfaces.
- Use this skill when the user wants help cleaning up giant root views, wrapper-heavy architecture, environment abuse, hidden control flow in modifiers, or state scattering in SwiftUI code.
- Use this skill when the user wants SwiftUI composition guidance that stays grounded in current Apple scene and lifecycle behavior instead of framework-agnostic UI theory.
- Recommend `explore-apple-swift-docs` when the user primarily needs Apple or Swift documentation lookup rather than architecture guidance.
- Recommend `xcode-build-run-workflow` when the work becomes build, run, preview, diagnostics, file-membership, or guarded mutation work in an existing Xcode-managed project.
- Recommend `xcode-testing-workflow` when the work becomes Swift Testing, XCTest, XCUITest, `.xctestplan`, or test diagnosis.
- Recommend `apple-ui-accessibility-workflow` when the work is primarily about accessibility-specific implementation or review instead of absorbing that surface here.

## When Not To Use

- Do not use this skill as the primary path for raw Apple-docs search or source selection.
- Do not use this skill as the primary path for SwiftUI styling, animation, or general component-library advice when the real issue is not app structure.
- Do not use this skill as the primary path for execution-heavy validation of a proposed scene or command structure.
- Do not use this skill as a generic dumping ground for every SwiftUI question just because a `View` is involved.

## Single-Path Workflow

1. Classify the request:
   - app and scene structure
   - commands
   - focus and focused context
   - environment and dependency flow
   - upward data flow and preferences
   - view-composition cleanup
2. Apply the Apple docs gate before recommending structure:
   - read the relevant SwiftUI documentation first
   - state the documented behavior being relied on before giving architecture guidance
   - if Apple docs and the current code disagree, stop and surface that conflict
   - if no relevant Apple docs can be found, say that explicitly before proceeding
3. Choose the ownership boundary:
   - app-level
   - scene-level
   - focused-scene-level
   - view-tree-level
   - local view
4. Choose the transport that fits the responsibility:
   - SwiftData's direct SwiftUI path: `modelContainer` at the app or scene boundary, environment `modelContext`, `@Query`, SwiftData model objects, and narrow bindings
   - explicit initializer injection
   - `Binding`
   - environment value
   - `FocusState`
   - focused value
   - focused object
   - focused scene value
   - focused scene object
   - preference key
   - local state only
5. Check the anti-patterns before finalizing guidance:
   - repositories, stores, service layers, mirrored DTOs, view-model cache layers, or wrapper objects inserted between SwiftData and SwiftUI
   - app responsibilities stuffed into a leaf view
   - scene responsibilities stuffed into a global environment object
   - environment used as a dependency dump
   - preference keys used as a general state bus
   - giant root views with unrelated lifecycle, command, and rendering concerns mixed together
   - wrapper-heavy layers added only to look architectural
   - control flow hidden in modifiers that obscure who owns the action
   - multiple SwiftUI `View` component types grouped into one file, especially when that prevents one file-local Xcode preview per component
   - one SwiftUI view model shared across a view cluster or stored outside the matching `<ViewFileName>+Model.swift` file
   - a root `Controllers/` directory used for UIKit or AppKit view-controller support instead of `<ViewName>+Controller.swift` beside the matching view
   - app-wide state hidden in a service, leaf view, or shared environment object instead of an app-entry `<AppName>App+ViewModel.swift`
6. Return one recommendation path with:
   - the ownership boundary
   - the chosen transport
   - the documented behavior being relied on
   - the anti-pattern correction when relevant
   - one handoff when the work is really docs lookup, execution, or accessibility work

## Inputs

- `request`: optional free-text task description used to classify the SwiftUI architecture question.
- `scope`: optional explicit scope such as `app-scene-structure`, `commands`, `focus`, `environment`, `preferences`, or `composition`.
- `platform_context`: optional platform emphasis such as `macos`, `ios`, `ipados`, or `mixed-apple`.
- `repo_shape`: optional high-level repo context such as `xcode-app`, `document-app`, `multiwindow-app`, or `unknown`.
- Defaults:
  - docs-first guidance always applies
  - desktop-oriented SwiftUI concerns stay in scope when they materially affect scene or command ownership
  - explicit injection is preferred over broader implicit channels when both are viable and the narrower path is clearer

## Outputs

- `status`
  - `success`: the request belongs to this workflow and a structure recommendation is ready
  - `handoff`: the request belongs to another skill after SwiftUI-aware classification
  - `blocked`: the request lacks enough context to recommend a boundary honestly
- `path_type`
  - `primary`: the recommendation comes from a directly supported architecture path
  - `fallback`: the recommendation depends on limited request context because repo or platform shape is unclear
- `output`
  - resolved request class
  - chosen ownership boundary
  - chosen transport
  - documented SwiftUI behavior relied on
  - anti-pattern findings when relevant
  - recommended skill when handing off
  - one concise next step

## Guards and Stop Conditions

- Do not recommend environment values as a default substitute for explicit dependency flow.
- When SwiftData backs a SwiftUI surface, do not recommend any data-access abstraction between SwiftData and SwiftUI. SwiftData should directly drive SwiftUI through `modelContainer`, environment `modelContext`, `@Query`, model objects, and bindings; separate boundaries are only for non-SwiftUI concerns such as import/export, networking, migration tooling, tests, or server sync.
- Do not recommend preference keys for ordinary downward or lateral data flow.
- Do not collapse commands, focus, and scene ownership into a single shared mutable object just because it is easy to wire.
- Do not present a giant root view or extra wrapper layer as architectural improvement unless it clearly removes a real ownership problem.
- Do not silently absorb accessibility-specific work, raw Apple-docs lookup, or Xcode execution work.
- Stop with `blocked` when the request is too vague to determine whether the issue is app-level, scene-level, or local-view structure.

## Fallbacks and Handoffs

- Prefer explicit scope and platform context when the user provides them.
- Fall back to request-text inference when repo shape and platform shape are unclear.
- Recommend `explore-apple-swift-docs` when the real need is broader Apple or Swift docs lookup.
- Recommend `xcode-build-run-workflow` when the next honest step is build, run, preview, diagnostics, file-membership follow-through, or guarded mutation.
- Recommend `xcode-testing-workflow` when the next honest step is test execution or test diagnosis.
- Recommend `apple-ui-accessibility-workflow` when the next honest step is accessibility-specific implementation or review.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` exists to preserve the repo-wide customization-file contract, but the first version of this skill defines no runtime-enforced knobs.

Keep the first release focused on the decision model and the documented boundary. If future iterations add a real deterministic need for runtime knobs, document them explicitly before letting runtime behavior depend on them.

## References

### Workflow References

- `references/app-and-scene-structure.md`
- `references/navigation-splitview-sidebar-and-inspector.md`
- `references/commands-and-focus.md`
- `references/focus-and-focused-context.md`
- `references/environment-and-preferences.md`
- `references/architecture-decision-rules.md`
- `references/anti-patterns-and-corrections.md`
- `references/customization-flow.md`

### Support References

- Recommend `explore-apple-swift-docs` when the user needs direct Apple-docs lookup instead of SwiftUI architecture guidance.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable repo policy rather than a one-off architecture recommendation.

### Script Inventory

- `scripts/customization_config.py`
