# Phase 6 Checklist

## Goal

Converge the remaining job-specific HTTP SSE path onto the shared host event model without turning `ServerState` into a server-side event bus and without rebuilding a second transport-specific state model.

## Why This Phase Exists

The shared host already exposes stable snapshots plus typed `HostEvent` updates that MCP consumes for live resource notifications. The last major live-update path still using bespoke subscriber bookkeeping is the job-specific HTTP SSE route.

This phase is a durable building-block change because it:

- removes the remaining duplicated live-update plumbing from `ServerHost`
- lets HTTP SSE and MCP consume the same host-owned event backbone
- keeps `ServerHost` as the only transport-truth and live-update source
- preserves `ServerState` as the SwiftUI-facing projection instead of letting it become a server event system

The simpler path considered first was keeping the current job-scoped subscriber dictionary and just treating SSE as a permanent exception. That would work, but it would leave the one remaining bespoke streaming path in the host after the shared event model already proved itself.

## Scope

### Host

- Update `Sources/SpeakSwiftlyServer/Host/HostEvents.swift`
  Add a host-native per-job event update payload that can carry one encoded job event with a monotonic history position and terminal marker.

- Update `Sources/SpeakSwiftlyServer/Host/ServerHost.swift`
  Emit per-job host events whenever a `ServerJobEvent` is recorded.

- Update `Sources/SpeakSwiftlyServer/Host/ServerHost.swift`
  Rebuild `sseStream(for:)` so it replays current history, then follows the shared host event stream instead of maintaining per-job subscriber and heartbeat registries inside `JobRecord`.

- Update `Sources/SpeakSwiftlyServer/Host/ServerHost.swift`
  Remove the now-redundant per-job SSE subscriber bookkeeping from `JobRecord` and related helper methods.

### HTTP

- Keep `Sources/SpeakSwiftlyServer/HTTP/HTTPSurface.swift` route semantics unchanged.
  The route shape should stay job-specific even after the stream backend converges.

### Docs

- Update `README.md`
  Document that HTTP SSE now rides the shared host event backbone while remaining a job-specific route.

- Update `docs/maintainers/server-consolidation-plan.md`
  Mark selective HTTP SSE convergence as landed once implemented.

- Update `docs/maintainers/phase-5-checklist.md`
  Remove the stale deferred item for SSE convergence.

## Explicit Non-Goals

- rebuilding the old standalone `playback-jobs` resource namespace
- inventing a second event model just for HTTP
- making `ServerState` the source of non-UI streams
- defining live config reload semantics

## Validation

- `swift build`
- `swift test`

Existing SSE replay and heartbeat coverage should continue to pass, and the host event tests should still confirm that MCP and non-UI consumers receive the shared host event stream.

## Status

Phase 6 is now landed. `ServerHost` emits per-job event updates alongside job snapshot updates, the HTTP SSE route replays current job history and then follows the shared host event stream, and the old per-job subscriber and heartbeat registries have been removed from `JobRecord`. The route shape remains job-specific, but its live-update backend now shares the same host-owned event model used by the rest of the server.
