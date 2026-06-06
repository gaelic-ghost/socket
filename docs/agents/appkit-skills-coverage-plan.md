# AppKit Skills Coverage Plan

## Purpose

Audit the current Socket skill coverage for AppKit compared with SwiftUI, then
propose a durable Apple Dev Skills expansion that keeps agents neutral between
SwiftUI, AppKit, and mixed AppKit/SwiftUI app shapes.

This report is a planning artifact. Durable decisions should move into
`ROADMAP.md`, `plugins/apple-dev-skills/AGENTS.md`, and the shipped skill files
when implementation starts.

## Current Coverage

### Strong SwiftUI Coverage

`plugins/apple-dev-skills/skills/swiftui-app-architecture-workflow/` provides a
dedicated SwiftUI app-architecture workflow. It covers `App`, `Scene`,
`WindowGroup`, `Window`, `Settings`, `DocumentGroup`, commands, focus, focused
values, environment, preference keys, ownership boundaries, and common
anti-patterns.

That means SwiftUI currently has a first-party Apple Dev Skills decision surface
for app structure and desktop-oriented SwiftUI concerns.

### General Apple Docs Coverage

`plugins/apple-dev-skills/skills/explore-apple-swift-docs/` is the canonical
docs-routing surface for Apple APIs, including AppKit, SwiftUI, Observation, and
Foundation-on-Apple.

This gives AppKit work a required Apple-docs gate, but it does not itself teach
AppKit app ownership, menu-bar app structure, restoration, controller lifetimes,
or mixed AppKit/SwiftUI decisions.

### SwiftASB-Specific AppKit Coverage

`plugins/swiftasb-skills/skills/build-appkit-app/` provides useful AppKit
guidance, but only for SwiftASB integrations. It names `NSApplication`,
`NSApplicationDelegate`, `NSWindowController`, `NSViewController`, `NSWindow`,
menu and toolbar actions, panels, document windows, and main-actor UI updates.

This is valuable evidence for the desired AppKit shape, but it should not be the
general AppKit architecture owner because it is intentionally scoped to
SwiftASB-backed features.

## Gap

Socket currently lacks the AppKit equivalent of
`swiftui-app-architecture-workflow`.

The practical effect is that an agent working on a macOS app can be steered
toward SwiftUI app-architecture guidance even when the real problem belongs to
AppKit's app delegate, responder chain, menu validation, status item, window
controller, document controller, restoration, or archiving model.

That does not mean the repository is anti-AppKit. It means AppKit has a docs gate
and one product-specific integration skill, while SwiftUI has a broad
architecture decision skill with supporting references.

## Recommended Skill Shape

Add `plugins/apple-dev-skills/skills/appkit-app-architecture-workflow/` as a
general Apple Dev Skills workflow.

This should be a durable building-block change. Its job should be to help agents
choose and explain AppKit ownership shapes before implementation, not to replace
the Xcode build/test skills or the Apple docs router.

### Core Scope

- App lifecycle and app delegate ownership.
- Menu bar apps, `NSStatusItem`, status-item menus, popovers, panels, activation
  policy, and quit behavior.
- Main menu, contextual menu, toolbar, responder-chain action routing, and menu
  validation.
- Window ownership through `NSWindow`, `NSWindowController`, `NSViewController`,
  panels, inspectors, and tabbed or multiwindow app shapes.
- Old-school restoration through `NSWindowRestoration`, restoration identifiers,
  `NSApplicationDelegate`, `NSWindowController`, and document or workspace
  reopening.
- Document-style and workspace-style ownership without forcing SwiftUI
  `DocumentGroup`.
- AppKit MVC: model ownership, controller lifetimes, delegate responsibilities,
  target/action, bindings where appropriate, and view-controller boundaries.
- Object persistence and archiving choices, including `NSSecureCoding`,
  `NSKeyedArchiver`, `Codable`, user defaults, files, Core Data, SwiftData, and
  explicit migration boundaries.
- Observation and AppKit interop: `@Observable` model ownership, main-actor UI
  updates, bridging model changes into controls, and avoiding unnecessary
  SwiftUI-only state assumptions.
- Mixed AppKit/SwiftUI composition through `NSHostingView`,
  `NSHostingController`, SwiftUI views embedded in AppKit, AppKit views exposed
  to SwiftUI, and clear ownership handoffs.

### Explicit Non-Scope

- Do not make this the raw Apple-docs lookup skill; hand off to
  `explore-apple-swift-docs`.
- Do not make it the Xcode build, run, signing, file-membership, or testing
  owner; hand off to `xcode-build-run-workflow` or `xcode-testing-workflow`.
- Do not absorb SwiftASB-specific runtime guidance; keep those details in
  `swiftasb-skills`.
- Do not present AppKit as legacy-only or SwiftUI as automatically preferred.
  The recommendation should choose the framework based on the app shape and the
  API surface that actually owns the behavior.

## Suggested Reference Files

The new skill should mirror the SwiftUI architecture skill's reference-heavy
shape, but with AppKit-specific topics:

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

## Apple Documentation Gate

Implementation should start from official Apple documentation for the exact API
families involved. Initial source targets include:

- [AppKit](https://developer.apple.com/documentation/AppKit)
- [NSApplication](https://developer.apple.com/documentation/appkit/nsapplication)
- [NSApplicationDelegate](https://developer.apple.com/documentation/appkit/nsapplicationdelegate)
- [NSWindow](https://developer.apple.com/documentation/appkit/nswindow)
- [NSWindowController](https://developer.apple.com/documentation/appkit/nswindowcontroller)
- [NSViewController](https://developer.apple.com/documentation/appkit/nsviewcontroller)
- [NSStatusItem](https://developer.apple.com/documentation/appkit/nsstatusitem)
- [NSMenu](https://developer.apple.com/documentation/appkit/nsmenu)
- [NSResponder](https://developer.apple.com/documentation/appkit/nsresponder)
- [NSWindowRestoration](https://developer.apple.com/documentation/appkit/nswindowrestoration)
- [NSSecureCoding](https://developer.apple.com/documentation/foundation/nssecurecoding)
- [NSKeyedArchiver](https://developer.apple.com/documentation/foundation/nskeyedarchiver)
- [Observation](https://developer.apple.com/documentation/Observation)
- [NSHostingView](https://developer.apple.com/documentation/swiftui/nshostingview)
- [NSHostingController](https://developer.apple.com/documentation/swiftui/nshostingcontroller)

## Acceptance Criteria

- Apple Dev Skills exposes an AppKit architecture workflow that is parallel in
  weight to the SwiftUI architecture workflow.
- Menu bar apps and status-item apps are first-class AppKit shapes, not edge
  cases hidden under generic Xcode guidance.
- Restoration, archiving, MVC, target/action, responder chain, and controller
  lifetimes are documented as modern AppKit concerns instead of treated as stale
  trivia.
- Mixed AppKit/SwiftUI guidance names which framework owns each responsibility
  and how state crosses the boundary.
- Observation guidance explains practical AppKit use without assuming SwiftUI
  property-wrapper semantics.
- Handoffs stay clear among AppKit architecture, SwiftUI architecture,
  Apple-docs lookup, Xcode execution, accessibility, and SwiftASB integration.
- Socket metadata validation and Apple Dev Skills child validation pass after
  implementation.

