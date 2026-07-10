---
name: appkit-app-architecture-workflow
description: Guide AppKit app-structure decisions for macOS apps across app delegates, status-item menu bar apps, responder-chain menus, windows, controllers, restoration, archiving, Observation, and mixed AppKit/SwiftUI composition. Use when the user wants help deciding where AppKit responsibilities belong or how to avoid steering a macOS app into SwiftUI-only structure when AppKit owns the behavior.
---

# AppKit App Architecture Workflow

## Purpose

Provide a docs-first workflow for AppKit app-structure decisions in macOS apps.
This skill owns ownership-boundary guidance for AppKit lifetimes, menu bar apps,
menus, responder-chain action routing, windows, controllers, restoration,
archiving, AppKit MVC, Observation interop, and mixed AppKit/SwiftUI composition.

It is not the Apple-docs router, not the SwiftUI architecture workflow, not the
accessibility workflow, and not the Xcode execution workflow.

For Xcode app source layout, keep UIKit/AppKit controller support view-adjacent:
`Sources/Views/Shared`, `Sources/Views/macOS`, and `Sources/Views/iOS` own view
surfaces, and controller support files use concatenated prefixed names such as `GEAWhateverViewController.swift`
beside their matching view. Do not collect ordinary app controller support in a
root `Controllers/` directory.

## When To Use

- Use this skill when the user wants help structuring an AppKit or mixed
  AppKit/SwiftUI macOS app.
- Use this skill when the question involves `NSApplication`,
  `NSApplicationDelegate`, app activation policy, app reopen behavior, menu bar
  apps, `NSStatusItem`, status menus, popovers, panels, or quit behavior.
- Use this skill when the question involves the main menu, contextual menus,
  toolbar actions, target/action, responder-chain action routing, or menu
  validation.
- Use this skill when deciding whether app-level, window-level, controller-level,
  document-level, model-level, or hosted SwiftUI state should own a
  responsibility.
- Use this skill for old-school AppKit restoration, including restoration
  identifiers, `NSWindowRestoration`, window-controller restoration, document
  reopening, and workspace reopening.
- Use this skill when deciding between `NSSecureCoding`, `NSKeyedArchiver`,
  `Codable`, user defaults, files, Core Data, SwiftData, or another persistence
  surface for AppKit-owned state.
- Use this skill when a mixed AppKit/SwiftUI app uses SwiftData and the agent
  must keep SwiftData directly driving SwiftUI-owned screens while AppKit keeps
  only the AppKit-owned lifetime, controller, restoration, or bridge boundary.
- Use this skill when using Swift Observation with AppKit controls,
  controllers, delegates, or hosted SwiftUI views.
- Use this skill when embedding SwiftUI in AppKit through `NSHostingView` or
  `NSHostingController`, or when exposing AppKit views to SwiftUI through
  representable bridges.
- Recommend `swiftui-app-architecture-workflow` when the actual owner is
  SwiftUI `App`, scenes, commands, focus, environment, preferences, or reusable
  view composition.
- Recommend `explore-apple-swift-docs` when the user primarily needs Apple or
  Swift documentation lookup rather than architecture guidance.
- Recommend `xcode-build-run-workflow` when the work becomes build, run,
  preview, diagnostics, file-membership, or guarded mutation work in an existing
  Xcode-managed project.
- Recommend `xcode-testing-workflow` when the work becomes Swift Testing,
  XCTest, XCUITest, `.xctestplan`, or test diagnosis.
- Recommend `apple-ui-accessibility-workflow` when the work is primarily about
  accessibility-specific implementation or review.

## When Not To Use

- Do not use this skill as the primary path for raw Apple-docs search or source
  selection.
- Do not use this skill as the primary path for SwiftUI-first scene,
  environment, focus, preference, or reusable view-composition decisions.
- Do not use this skill as a generic macOS UI style, animation, or component
  library workflow when the real issue is not AppKit app structure.
