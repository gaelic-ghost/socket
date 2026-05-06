---
name: build-appkit-app
description: Build or refactor an AppKit app feature on top of SwiftASB using explicit application, window, document, thread, and turn ownership with main-actor UI updates and clear runtime diagnostics.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with SwiftASB v1.0.3 or newer, Swift 6, SwiftPM, AppKit, Xcode, and local Codex app-server integrations.
metadata:
  owner: gaelic-ghost
  repo: socket
  package: SwiftASB
  category: swiftasb-appkit
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(xcodebuild:*)
---

# Build AppKit App With SwiftASB

## Purpose

Help an AppKit app use [SwiftASB](https://github.com/gaelic-ghost/SwiftASB) to start local Codex work, show thread and turn progress, answer approvals or elicitation requests, list stored threads, and expose recent history from app-owned controllers or models.

The real job is to keep AppKit's app, window, document, and view-controller lifetimes in charge of UI behavior while SwiftASB owns the local Codex subprocess, app-wide library companion, typed thread and turn handles, events, request responses, diagnostics, and local history.

## Required Documentation Gate

Before implementing or proposing AppKit structure, read the relevant Apple documentation through Apple Dev Skills or official Apple docs.

Minimum rules to rely on:

- `NSApplication` manages the app's main event loop, windows, menus, events, and app-wide resources.
- `NSApplicationDelegate` handles app lifecycle callbacks such as launch, termination, activation, reopen, and window-update behavior.
- `NSWindowController` manages a window and often participates in document-based ownership.
- `NSViewController` manages a view and has lifecycle methods suitable for window content.
- AppKit UI types such as `NSWindow` and many delegate callbacks are main-actor UI surfaces; update AppKit views and controllers from the main actor.

Authoritative docs:

- [AppKit](https://developer.apple.com/documentation/AppKit)
- [NSApplication](https://developer.apple.com/documentation/appkit/nsapplication)
- [NSApplicationDelegate](https://developer.apple.com/documentation/AppKit/NSApplicationDelegate)
- [NSWindowController](https://developer.apple.com/documentation/appkit/nswindowcontroller)
- [NSViewController](https://developer.apple.com/documentation/AppKit/NSViewController)
- [NSWindow](https://developer.apple.com/documentation/appkit/nswindow)

## When To Use

- Use this skill when an AppKit app needs a SwiftASB-backed feature.
- Use this skill after `swiftasb:choose-integration-shape` selects an AppKit, document, window-controller, or menu-bar app shape.
- Use this skill when AppKit menus, toolbar actions, sidebars, inspectors, document windows, or panels need to start, steer, interrupt, or inspect Codex turns.
- Use this skill for refactors that move AppKit code away from raw JSON-RPC, ad hoc process ownership, or generated wire models and toward SwiftASB's public handles.

## Source Check

Verify current SwiftASB docs and public API before editing:

- [SwiftASB GitHub repository](https://github.com/gaelic-ghost/SwiftASB)
- `README.md`
- `Sources/SwiftASB/SwiftASB.docc/GettingStartedWithSwiftASB.md`
- `Sources/SwiftASB/SwiftASB.docc/HandlingTurnProgressAndApprovals.md`
- `Sources/SwiftASB/SwiftASB.docc/ReadingDiagnosticsAndHistory.md`
- `Sources/SwiftASB/SwiftASB.docc/ThreadHistoryAndObservables.md`
- `Sources/SwiftASB/Public/CodexAppServer+Library.swift`
- `Sources/SwiftASB/Public/CodexAppServer.swift`
- `Sources/SwiftASB/Public/CodexThread+Dashboard.swift`
- `Sources/SwiftASB/Public/CodexTurnHandle.swift`

As of SwiftASB `v1.0.3`, AppKit-facing integrations should prefer:

- `CodexAppServer` for subprocess startup, initialization, diagnostics, stored-thread operations, model capability reads, MCP status reads, and hook diagnostics
- `CodexAppServer.makeLibrary(configuration:)` for app-wide stored-thread lists, cwd grouping, library-local selection, Git branch metadata, and model/MCP/hook snapshots
- `CodexThread` for conversation-scoped turn creation, thread events, thread actions, request responses, and local history
- `CodexTurnHandle` for one active turn, including events, steering, interruption, request responses, minimap state, and completion handoff
- `CodexThread.makeDashboard()` and `CodexTurnHandle.minimap` as UI-friendly current-state mirrors
- local history helpers and recent companions for inspector panels, transcript sidebars, and completed work views

## Implementation Workflow

1. Confirm the AppKit ownership shape: app delegate, document, window controller, view controller, menu-bar controller, or helper object.
2. Read the Apple docs for the framework behavior the change relies on.
3. Add SwiftASB as a package dependency only if it is not already present:
   - package URL: `https://github.com/gaelic-ghost/SwiftASB`
   - minimum version: `1.0.3` when using app-wide library or app-snapshot guidance; otherwise verify the support window in SwiftASB's README
   - product: `SwiftASB`
4. Choose the SwiftASB owner:
   - application-level model owns `CodexAppServer` when one runtime serves many windows
   - application, window, or document model owns `CodexAppServer.Library` when the UI needs stored-thread lists before a thread is selected
   - document or window model owns `CodexThread` when work belongs to one workspace or document
   - active command method or controller owns `CodexTurnHandle` while one turn is running
5. Start and initialize the app-server from an explicit async lifecycle point.
6. Create, resume, or fork a thread for the window, document, or workspace.
7. Route menu and toolbar actions into local controller methods that start, steer, interrupt, or inspect turns.
8. Update AppKit views on the main actor from SwiftASB events, dashboard, minimap, diagnostics, and local history.
9. Route approval and elicitation responses through the matching `CodexTurnHandle` or `CodexThread`.
10. Make startup, compatibility, turn, approval, cancellation, and shutdown errors human-readable.
11. Validate with the repository's documented Xcode path.

## Ownership Pattern

Prefer one AppKit-facing object that makes lifetime visible:

```swift
import AppKit
import SwiftASB

@MainActor
final class CodexWorkspaceWindowController: NSWindowController {
    private let appServer: CodexAppServer
    private var library: CodexAppServer.Library?
    private var thread: CodexThread?
    private var currentTurn: CodexTurnHandle?

    @IBOutlet private var statusField: NSTextField!

    init(appServer: CodexAppServer) {
        self.appServer = appServer
        super.init(window: nil)
    }

    required init?(coder: NSCoder) {
        nil
    }

    func connect(workspacePath: String) {
        Task { @MainActor in
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

                thread = try await appServer.startThread(
                    .init(currentDirectoryPath: workspacePath)
                )
                library = try await appServer.makeLibrary(
                    configuration: .init(
                        sortedBy: .turnFinishedNewestFirst,
                        groupedBy: .cwd,
                        query: .unarchived(limit: 30),
                        mcpServerStatusRequest: .init(detail: .toolsAndAuthOnly)
                    )
                )
                statusField.stringValue = "Codex is ready."
            } catch {
                statusField.stringValue = "SwiftASB could not start Codex: \(error)"
            }
        }
    }

    @IBAction func runSelectedTask(_ sender: Any?) {
        guard let thread else {
            statusField.stringValue = "SwiftASB cannot start a turn before a thread exists."
            return
        }

        Task { @MainActor in
            do {
                let turn = try await thread.startTextTurn("Summarize the current workspace.")
                currentTurn = turn

                for try await event in turn.events {
                    if case .completed = event {
                        _ = try await turn.complete()
                        currentTurn = nil
                        statusField.stringValue = "Codex turn finished."
                        return
                    }
                }
            } catch {
                currentTurn = nil
                statusField.stringValue = "SwiftASB turn failed: \(error)"
            }
        }
    }

    @IBAction func interruptTurn(_ sender: Any?) {
        Task { @MainActor in
            do {
                try await currentTurn?.interrupt()
                statusField.stringValue = "Interrupt sent to Codex."
            } catch {
                statusField.stringValue = "SwiftASB could not interrupt the turn: \(error)"
            }
        }
    }
}
```

Use this as a shape, not as a file to paste blindly. Match the app's actual nib/storyboard/programmatic-window setup, document model, and error UI.

## UI Guidance

- Show Codex runtime startup and compatibility failures before enabling menu or toolbar actions.
- Keep menu validation tied to real state: no thread, active turn, waiting approval, or idle.
- Disable same-thread start actions while a turn is active, or create a separate thread when concurrent work is truly intended.
- Use a `CodexAppServer.Library` for source lists, launchers, project browsers, stored-thread selection, app-wide model capabilities, MCP status, and hook diagnostics.
- Show approvals as concrete AppKit UI: sheet, popover, panel, or inspector row that names the command, file change, permission, or MCP action.
- Use `dashboard` and `minimap` state for activity views instead of replaying every raw event into controller-owned arrays.
- Keep document and window closure explicit: interrupt active work or make it clear that background work continues elsewhere.
- Surface diagnostics and MCP status in places a Mac maintainer can actually inspect, such as a status item, inspector, log pane, or preferences diagnostics view.

## Validation

Use the repository's documented Xcode build and test path. For Xcode projects, do not assume SwiftPM validation is enough because scheme, target membership, entitlements, sandboxing, signing, and resources may be Xcode-owned.

Live Codex integration tests should be opt-in, isolated in temporary workspaces, and bounded by hard timeouts.

## Handoffs

- Use `swiftasb:explain-swiftasb` when the user needs adoption tradeoffs before implementation.
- Use `swiftasb:choose-integration-shape` when ownership or app shape is unclear.
- Use `swiftasb:diagnose-integration` when startup, turn, approval, MCP, diagnostics, or history behavior fails.
- Use `apple-dev-skills:explore-apple-swift-docs` for AppKit, SwiftUI, SwiftPM, or Observation documentation.
- Use Apple build, test, or Xcode workflow skills for project execution and diagnostics.

## Guardrails

- Do not make a window or view controller secretly own app-wide Codex runtime work if the app has multiple windows that should share one `CodexAppServer`.
- Do not mutate AppKit UI from detached background work without returning to the main actor.
- Do not put raw generated `CodexWire...` models into AppKit controller or view state.
- Do not introduce a command bus or broad coordinator just to forward SwiftASB events; use local AppKit actions and SwiftASB handles unless the app already has a real architecture surface for that job.
- Do not start overlapping turns on the same thread; SwiftASB rejects that because the live app-server does not expose a reliable independent lifecycle for them.
- Do not hide local Codex CLI discovery, compatibility, or startup failures behind generic messages.
- Do not run multiple SwiftPM or Xcode build/test commands concurrently.
