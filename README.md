# SpeakSwiftlyServer

Swift executable package for a localhost HTTP server that exposes `SpeakSwiftlyCore` over a small, app-friendly API.

## Overview

This repository is the Swift-native sibling to `../speak-to-user-server`. It uses [Hummingbird](https://github.com/hummingbird-project/hummingbird) to host a localhost macOS HTTP service with in-memory job tracking and server-sent events, while delegating speech, profile management, and worker lifecycle to the typed `SpeakSwiftlyCore` runtime.

### Motivation

The target is a thin Swift service that a forthcoming macOS app can install and manage as a LaunchAgent without needing a separate Python runtime. Matching the existing Python server’s HTTP contract keeps the app-facing integration stable while moving the runtime path fully into Swift.

That means this package intentionally stays narrow: Hummingbird for HTTP, `SpeakSwiftlyCore` for speech and profile operations, and a small amount of server state to translate typed worker events into job snapshots and SSE replay.

## Setup

Build the package with SwiftPM:

```bash
swift build
```

Run the test suite:

```bash
swift test
```

## Usage

Run the server locally:

```bash
swift run SpeakSwiftlyServer
```

The service binds to `127.0.0.1:7337` by default and supports these environment variables:

- `APP_NAME`
- `APP_ENVIRONMENT`
- `APP_HOST`
- `APP_PORT`
- `APP_SSE_HEARTBEAT_SECONDS`
- `APP_COMPLETED_JOB_TTL_SECONDS`
- `APP_COMPLETED_JOB_MAX_COUNT`
- `APP_JOB_PRUNE_INTERVAL_SECONDS`

The current HTTP surface is:

- `GET /healthz`
- `GET /readyz`
- `GET /status`
- `GET /profiles`
- `POST /profiles`
- `DELETE /profiles/{profile_name}`
- `POST /speak`
- `GET /jobs/{job_id}`
- `GET /jobs/{job_id}/events`

`POST /speak`, `POST /profiles`, and `DELETE /profiles/{profile_name}` return job metadata immediately. Progress, worker status changes, acknowledgements, and terminal results are exposed through `GET /jobs/{job_id}/events` as SSE.

## Development

The executable entrypoint lives in [`Sources/SpeakSwiftlyServer/SpeakSwiftlyServer.swift`](/Users/galew/Workspace/SpeakSwiftlyServer/Sources/SpeakSwiftlyServer/SpeakSwiftlyServer.swift). The server itself stays intentionally small:

- [`ServerApp.swift`](/Users/galew/Workspace/SpeakSwiftlyServer/Sources/SpeakSwiftlyServer/ServerApp.swift) wires Hummingbird routes.
- [`ServerState.swift`](/Users/galew/Workspace/SpeakSwiftlyServer/Sources/SpeakSwiftlyServer/ServerState.swift) tracks worker readiness, cached profiles, job history, SSE subscribers, and retention.
- [`ServerRuntimeBridge.swift`](/Users/galew/Workspace/SpeakSwiftlyServer/Sources/SpeakSwiftlyServer/ServerRuntimeBridge.swift) keeps the runtime boundary thin around `SpeakSwiftlyCore`.
- [`ServerModels.swift`](/Users/galew/Workspace/SpeakSwiftlyServer/Sources/SpeakSwiftlyServer/ServerModels.swift) defines request and response payloads.

The design is deliberately direct. Adding extra wrappers, managers, or intermediate layers here would be easy, but it would also be the kind of unnecessary complexity that makes a small localhost service harder to reason about, so the server is kept close to the typed runtime API on purpose.

## Verification

Current baseline checks:

```bash
swift build
swift test
```

The current test suite covers configuration parsing, background job completion and pruning, SSE replay and heartbeat behavior, and route-level health, profile, and job lifecycle responses against a controlled typed runtime.

## Roadmap

Planned work is tracked in [`ROADMAP.md`](/Users/galew/Workspace/SpeakSwiftlyServer/ROADMAP.md).

## License

A project license has not been added yet.
