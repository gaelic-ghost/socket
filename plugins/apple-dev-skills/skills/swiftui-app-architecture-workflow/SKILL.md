---
name: swiftui-app-architecture-workflow
description: Guide SwiftUI app-structure decisions for Apple apps across `App`, scenes, commands, focus, environment, preferences, window and document coordination, and reusable view composition. Use when the user wants help deciding where ownership belongs in a SwiftUI app, which data-flow mechanism fits a responsibility, or how to correct wrapper-heavy and state-scattering SwiftUI shapes without drifting into generic styling or execution work.
---

# SwiftUI App Architecture Workflow

## Purpose

Provide a docs-first workflow for SwiftUI app-structure decisions in Apple apps. This skill owns ownership-boundary guidance, transport-choice guidance, focused-context guidance, and anti-pattern correction for SwiftUI app composition across scenes, commands, focus, environment, preferences, and reusable view structure.

It is not the Apple-docs router, not the accessibility workflow, and not the Xcode execution workflow.

## When To Use

- Use this skill when the user wants help structuring a SwiftUI app across `App`, `Scene`, `WindowGroup`, `Window`, `Settings`, or `DocumentGroup`.
- Use this skill when the user wants help deciding where app-level, scene-level, and view-level responsibilities belong.
- Use this skill when the user wants help choosing between explicit dependency injection, environment values, focused values, scene-focused values, preference keys, bindings, or local state.
- Use this skill when the user wants help with `FocusState`, `focusable`, focus scopes, focus sections, default focus, focused objects, or other focused-context design that changes ownership or data-flow choices.
- Use this skill when the user wants help with command ownership, command menus, command groups, focused command handling, or desktop-oriented SwiftUI command surfaces.
- Use this skill when the user wants help cleaning up giant root views, wrapper-heavy architecture, environment abuse, hidden control flow in modifiers, or state scattering in SwiftUI code.
- Use this skill when the user wants SwiftUI composition guidance that stays grounded in current Apple scene and lifecycle behavior instead of framework-agnostic UI theory.
- Recommend `explore-apple-swift-docs` when the user primarily needs Apple or Swift documentation lookup rather than architecture guidance.
- Recommend `xcode-build-run-workflow` when the work becomes build, run, preview, diagnostics, file-membership, or guarded mutation work in an existing Xcode-managed project.
- Recommend `xcode-testing-workflow` when the work becomes Swift Testing, XCTest, XCUITest, `.xctestplan`, or test diagnosis.
- Defer accessibility-specific implementation and review to the planned accessibility workflow instead of absorbing that surface here.

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
   - app responsibilities stuffed into a leaf view
   - scene responsibilities stuffed into a global environment object
   - environment used as a dependency dump
   - preference keys used as a general state bus
   - giant root views with unrelated lifecycle, command, and rendering concerns mixed together
   - wrapper-heavy layers added only to look architectural
   - control flow hidden in modifiers that obscure who owns the action
6. Return one recommendation path with:
   - the ownership boundary
   - the chosen transport
   - the documented behavior being relied on
   - the anti-pattern correction when relevant
   - one handoff when the work is really docs lookup, execution, or accessibility work

## Inputs

- `request`: optional free-text task description used to classify the SwiftUI architecture question.
- `scope`: optional explicit scope such as `app-scene-structure`, `commands-and-focus`, `environment`, `preferences`, or `composition`.
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
- Defer accessibility-specific work to the planned accessibility workflow once that surface exists.

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
