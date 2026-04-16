# SwiftUI App Architecture Workflow Plan

Date: 2026-04-16

## Purpose

Record the chosen direction for Milestone 40 so `swiftui-app-architecture-workflow` lands as a focused SwiftUI app-structure workflow instead of dissolving into generic component advice, a second Apple-docs router, or a shadow Xcode execution surface.

## Decision

The first version of `swiftui-app-architecture-workflow` should be a docs-first architecture and decision-making specialist.

It should help with:

- top-level SwiftUI app and scene structure
- choosing the right ownership boundary for app, scene, and view responsibilities
- choosing the right data-flow mechanism for a given SwiftUI responsibility
- focus and focused-context design across focus state, focusable surfaces, focused values, focused objects, and command coordination
- anti-pattern review and correction for agent-generated SwiftUI shapes

It should not become the primary owner of:

- broad Apple documentation source selection
- accessibility implementation or review
- build, run, test, or project-integrity execution work
- generic styling, animation, or component-library advice

Those concerns should stay with the existing docs-routing, execution, and future accessibility skills.

## Scope Boundary

### In Scope

- SwiftUI app entry and scene composition through `App` and `Scene`
- scene types and scene-specific responsibilities such as `WindowGroup`, `Window`, `Settings`, and `DocumentGroup`
- scene identity, multiwindow ownership, and per-window state expectations
- command menus, command groups, command placement, and command ownership
- focus state, focus scopes, focus sections, focusable interactions, default focus, and focus-driven navigation boundaries
- focused values and scene-focused values as command and context bridges
- focused objects and scene-focused objects when reference-typed focused context is genuinely the right tool
- environment propagation and custom environment values when shared contextual scope is truly justified
- preference keys as an upward data-flow tool when a child view must publish layout or state-derived information to an ancestor
- reusable SwiftUI composition patterns that keep control flow local and readable
- review and correction of common wrapper-heavy, environment-heavy, state-scattering SwiftUI codegen output

### Out Of Scope

- replacing `explore-apple-swift-docs` as the Apple-docs routing surface
- replacing `xcode-build-run-workflow` or `xcode-testing-workflow` for execution or mutation work
- replacing a future Apple accessibility workflow for accessibility-specific implementation and review
- absorbing generic visual-design or component-library guidance that is not specifically about SwiftUI app structure
- pretending to be a runtime validator for scene behavior without handing off to execution workflows

## Documentation Sources

The first version should anchor itself in the SwiftUI APIs that define the actual ownership and behavior boundaries:

