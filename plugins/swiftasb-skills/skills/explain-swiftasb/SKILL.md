---
name: explain-swiftasb
description: Explain SwiftASB in user-facing terms, including what it does, what it does not do, adoption tradeoffs, licensing, and when it is or is not the right foundation for a Swift app or package.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with SwiftASB v1.0.3 or newer, Swift 6, SwiftPM, SwiftUI, AppKit, and local Codex app-server integrations.
metadata:
  owner: gaelic-ghost
  repo: socket
  package: SwiftASB
  category: swiftasb-explanation
allowed-tools: Read Bash(rg:*) Bash(git:*)
---

# Explain SwiftASB

## Purpose

Help a user understand whether [SwiftASB](https://github.com/gaelic-ghost/SwiftASB) is the right foundation for their Swift app, tool, or package before implementation starts.

Start with the real job: SwiftASB lets Swift code drive the local Codex app-server through a Swift-native API. It owns the local Codex subprocess, typed request and response conversion, app-wide stored-thread library state, thread and turn handles, interactive request handling, diagnostics, local history reads, and SwiftUI-friendly observable companions.

## When To Use

- Use this skill when a user asks what SwiftASB is or whether they should build on it.
- Use this skill before planning a SwiftASB integration when the app shape or adoption tradeoffs are unclear.
- Use this skill when an agent needs to explain SwiftASB to a non-maintainer user in plain language.
- Use this skill when licensing, runtime dependency, or API-boundary concerns affect adoption.

## Source Check

Before giving exact API claims, inspect the current SwiftASB source of truth:

- [SwiftASB GitHub repository](https://github.com/gaelic-ghost/SwiftASB)
- `README.md`
- `Sources/SwiftASB/SwiftASB.docc/`
- the public files under `Sources/SwiftASB/Public/`
- the latest release notes or tags

As of SwiftASB `v1.0.3`, the supported public surface centers on:

- `CodexAppServer`, the owner of the local Codex subprocess, stored-thread operations, app-wide library creation, and capability reads
- `CodexAppServer.Library`, the app-wide observable companion for stored-thread lists, cwd grouping, selection, Git branch metadata, and model/MCP/hook snapshots
- `CodexThread`, the handle for one Codex conversation thread
- `CodexTurnHandle`, the handle for one active turn
- observable companions such as `CodexThread.Dashboard`, `CodexTurnHandle.Minimap`, `RecentTurns`, `RecentFiles`, and `RecentCommands`

Generated `CodexWire...` models are internal scaffolding, not the recommended app-facing API.

## Explanation Workflow

1. Identify what the user wants to build.
2. State SwiftASB's job in one plain paragraph.
3. Name the runtime dependency: a local Codex CLI/app-server must be available.
4. Explain the main public owners only after the practical job is clear.
5. Describe the adoption benefits:
   - Swift-native values instead of raw JSON-RPC payloads
   - async streams for live thread and turn events
   - typed approval and elicitation responses
   - observable companions for app-wide libraries, SwiftUI inspectors, rails, and progress views
   - local history helpers for recent turns, files, and commands
6. Describe the adoption costs:
   - the app depends on a local Codex runtime
   - compatibility follows SwiftASB's reviewed Codex CLI support window
   - same-thread overlapping turns are rejected client-side
   - generated wire features are not all public API
   - users must understand the package license before commercial use
7. Give a clear fit recommendation.

## Fit Guidance

SwiftASB is a good fit when the user needs a Swift app or package to:

- start or control local Codex work
- show live command, file-edit, MCP, hook, approval, diagnostic, library, or history state
- build SwiftUI or AppKit surfaces around Codex conversations
- keep raw app-server protocol models out of their own public API
- use typed Swift handles for threads, turns, approvals, elicitation, diagnostics, and recent history

SwiftASB is probably not the right first choice when the user needs:

- a hosted AI SDK unrelated to the local Codex app-server
- a server-side multi-user agent platform
- a cross-platform non-Apple UI toolkit as the primary target
- a stable public wrapper for every experimental Codex app-server feature
- an integration that cannot depend on a local Codex CLI runtime

## Output Shape

Answer in this order:

1. `Recommendation`: one direct fit call.
2. `What SwiftASB would do here`: plain-language role.
3. `What the app would own`: UI, product behavior, persistence choices, and user policy.
4. `What SwiftASB would own`: app-server process, app-wide library state, typed thread and turn API, events, requests, diagnostics, and companions.
5. `Tradeoffs`: runtime, compatibility, same-thread turn policy, and licensing.
6. `Next integration step`: the next skill or repo action.

## Handoffs

- Use `swiftasb:choose-integration-shape` when the user wants to proceed but the app shape is not settled.
- Use `swiftasb:build-swiftui-app` when the chosen target is a SwiftUI app.
- Use `swiftasb:build-appkit-app` when the chosen target is an AppKit app.
- Use `swiftasb:build-swift-package` when the chosen target is a package library, command-line package, helper package, or test harness.
- Use `apple-dev-skills:explore-apple-swift-docs` before making Apple framework claims.
- Use Apple build or Xcode workflow skills when the task shifts from explanation to project execution.

## Guardrails

- Do not call SwiftASB a general AI SDK.
- Do not present generated wire models as the public consumer API.
- Do not promise support for app-server families that SwiftASB has not promoted into public API.
- Do not hide the local Codex runtime dependency.
- Do not flatten licensing into "open source" without explaining that SwiftASB's package license is documented in its own repository.
