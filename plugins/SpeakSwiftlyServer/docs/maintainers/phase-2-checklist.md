# Phase 2 Checklist

## Objective

Turn the structural Phase 1 host split into an operationally useful shared state model for three consumers:

- app UI through `@Observable`
- HTTP routes and SSE
- a future MCP adapter

## Scope

Phase 2 expands host-native state and transport assembly boundaries, but it still does not mount the MCP route or adopt `swift-configuration` yet.

## Core Decisions

- `ServerHost` remains the single backend owner and authoritative source of truth.
- `ServerState` remains `@Observable` and `@MainActor`, but it is only a UI-facing projection of host state.
- Server-side update streams stay off `MainActor`.
- Transport payload models stay at the HTTP and MCP boundaries; they are no longer the primary internal state model.

## File Changes

### Host

- Add `Sources/SpeakSwiftlyServer/Host/HostStateModels.swift`
  Define shared host-native snapshots such as overview, transport status, queue status, playback status, current generation job, and recent errors.

- Update `Sources/SpeakSwiftlyServer/Host/ServerHost.swift`
  Publish richer shared state, track recent errors, track generation timing, and expose a host-owned async update stream for non-UI consumers.

- Update `Sources/SpeakSwiftlyServer/Host/ServerState.swift`
  Mirror host-native snapshots directly so SwiftUI can observe them without depending on HTTP route payload shapes.

### HTTP

- Update `Sources/SpeakSwiftlyServer/HTTP/HTTPSurface.swift`
  Rename the Hummingbird assembly boundary to `assembleHBApp` and keep HTTP response shaping thin.

### Config

- Update `Sources/SpeakSwiftlyServer/Config/AppConfig.swift`
  Make HTTP and MCP transport config more explicit so the host can publish adapter status honestly.

## Acceptance Criteria

- The host publishes a shared state model that includes:
  - overall host and worker status
  - current generation job summary with elapsed generation time
  - playback state summary
  - generation and playback queue counts
  - HTTP and MCP adapter status with bind details
  - recent brief operator-facing errors

- `ServerState` mirrors that shared state for SwiftUI use.
- `ServerHost` exposes a non-`MainActor` async update stream suitable for future SSE and MCP consumers.
- The HTTP app assembly function is named `assembleHBApp`.
- Existing HTTP behavior continues to work after the rename and state-model shift.

## Follow-On Work

- Phase 3 should adopt `swift-configuration` and define reload policy.
- Phase 4 should mount MCP into the same Hummingbird app and consume the shared host update stream.
