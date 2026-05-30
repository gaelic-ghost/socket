---
name: build-swift-package
description: Build or refactor a Swift package API on top of SwiftASB without leaking raw app-server wire models, while keeping live Codex probes opt-in, isolated, timeout-bounded, and documented.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with SwiftASB v1.5.0 or newer, Swift 6, SwiftPM, package libraries, command-line tools, and local Codex app-server integrations.
metadata:
  owner: gaelic-ghost
  repo: socket
  package: SwiftASB
  category: swiftasb-package
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*)
---

# Build Swift Package With SwiftASB

## Purpose

Help a Swift package use [SwiftASB](https://github.com/gaelic-ghost/SwiftASB) internally while exposing the package's own small, Swift-native API to its callers.

The real job is to keep the package's public surface understandable. SwiftASB can own Codex runtime startup, app-wide library and inventory state, stable worktree groups, repository/worktree filters, selected-worktree Git status, project identity and thread-source facts, app-server-owned worktree snapshots, app-server-routed filesystem/config/extension/MCP reads, workspace permission facts, feature policy, feature-operation events, code-review and shell-command entry points, typed threads, turns, events, diagnostics, query descriptors, and local history inside the implementation, but the package author should decide deliberately whether consumers see SwiftASB handles directly or a narrower domain-specific API.

## Required Documentation Gate

Before implementing or proposing package structure, read the relevant SwiftPM and Swift documentation through Apple Dev Skills, Swift.org, or official Apple docs.

Minimum rules to rely on:

- A Swift package is configured by a `Package.swift` manifest at the package root.
- `Package` defines package name, products, targets, dependencies, platforms, resources, and Swift language mode.
- A library product is the externally visible artifact clients import.
- A package dependency should resolve from a real remote source that other contributors can fetch.
- Version-based dependency requirements are the recommended default for published package dependencies.

Authoritative docs:

- [Swift Package Manager](https://www.swift.org/documentation/package-manager/)
- [PackageDescription](https://developer.apple.com/documentation/packagedescription)
- [Package](https://developer.apple.com/documentation/PackageDescription/Package)
- [Swift Package Manager PackageDescription API](https://docs.swift.org/package-manager/PackageDescription/PackageDescription.html)

## When To Use

- Use this skill when a Swift package wants to build features on top of SwiftASB.
- Use this skill after `swiftasb:choose-integration-shape` selects a package library, command-line package, helper package, or test harness shape.
- Use this skill when a package should expose SwiftASB-backed capabilities without making raw app-server wire types its public API.
- Use this skill when live Codex behavior needs to be tested or documented without becoming a normal unit-test dependency.

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
- `Sources/SwiftASB/Public/CodexTurnHandle.swift`

As of SwiftASB `v1.5.0`, package integrations should prefer:

- `CodexAppServer.start(_:)` with `CodexAppServer.StartupRequest` for normal one-call subprocess startup, compatibility validation, initialization, and typed `CodexAppServerStartupError` failures
- lower-level `CodexAppServer.start()`, `cliExecutableDiagnostics()`, and `initialize(_:)` only when the package intentionally owns custom diagnostics, compatibility policy, or test setup before initialization
- `CodexAppServer` for subprocess ownership, diagnostics, stored-thread operations, model capability reads, feature-operation-event streams, and hook diagnostics
- `CodexAppServer.makeLibrary(configuration:)` when the package intentionally exposes app-wide stored-thread lists, cwd or repository grouping, stable worktree groups, repository/worktree filters, selected worktree or repository context, selected-worktree Git status, library-local selection, `CodexWorkspace.ProjectInfo` project identity, `CodexAppServer.ThreadSource` source facts, or app-wide model/MCP/hook snapshots that refresh when app-server app/skill/MCP state changes
- `CodexAppServer.makeInventory(configuration:)` when the package intentionally exposes routine app-wide model capabilities, global MCP summaries, hook diagnostics, apps, skills, plugins, or collaboration modes
- `CodexAppServer.fs`, `CodexAppServer.config`, and `CodexAppServer.extensions` when the package intentionally exposes app-server-owned filesystem, config, advanced extension pagination, plugin detail reads, or already-configured marketplace upgrades
- `CodexAppServer.mcp` when the package intentionally exposes MCP installs, full status snapshots, or app-wide or thread-scoped MCP resource contents
- `SwiftASBFeaturePolicy` and `CodexAppServer.featureOperationEvents()` when the package intentionally exposes SwiftASB-owned authority choices or mutation-operation records
- `CodexWorkspace` when consumers need session cwd, app-server-owned worktree snapshots, project identity, Git repository facts, selected Git status snapshots, active permission profile, or runtime filesystem/network permission facts
- `CodexThread` for conversation-scoped turn creation, archive/unarchive, thread actions, thread goals, request responses, and local history
- `CodexThread.startReview(against:placement:)` and `CodexReviewHandle` when the package intentionally exposes app-server review starts
- `CodexThread.sendShellCommand(_:)` only when the package intentionally exposes high-impact user-level shell execution and requires the host to enable `shellCommandExecution`
- `CodexTurnHandle` for one active turn, including events, steering, interruption, request responses, and completion handoff
- query descriptors when the package API needs repeatable thread-list, file-discovery, history-window, recent-file, or recent-command intent
- package-owned public types for the user's domain when consumers do not need direct SwiftASB handles

## Implementation Workflow

1. Inspect the package manifest and target layout.
2. Read the SwiftPM docs for the package behavior the change relies on.
3. Decide whether SwiftASB is implementation detail or public API:
   - implementation detail: expose package-owned request, result, progress, and error types
   - public dependency: expose selected SwiftASB handles only when consumers genuinely need them
4. Add SwiftASB as a dependency only if it is not already present:
   - package URL: `https://github.com/gaelic-ghost/SwiftASB`
   - minimum version: `1.5.0` when using one-call startup with typed startup errors, app-wide library or inventory, stable worktree groups, repository/worktree filters, selected-worktree Git status, feature policy, feature-operation events, extension marketplace maintenance, project identity, thread source, filesystem match metadata, MCP installs/status/resource reads, config warnings, extension inventory, workspace, query-descriptor, thread archive/unarchive, code-review starts, shell-command execution, or recent-activity guidance; otherwise verify the support window in SwiftASB's README
   - product: `SwiftASB`
5. Add the dependency to the target that owns Codex behavior, not every target by default.
6. Decide whether filesystem/config/extension/MCP/workspace/worktree/selected-Git-status/project-identity/thread-source facts, app-wide inventory, feature-policy choices, review starts, shell commands, or feature-operation events are part of the package API or only implementation detail.
7. Keep startup, turn, approval, cancellation, diagnostics, history, and app-server-owned fact errors descriptive and package-specific.
8. Keep normal tests deterministic with package-owned fakes, adapters, fixtures, or small pure transformations.
9. Add live Codex probes only behind explicit opt-in flags, temporary workspaces, serial execution, and hard timeouts.
10. Document runtime requirements, compatibility expectations, and live-test flags in the package README or contributor docs.
11. Validate with `swift build` and `swift test`, plus any repo-documented checks.

## Public API Pattern

Prefer a narrow package-owned facade when the package is not primarily a SwiftASB wrapper:

```swift
import SwiftASB

public struct WorkspaceSummaryRequest: Sendable {
    public var workspacePath: String
    public var prompt: String

    public init(workspacePath: String, prompt: String) {
        self.workspacePath = workspacePath
        self.prompt = prompt
    }
}

public struct WorkspaceSummary: Sendable {
    public var text: String
}

public actor WorkspaceSummarizer {
    private let appServer: CodexAppServer

    public init() {
        self.appServer = CodexAppServer()
    }

    public func shutdown() async {
        await appServer.stop()
    }

    public func summarize(_ request: WorkspaceSummaryRequest) async throws -> WorkspaceSummary {
        _ = try await appServer.start(
            .init(
                clientInfo: .init(
                    name: "WorkspaceSummarizer",
                    title: "Workspace Summarizer",
                    version: "1.0.0"
                )
            )
        )

        let thread = try await appServer.startThread(
            .init(currentDirectoryPath: request.workspacePath)
        )
        let turn = try await thread.startTextTurn(request.prompt)

        for try await event in turn.events {
            if case .completed = event {
                _ = try await turn.complete()
                return WorkspaceSummary(text: "Summary completed.")
            }
        }

        throw WorkspaceSummaryError.turnEndedWithoutCompletion
    }
}

public enum WorkspaceSummaryError: Error, Sendable {
    case turnEndedWithoutCompletion
}
```

Use this as a shape, not as a file to paste blindly. Most packages should return their own real result data, stream their own progress values, and map SwiftASB failures into errors their consumers can understand.

## API Design Guidance

- Keep the public API focused on the package's job, not on exposing every SwiftASB capability.
- Prefer typed request, result, progress, and options values over strings, booleans, or parallel parameters.
- Expose `CodexAppServer`, `CodexThread`, or `CodexTurnHandle` only when the package is intentionally a thin SwiftASB extension surface.
- Keep generated `CodexWire...` models out of public API unless the user explicitly asks for protocol-level work.
- Prefer `CodexAppServer.fs`, `CodexAppServer.config`, `CodexAppServer.makeInventory(configuration:)`, `CodexAppServer.extensions`, `CodexAppServer.mcp`, `CodexWorkspace`, and `SwiftASBFeaturePolicy` over direct local reads when the package needs facts owned by the Codex app-server, including worktree snapshots, selected Git status, project identity, repository facts, inventory, extension detail, MCP status/resources, marketplace maintenance, and feature-category choices.
- Expose feature-operation events only when consumers need audit or status records for SwiftASB-owned mutations. Do not create duplicate package events for routine read-only refreshes.
- Preserve SwiftASB's file-discovery match metadata if the package exposes fuzzy search results; do not recompute highlight ranges or ranking reasons in a parallel scoring system unless the package has its own product-specific ranking.
- Use query descriptor types when the package needs to preserve list, file-discovery, history-window, recent-file, or recent-command intent as data.
- Expose thread-management actions such as goals, naming, metadata updates, compaction, or rollback only when those actions are truly part of the package's public job; otherwise keep them as implementation detail around `CodexThread`.
- Expose review starts or shell-command execution only when those actions are truly part of the package's public job; shell commands must remain explicit high-impact user-level execution rather than a hidden helper path.
- Keep cancellation explicit; do not drop a `CodexTurnHandle` silently when the package promises cancellation behavior.
- Document that a local Codex CLI/app-server runtime is required.
- Document SwiftASB compatibility as a reviewed support window, not a generic promise that every future Codex app-server schema is public API.

## Testing Guidance

- Keep default `swift test` deterministic and free of live Codex subprocess requirements.
- Use fakes or protocol-shaped seams for package-owned behavior when the test is about your package, not Codex runtime compatibility.
- Put live Codex probes behind an explicit environment flag such as `SWIFTASB_LIVE_TESTS=1`.
- Run live probes in temporary workspaces with hard timeouts.
- Do not run live probes concurrently with other SwiftPM or Xcode build/test commands.
- Make live failure text name the exact boundary: executable discovery, typed startup validation, initialization, thread start, turn start, request response, MCP install, MCP resource read, review start, shell command, diagnostics, history, or shutdown.

## Validation

Run the repository's documented validation path. For plain Swift packages, the baseline is:

```bash
swift build
swift test
```

If the package is also an Xcode app workspace, use the repository's documented Xcode workflow instead of assuming SwiftPM is sufficient.

## Handoffs

- Use `swiftasb:explain-swiftasb` when the user needs adoption tradeoffs before implementation.
- Use `swiftasb:choose-integration-shape` when ownership or public API shape is unclear.
- Use `swiftasb:diagnose-integration` when startup, turn, approval, MCP, diagnostics, or history behavior fails.
- Use `apple-dev-skills:sync-swift-package-guidance` when the package repo's `AGENTS.md` or maintainer workflow needs alignment.
- Use Apple Swift package workflow skills for package build, test, manifest, resource, DocC, or release execution.

## Guardrails

- Do not commit machine-local SwiftASB dependency paths such as `/Users/...`, `~/...`, or `../SwiftASB` into public package manifests.
- Do not make live Codex subprocess work part of normal unit tests.
- Do not expose raw generated app-server wire models as the default public API.
- Do not treat same-thread overlapping turns as supported; SwiftASB rejects them because the live app-server does not expose a reliable independent lifecycle for that case.
- Do not hide local Codex CLI discovery, compatibility, startup, or protocol failures behind generic errors; preserve `CodexAppServerStartupError` cases when mapping errors into package-owned error types.
- Do not run multiple SwiftPM or Xcode build/test commands concurrently.