- Do not use this skill as the primary path for Xcode execution, signing,
  target-membership, sandbox, entitlement, or test mechanics.
- Do not absorb SwiftASB-specific runtime guidance; use the SwiftASB skills when
  the AppKit app is specifically integrating SwiftASB.

## Single-Path Workflow

1. Classify the request:
   - app lifecycle and app delegate
   - menu bar or status-item app
   - menus, toolbar actions, responder chain, and validation
   - windows, controllers, panels, and inspectors
   - restoration, documents, and workspaces
   - AppKit MVC, target/action, bindings, and delegates
   - archiving, persistence, and migration
   - Observation and AppKit
   - mixed AppKit/SwiftUI composition
2. Apply the Apple docs gate before recommending structure:
   - read the relevant AppKit, SwiftUI, Observation, or Foundation
     documentation first
   - state the documented behavior being relied on before giving architecture
     guidance
   - if Apple docs and the current code disagree, stop and surface that conflict
   - if no relevant Apple docs can be found, say that explicitly before
     proceeding
3. Choose the AppKit ownership boundary:
   - app delegate or app-level model
   - status-item or menu-bar controller
   - main-menu or responder-chain action target
   - document controller or document model
   - window controller
   - view controller
   - model object
   - hosted SwiftUI boundary
   - local view-only state
4. Choose the state and action transport:
   - direct initializer injection
   - target/action
   - delegate method
   - responder-chain action
   - menu validation
   - AppKit binding
   - notification or publisher only for real broadcast state
   - Observation-driven model update
   - explicit SwiftUI hosting input/output
   - persistence or restoration payload
5. Check the anti-patterns before finalizing guidance:
   - SwiftUI scene structure forced onto AppKit-owned behavior
   - repositories, stores, service layers, mirrored DTOs, view-model cache
     layers, or wrapper objects inserted between SwiftData and SwiftUI-owned
     screens
   - a root `Controllers/` directory used for ordinary view-controller support
     instead of `GEAWhateverViewController.swift` beside the matching view
   - app-wide runtime work hidden in a view controller
   - menu or status-item behavior hidden in a leaf view
   - responder-chain actions replaced by a broad command bus without a real need
   - restoration payloads used as durable domain storage
   - archives used without migration or secure-coding boundaries
   - Observation treated like automatic AppKit UI binding
   - AppKit and SwiftUI each owning the same state
6. Return one recommendation path with:
   - the request class
   - the chosen ownership boundary
   - the chosen state or action transport
   - the documented Apple behavior relied on
   - any anti-pattern correction
   - one handoff when the work is really docs lookup, SwiftUI architecture,
     execution, accessibility, or SwiftASB integration

## Inputs

- `request`: optional free-text task description used to classify the AppKit
  architecture question.
- `scope`: optional explicit scope such as `app-lifecycle`, `menu-bar`,
  `menus`, `windows`, `restoration`, `mvc`, `archiving`, `observation`, or
  `mixed-appkit-swiftui`.
- `repo_shape`: optional high-level repo context such as `xcode-app`,
  `document-app`, `menu-bar-app`, `multiwindow-app`, `swiftpm-macos`, or
  `unknown`.
- `swiftui_presence`: optional emphasis such as `none`, `hosted-in-appkit`,
  `appkit-embedded-in-swiftui`, or `mixed-ownership`.
- Defaults:
  - docs-first guidance always applies
  - AppKit is treated as a modern macOS framework, not as a legacy fallback
  - SwiftUI is recommended when SwiftUI owns the behavior more directly
  - explicit ownership is preferred over broad shared objects when both are
    viable and the narrower path is clearer

## Outputs

- `status`
  - `success`: the request belongs to this workflow and a structure
    recommendation is ready
  - `handoff`: the request belongs to another skill after AppKit-aware
    classification
  - `blocked`: the request lacks enough context to recommend a boundary honestly
- `path_type`
  - `primary`: the recommendation comes from a directly supported AppKit
    architecture path
  - `fallback`: the recommendation depends on limited request context because
    repo or app shape is unclear
