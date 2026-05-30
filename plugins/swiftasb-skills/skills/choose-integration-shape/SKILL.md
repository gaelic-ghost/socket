---
name: choose-integration-shape
description: Choose the right SwiftASB integration shape for a SwiftUI app, AppKit app, command-line tool, helper service, package library, test harness, or mixed Swift project before implementation starts.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with SwiftASB v1.6.0 or newer, Swift 6, SwiftPM, SwiftUI, AppKit, and local Codex app-server integrations.
metadata:
  owner: gaelic-ghost
  repo: socket
  package: SwiftASB
  category: swiftasb-planning
allowed-tools: Read Bash(rg:*) Bash(git:*)
---

# Choose SwiftASB Integration Shape

## Purpose

Pick the smallest correct way for a project to use [SwiftASB](https://github.com/gaelic-ghost/SwiftASB) before code changes begin.

The practical decision is who owns the local Codex runtime, who owns the app-wide stored-thread library and inventory companions, who owns each conversation thread and its agenda, where active turn state is shown, where app-server-owned worktree, selected Git status, project identity, thread source, filesystem/config/extension/MCP facts appear, which SwiftASB feature categories the host app enables, and how much SwiftASB behavior should be exposed through the user's own app or package API.

## When To Use

- Use this skill when a user wants to build on SwiftASB but has not chosen the app or package architecture.
- Use this skill before adding SwiftASB to a SwiftUI, AppKit, command-line, helper-service, or package-only project.
- Use this skill when an existing project has mixed UI, package, and helper targets and needs a clear ownership decision.
- Use this skill when the agent needs to explain the integration plan before editing code.

## Source Check

Verify current SwiftASB docs and public API before naming exact symbols:

- [SwiftASB GitHub repository](https://github.com/gaelic-ghost/SwiftASB)
- `README.md`
- `Sources/SwiftASB/SwiftASB.docc/GettingStartedWithSwiftASB.md`
- `Sources/SwiftASB/SwiftASB.docc/SwiftUIObservableCompanions.md`
- `Sources/SwiftASB/SwiftASB.docc/ThreadHistoryAndObservables.md`
- `Sources/SwiftASB/SwiftASB.docc/AppWideCapabilities.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexInventory.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexMCP.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexFS.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexConfig.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexExtensions.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexWorkspace.md`
- `Sources/SwiftASB/SwiftASB.docc/FeaturePermissionPolicy.md`
- `Sources/SwiftASB/SwiftASB.docc/ThreadHistoryAndObservables.md`
- `Sources/SwiftASB/Public/`

For SwiftUI, AppKit, SwiftPM, or Xcode behavior, use Apple Dev Skills and Apple documentation first. SwiftASB chooses the Codex integration shape; Apple frameworks still own app lifecycle, view updates, window behavior, and project execution.

## Classification Workflow

1. Inspect the repository shape:
   - SwiftPM package
   - Xcode app project or workspace
   - SwiftUI app
   - AppKit app
   - command-line executable
   - helper daemon or local service
   - tests or integration harness only
2. Identify the user-visible job:
   - chat or transcript UI
   - workspace inspector
   - sandbox-safe file browser or fuzzy file picker
   - command/file activity monitor
   - approval and elicitation UI
   - model, MCP, hook, config, extension, remote-control, feature-operation, or permission diagnostics
   - selected-worktree Git status or marketplace-maintenance UI
   - app-wide inventory UI, MCP install UI, MCP resource viewer, or MCP inspector
   - plan/goal UI, code-review UI, or explicit shell-command UI
   - package API for other apps
   - automation or one-shot task execution
3. Choose the SwiftASB owner:
   - app-wide model owns `CodexAppServer`
   - normal clients start with `CodexAppServer.start(_:)` so startup, compatibility validation, initialization, selected-CLI diagnostics, and typed startup errors stay in one SwiftASB-owned call
   - lower-level startup remains a custom diagnostics or test path when the app must inspect the selected executable before deciding whether to initialize
   - app-wide or window-scoped launcher model owns `CodexAppServer.Library` when the UI lists stored threads before a thread is chosen
   - document or workspace model owns `CodexThread`
   - active task model owns `CodexTurnHandle`
   - routine app-wide catalogs stay on `CodexAppServer.makeInventory(configuration:)`; advanced extension pagination and marketplace upgrades stay on `CodexAppServer.extensions`
   - app-server-owned filesystem/config/extension/MCP/workspace/worktree/project-identity/thread-source reads stay on `CodexAppServer.fs`, `CodexAppServer.config`, `CodexAppServer.extensions`, `CodexAppServer.mcp`, and `CodexWorkspace`
   - app-wide feature authority stays in `SwiftASBFeaturePolicy`, and mutation visibility comes from `CodexAppServer.featureOperationEvents()`
   - plan and goal UI stays on `CodexThread.makeAgenda()`, `CodexThread.startPlanningTurn(...)`, and `CodexThread` goal helpers
   - code-review starts stay on `CodexThread.startReview(against:placement:)`
   - user-level shell commands stay behind a visible host-app opt-in to `shellCommandExecution`
4. Choose the state surface:
   - SwiftUI observable companions
   - app-wide library companion
   - AppKit controller-owned models
   - command-line event loop
   - package API values and async streams
   - test harness mocks or live opt-in probes
5. Name validation:
   - SwiftPM packages: `swift build` and `swift test`
   - Xcode apps: repository-documented Xcode build and test path
   - live Codex integration: opt-in flags, temporary workspaces, and hard timeouts only

## Shape Recommendations

### SwiftUI App

Use an app or workspace model to own `CodexAppServer`, then create a `CodexAppServer.Library` when the UI needs a launcher, sidebar, or project browser before choosing a thread. Create a `CodexThread` per conversation or workspace. Store SwiftASB observable companions in a view model instead of replaying raw events into unrelated state.

Prefer:

- `CodexAppServer.makeLibrary(configuration:)` for stored-thread sidebars, cwd or repository grouping, stable worktree groups, repository/worktree filters, selected worktree or repository context, library-local selection, `CodexWorkspace.ProjectInfo` project identity, `CodexAppServer.ThreadSource` source facts, and app-wide model/MCP/hook snapshots that refresh when app-server app/skill/MCP state changes
- `CodexAppServer.makeInventory(configuration:)` for routine app-wide capability and extension UI such as model capabilities, global MCP summaries, hook diagnostics, apps, skills, plugins, and collaboration modes
- `SwiftASBFeaturePolicy` on `CodexAppServer.Configuration` or `CodexAppServer.Library.Configuration` when the app should enable, disable, or present feature categories such as `gitObservability`, `extensionInventory`, and `extensionMaintenance`
- `CodexAppServer.Library.selectedGitStatus` and `refreshSelectedGitStatus()` for selected-worktree Git facts when `gitObservability` is enabled
- `CodexAppServer.featureOperationEvents()` for human-readable records of SwiftASB-owned mutations such as marketplace upgrades
- `CodexAppServer.ThreadListQD` for repeatable thread-list intent across direct reads and library loading
- `CodexAppServer.fs` and `CodexFS.FileDiscoveryQD` for sandbox-safe metadata, directory, file-byte, watch, fuzzy file-discovery UI, highlight ranges, and ranking explanations
- `CodexAppServer.mcp.install(_:)`, `statusSnapshot()`, and `readResource(...)` for MCP installs, full MCP detail reads, and app-wide or thread-scoped MCP resource contents
- `CodexAppServer.config`, `CodexAppServer.extensions`, and `CodexWorkspace` for diagnostics, worktree snapshots, selected Git status, project identity, repository facts, permissions, advanced extension pagination, plugin-detail inspection, marketplace maintenance, and runtime facts that should come from the app-server
- `CodexThread.startReview(against:placement:)` for app-server code review UI
- `CodexThread.sendShellCommand(_:)` only when the app deliberately exposes high-impact user-level shell execution and enables `shellCommandExecution`
- `CodexThread.makeDashboard()` for thread-wide activity
- `CodexThread.makeAgenda()` and `CodexThread.startPlanningTurn(...)` for current goal, accepted plan, proposed plan text, and explicit plan-mode controls
- `CodexTurnHandle.minimap` for active turn state
- recent companions for inspector rails and completed history
- explicit user-visible error strings for `CodexAppServerStartupError`, compatibility, and turn failures

Handoff: `swiftasb:build-swiftui-app`.

### AppKit App

Use an application, document, or window-controller-owned model to hold SwiftASB handles. Keep UI mutation on the main actor and make lifetime explicit so windows do not accidentally keep app-server work alive after close.

Plan:

- where `CodexAppServer` starts and stops
- whether the app, scene, window, or document owns a `CodexAppServer.Library`
- which window or document owns each `CodexThread`
- where filesystem/config/extension/MCP/workspace/worktree/selected-Git-status/project-identity/thread-source facts are shown without direct app-process filesystem assumptions
- whether the helper exposes feature-category toggles or only uses SwiftASB defaults
- how menu or toolbar actions start, steer, interrupt, or inspect turns
- how streamed events reach AppKit views safely

Handoff: `swiftasb:build-appkit-app`.

### Command-Line Tool

Use `CodexAppServer` in a short-lived async main flow. Call `start(_:)`, create or resume a thread, start a turn, stream terminal output or summary, and stop the app-server predictably. Use the lower-level startup calls only when the tool needs a diagnostics screen or custom compatibility decision before initialization.

Avoid building SwiftUI observable companions unless the tool also feeds a UI.

### Helper Service

Use a long-lived owner for `CodexAppServer`, but keep library refreshes, thread ownership, and cancellation explicit. Document how the service starts, stops, exposes status, and avoids overlapping same-thread turns.

Treat service interruption, process cleanup, and logs as part of the product behavior.

Use `CodexAppServer.fs`, `CodexAppServer.config`, `CodexAppServer.makeInventory(configuration:)`, `CodexAppServer.extensions`, `CodexAppServer.mcp`, `CodexWorkspace`, and `SwiftASBFeaturePolicy` when the service needs Codex-owned workspace, worktree, selected Git status, project identity, thread source, config, plugin, skill, MCP resource, filesystem facts, inventory, or extension-maintenance authority instead of reading local state directly.

### Package Library

Expose the package's own narrow API instead of re-exporting all SwiftASB types by default. Use SwiftASB internally unless the consumer genuinely needs direct `CodexAppServer`, `CodexThread`, or `CodexTurnHandle` access.

Keep live Codex tests opt-in and timeout-bounded.

Handoff: `swiftasb:build-swift-package`.

### Test Harness

Prefer mock or deterministic transport tests for package behavior. Use live Codex probes only when the test's purpose is runtime compatibility, and isolate them with temporary directories and environment flags.

## Output Shape

Return:

1. `Chosen shape`: one of SwiftUI app, AppKit app, command-line tool, helper service, package library, test harness, or mixed.
2. `SwiftASB owners`: who owns `CodexAppServer`, `CodexThread`, and `CodexTurnHandle`.
3. `State surface`: library companion, observable companions, AppKit model, CLI stream, package API, or tests.
4. `User-visible behavior`: progress, approvals, errors, diagnostics, history, worktree, project identity, thread source, filesystem/config/extension/MCP/workspace facts, cancellation, and, when relevant, inventory, feature-policy choices, mutation-operation events, selected-worktree Git status, MCP installs, code reviews, shell commands, and marketplace maintenance.
5. `Validation path`: exact build/test family to run.
6. `Next skill`: the next SwiftASB or Apple workflow skill.

## Guardrails

- Do not add a new manager or coordinator without naming the concrete ownership problem it solves.
- Do not leak raw generated wire types into the user's public API unless the user explicitly asks for protocol-level work.
- Do not hide same-thread overlap rejection; design the UI or API around one active turn per thread.
- Do not run live Codex probes as ordinary unit tests.
- Do not choose Apple framework architecture without reading the relevant Apple docs first.
- Do not expose `sendShellCommand(_:)` as a routine helper; treat it as explicit, high-impact user-level shell execution.
