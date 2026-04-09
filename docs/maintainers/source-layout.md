# Source Layout

## Purpose

This document is the maintainer map for the post-`SpeakSwiftly 2.2.0` source split. The goal is to keep future cleanup, review, and feature work landing in the smallest file family that already owns the relevant concern, instead of letting `ServerHost.swift`, `ServerModels.swift`, or one mixed test file grow back into monoliths.

## Host Sources

- `Sources/SpeakSwiftlyServer/Host/ServerHost.swift`
  Holds the actor declaration, stored state, construction, lifecycle, transport watch hooks, and shared snapshot basics.
- `Sources/SpeakSwiftlyServer/Host/ServerHost+Queries.swift`
  Holds the public query surface, runtime/text-profile reads and writes, generated-artifact reads, and immediate control entrypoints.
- `Sources/SpeakSwiftlyServer/Host/ServerHost+Jobs.swift`
  Holds request submission, SSE replay, request-event consumption, profile-cache reconciliation, worker status handling, and in-memory job retention.
- `Sources/SpeakSwiftlyServer/Host/ServerHost+State.swift`
  Holds publish flow, runtime refresh, derived host snapshots, and live configuration reload helpers.
- `Sources/SpeakSwiftlyServer/Host/ServerHost+Support.swift`
  Holds transport-status helpers, recent-error emission, event mapping, SSE encoding, and shared immediate-success helpers.

## Model Sources

- `Sources/SpeakSwiftlyServer/Host/ServerModels.swift`
  Request payloads plus shared normalization-format helpers.
- `Sources/SpeakSwiftlyServer/Host/ProfileModels.swift`
  Voice-profile snapshots plus text-profile and replacement transport models.
- `Sources/SpeakSwiftlyServer/Host/QueueStatusModels.swift`
  Queue, playback, health, readiness, and status snapshots.
- `Sources/SpeakSwiftlyServer/Host/JobEventModels.swift`
  Job event payloads and retained request snapshots.
- `Sources/SpeakSwiftlyServer/Host/HostStateModels.swift`
  Shared host-overview snapshots for app state, HTTP, and MCP resources.

## Test Sources

- `Tests/SpeakSwiftlyServerTests/SpeakSwiftlyServerTests.swift`
  Lifecycle-heavy HTTP route tests.
- `Tests/SpeakSwiftlyServerTests/SpeakSwiftlyServerMCPRouteTests.swift`
  MCP route, catalog, and subscription tests kept separate from the HTTP-focused route suite.
- `Tests/SpeakSwiftlyServerTests/SpeakSwiftlyServerCoreTests.swift`
  Configuration, host-state, and lower-level unit coverage.
- `Tests/SpeakSwiftlyServerTests/MockRuntime.swift`
  The main typed-runtime test double. If it grows again, split it by control surface instead of adding more behavior to one file.

## Current Cleanup Follow-Through

- Keep same-type `ServerHost` extensions as the preferred split mechanism for host refactors. Do not introduce helper coordinators or wrapper objects unless a real ownership boundary changes.
- Keep transport-local shaping at the edge. If `SpeakSwiftly` or `TextForSpeech` can express a concept directly, prefer deleting server-local inference instead of adding another translation layer.
- If a test file starts mixing HTTP, MCP, LaunchAgent, and host-state concerns again, split it before adding more cases.
