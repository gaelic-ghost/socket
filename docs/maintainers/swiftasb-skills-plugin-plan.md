# SwiftASB Skills Plugin Plan

This plan records the first durable shape for a Socket-hosted SwiftASB companion plugin.

The plugin's job is to help agents build SwiftUI apps, AppKit apps, command-line tools, helper utilities, and Swift packages on top of SwiftASB, then explain the tradeoffs clearly enough that users can decide whether SwiftASB belongs in their project. It should teach the SwiftASB integration surface without turning the SwiftASB package repository into the only Codex-visible guidance source.

## Intent

The SwiftASB skills plugin should help agents do three things:

- explain SwiftASB in plain language for app builders and package authors
- choose the right integration shape for a user's app, tool, or package
- implement SwiftASB-backed features while staying close to the real SwiftASB public API and Apple framework behavior

This is a companion guidance plugin, not a runtime plugin. The first version should not bundle an MCP server, duplicate generated schema files, or copy SwiftASB source code into `socket`.

## Packaging Direction

Package the guidance as an independent child plugin under:

```text
plugins/swiftasb-skills/
```

The child plugin should own its Codex-facing guidance surface:

- `.codex-plugin/plugin.json`
- `skills/`
- README or maintainer notes that explain the plugin's role
- any validation scripts needed for the plugin's own authored guidance

The root Socket marketplace should list the plugin as a normal local child entry when the plugin is ready to install:

```json
{
  "name": "swiftasb-skills",
  "source": {
    "source": "local",
    "path": "./plugins/swiftasb-skills"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Developer Tools"
}
```

Keep the SwiftASB Swift package repository as the source of truth for the library, public API, generated wire types, release notes, licensing, live integration tests, and package-level documentation. Use this Socket plugin for Codex-visible agent workflows and user-facing decision support.

## Relationship To Apple Dev Skills

The SwiftASB plugin should rely on Apple Dev Skills for Apple framework rules and Xcode workflow selection.

That means:

- use Apple Dev Skills for SwiftUI, AppKit, SwiftPM, Xcode, DocC, build, and test workflow rules
- use SwiftASB skills for the SwiftASB-specific decision, integration, explanation, and troubleshooting work
- avoid duplicating broad SwiftUI or AppKit architecture guidance unless the guidance is specifically about using SwiftASB inside that framework-owned shape

In practice, a SwiftUI task should first respect documented SwiftUI and Observation behavior, then apply SwiftASB's app-server, thread, turn, dashboard, minimap, and compatibility guidance inside that framework model.

## Proposed Skill Inventory

### `swiftasb:explain-swiftasb`

Explain what SwiftASB does for a user in practical terms.

This skill should cover:

- the real problem SwiftASB solves
- how it relates to the Codex app-server protocol
- what app builders get from Swift-native types and observable companions
- what SwiftASB does not provide
- when a project should avoid SwiftASB
- licensing and compatibility caveats that affect adoption decisions

### `swiftasb:choose-integration-shape`

Help an agent decide how SwiftASB should fit into a user's project before implementation starts.

This skill should classify the project shape:

- SwiftUI app
- AppKit app
- menu bar app
- command-line tool
- helper daemon or local service
- package-only library
- test or integration harness

The output should recommend the SwiftASB entry points, user-visible behavior, state ownership, validation path, and documentation updates that fit that project shape.

### `swiftasb:build-swiftui-app`

Guide agents through SwiftUI-facing SwiftASB integration.

This skill should emphasize:

- framework-owned view and task behavior
- observable companions for thread and turn state
- user-visible progress, cancellation, and failure states
- safe same-thread turn handling
- clear boundaries between app UI state and SwiftASB client state
- build and test checks appropriate for the app repository

### `swiftasb:build-appkit-app`

Guide agents through AppKit-facing SwiftASB integration.

This skill should emphasize:

- application and window ownership
- object lifetime for clients, thread handles, and turn handles
- menu or toolbar actions that start, cancel, resume, or inspect work
- main-thread UI updates
- logging and diagnostics that are useful to a Mac app maintainer
- build and test checks appropriate for the app repository

### `swiftasb:build-swift-package`

Guide agents through package-author integration.

This skill should help package authors:

- expose SwiftASB-backed capabilities without leaking raw wire types as the default API
- keep public APIs Swift-native and explainable
- keep live Codex subprocess checks opt-in, timeout-bounded, and isolated
- document compatibility expectations
- add focused tests around the package's own behavior

### `swiftasb:diagnose-integration`

Help agents debug SwiftASB integration failures.

This skill should cover:

- Codex CLI discovery and diagnostics
- app-server startup failures
- schema or compatibility mismatch symptoms
- same-thread concurrency rejection
- turn timeout and cancellation behavior
- thread history, compaction, and resume/fork surfaces where relevant
- when to run live integration probes and how to keep them isolated

## First Implementation Slice

The first slice should be intentionally small:

- [x] Create `plugins/swiftasb-skills/` with a plugin manifest.
- [x] Add `swiftasb:explain-swiftasb`.
- [x] Add `swiftasb:choose-integration-shape`.
- [x] Add `swiftasb:build-swiftui-app`.
- [x] Wire `swiftasb-skills` into `.agents/plugins/marketplace.json`.
- [x] Update `README.md` and `ROADMAP.md` so Socket documents the new child plugin surface.
- [x] Run `uv run scripts/validate_socket_metadata.py`.
- [ ] Run any child-plugin validation added by the new plugin.

## Later Slices

After the first slice proves useful, add:

- [x] `swiftasb:build-appkit-app`.
- [x] `swiftasb:build-swift-package`.
- [x] `swiftasb:diagnose-integration`.
- [ ] Examples that show how agents should explain SwiftASB to users before implementation.
- [ ] Install testing with a temporary `CODEX_HOME`.
- [x] Decide against a SwiftASB repo-local marketplace because SwiftASB is expected to be consumed as a Swift package dependency inside other apps, command-line tools, and packages; Codex-visible guidance belongs in the Socket-hosted companion plugin.

## Definition Of Done

The plugin is ready for first release when:

- [x] Socket exposes `swiftasb-skills` as an installable child plugin.
- [x] The skills consistently describe SwiftASB as a Swift-native app-server client rather than a general AI SDK or a raw protocol dump.
- [x] The guidance sends Apple framework questions through Apple Dev Skills instead of duplicating broad SwiftUI or AppKit rules.
- [x] The guidance points agents back to the SwiftASB package docs for source-of-truth API, licensing, release, and compatibility details.
- [ ] Root Socket docs, marketplace wiring, and validation all agree on the plugin's install surface.
