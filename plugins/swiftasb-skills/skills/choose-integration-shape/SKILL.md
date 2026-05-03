---
name: choose-integration-shape
description: Choose the right SwiftASB integration shape for a SwiftUI app, AppKit app, command-line tool, helper service, package library, test harness, or mixed Swift project before implementation starts.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with SwiftASB v1.0.1 or newer, Swift 6, SwiftPM, SwiftUI, AppKit, and local Codex app-server integrations.
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

The practical decision is who owns the local Codex runtime, who owns each conversation thread, where active turn state is shown, and how much SwiftASB behavior should be exposed through the user's own app or package API.

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
   - command/file activity monitor
   - approval and elicitation UI
   - package API for other apps
   - automation or one-shot task execution
3. Choose the SwiftASB owner:
   - app-wide model owns `CodexAppServer`
   - document or workspace model owns `CodexThread`
   - active task model owns `CodexTurnHandle`
4. Choose the state surface:
   - SwiftUI observable companions
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

Use an app or workspace model to own `CodexAppServer`, then create a `CodexThread` per conversation or workspace. Store SwiftASB observable companions in a view model instead of replaying raw events into unrelated state.

Prefer:

- `CodexThread.makeDashboard()` for thread-wide activity
- `CodexTurnHandle.minimap` for active turn state
- recent companions for inspector rails and completed history
- explicit user-visible error strings for startup, compatibility, and turn failures

Handoff: `swiftasb:build-swiftui-app`.

### AppKit App

Use an application, document, or window-controller-owned model to hold SwiftASB handles. Keep UI mutation on the main actor and make lifetime explicit so windows do not accidentally keep app-server work alive after close.

Plan:

- where `CodexAppServer` starts and stops
- which window or document owns each `CodexThread`
- how menu or toolbar actions start, steer, interrupt, or inspect turns
- how streamed events reach AppKit views safely

Handoff: `swiftasb:build-appkit-app`.

### Command-Line Tool

Use `CodexAppServer` in a short-lived async main flow. Start, initialize, create or resume a thread, start a turn, stream terminal output or summary, and stop the app-server predictably.

Avoid building SwiftUI observable companions unless the tool also feeds a UI.

### Helper Service

Use a long-lived owner for `CodexAppServer`, but keep thread ownership and cancellation explicit. Document how the service starts, stops, exposes status, and avoids overlapping same-thread turns.

Treat service interruption, process cleanup, and logs as part of the product behavior.

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
3. `State surface`: observable companions, AppKit model, CLI stream, package API, or tests.
4. `User-visible behavior`: progress, approvals, errors, diagnostics, history, and cancellation.
5. `Validation path`: exact build/test family to run.
6. `Next skill`: the next SwiftASB or Apple workflow skill.

## Guardrails

- Do not add a new manager or coordinator without naming the concrete ownership problem it solves.
- Do not leak raw generated wire types into the user's public API unless the user explicitly asks for protocol-level work.
- Do not hide same-thread overlap rejection; design the UI or API around one active turn per thread.
- Do not run live Codex probes as ordinary unit tests.
- Do not choose Apple framework architecture without reading the relevant Apple docs first.
