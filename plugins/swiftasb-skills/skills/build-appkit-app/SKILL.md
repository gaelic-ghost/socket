---
name: build-appkit-app
description: Build or refactor an AppKit app feature on top of SwiftASB using explicit application, window, document, thread, and turn ownership with main-actor UI updates and clear runtime diagnostics.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with SwiftASB v1.8.0 or newer, Swift 6, SwiftPM, AppKit, Xcode, and local Codex app-server integrations.
metadata:
  owner: gaelic-ghost
  repo: socket
  package: SwiftASB
  category: swiftasb-appkit
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(xcodebuild:*)
---

# Build AppKit App With SwiftASB

## Purpose

Help an AppKit app use [SwiftASB](https://github.com/gaelic-ghost/SwiftASB) to start local Codex work, show thread, agenda, and turn progress, answer approvals or elicitation requests, list stored threads, archive or unarchive stored threads, inspect app-server-owned worktree, selected Git status, project identity, thread source, filesystem/config/extension/MCP/workspace facts, observe SwiftASB-owned feature operations, expose app-wide inventory, and expose recent history from app-owned controllers or models.

The real job is to keep AppKit's app, window, document, and view-controller lifetimes in charge of UI behavior while SwiftASB owns the local Codex subprocess, app-wide library and inventory companions, thread agenda companions, stable worktree groups, repository/worktree filters, selected-worktree Git status, project identity and thread-source facts, app-server-owned worktree snapshots, app-server-routed filesystem/config/extension/MCP reads, workspace permission facts, feature policy, feature-operation events, plan-mode turn starts, goal helpers, review and shell-command entry points, typed thread, agenda, and turn handles, events, request responses, diagnostics, and local history.

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
- `Sources/SwiftASB/SwiftASB.docc/AppWideCapabilities.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexInventory.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexMCP.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexFS.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexConfig.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexExtensions.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexWorkspace.md`
- `Sources/SwiftASB/SwiftASB.docc/FeaturePermissionPolicy.md`
- `Sources/SwiftASB/SwiftASB.docc/ThreadManagement.md`
- `Sources/SwiftASB/Public/CodexAppServer+Library.swift`
- `Sources/SwiftASB/Public/CodexAppServer+Inventory.swift`
- `Sources/SwiftASB/Public/CodexAppServer+LoadedThreads.swift`
- `Sources/SwiftASB/Public/CodexAppServer+CodexExtensions.swift`
- `Sources/SwiftASB/Public/CodexAppServer+MCP.swift`
- `Sources/SwiftASB/Public/CodexMCP.swift`
- `Sources/SwiftASB/Public/CodexFS.swift`
- `Sources/SwiftASB/Public/CodexConfig.swift`
- `Sources/SwiftASB/Public/CodexWorkspace.swift`
- `Sources/SwiftASB/Public/CodexAppServer+Bootstrap.swift`
- `Sources/SwiftASB/Public/CodexAppServer.swift`
- `Sources/SwiftASB/Public/CodexDiagnostics.swift`
- `Sources/SwiftASB/Public/CodexErrors.swift`
- `Sources/SwiftASB/Public/CodexReviewHandle.swift`
- `Sources/SwiftASB/Public/CodexThread.swift`
- `Sources/SwiftASB/Public/CodexThread+Dashboard.swift`
- `Sources/SwiftASB/Public/CodexThread+Agenda.swift`
- `Sources/SwiftASB/Public/CodexTurnHandle.swift`

As of SwiftASB `v1.8.0`, AppKit-facing integrations should prefer:

- `CodexAppServer.start(_:)` with `CodexAppServer.StartupRequest` for normal one-call subprocess startup, compatibility validation, initialization, and typed `CodexAppServerStartupError` failures
- lower-level `CodexAppServer.start()`, `cliExecutableDiagnostics()`, and `initialize(_:)` only when the app intentionally owns custom diagnostics, compatibility policy, or test setup before initialization
- `CodexAppServer` for subprocess ownership, diagnostics, stored-thread operations, model capability reads, feature-operation-event streams, and hook diagnostics
- `CodexAppServer.makeLibrary(configuration:)` for app-wide stored-thread lists, cwd or repository grouping, stable worktree groups, repository/worktree filters, selected worktree or repository context, selected-worktree Git status, library-local selection, `CodexWorkspace.ProjectInfo` project identity, `CodexAppServer.ThreadSource` source badges, and model/MCP/hook snapshots that refresh when app-server app/skill/MCP state changes
- `CodexAppServer.makeInventory(configuration:)` for routine app-wide model capabilities, global MCP summaries, hook diagnostics, apps, skills, plugins, and collaboration modes
- `CodexAppServer.fs`, `CodexAppServer.config`, and `CodexAppServer.extensions` for app-server-owned file metadata, directory/file reads, file discovery with match metadata, effective config, advanced extension pagination, plugin detail reads, and already-configured marketplace upgrades
- `CodexAppServer.mcp` for MCP server installs, full status snapshots, and app-wide or thread-scoped MCP resource contents
- `SwiftASBFeaturePolicy` for feature-category defaults and host app authority, with `gitObservability`, `extensionInventory`, and `extensionMaintenance` enabled by default and mutation-oriented categories disabled until the app opts in
- `CodexAppServer.featureOperationEvents()` for human-readable SwiftASB-owned mutation records, such as marketplace maintenance attempts
- `CodexWorkspace` for session cwd, app-server-owned worktree snapshots, project identity, Git repository facts, selected Git status snapshots, active permission profile, and runtime filesystem/network permission facts
- `CodexThread` for conversation-scoped text turns, plan-mode turns, thread events, thread actions, archive/unarchive, thread goals, request responses, and local history
- `CodexThread.startReview(against:placement:)` for code-review UI, and `CodexThread.sendShellCommand(_:)` only for explicit user-level shell actions when `shellCommandExecution` is enabled
- `CodexTurnHandle` for one active turn, including events, steering, interruption, request responses, minimap state, and completion handoff
- `CodexTurnItem.Kind.sleep` when custom transcript, history, or activity UI switches over public turn item kinds
- `CodexThread.makeDashboard()`, `CodexThread.makeAgenda()`, and `CodexTurnHandle.minimap` as UI-friendly current-state mirrors
- local history helpers and recent companions for inspector panels, transcript sidebars, and completed work views
- query descriptors such as `CodexAppServer.ThreadListQD`, `CodexFS.FileDiscoveryQD`, `CodexThread.HistoryWindowQD`, `CodexThread.RecentFilesQD`, and `CodexThread.RecentCommandsQD` for repeatable sidebar, file-picker, inspector, and history intent
- optional `ASBPresentation` and `ASBAppKit` products when the app wants SwiftASB presentation snapshots or the packaged AppKit thread sidebar view

## Implementation Workflow

1. Confirm the AppKit ownership shape: app delegate, document, window controller, view controller, menu-bar controller, or helper object.
2. Read the Apple docs for the framework behavior the change relies on.
3. Add SwiftASB as a package dependency only if it is not already present:
   - package URL: `https://github.com/gaelic-ghost/SwiftASB`
   - minimum version: `1.8.0` when using current one-call startup, Codex CLI `0.142.x` compatibility, app-wide library or inventory, stable worktree groups, repository/worktree filters, selected-worktree Git status, feature policy, feature-operation events, extension marketplace maintenance, project identity, thread source, filesystem match metadata, MCP installs/status/resource reads, config warnings, extension inventory, workspace, query-descriptor, thread archive/unarchive, code-review starts, shell-command execution, plan/goal UI, sleep turn-item classification, presentation products, or recent-activity guidance; otherwise verify the support window in SwiftASB's README
   - product: `SwiftASB`
   - optional products: `ASBPresentation` and `ASBAppKit` when the app uses SwiftASB's reusable presentation snapshots or packaged AppKit views
4. Choose the SwiftASB owner:
   - application-level model owns `CodexAppServer` when one runtime serves many windows
   - application, window, or document model owns `CodexAppServer.Library` when the UI needs stored-thread lists before a thread is selected
   - document or window model owns `CodexThread` when work belongs to one workspace or document
   - active command method or controller owns `CodexTurnHandle` while one turn is running
5. Start the app-server from an explicit async lifecycle point, using `appServer.start(_:)` for normal clients and the lower-level `start()` plus `initialize(_:)` sequence only for custom diagnostics or tests.
6. Create, resume, or fork a thread for the window, document, or workspace.
7. Route menu and toolbar actions into local controller methods that start, steer, interrupt, or inspect turns.
8. Use `appServer.fs`, `appServer.config`, `appServer.makeInventory(configuration:)`, `appServer.extensions`, `appServer.mcp`, `CodexWorkspace`, and `SwiftASBFeaturePolicy` when inspectors, preferences, file pickers, MCP panes, or diagnostics need Codex-owned filesystem, config, plugin/skill/app, collaboration-mode, marketplace-maintenance, resource, worktree, selected Git status, project identity, thread source, permission facts, or feature-category choices.
9. Update AppKit views on the main actor from SwiftASB events, dashboard, agenda, minimap, diagnostics, and local history.
10. Route approval and elicitation responses through the matching `CodexTurnHandle` or `CodexThread`.
11. Make startup, compatibility, turn, approval, cancellation, and shutdown errors human-readable.
12. Validate with the repository's documented Xcode path.

## Ownership Pattern

Prefer one AppKit-facing object that makes lifetime visible:

```swift
import AppKit
import SwiftASB

@MainActor
final class CodexWorkspaceWindowController: NSWindowController {
    private let appServer: CodexAppServer
    private var inventory: CodexAppServer.Inventory?
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
                let session = try await appServer.start(
                    .init(
                        clientInfo: .init(
                            name: "ExampleApp",
                            title: "Example App",
                            version: "1.0.0"
                        )
                    )
                )
                _ = session.cliExecutableDiagnostics

                inventory = try await appServer.makeInventory(
                    configuration: .init(
                        hookListCurrentDirectoryPaths: [workspacePath],
                        extensionCurrentDirectoryPaths: [workspacePath]
                    )
                )
                thread = try await appServer.startThread(
                    .init(currentDirectoryPath: workspacePath)
                )
                library = try await appServer.makeLibrary(
                    configuration: .init(
                        sortedBy: .turnFinishedNewestFirst,
                        groupedBy: .repository,
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

- Show `CodexAppServerStartupError` startup and compatibility failures before enabling menu or toolbar actions.
- Keep menu validation tied to real state: no thread, active turn, waiting approval, or idle.
- Disable same-thread start actions while a turn is active, or create a separate thread when concurrent work is truly intended.
- Use `CodexAppServer.Inventory` for routine app-wide model capabilities, global MCP summaries, hook diagnostics, apps, skills, plugins, and collaboration modes.
- Use a `CodexAppServer.Library` for source lists, launchers, project browsers, stored-thread selection, selected-worktree Git status, project identity display, thread-source badges, app-wide model capabilities, MCP status, and hook diagnostics.
- Use `CodexAppServer.fs` and `CodexFS.FileDiscoveryQD` for sandbox-safe file pickers, metadata inspectors, directory browsers, file-byte previews, watches, highlighted matches, and ranking explanations.
- Use `CodexAppServer.mcp` when the app needs to install MCP servers, show full MCP details, or show text/blob resource contents advertised by a configured MCP server.
- Use `CodexAppServer.config`, `CodexAppServer.extensions`, and `CodexWorkspace` for preferences or diagnostics panes that show effective config, requirements, advanced extension detail, marketplace maintenance, worktree snapshots, selected Git status, project identity, active profile, and filesystem/network permissions.
- Use `SwiftASBFeaturePolicy` to present feature-category toggles only when the app actually lets users change SwiftASB-owned authority. Read-only Git observability and extension inventory are enabled by default; stronger mutation categories should stay deliberate app choices.
- Subscribe to `CodexAppServer.featureOperationEvents()` when AppKit needs to show marketplace-upgrade results or future SwiftASB-owned mutation records in a status pane, log view, or inspector.
- Use `CodexThread.archive()` and `CodexThread.unarchive()` for archive UI actions when the app already owns the selected thread handle.
- Use `CodexThread.readGoal()`, `setGoal(_:)`, `clearGoal()`, `setName(_:)`, `updateMetadata(gitInfo:)`, `compactContext()`, and `rollbackLastTurns(_:)` from explicit menu, toolbar, inspector, or document actions that already own the selected thread.
- Use `CodexThread.startReview(against:placement:)` only from review controls that clearly say what will be reviewed and whether the result appears inline or detached.
- Use `CodexThread.sendShellCommand(_:)` only behind explicit user opt-in for high-impact shell execution; preserve shell syntax and explain that it does not inherit the thread sandbox policy.
- Show approvals as concrete AppKit UI: sheet, popover, panel, or inspector row that names the command, file change, permission, or MCP action.
- Use `dashboard` and `minimap` state for activity views instead of replaying every raw event into controller-owned arrays.
- Handle `CodexTurnItem.Kind.sleep` explicitly in custom turn item switches so AppKit transcript and activity UI remains current with Codex CLI `0.142.x` events.
- Use `ASBThreadSidebarView` from `ASBAppKit` when the app wants the packaged dense source-list renderer over `ASBPresentation` snapshots.
- Keep document and window closure explicit: interrupt active work or make it clear that background work continues elsewhere.
- Surface diagnostics, including config warnings, deprecation notices, MCP status changes, and remote-control status changes, in places a Mac maintainer can actually inspect, such as a status item, inspector, log pane, or preferences diagnostics view.

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
- Do not hide local Codex CLI discovery, compatibility, or startup failures behind generic messages; preserve `CodexAppServerStartupError` cases when mapping errors into AppKit status text.
- Do not run multiple SwiftPM or Xcode build/test commands concurrently.
