---
name: diagnose-integration
description: Diagnose SwiftASB integration failures across Codex CLI discovery, app-server startup, initialization, threads, turns, approvals, inventory, MCP install/status/resources, reviews, shell commands, worktree grouping, selected Git status, project identity, thread source, filesystem/config/extension/workspace reads, feature policy, feature-operation events, diagnostics, history paging, and live-test isolation.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with SwiftASB v1.8.0 or newer, Swift 6, SwiftPM, SwiftUI, AppKit, CLI tools, package libraries, and local Codex app-server integrations.
metadata:
  owner: gaelic-ghost
  repo: socket
  package: SwiftASB
  category: swiftasb-diagnostics
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(xcodebuild:*)
---

# Diagnose SwiftASB Integration

## SwiftData And SwiftUI Rule

When a task combines SwiftData with SwiftUI, keep SwiftData directly coupled to SwiftUI through Apple's data-driven path: `modelContainer`, environment `modelContext`, `@Query`, SwiftData model objects, and bindings. Do not add repositories, stores, service layers, DTO mirrors, view-model caches, wrapper objects, or other abstraction layers between SwiftData and SwiftUI. If this skill is not the right owner for SwiftData-backed SwiftUI work, hand off to `apple-dev-skills:swiftui-app-architecture-workflow` instead of inventing an intermediate data layer.

## Purpose

Find the concrete failure point in a SwiftASB integration and explain it in terms the app maintainer can act on.

The job is not just to say that "Codex failed." A useful diagnosis identifies which boundary failed: package dependency wiring, Codex CLI discovery, app-server process startup, initialization, app-wide library or inventory refresh, worktree grouping/filtering, selected Git status, project identity or thread-source mapping, thread creation, stored-thread archive state, turn lifecycle, code-review start, shell-command execution, interactive request routing, filesystem/config/extension/MCP/workspace reads, feature policy, feature-operation events, model capability reads, MCP install/status/resource reads, hook diagnostics, diagnostic stream handling, local history reads, or live-test isolation.

## When To Use

- Use this skill when a SwiftASB-backed app, CLI, helper service, package, or test harness fails.
- Use this skill when logs mention `CodexAppServerError`, app-server transport failures, protocol failures, same-thread turn rejection, missing Codex CLI, inventory refresh problems, MCP install/status/resource issues, review-start failures, shell-command feature gates, approval or elicitation problems, filesystem/config/extension/workspace read failures, selected Git status failures, feature-category disabled errors, feature-operation event confusion, project identity or thread-source mismatches, config warnings, deprecation notices, remote-control status changes, or history paging failures.
- Use this skill before changing SwiftASB integration code when the failure boundary is still unclear.
- Use this skill when deciding whether a failing check should be a normal unit test, an opt-in live Codex probe, or an app-level integration test.

## Source Check

Verify current SwiftASB docs and public API before naming exact symbols:

