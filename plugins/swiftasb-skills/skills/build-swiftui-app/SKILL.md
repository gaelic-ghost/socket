---
name: build-swiftui-app
description: Build or refactor a SwiftUI app feature on top of SwiftASB using framework-owned SwiftUI state, SwiftASB thread and turn handles, observable companions, clear runtime diagnostics, and safe validation.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with SwiftASB v1.3.1 or newer, Swift 6, SwiftPM, SwiftUI, Observation, Xcode, and local Codex app-server integrations.
metadata:
  owner: gaelic-ghost
  repo: socket
  package: SwiftASB
  category: swiftasb-swiftui
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(xcodebuild:*)
---

# Build SwiftUI App With SwiftASB

## Purpose

Help a SwiftUI app use [SwiftASB](https://github.com/gaelic-ghost/SwiftASB) to start Codex work, show live progress, handle approvals or user input, list stored threads, archive or unarchive stored threads, inspect app-server-owned worktree, selected Git status, project identity, thread source, filesystem/config/extension/MCP-resource/workspace facts, observe SwiftASB-owned feature operations, and expose recent thread history without replaying raw app-server protocol payloads into app state.

The real job is to connect SwiftUI views to SwiftASB's Swift-native handles and observable companions. SwiftUI owns view lifetime and rendering. SwiftASB owns the local Codex app-server process, app-wide library companion, stable worktree groups, repository/worktree filters, selected-worktree Git status, project identity and thread-source facts, app-server-owned worktree snapshots, app-server-routed filesystem/config/extension/MCP-resource reads, workspace permission facts, feature policy, feature-operation events, thread and turn handles, typed events, request responses, diagnostics, and recent-history companions.

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
- `Sources/SwiftASB/SwiftASB.docc/ThreadHistoryAndObservables.md`
- `Sources/SwiftASB/SwiftASB.docc/HandlingTurnProgressAndApprovals.md`
- `Sources/SwiftASB/SwiftASB.docc/AppWideCapabilities.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexFS.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexConfig.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexExtensions.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexWorkspace.md`
- `Sources/SwiftASB/SwiftASB.docc/FeaturePermissionPolicy.md`
- `Sources/SwiftASB/SwiftASB.docc/ThreadManagement.md`
- `Sources/SwiftASB/Public/CodexAppServer+Library.swift`
- `Sources/SwiftASB/Public/CodexAppServer+LoadedThreads.swift`
- `Sources/SwiftASB/Public/CodexAppServer+CodexExtensions.swift`
- `Sources/SwiftASB/Public/CodexAppServer+MCP.swift`
- `Sources/SwiftASB/Public/CodexFS.swift`
- `Sources/SwiftASB/Public/CodexConfig.swift`
- `Sources/SwiftASB/Public/CodexWorkspace.swift`
- `Sources/SwiftASB/Public/CodexAppServer+Bootstrap.swift`
- `Sources/SwiftASB/Public/CodexAppServer.swift`
- `Sources/SwiftASB/Public/CodexDiagnostics.swift`
- `Sources/SwiftASB/Public/CodexErrors.swift`
- `Sources/SwiftASB/Public/CodexThread.swift`
- `Sources/SwiftASB/Public/CodexThread+Dashboard.swift`
- `Sources/SwiftASB/Public/CodexTurnHandle.swift`

As of SwiftASB `v1.3.1`, SwiftUI-facing integrations should prefer:

- `CodexAppServer.start(_:)` with `CodexAppServer.StartupRequest` for normal one-call startup, compatibility validation, initialization, and typed `CodexAppServerStartupError` failures
- lower-level `CodexAppServer.start()`, `cliExecutableDiagnostics()`, and `initialize(_:)` only when the app intentionally owns custom diagnostics, compatibility policy, or test setup before initialization
- `CodexAppServer` for process ownership, diagnostics, thread creation, stored-thread operations, MCP resource reads, feature-operation-event streams, and app-wide capability reads
- `CodexAppServer.makeLibrary(configuration:)` for app-wide stored-thread lists, cwd or repository grouping, stable worktree groups, repository/worktree filters, selected worktree or repository context, selected-worktree Git status, library-local selection, `CodexWorkspace.ProjectInfo` project identity, `CodexAppServer.ThreadSource` source badges, and model/MCP/hook snapshots that refresh when app-server app/skill/MCP state changes
- `CodexAppServer.fs`, `CodexAppServer.config`, and `CodexAppServer.extensions` for app-server-owned file metadata, directory/file reads, file discovery with match metadata, effective config, app, skill, plugin, collaboration-mode inventory, plugin detail reads, and already-configured marketplace upgrades
- `CodexAppServer.readMcpResource(_:)` for app-wide or thread-scoped MCP resource contents
- `SwiftASBFeaturePolicy` for feature-category defaults and host app authority, with `gitObservability`, `extensionInventory`, and `extensionMaintenance` enabled by default and mutation-oriented categories disabled until the app opts in
- `CodexAppServer.featureOperationEvents()` for human-readable SwiftASB-owned mutation records, such as marketplace maintenance attempts
- `CodexWorkspace` for session cwd, app-server-owned worktree snapshots, project identity, Git repository facts, selected Git status snapshots, active permission profile, and runtime filesystem/network permission facts
- `CodexThread` for conversation-scoped turn creation, request routing, archive/unarchive, thread actions, thread goals, and local history
- `CodexTurnHandle` for one active turn, including events, steering, interruption, request responses, and completion handoff
- `CodexThread.makeDashboard()` for thread-level current state
- `CodexTurnHandle.minimap` for active-turn current state
- `CodexThread.makeRecentTurns(...)`, `makeRecentFiles(...)`, and `makeRecentCommands(...)` for local history views
- `CodexAppServer.ThreadListQD`, `CodexFS.FileDiscoveryQD`, `CodexThread.HistoryWindowQD`, `CodexThread.RecentFilesQD`, and `CodexThread.RecentCommandsQD` when SwiftUI state needs repeatable query intent

## Implementation Workflow

1. Confirm the app's existing SwiftUI state pattern.
2. Read Apple docs for the framework behavior the change relies on.
3. Add SwiftASB as a package dependency only if it is not already present:
   - package URL: `https://github.com/gaelic-ghost/SwiftASB`
   - minimum version: `1.3.1` when using one-call startup with typed startup errors, app-wide library, stable worktree groups, repository/worktree filters, selected-worktree Git status, feature policy, feature-operation events, extension marketplace maintenance, project identity, thread source, filesystem match metadata, MCP resource reads, config warnings, extension inventory, workspace, query-descriptor, thread archive/unarchive, or recent-activity guidance; otherwise verify the support window in SwiftASB's README
   - product: `SwiftASB`
4. Choose the owner object:
   - app-wide model owns `CodexAppServer`
   - app-wide, scene, or workspace model owns `CodexAppServer.Library` when the UI needs stored-thread lists before a thread is selected
   - workspace, document, or conversation model owns `CodexThread`
   - active-turn method or model owns `CodexTurnHandle`
5. Start the app-server from an explicit async entrypoint, using `appServer.start(_:)` for normal clients and the lower-level `start()` plus `initialize(_:)` sequence only for custom diagnostics or tests.
6. Create or resume a thread through `CodexAppServer`.
7. Create `CodexAppServer.Library` from the app server when the UI has a launcher, sidebar, project browser, or app-wide diagnostics surface.
8. Use `appServer.fs`, `appServer.config`, `appServer.extensions`, `appServer.readMcpResource(_:)`, `CodexWorkspace`, and `SwiftASBFeaturePolicy` when SwiftUI needs filesystem, config, plugin/skill/app, collaboration-mode, marketplace-maintenance, MCP-resource, worktree, selected Git status, project identity, thread source, permission facts, or feature-category choices from Codex.
9. Create observable companions from the thread and current turn.
10. Render state from companions directly where possible.
11. Route approval and elicitation responses through the owning `CodexTurnHandle` or `CodexThread`.
12. Make startup, compatibility, turn, approval, cancellation, and shutdown errors human-readable.
13. Validate with the repository's documented SwiftPM or Xcode path.

## State Ownership Pattern

Prefer one app-facing model that makes ownership visible:

```swift
import Observation
import SwiftASB

@MainActor
@Observable
final class CodexWorkspaceModel {
    private let appServer = CodexAppServer()

    var library: CodexAppServer.Library?
    var thread: CodexThread?
    var dashboard: CodexThread.Dashboard?
    var currentMinimap: CodexTurnHandle.Minimap?
    var errorMessage: String?

    func start(workspacePath: String) async {
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

            let thread = try await appServer.startThread(
                .init(currentDirectoryPath: workspacePath)
            )
            self.thread = thread
            library = try await appServer.makeLibrary(
                configuration: .init(
                    sortedBy: .turnFinishedNewestFirst,
                    groupedBy: .repository,
                    query: .unarchived(limit: 30),
                    mcpServerStatusRequest: .init(detail: .toolsAndAuthOnly)
                )
            )
            dashboard = await thread.makeDashboard()
        } catch {
            errorMessage = "SwiftASB could not start the local Codex runtime: \(error)"
        }
    }

    func refreshAppSnapshots() async {
        await library?.refreshAppSnapshots()
    }

    func selectThread(_ threadID: String?) {
        library?.selectThread(threadID)
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

- Show `CodexAppServerStartupError` startup and compatibility failures before offering turn controls.
- Disable same-thread turn controls while one turn is active, or create a separate thread when concurrent work is truly intended.
- Use `library` for stored-thread sidebars, cwd or repository grouping, stable worktree groups, repository/worktree filters, selected worktree or repository context, selected Git status, project identity display, thread-source badges, library-local selection, app-wide model capabilities, MCP server status, and hook diagnostics.
- Show `library.selectedGitStatus`, `lastGitStatusReadAt`, and `latestGitStatusErrorDescription` when a selected-worktree status panel needs branch, SHA, remotes, dirty/untracked counts, or refresh failures.
- Use `CodexAppServer.ThreadListQD` when the same sidebar query should drive both direct `listThreads` reads and library loading.
- Use `CodexAppServer.fs` and `CodexFS.FileDiscoveryQD` for sandbox-safe file pickers, metadata panes, directory browsers, file-byte previews, watches, highlighted matches, and ranking explanations.
- Use `CodexAppServer.readMcpResource(_:)` when the UI needs to show text or blob resource contents advertised by a configured MCP server.
- Use `CodexAppServer.config`, `CodexAppServer.extensions`, and `CodexWorkspace` for diagnostics views that show effective config, requirements, available apps/skills/plugins, collaboration modes, worktree snapshots, selected Git status, project identity, active profile, and filesystem/network permissions.
- Use `SwiftASBFeaturePolicy` to present feature-category toggles only when the app actually lets users change SwiftASB-owned authority. Read-only Git observability and extension inventory are enabled by default; stronger mutation categories should stay deliberate app choices.
- Subscribe to `CodexAppServer.featureOperationEvents()` when SwiftUI needs to show marketplace-upgrade results or future SwiftASB-owned mutation records. Do not emit parallel UI events for routine read-only refreshes.
- Use `CodexThread.readGoal()`, `setGoal(_:)`, `clearGoal()`, `setName(_:)`, `archive()`, `unarchive()`, `updateMetadata(gitInfo:)`, `compactContext()`, and `rollbackLastTurns(_:)` from app-facing actions that already own the selected thread.
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
- Do not hide local Codex CLI discovery, compatibility, or startup failures behind generic "failed" messages; preserve `CodexAppServerStartupError` cases when mapping errors into UI text.
- Do not run multiple SwiftPM or Xcode build/test commands concurrently.
