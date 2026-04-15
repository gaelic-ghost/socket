# Embedding The Server

## Overview

Use ``EmbeddedServerSession`` when an app wants to host the shared SpeakSwiftly server runtime inside its own process instead of starting the standalone executable separately.

`EmbeddedServerSession` gives app code two jobs:

- start and stop the shared host lifecycle
- expose an app-facing ``ServerState`` object that SwiftUI and other main-actor UI code can observe directly

The session keeps transport ownership, config loading, and host shutdown logic internal. Behind that wrapper, the embedded path now composes the host lifecycle, optional config watching, optional MCP lifecycle, and HTTP serving as service-owned siblings under one outer lifecycle group. App code should still treat that as an internal implementation detail: hold onto the session object, bind UI to `session.state`, and use the state snapshots as the public read model for the embedded host.

## Core Types

### ``EmbeddedServerSession``

Start the shared host through ``EmbeddedServerSession/start(environment:options:)``. The embedded path still uses the same environment-driven config model as the standalone runtime, but it now carries its own embedded-session default port and lets app code provide explicit `Options(port:runtimeProfileRootURL:)` values when another localhost port or another runtime-owned persistence root is a better fit.

Call ``EmbeddedServerSession/stop()`` when the app wants a graceful shutdown. If a session has already been asked to stop, a second stop request simply waits for the same shutdown to finish.

### ``ServerState``

``ServerState`` is the main-actor observable projection of the embedded host. It carries high-level overview data, queue snapshots, transport status, runtime configuration, recent errors, and the cached voice-profile list.

Treat `ServerState` as the UI-facing model, not as the authority that owns the server process. The real host lifecycle still lives behind the embedded session and server host internals.

### Snapshot Families

The library keeps the observable state in small transport-neutral snapshot types:

- ``HostOverviewSnapshot`` for host identity and readiness
- ``QueueStatusSnapshot`` and ``PlaybackStatusSnapshot`` for active and queued work
- ``RuntimeConfigurationSnapshot`` for persisted and active runtime configuration
- ``TransportStatusSnapshot`` and ``RecentErrorSnapshot`` for operator-facing health signals

When you need the whole current picture at once, use ``HostStateSnapshot`` as the aggregate read model.

## When To Use The Executable Instead

Use the embedded session when an app owns the process and wants direct observable state. Use the standalone executable and the HTTP or MCP surfaces when another process, a LaunchAgent, or an external operator should own runtime startup and shutdown.

If the app needs explicit ownership of where the runtime persists profiles, generated artifacts, and staged runtime configuration, pass `runtimeProfileRootURL` on the embedded session options. That same root is forwarded into both the server's own runtime-configuration store and the underlying `SpeakSwiftly` startup path so the embedded app does not have to manage those two persistence layers separately.

For the transport inventory and command-line surface, see <doc:Operator-Surfaces>.