- `output`
  - resolved request class
  - chosen ownership boundary
  - chosen state or action transport
  - documented Apple behavior relied on
  - anti-pattern findings when relevant
  - recommended skill when handing off
  - one concise next step

## Guards and Stop Conditions

- Do not present AppKit as legacy-only or SwiftUI as automatically preferred.
- Do not force AppKit-owned menu, status-item, window-restoration, document, or
  responder-chain behavior into SwiftUI scene structure unless the app is truly
  SwiftUI-owned.
- Do not let both AppKit and SwiftUI own the same mutable model state.
- When SwiftData backs a SwiftUI-hosted surface, do not place AppKit
  controllers, repositories, stores, service layers, mirrored state, or
  view-model cache layers between SwiftData and SwiftUI. AppKit may own the host
  lifetime or bridge, but SwiftUI should be driven directly by SwiftData through
  `modelContainer`, environment `modelContext`, `@Query`, model objects, and
  bindings.
- Do not recommend `NSKeyedArchiver`, `NSSecureCoding`, Core Data, SwiftData,
  user defaults, or plain files without naming what state is being persisted and
  who reads it next.
- Do not recommend `NotificationCenter`, Combine, or other broadcast mechanisms
  for ordinary parent-to-child ownership or local controller state.
- Do not hide controller lifetimes behind broad coordinators, managers, command
  buses, or wrappers unless a concrete ownership problem requires that surface.
- Do not silently absorb raw Apple-docs lookup, SwiftUI architecture,
  accessibility work, Xcode execution, or SwiftASB integration.
- Stop with `blocked` when the request is too vague to determine whether the
  issue is app-level, status-item-level, window-level, controller-level,
  document-level, model-level, or hosted-SwiftUI structure.

## Fallbacks and Handoffs

- Prefer explicit scope and repo shape when the user provides them.
- Fall back to request-text inference when repo shape and app shape are unclear.
- Recommend `explore-apple-swift-docs` when the real need is broader Apple or
  Swift docs lookup.
- Recommend `swiftui-app-architecture-workflow` when the real owner is SwiftUI
  app, scene, command, focus, environment, preference, or view-composition
  structure.
- Recommend `xcode-build-run-workflow` when the next honest step is build, run,
  preview, diagnostics, file-membership follow-through, signing, entitlements,
  sandboxing, or guarded mutation.
- Recommend `xcode-testing-workflow` when the next honest step is test execution
  or test diagnosis.
- Recommend `apple-ui-accessibility-workflow` when the next honest step is
  accessibility-specific implementation or review.
- Recommend SwiftASB skills when the AppKit question is specifically about
  adding, diagnosing, or explaining SwiftASB integration.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` exists to preserve the repo-wide
customization-file contract, but the first version of this skill defines no
runtime-enforced knobs.

Keep the first release focused on the decision model and the documented
boundary. If future iterations add a real deterministic need for runtime knobs,
document them explicitly before letting runtime behavior depend on them.

## References

### Workflow References

- `references/app-delegate-and-lifecycle.md`
- `references/menu-bar-status-item-and-activation.md`
- `references/menus-responder-chain-and-validation.md`
- `references/windows-controllers-panels-and-inspectors.md`
- `references/restoration-documents-and-workspaces.md`
- `references/appkit-mvc-target-action-and-bindings.md`
- `references/archiving-persistence-and-migration.md`
- `references/observation-and-appkit.md`
- `references/mixed-appkit-swiftui-composition.md`
- `references/architecture-decision-rules.md`
- `references/anti-patterns-and-corrections.md`
- `references/customization-flow.md`

### Support References

- Recommend `explore-apple-swift-docs` when the user needs direct Apple-docs
  lookup instead of AppKit architecture guidance.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user
  needs reusable repo policy rather than a one-off architecture recommendation.

### Script Inventory

- `scripts/customization_config.py`
