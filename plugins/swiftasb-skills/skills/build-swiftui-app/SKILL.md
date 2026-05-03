---
name: build-swiftui-app
description: Build or refactor a SwiftUI app feature on top of SwiftASB using framework-owned SwiftUI state, SwiftASB thread and turn handles, observable companions, clear runtime diagnostics, and safe validation.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with SwiftASB v1.0.0 or newer, Swift 6, SwiftPM, SwiftUI, Observation, Xcode, and local Codex app-server integrations.
metadata:
  owner: gaelic-ghost
  repo: socket
  package: SwiftASB
  category: swiftasb-swiftui
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(xcodebuild:*)
---

# Build SwiftUI App With SwiftASB

## Purpose

Help a SwiftUI app use [SwiftASB](https://github.com/gaelic-ghost/SwiftASB) to start Codex work, show live progress, handle approvals or user input, and expose recent thread history without replaying raw app-server protocol payloads into app state.

The real job is to connect SwiftUI views to SwiftASB's Swift-native handles and observable companions. SwiftUI owns view lifetime and rendering. SwiftASB owns the local Codex app-server process, thread and turn handles, typed events, request responses, diagnostics, and recent-history companions.

## Required Documentation Gate

Before implementing or proposing SwiftUI structure, read the relevant Apple documentation through Apple Dev Skills or official Apple docs.

Minimum rules to rely on:

- SwiftUI `@State` is view-managed storage, and SwiftUI updates dependent views when the value changes.
- SwiftUI can store `@Observable` objects in `@State`; subviews update when they read changed observable properties.
- SwiftUI app structure is built from an `App` whose body provides one or more `Scene` values.
- Observation support should come from the `@Observable` macro rather than bare `Observable` protocol conformance.

Authoritative docs:

- [SwiftUI State](https://developer.apple.com/documentation/swiftui/state)
- [SwiftUI App](https://developer.apple.com/documentation/swiftui/app)
- [SwiftUI Scene](https://developer.apple.com/documentation/SwiftUI/Scene)
- [Observation Observable macro](https://developer.apple.com/documentation/Observation/Observable%28%29)

## When To Use

- Use this skill when a SwiftUI app needs a SwiftASB-backed feature.
- Use this skill after `swiftasb:choose-integration-shape` selects a SwiftUI app shape.
- Use this skill when a SwiftUI app needs live Codex progress, approvals, diagnostics, recent turns, recent files, or recent commands.
- Use this skill for refactors that move a SwiftUI app away from raw JSON-RPC or ad hoc event replay and toward SwiftASB companions.

## Source Check

Verify current SwiftASB docs and public API before editing:

- [SwiftASB GitHub repository](https://github.com/gaelic-ghost/SwiftASB)
- `Sources/SwiftASB/SwiftASB.docc/GettingStartedWithSwiftASB.md`
- `Sources/SwiftASB/SwiftASB.docc/SwiftUIObservableCompanions.md`
- `Sources/SwiftASB/SwiftASB.docc/HandlingTurnProgressAndApprovals.md`
- `Sources/SwiftASB/Public/CodexAppServer.swift`
- `Sources/SwiftASB/Public/CodexThread+Dashboard.swift`
- `Sources/SwiftASB/Public/CodexTurnHandle.swift`

As of SwiftASB `v1.0.0`, SwiftUI-facing integrations should prefer:

- `CodexAppServer` for process startup, initialization, diagnostics, thread creation, and app-wide capability reads
- `CodexThread` for conversation-scoped turn creation, request routing, thread actions, and local history
- `CodexTurnHandle` for one active turn, including events, steering, interruption, request responses, and completion handoff
- `CodexThread.makeDashboard()` for thread-level current state
- `CodexTurnHandle.minimap` for active-turn current state
- `CodexThread.makeRecentTurns(...)`, `makeRecentFiles(...)`, and `makeRecentCommands(...)` for local history views

## Implementation Workflow

1. Confirm the app's existing SwiftUI state pattern.
2. Read Apple docs for the framework behavior the change relies on.
3. Add SwiftASB as a package dependency only if it is not already present:
   - package URL: `https://github.com/gaelic-ghost/SwiftASB`
   - minimum version: `1.0.0`
   - product: `SwiftASB`
4. Choose the owner object:
   - app-wide model owns `CodexAppServer`
   - workspace, document, or conversation model owns `CodexThread`
   - active-turn method or model owns `CodexTurnHandle`
5. Start and initialize the app-server from an explicit async entrypoint.
6. Create or resume a thread through `CodexAppServer`.
7. Create observable companions from the thread and current turn.
8. Render state from companions directly where possible.
9. Route approval and elicitation responses through the owning `CodexTurnHandle` or `CodexThread`.
10. Make startup, compatibility, turn, approval, cancellation, and shutdown errors human-readable.
11. Validate with the repository's documented SwiftPM or Xcode path.

## State Ownership Pattern

Prefer one app-facing model that makes ownership visible:

```swift
import Observation
import SwiftASB

@MainActor
@Observable
final class CodexWorkspaceModel {
    private let appServer = CodexAppServer()

    var thread: CodexThread?
    var dashboard: CodexThread.Dashboard?
    var currentMinimap: CodexTurnHandle.Minimap?
    var errorMessage: String?

    func start(workspacePath: String) async {
        do {
            try await appServer.start()
            _ = try await appServer.cliExecutableDiagnostics()
            try await appServer.initialize(
                .init(
                    clientInfo: .init(
                        name: "ExampleApp",
                        title: "Example App",
                        version: "1.0.0"
                    )
                )
            )

            let thread = try await appServer.startThread(
                .init(currentDirectoryPath: workspacePath)
            )
            self.thread = thread
            dashboard = await thread.makeDashboard()
        } catch {
            errorMessage = "SwiftASB could not start the local Codex runtime: \(error)"
        }
    }

    func run(_ prompt: String) async {
        guard let thread else {
            errorMessage = "SwiftASB cannot start a turn before a thread exists."
            return
        }

        do {
            let turn = try await thread.startTextTurn(prompt)
            currentMinimap = turn.minimap

            for try await event in turn.events {
                if case .completed = event {
                    _ = try await turn.complete()
                    currentMinimap = nil
                    return
                }
            }
        } catch {
            errorMessage = "SwiftASB turn failed before completion: \(error)"
        }
    }

    func stop() async {
        await appServer.stop()
    }
}
```

Use this as a shape, not as a file to paste blindly. Match the app's real lifetime, error model, and UI needs.

## UI Guidance

- Show Codex runtime startup and compatibility failures before offering turn controls.
- Disable same-thread turn controls while one turn is active, or create a separate thread when concurrent work is truly intended.
- Use `dashboard` for thread-wide current activity.
- Use `currentMinimap` for the active turn's command, file-edit, dynamic-tool, collab-tool, MCP, and compaction activity.
- Use recent companions for inspector rails and completed history instead of building a second cache from raw events.
- Keep approval and elicitation prompts user-facing and concrete: tell the user what command, file change, permission, or MCP action is being requested.
- Keep cancellation visible and reversible where the app's product model allows it.

## Validation

Run the repository's documented validation path.

For SwiftPM packages:

```bash
swift build
swift test
```

For Xcode apps, use the repository's documented `xcodebuild` or Xcode MCP workflow. Do not assume SwiftPM validation is enough for an app project with Xcode-owned project settings.

Live Codex integration tests should be opt-in, isolated in temporary workspaces, and bounded by hard timeouts.

## Handoffs

- Use `swiftasb:explain-swiftasb` when the user needs adoption tradeoffs before implementation.
- Use `swiftasb:choose-integration-shape` when ownership or app shape is unclear.
- Use `apple-dev-skills:explore-apple-swift-docs` for SwiftUI, Observation, SwiftPM, or AppKit documentation.
- Use Apple build, test, or Xcode workflow skills for project execution and diagnostics.

## Guardrails

- Do not put raw generated `CodexWire...` models into SwiftUI view state.
- Do not introduce a command bus or broad coordinator just to forward SwiftASB events; use local model methods and SwiftASB handles unless the app already has a real architecture surface for that job.
- Do not start overlapping turns on the same thread; SwiftASB rejects that because the live app-server does not expose a reliable independent lifecycle for them.
- Do not hide local Codex CLI discovery, compatibility, or startup failures behind generic "failed" messages.
- Do not run multiple SwiftPM or Xcode build/test commands concurrently.