- [App](https://developer.apple.com/documentation/swiftui/app)
- [Scene](https://developer.apple.com/documentation/swiftui/scene)
- [Scenes](https://developer.apple.com/documentation/swiftui/scenes)
- [WindowGroup](https://developer.apple.com/documentation/swiftui/windowgroup)
- [Settings](https://developer.apple.com/documentation/swiftui/settings)
- [DocumentGroup](https://developer.apple.com/documentation/swiftui/documentgroup)
- [Scene.environment(_:_:)](https://developer.apple.com/documentation/swiftui/scene/environment(_:_:))
- [CommandGroup](https://developer.apple.com/documentation/swiftui/commandgroup)
- [FocusState](https://developer.apple.com/documentation/swiftui/focusstate)
- [FocusedValues](https://developer.apple.com/documentation/swiftui/focusedvalues)
- [FocusedObject](https://developer.apple.com/documentation/swiftui/focusedobject)
- [FocusInteractions](https://developer.apple.com/documentation/swiftui/focusinteractions)
- [EnvironmentValues.openWindow](https://developer.apple.com/documentation/swiftui/environmentvalues/openwindow)
- [OpenSettingsAction](https://developer.apple.com/documentation/swiftui/opensettingsaction)
- [View.focusedSceneValue(_:_:)](https://developer.apple.com/documentation/swiftui/view/focusedscenevalue(_:_:))
- [Focus](https://developer.apple.com/documentation/swiftui/focus)

The skill should make a few documented behaviors explicit and foundational:

- a `Scene` is the lifecycle boundary that the system manages
- `WindowGroup` creates independent state for each window instance
- `Scene.environment(_:_:)` only affects that scene and its descendant views
- `focusedSceneValue` is the documented path for values that commands need regardless of where focus sits within the active scene
- `FocusState` is the documented state wrapper for reading and driving focus placement within a scene
- `focusedObject` versus `focusedSceneObject` is a real ownership distinction, not a stylistic alias

The skill should not silently rely on memory or generalized SwiftUI lore when Apple documentation answers the question directly.

## Core Questions The Skill Should Answer

- Where should this responsibility live: app, scene, view tree, focused scene, or local view?
- Should this dependency be passed explicitly, placed in the environment, exposed through a focused value, or expressed through a preference?
- When is a command truly app-level or scene-level, and when should a leaf view not own it?
- When should a view remain one file, and when should a small compositional split happen without inventing wrapper layers?
- When does a multiwindow design need scene-local ownership instead of shared mutable state?

## Workflow Shape

The first version should stay single-path and narrow:

1. Classify the request:
   - app and scene structure
   - commands
   - focus and focused context
   - environment and dependency flow
   - upward data flow and preferences
   - view-composition cleanup
2. Apply the Apple docs gate:
   - gather the relevant SwiftUI references first
   - state the documented behavior being relied on before recommending structure
3. Choose the ownership boundary:
   - app-level
   - scene-level
   - focused-scene-level
   - view-tree-level
   - local view
4. Choose the transport:
   - explicit initializer injection
   - binding
   - environment value
   - focused value
   - focused scene value
   - preference key
   - local state only
5. Check anti-patterns:
   - environment abuse
   - giant root views
   - wrapper-heavy controller layers
   - hidden control flow in modifiers
   - preferences used as a general state bus
   - leaf views owning app or scene commands
6. Return one recommendation path with one concrete boundary explanation and one handoff when the work is really docs lookup, execution, or accessibility work.

## Reference File Plan

The initial reference set should be small and explicit:

- `references/app-and-scene-structure.md`
  Covers app entry, scene types, scene lifecycle, multiwindow ownership, and scene-local state expectations.
- `references/navigation-splitview-sidebar-and-inspector.md`
  Covers native split-view composition, sidebar selection structure, content-detail-inspector flow, built-in sidebar and inspector commands, and when split-view visibility belongs at the scene root.
- `references/commands-and-focus.md`
  Covers command groups, command menus, command ownership, and the command-facing handoff to focused context.
- `references/focus-and-focused-context.md`
  Covers `FocusState`, focus scopes, focus sections, focusable interactions, focused values, focused objects, and scene-wide versus subtree-wide focused context.
- `references/environment-and-preferences.md`
  Covers the environment boundary, custom environment values, preference keys, and when neither is the right tool.
- `references/architecture-decision-rules.md`
  Provides concise decision rules for explicit injection versus environment versus focus versus preferences.
- `references/anti-patterns-and-corrections.md`
  Names the bad shapes directly and explains the correction path in repo language.

## Repo File Plan

The first implementation slice should add:

- `skills/swiftui-app-architecture-workflow/SKILL.md`
- `skills/swiftui-app-architecture-workflow/agents/openai.yaml`
- `skills/swiftui-app-architecture-workflow/references/app-and-scene-structure.md`
- `skills/swiftui-app-architecture-workflow/references/navigation-splitview-sidebar-and-inspector.md`
- `skills/swiftui-app-architecture-workflow/references/commands-and-focus.md`
- `skills/swiftui-app-architecture-workflow/references/focus-and-focused-context.md`
- `skills/swiftui-app-architecture-workflow/references/environment-and-preferences.md`
- `skills/swiftui-app-architecture-workflow/references/architecture-decision-rules.md`
- `skills/swiftui-app-architecture-workflow/references/anti-patterns-and-corrections.md`

The first slice should not add a runtime wrapper script yet.

## Why No Runtime Script Yet

Unlike the Xcode execution workflows, this milestone does not currently need deterministic local orchestration. The value is in the decision model, the boundary, and the anti-pattern guardrails. Adding a script too early would create maintenance surface without solving a real workflow problem yet.

## Adjacent Skill Boundaries

- `explore-apple-swift-docs`
  Owns Apple-docs source selection and direct documentation lookup.
- `xcode-build-run-workflow`
  Owns build, run, preview, diagnostics, file-membership, and guarded mutation work in existing Xcode-managed projects.
- `xcode-testing-workflow`
  Owns test-focused execution and diagnosis.
- planned accessibility workflow
  Should own accessibility-specific implementation and review rather than having this skill grow sideways into that surface.

## Quality Expectations

The skill should improve:

- ownership clarity
- top-level app and scene readability
- command placement clarity
- dependency-flow honesty
- scene-aware desktop behavior
- resistance to state sprawl and wrapper-heavy codegen

The skill should avoid rewarding:

- environment as a dumping ground
- extra controllers or coordinators added only to look architectural
- preference keys used as a hidden state bus
- giant root views that mix app lifecycle, command wiring, and leaf rendering detail

## First Implementation Slice

The first implementation slice should:

- create the new `swiftui-app-architecture-workflow` skill surface
- lock the skill boundary in `SKILL.md`
- add the initial reference set listed above
- teach the ownership-boundary and transport-decision model
- teach the anti-patterns directly instead of only describing ideal patterns
- keep docs routing and execution handoffs explicit

## Deferred Follow-Up

These can wait until the first version proves useful:

- a runtime wrapper or classification helper
- deeper coverage for `Window`, `MenuBarExtra`, utility windows, and newer desktop-specific scene types
- dedicated examples for document-based apps beyond the first boundary guidance
- tighter integration with the future accessibility workflow
- inventory and validator updates once the skill is ready to be treated as part of the active shipped surface

## Concerns And Risks

- The biggest risk is duplicating `explore-apple-swift-docs` with a weaker docs router.
- The second risk is turning this into generic SwiftUI advice instead of app-structure guidance.
- The third risk is letting the skill drift into build or mutation work that belongs with the Xcode execution skills.
- The fourth risk is failing to name anti-patterns directly, which would make the skill too abstract to be useful against agent-generated SwiftUI code.

## Recommended Roadmap Interpretation

Milestone 40 should now be read as:

- phase one: docs-first SwiftUI app-architecture and decision-model workflow
- later follow-up: deeper desktop scene coverage, stronger worked examples, and possible runtime support if a real deterministic need appears