- [SwiftASB GitHub repository](https://github.com/gaelic-ghost/SwiftASB)
- `README.md`
- `Sources/SwiftASB/SwiftASB.docc/GettingStartedWithSwiftASB.md`
- `Sources/SwiftASB/SwiftASB.docc/HandlingTurnProgressAndApprovals.md`
- `Sources/SwiftASB/SwiftASB.docc/ReadingDiagnosticsAndHistory.md`
- `Sources/SwiftASB/SwiftASB.docc/AppWideCapabilities.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexInventory.md`
- `Sources/SwiftASB/SwiftASB.docc/CodexMCP.md`
- `Sources/SwiftASB/SwiftASB.docc/ThreadHistoryAndObservables.md`
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

The current Codex app-server API includes lifecycle operations such as `thread/start`, `thread/resume`, `thread/fork`, `thread/archive`, `thread/unarchive`, `review/start`, `thread/shellCommand`, `turn/start`, `turn/steer`, `turn/interrupt`, filesystem reads and watches, config reads, extension inventory, MCP resource reads, `command/exec`, `model/list`, `modelProvider/capabilities/read`, `mcpServerStatus/list`, and `hooks/list`, plus notifications for thread status, command output, MCP startup status, config warnings, deprecation notices, remote-control status, hook activity, filesystem watch activity, and skills/plugin state. Use the official [Codex app-server docs](https://developers.openai.com/codex/app-server#api-overview) when the diagnosis depends on upstream app-server behavior rather than SwiftASB's public wrapper.

## Diagnostic Workflow

1. Capture the exact symptom:
   - thrown error text
   - app logs
   - failing test name
   - user-visible behavior
   - current branch and package version
2. Classify the boundary:
   - dependency wiring
   - Codex CLI discovery
   - app-server process startup
   - initialization
   - app-wide library, inventory, or snapshots
   - filesystem, config, extension, MCP, workspace-permission, worktree, selected-Git-status, project-identity, or thread-source reads
   - feature policy or feature-operation event handling
   - thread lifecycle
   - stored-thread archive or unarchive
   - review start or shell-command execution
   - turn lifecycle
   - approval or elicitation response handling
   - diagnostics stream
   - app-wide model, MCP, or hook snapshots
   - local history or remote turn paging
   - test isolation
3. Verify the smallest source-of-truth fact that can confirm or reject the classification.
4. Recommend the narrowest fix and the exact validation command.
5. If the failure is from active SwiftASB development, separate "consumer app bug" from "SwiftASB package issue" before editing either repo.

## Boundary Checks

### Dependency Wiring

Check that the package dependency is real and remote-fetchable:

```swift
.package(url: "https://github.com/gaelic-ghost/SwiftASB", from: "1.8.0")
```

Then check the target that talks to Codex depends on:

```swift
.product(name: "SwiftASB", package: "SwiftASB")
```

Do not commit machine-local package paths such as `/Users/...`, `~/...`, or `../SwiftASB` into public projects.

### Codex CLI Discovery

SwiftASB expects a local Codex CLI runtime. A diagnosis should tell the maintainer which executable was attempted and whether SwiftASB reported it as supported.

For SwiftASB `v1.8.0`, treat Codex CLI `0.142.x` as the preferred reviewed schema family. Compatible Codex CLI `0.141.x` installs remain in the prior-minor reviewed window; `0.140.x` is outside the default support window.

For normal clients, `CodexAppServer.start(_:)` returns `StartupSession.cliExecutableDiagnostics` after launching, validating the selected Codex CLI against the reviewed support window, and initializing. Use `CodexAppServer.cliExecutableDiagnostics()` after lower-level `start()` when a UI, CLI, or test intentionally needs to show executable facts before deciding whether to initialize.

- resolved executable path
- version string
- support-window compatibility
- likely runtime setup issue

If the app requires a fixed binary, inspect whether it passes `CodexAppServer.Configuration.codexExecutableURL`.

### App-Server Startup And Initialization

The expected order for most clients is:

1. create `CodexAppServer`
2. call `start(_:)` with client metadata
3. inspect `StartupSession.cliExecutableDiagnostics` when the UI needs selected-CLI facts
4. create, resume, or fork a thread

When diagnosing SwiftASB `v1.8.0` or newer, first check whether the thrown error is `CodexAppServerStartupError`. `codexCLINotFound` points at executable discovery, `incompatibleCodexCLI` and `unknownCodexCLIVersion` point at reviewed-support-window validation, `launchFailed` points at process startup, and `initializeFailed` points at protocol initialization or malformed client metadata.

Use the lower-level sequence only when the app intentionally owns custom diagnostics or compatibility decisions:

1. create `CodexAppServer`
2. call `start()`
3. inspect `cliExecutableDiagnostics()`
4. call `initialize(_:)` once with client metadata

If lower-level initialization fails, separate process startup from protocol initialization. Startup failures are usually executable, environment, sandbox, or process problems. Initialization failures are usually protocol, compatibility, or malformed client metadata problems.

### Thread Lifecycle

Use `CodexAppServer` for app-wide stored-thread operations and thread creation. Use `CodexThread` for conversation-scoped actions.

Check whether the app is:

- starting an ephemeral thread when it expects stored history
- resuming or forking the wrong thread id
- using the wrong current working directory
- expecting remote turn paging before history has materialized
- treating thread status notifications as terminal turn completion
- mixing thread goals, plan/agenda state, naming, archive/unarchive, metadata updates, compaction, or rollback into a UI surface that no longer owns the selected `CodexThread`

### App-Wide Library

Use `CodexAppServer.makeLibrary(configuration:)` when a UI or package needs stored-thread lists before choosing a thread.

If a library surface does not update, check whether the app is:

- expecting repository-root grouping when `Library.GroupedBy.cwd` matches exact app-server `cwd` metadata
- expecting worktree groups to be the same as visible grouping, instead of using the library's stable worktree groups and repository/worktree filters
- expecting `selectedGitStatus` to exist when `gitObservability` is disabled, no thread is selected, or the selected worktree has no usable cwd
- copying library arrays into a second state store instead of observing the library companion directly
- relying on app-wide snapshots before `refreshAppSnapshots()` has loaded model, MCP, and hook data
- grouping project rows by old ad hoc Git fields instead of `CodexWorkspace.ProjectInfo`
- drawing source badges from guessed client labels instead of `CodexAppServer.ThreadSource`
- ignoring app-server app/skill/MCP status notifications that now trigger snapshot refreshes
- treating `selectedThreadID` as stored Codex metadata instead of library-local UI selection state
- hiding reconciliation or snapshot errors from the user-facing diagnostics view
- hiding `latestGitStatusErrorDescription` or treating selected Git status refresh as direct app-process filesystem access instead of sandboxed app-server `command/exec`

### Filesystem, Config, Inventory, Extensions, MCP, And Workspace Facts

Use app-server-owned fact surfaces when a sandboxed app, helper, or package should not inspect machine state directly:

- `CodexAppServer.fs` for metadata, directory entries, file bytes, watches, and bounded fuzzy file discovery
- `CodexFS.FileDiscoveryQD` when file-picker or search intent should be repeatable state
- `CodexFS.FileDiscoveryHit.matchKind`, `matchedFileNameRanges`, `matchedRelativePathRanges`, and `rankingReasons` when fuzzy search UI ranking or highlighting looks wrong
- `CodexAppServer.config` for effective config and requirements reads
- `CodexAppServer.makeInventory(configuration:)` for routine model capabilities, global MCP summaries, hook diagnostics, apps, skills, plugins, and collaboration modes
- `CodexAppServer.extensions` for advanced extension pagination, plugin-detail inspection, and already-configured marketplace upgrades
- `CodexAppServer.extensions.upgradeMarketplace(_:)` for upgrading an already-configured plugin marketplace when `extensionMaintenance` is enabled
- `CodexAppServer.mcp.install(_:)` for MCP installs that write Codex config and refresh MCP status
- `CodexAppServer.mcp.statusSnapshot()` and `CodexAppServer.mcp.readResource(...)` for full MCP details and app-wide or thread-scoped MCP resource contents
- `SwiftASBFeaturePolicy` for feature-category defaults and host app authority
- `CodexAppServer.featureOperationEvents()` for human-readable SwiftASB-owned mutation records
- `CodexWorkspace` values on requests and thread sessions for active permission profile, cwd, worktree snapshots, project identity, Git repository facts, selected Git status snapshots, and filesystem/network permissions

If one of these surfaces fails, check whether the app passed the right current directory, expected direct disk semantics from an app-server read, asked for unpromoted mutation behavior, used `extensions` where `Inventory` is the better routine UI surface, disabled the relevant feature category, or hid app-server permission/profile facts behind a local fallback.

### Feature Policy And Operation Events

SwiftASB feature policy is separate from Codex approval requests. It decides whether SwiftASB-owned convenience features such as Git observability or extension maintenance are eligible to run; it does not answer a turn's approval prompt.

If a feature operation fails, check:

- whether `CodexAppServer.Configuration.featurePolicy` or `CodexAppServer.Library.Configuration.featurePolicy` disables the category
- whether the failure is from SwiftASB's feature gate or from the underlying app-server method
- whether `featureOperationEvents()` emitted a started, succeeded, failed, cancelled, or skipped event
- whether the event names affected paths, commands, app-server method, intent kind, rollback availability, and diagnostic text

Routine read-only refreshes should usually be quiet. Missing feature-operation events for Git status reads or extension inventory is expected unless a mutation or maintenance action ran.

### Turn Lifecycle

Use `CodexThread.startTextTurn(...)` to create a normal `CodexTurnHandle`. Use `CodexThread.startPlanningTurn(...)` when the user chose plan mode; it sets app-server collaboration mode instead of sending slash-command text through the prompt. Use that handle for active-turn events, steering, interruption, interactive responses, and completion handoff.

If a turn does not behave as expected, check:

- whether another turn is already active on the same thread
- whether the app is consuming `turn.events`
- whether terminal completion is being detected
- whether `complete()` is called only after terminal state when a sealed local snapshot is needed
- whether cancellation uses `interrupt()` rather than dropping the handle silently
- whether a planning control used `startPlanningTurn(...)` or `TurnCollaborationMode.plan(...)` instead of prompt text
- whether custom switches over `CodexTurnItem.Kind` handle `.sleep` instead of treating Codex CLI `0.142.x` sleep items as unknown failures

For plan and goal UI, use `CodexThread.makeAgenda()` to read the current goal, accepted plan, proposed plan deltas, and summary titles. If agenda state looks stale, check that the UI observes the `Agenda` object itself, that `makeAgenda()` succeeded in reading the initial goal, and that the app is not copying plan arrays into disconnected state. Goal mutations should go through `Agenda.setGoal(...)`, `pauseGoal()`, `resumeGoal()`, or `clearGoal()` when the agenda owns the view state.

SwiftASB rejects overlapping turns on the same thread with `CodexAppServerError.invalidState` because the live app-server does not expose a reliable independent lifecycle for same-thread overlap.

### Review Starts And Shell Commands

Use `CodexThread.startReview(against:placement:)` for app-server reviews. Check the subject and placement first: inline reviews run on the current thread, while detached reviews return a review-thread id through `CodexReviewHandle`.

Use `CodexThread.sendShellCommand(_:)` only for explicit user-level shell execution. It wraps app-server `thread/shellCommand`, preserves shell syntax, and does not inherit the thread sandbox policy. If it fails, check whether `SwiftASBFeatureCategory.ID.shellCommandExecution` is enabled before debugging transport behavior.

### Approvals And Elicitation

Approval and elicitation requests are not diagnostics. They are server-originated requests that need typed responses.

Use the same owner that received the request:

- `CodexTurnHandle.respond(to:with:)` for active-turn requests
- `CodexThread.respond(to:with:)` for thread-scoped requests

If a request response fails, check that the response is sent through the matching thread or turn owner and that the app is not trying to answer a passive diagnostic event.

### Diagnostics Stream

`CodexAppServer.diagnosticEvents()` reports passive runtime diagnostics such as:

- `warning`
- `guardianWarning`
- `modelRerouted`
- `modelVerification`
- `configWarning`
- `deprecationNotice`
- `mcpServerStatusChanged`
- `remoteControlStatusChanged`

Diagnostics explain what the runtime is warning about. They are not approval prompts and do not need responses.

### Inventory, Models, MCP Status, And Hooks

Use app-wide snapshots for settings, inspectors, and runtime health:

- `CodexAppServer.makeInventory(configuration:)`
- `CodexAppServer.listModels(...)`
- `CodexAppServer.readModelCapabilities()`
- `CodexAppServer.mcp.statusSnapshot()`
- `CodexAppServer.mcp.readResource(...)`
- `CodexAppServer.listHooks(...)`
- `CodexAppServer.Library.refreshAppSnapshots()`

If a model, MCP, hook, app, skill, plugin, or collaboration-mode issue appears in the UI, inspect whether the app is showing Inventory state, model feature gates, configured server status, auth state, tools/resources metadata, hook diagnostics, or startup notifications. Do not infer runtime health only from a failed turn unless the app-wide status surface has also been checked.

### History And Paging

Distinguish local history helpers from direct app-server paging.

Use recent companions and local history helpers for UI history:

- `CodexThread.makeRecentTurns(...)`
- `CodexThread.makeRecentFiles(...)`
- `CodexThread.makeRecentCommands(...)`
- `CodexThread.HistoryWindowQD`
- `CodexThread.RecentFilesQD`
- `CodexThread.RecentCommandsQD`
- `CodexThread.readRecentTurnHistoryWindow(limit:)`
- `CodexThread.windowAroundTurn(...)`
- `CodexThread.windowAroundItem(...)`

Use `CodexAppServer.listThreadTurns(...)` when the app specifically needs direct app-server paging and is prepared to surface app-server failures.

Recent companions may start from an empty local view for ephemeral or not-yet-materialized history while still listening to live events. That is different from a lower-level remote paging failure.

### Test Isolation

Keep normal package tests deterministic. Use live Codex probes only when the purpose is runtime compatibility or real app-server behavior.

Live probes should be:

- opt-in by environment flag
- run in a temporary workspace
- bounded by hard timeouts
- serial rather than parallel with other SwiftPM or Xcode test runs
- written so failure text names the exact runtime boundary

## Output Shape

Return:

1. `Most likely boundary`: the narrow failure boundary.
2. `Evidence`: the log, code path, command, or API behavior that supports it.
3. `What it means`: plain-language impact for the app or package.
4. `Fix`: one narrow repair path.
5. `Validation`: exact command or manual check.
6. `Escalate to SwiftASB?`: yes/no, with the reason.

## Guardrails

- Do not call every thrown error a SwiftASB bug.
- Do not change the consumer app and SwiftASB package in the same pass unless the evidence proves both need edits.
- Do not run live Codex probes as default unit tests.
- Do not hide exact operation names inside vague messages like "failed" or "invalid."
- Do not answer approval or elicitation requests as if they were diagnostics.
- Do not use raw generated wire types as the consumer-facing repair path unless the user is intentionally debugging protocol internals.
