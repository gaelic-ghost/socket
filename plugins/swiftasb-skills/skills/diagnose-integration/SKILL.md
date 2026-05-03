---
name: diagnose-integration
description: Diagnose SwiftASB integration failures across Codex CLI discovery, app-server startup, initialization, threads, turns, approvals, MCP status, diagnostics, history paging, and live-test isolation.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with SwiftASB v1.0.0 or newer, Swift 6, SwiftPM, SwiftUI, AppKit, CLI tools, package libraries, and local Codex app-server integrations.
metadata:
  owner: gaelic-ghost
  repo: socket
  package: SwiftASB
  category: swiftasb-diagnostics
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(xcodebuild:*)
---

# Diagnose SwiftASB Integration

## Purpose

Find the concrete failure point in a SwiftASB integration and explain it in terms the app maintainer can act on.

The job is not just to say that "Codex failed." A useful diagnosis identifies which boundary failed: package dependency wiring, Codex CLI discovery, app-server process startup, initialization, thread creation, turn lifecycle, interactive request routing, MCP status, diagnostic stream handling, local history reads, or live-test isolation.

## When To Use

- Use this skill when a SwiftASB-backed app, CLI, helper service, package, or test harness fails.
- Use this skill when logs mention `CodexAppServerError`, app-server transport failures, protocol failures, same-thread turn rejection, missing Codex CLI, MCP status issues, approval or elicitation problems, or history paging failures.
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
- `Sources/SwiftASB/Public/CodexDiagnostics.swift`
- `Sources/SwiftASB/Public/CodexErrors.swift`

The current Codex app-server API includes lifecycle operations such as `thread/start`, `thread/resume`, `thread/fork`, `turn/start`, `turn/steer`, `turn/interrupt`, `model/list`, and `mcpServerStatus/list`, plus notifications for thread status, command output, MCP startup status, and skills/plugin state. Use the official [Codex app-server docs](https://developers.openai.com/codex/app-server#api-overview) when the diagnosis depends on upstream app-server behavior rather than SwiftASB's public wrapper.

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
   - thread lifecycle
   - turn lifecycle
   - approval or elicitation response handling
   - diagnostics stream
   - app-wide model or MCP capability snapshots
   - local history or remote turn paging
   - test isolation
3. Verify the smallest source-of-truth fact that can confirm or reject the classification.
4. Recommend the narrowest fix and the exact validation command.
5. If the failure is from active SwiftASB development, separate "consumer app bug" from "SwiftASB package issue" before editing either repo.

## Boundary Checks

### Dependency Wiring

Check that the package dependency is real and remote-fetchable:

```swift
.package(url: "https://github.com/gaelic-ghost/SwiftASB", from: "1.0.0")
```

Then check the target that talks to Codex depends on:

```swift
.product(name: "SwiftASB", package: "SwiftASB")
```

Do not commit machine-local package paths such as `/Users/...`, `~/...`, or `../SwiftASB` into public projects.

### Codex CLI Discovery

SwiftASB expects a local Codex CLI runtime. A diagnosis should tell the maintainer which executable was attempted and whether SwiftASB reported it as supported.

Use `CodexAppServer.cliExecutableDiagnostics()` after `start()` and before or after initialization when a UI or CLI needs to show:

- resolved executable path
- version string
- support-window compatibility
- likely runtime setup issue

If the app requires a fixed binary, inspect whether it passes `CodexAppServer.Configuration.codexExecutableURL`.

### App-Server Startup And Initialization

The expected order is:

1. create `CodexAppServer`
2. call `start()`
3. inspect `cliExecutableDiagnostics()` when needed
4. call `initialize(_:)` once with client metadata
5. create, resume, or fork a thread

If initialization fails, separate process startup from protocol initialization. Startup failures are usually executable, environment, sandbox, or process problems. Initialization failures are usually protocol, compatibility, or malformed client metadata problems.

### Thread Lifecycle

Use `CodexAppServer` for app-wide stored-thread operations and thread creation. Use `CodexThread` for conversation-scoped actions.

Check whether the app is:

- starting an ephemeral thread when it expects stored history
- resuming or forking the wrong thread id
- using the wrong current working directory
- expecting remote turn paging before history has materialized
- treating thread status notifications as terminal turn completion

### Turn Lifecycle

Use `CodexThread.startTextTurn(...)` to create a `CodexTurnHandle`. Use that handle for active-turn events, steering, interruption, interactive responses, and completion handoff.

If a turn does not behave as expected, check:

- whether another turn is already active on the same thread
- whether the app is consuming `turn.events`
- whether terminal completion is being detected
- whether `complete()` is called only after terminal state when a sealed local snapshot is needed
- whether cancellation uses `interrupt()` rather than dropping the handle silently

SwiftASB rejects overlapping turns on the same thread with `CodexAppServerError.invalidState` because the live app-server does not expose a reliable independent lifecycle for same-thread overlap.

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

Diagnostics explain what the runtime is warning about. They are not approval prompts and do not need responses.

### Models And MCP Status

Use app-wide snapshots for settings, inspectors, and runtime health:

- `CodexAppServer.listModels(...)`
- `CodexAppServer.listMcpServerStatuses(...)`

If an MCP issue appears in the UI, inspect whether the app is showing configured server status, auth state, tools/resources metadata, or startup notifications. Do not infer MCP health only from a failed turn unless the app-wide status surface has also been checked.

### History And Paging

Distinguish local history helpers from direct app-server paging.

Use recent companions and local history helpers for UI history:

- `CodexThread.makeRecentTurns(...)`
- `CodexThread.makeRecentFiles(...)`
- `CodexThread.makeRecentCommands(...)`
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
