# TODO

## Thorough Review Slices

- [~] Slice 1: Host state and job tracking
  Files: `Sources/SpeakSwiftlyServer/Host/ServerHost+State.swift`, `Sources/SpeakSwiftlyServer/Host/ServerHost+JobTracking.swift`
  Focus: runtime-derived state refresh policy, degraded-worker fallback behavior, profile-cache reconciliation, SSE replay, request retention and pruning.

- [x] Slice 2: Runtime adapter transport bridging
  Files: `Sources/SpeakSwiftlyServer/Host/ServerRuntimeAdapter.swift`
  Focus: text-profile transport shaping, crash-vs-error behavior, path resolution, and runtime API drift handling.

- [ ] Slice 3: MCP tool dispatch and notification policy
  Files: `Sources/SpeakSwiftlyServer/MCP/MCPToolHandlers.swift`
  Focus: repeated argument parsing, accepted-request result shaping, resource-change notifications, and tool-handler drift.

- [ ] Slice 4: Embedded lifecycle and startup or shutdown ownership
  Files: `Sources/SpeakSwiftlyServer/EmbeddedServerSession.swift`, `Sources/SpeakSwiftlyServer/EmbeddedLifecycleServices.swift`
  Focus: readiness gates, sibling-service coordination, shutdown barriers, and transport-state transitions.

- [ ] Slice 5: LaunchAgent operator flow
  Files: `Sources/SpeakSwiftlyServer/LaunchAgent/LaunchAgentRuntime.swift`
  Focus: launchctl polling, uninstall timing, partial teardown states, and operator-facing diagnostics.

- [ ] Slice 6: E2E MCP stream harness
  Files: `Tests/SpeakSwiftlyServerE2ETests/E2EMCPEventStream.swift` and related E2E helpers
  Focus: stream connection timing, polling sleeps, notification matching, and flake risk.

## Slice 1 Findings

- [x] Fix degraded-worker cached fallback so it clears `generationQueueStatus` alongside playback state, and add regression coverage for the degraded queue snapshot path.
- [x] Refresh the cached voice-profile list after `reroll_voice_profile` completes, and add regression coverage that verifies profile-cache metadata is refreshed after reroll.
- [ ] Review whether profile-mutation reconciliation should rely on profile-name set comparisons alone, especially when concurrent external profile edits can happen between retries.

## Slice 2 Findings

- [x] Replace the text-profile transport bridge `preconditionFailure` path with thrown runtime errors that surface through HTTP text-profile routes as operator-readable JSON failures.
- [x] Translate MCP text-profile resource and tool bridge failures into explicit `MCPError.internalError(...)` payloads instead of relying on the default thrown-error path.
- [x] Recheck runtime-adapter path-resolution behavior for edge cases like non-normalized relative `cwd` values and whitespace-padded `cwd` inputs, and cover it with direct helper tests.
- [ ] Keep watching for future upstream transport-shape drift beyond the current text-profile bridge; if another released payload starts needing ad hoc JSON bridging, treat that as a new review slice rather than letting the adapter accumulate more silent translation seams.
