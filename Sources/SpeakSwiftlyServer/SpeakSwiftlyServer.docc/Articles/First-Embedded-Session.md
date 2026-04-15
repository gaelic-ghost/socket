# First Embedded Session

## Overview

This is the shortest realistic path through the library-first surface:

1. create an ``EmbeddedServerSession``
2. start it with the same environment-driven config model the standalone host uses
3. read `session.state` as the app-facing snapshot model
4. decide when to switch to the executable and transport docs instead

Use this walkthrough when you want to understand the package as an app-embedded host first, not as a LaunchAgent-managed service.

## Start The Session

Create and start the embedded session from app-owned code:

```swift
import SpeakSwiftlyServer

let session = try await EmbeddedServerSession.start(
    options: .init(
        port: 7811,
        runtimeProfileRootURL: FileManager.default
            .urls(for: .applicationSupportDirectory, in: .userDomainMask)
            .first?
            .appendingPathComponent("ExampleApp/SpeakSwiftlyRuntime", isDirectory: true)
    )
)
```

`EmbeddedServerSession` owns the host lifecycle. Internally it now coordinates host startup, optional config watching, optional MCP readiness, and HTTP serving through one service-owned lifecycle group, but app code should still treat the session itself as the lifecycle boundary. Keep the session alive for as long as you want the shared server running in-process. If you do not pass `Options(port:)`, the embedded session defaults to `127.0.0.1:7339`.

If you pass `runtimeProfileRootURL`, the embedded host uses that same root for both its own persisted runtime configuration and the underlying `SpeakSwiftly` profile and artifact persistence. Use that when the app wants an explicit app-owned or App Group-owned runtime root instead of relying on the default Application Support lookup.

## Read The App-Facing State

Once the session is running, bind UI and app logic to `session.state`:

```swift
import SpeakSwiftlyServer

let session = try await EmbeddedServerSession.start()

let state = session.state
let hostOverview = state.overview
let playbackStatus = state.playback
let availableVoices = state.voiceProfiles
```

Treat ``ServerState`` as the app-facing read model. It is the place to inspect readiness, queue state, transport state, runtime configuration, recent errors, and the cached voice-profile list without reaching into host internals directly.

When you need one aggregated picture instead of several observable fields, follow the snapshot families described in <doc:Embedding-The-Server>.

## Know When To Leave DocC

Stay in the library-first docs when you are answering questions like:

- how does an app start the shared host
- which state type should SwiftUI observe
- what filesystem layout should an app own for a managed install

Jump to the operator docs when the question becomes:

- how do I install or refresh the LaunchAgent
- which HTTP or MCP route exposes this runtime operation
- what does the command-line tool print or accept

For those surfaces, continue with <doc:Operator-Surfaces> and then use the repository docs linked there.
