# SwiftASB Explanation Examples

Use these examples when an agent needs to explain SwiftASB before implementation starts. They are intentionally short and decision-oriented. The agent should still verify the current SwiftASB README, DocC docs, release notes, and public API before making exact claims.

## Strong Fit: SwiftUI Workspace Inspector

Recommendation: SwiftASB is a good fit for this app.

What SwiftASB would do here: SwiftASB would let the SwiftUI app start the local Codex runtime, open a thread for the workspace, start turns, read app-server-owned workspace facts, and read live progress through Swift-native handles instead of replaying raw app-server JSON.

What the app would own: The app still owns its windows, navigation, inspector layout, persistence choices, user preferences, and approval UI. SwiftUI and Observation should own view updates.

What SwiftASB would own: `CodexAppServer` owns the subprocess and app-wide capability reads, `CodexAppServer.fs`, `CodexAppServer.config`, and `CodexAppServer.extensions` own app-server-routed facts, `CodexThread` owns one conversation, `CodexTurnHandle` owns one active turn, and companions such as `Dashboard`, `Minimap`, `RecentTurns`, `RecentFiles`, and `RecentCommands` provide UI-friendly state.

Tradeoffs: The app depends on a local Codex CLI runtime, same-thread overlapping turns are rejected, and compatibility follows SwiftASB's reviewed Codex support window.

Next integration step: Use `swiftasb:choose-integration-shape`, then `swiftasb:build-swiftui-app`.

## Strong Fit: AppKit Document Window

Recommendation: SwiftASB is a good fit if each document or workspace window needs its own Codex thread.

What SwiftASB would do here: SwiftASB would provide the typed runtime, thread, turn, filesystem/config/extension, workspace-permission, diagnostic, and history surfaces. The AppKit app can connect those surfaces to window-controller actions, menu validation, toolbar controls, sheets, panels, and inspector views.

What the app would own: AppKit still owns application lifecycle, document/window ownership, main-actor UI updates, menu state, toolbar actions, and user-facing presentation.

What SwiftASB would own: SwiftASB owns Codex startup, initialization, thread creation or resume, active turn events, request responses, interruption, app-server-owned fact reads, diagnostics, and local history reads.

Tradeoffs: The app needs explicit process lifetime decisions. A window controller should not secretly own app-wide Codex runtime work if multiple windows share one runtime.

Next integration step: Use `swiftasb:choose-integration-shape`, then `swiftasb:build-appkit-app`.

## Conditional Fit: Swift Package Library

Recommendation: SwiftASB can fit, but only if the package intentionally depends on a local Codex runtime.

What SwiftASB would do here: SwiftASB would sit inside the package implementation and provide typed Codex runtime control. The package should expose its own narrow request, result, progress, and error types unless consumers genuinely need direct SwiftASB handles.

What the package would own: The package owns its public API, versioning promises, test strategy, runtime documentation, and consumer-facing error model.

What SwiftASB would own: SwiftASB owns app-server startup, app-server-owned fact reads, thread and turn handles, diagnostics, interactive request routing, query descriptors, and local history helpers.

Tradeoffs: Normal `swift test` should stay deterministic. Live Codex probes need explicit environment flags, temporary workspaces, serial execution, and hard timeouts.

Next integration step: Use `swiftasb:choose-integration-shape`, then `swiftasb:build-swift-package`.

## Poor Fit: Hosted Multi-User Service

Recommendation: SwiftASB is probably not the right foundation.

What SwiftASB would do here: SwiftASB drives a local Codex app-server from Swift. It is not a hosted multi-user agent platform and does not remove the need for product-level auth, tenancy, job isolation, deployment, or server operations.

What the app would own: A hosted service would need to own user accounts, authorization, rate limits, workspace isolation, queueing, secrets, audit logs, and deployment health.

What SwiftASB would own: SwiftASB could still help a local Swift tool or internal helper drive Codex, but it should not be described as a complete hosted platform.

Tradeoffs: Treating SwiftASB as the server platform would hide major product and security decisions.

Next integration step: Use `swiftasb:explain-swiftasb` to document why the fit is weak, then choose a hosted architecture separately.
