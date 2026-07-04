---
name: swiftnio-workflow
description: Plan, implement, test, and diagnose direct SwiftNIO work in server-side Swift packages, including EventLoopGroup ownership, Channel pipelines, ChannelHandlers, ByteBuffer usage, back-pressure, nonblocking I/O, protocol implementations, EmbeddedChannel tests, and handoffs back to Vapor or Hummingbird when a higher-level framework is the better fit.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with SwiftNIO, SwiftPM, Vapor, Hummingbird, protocol servers, protocol clients, and server-side Swift services on macOS or Linux.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-swiftnio
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(curl:*)
---

# SwiftNIO Workflow

## Purpose

Build, modify, test, or diagnose direct SwiftNIO code without turning ordinary Vapor, Hummingbird, or SwiftPM service work into low-level networking work.

The practical decision is whether the service really needs to own event loops, channels, pipeline handlers, byte buffers, protocol framing, back-pressure, or bootstrap behavior directly. If a framework route, middleware, request context, or package-level API can solve the problem clearly, use that higher-level workflow instead.

## When To Use

- Use this skill when changing direct SwiftNIO types such as `EventLoopGroup`, `EventLoop`, `Channel`, `ChannelPipeline`, `ChannelHandler`, `ByteBuffer`, `ServerBootstrap`, `ClientBootstrap`, `NIOHTTP1`, `NIOWebSocket`, `NIOSSL`, or `NIOEmbedded`.
- Use this skill when implementing or diagnosing protocol framing, low-level clients or servers, custom channel handlers, back-pressure, flow control, event-loop affinity, futures, async bridging, or nonblocking I/O behavior.
- Use this skill when a Vapor or Hummingbird task crosses below framework APIs into NIO internals.
- Use this skill when diagnosing event-loop blocking, deadlocks, wrong-event-loop futures, leaked channels, missing flushes, incorrect buffer reads/writes, TLS or HTTP pipeline setup, or Linux-only NIO behavior.
- Do not use this skill for ordinary route, middleware, controller, model, request-context, migration, OpenAPI, Docker, Fly.io, or local SwiftPM work unless NIO behavior is the reason for the change.
- Do not replace Vapor or Hummingbird with direct SwiftNIO unless the user asked for direct protocol work or the current abstraction cannot support the concrete behavior.

## Source Check

Use repo-local Swift files, checked-out dependency sources, Dash MCP or Dash HTTP for installed Swift package DocC, and then official docs or source when Dash/local coverage is missing or stale. Check one of those source-specific paths before claiming SwiftNIO behavior:

- [SwiftNIO repository](https://github.com/apple/swift-nio)
- [SwiftNIO docs](https://apple.github.io/swift-nio/docs/current/NIOCore/)
- [SwiftNIO API docs on Swift Package Index](https://swiftpackageindex.com/apple/swift-nio/documentation)
- [Swift Server Workgroup](https://www.swift.org/server/)
- [SwiftNIO SSL](https://github.com/apple/swift-nio-ssl)
- [SwiftNIO HTTP/2](https://github.com/apple/swift-nio-http2)
- [SwiftNIO Extras](https://github.com/apple/swift-nio-extras)

Use Vapor, Hummingbird, SwiftPM, Docker, deployment, persistence, or observability docs when the NIO work depends on framework lifecycle, package layout, container runtime, database I/O, or instrumentation behavior.

## Planning Workflow

1. Inspect project shape:
   - `Package.swift`
   - direct NIO dependencies and products
   - executable or library target that owns NIO code
   - bootstraps, event-loop groups, channel initializers, handlers, codecs, and tests
   - framework entry points that may already wrap NIO
   - platform, TLS, HTTP, WebSocket, or transport requirements
2. Identify the real NIO job:
   - custom protocol server or client
   - protocol codec or channel handler
   - HTTP, WebSocket, TLS, or connection-level behavior below Vapor/Hummingbird
   - back-pressure or streaming fix
   - event-loop or async-bridging bug
   - `EmbeddedChannel` test or Linux-only diagnosis
3. Prefer higher-level framework APIs unless direct NIO unlocks a concrete behavior they cannot express.
4. Keep event-loop ownership explicit.
5. Keep handlers small and composable.
6. Keep buffer reads and writes deliberate.
7. Preserve nonblocking behavior.
8. Validate with the smallest useful unit, embedded-channel, integration, or runtime check.

## Event Loop Ownership

Treat event-loop ownership as an explicit boundary.

For application executables:

- create the `EventLoopGroup` at the process or service lifecycle boundary
- shut it down gracefully on exit
- avoid creating new event-loop groups per request or per connection
- keep work on the correct event loop unless a documented hop is required
- report the exact future, promise, task, channel, or handler involved when wrong-event-loop behavior appears

For libraries:

- prefer accepting an `EventLoopGroup`, `EventLoop`, channel, or async API from the caller instead of hiding global lifecycle state
- do not shut down an event-loop group the library did not create
- document which callbacks, futures, or async methods run on which event loop when it matters

Use Swift concurrency bridging deliberately. Do not mix futures, callbacks, and `async`/`await` in a way that hides cancellation, lifecycle, or event-loop affinity.

## Channels And Pipelines

When editing channel setup:

- name the bootstrap and whether it is client or server side
- name every handler or codec added to the pipeline and the order it runs
- separate protocol framing, decoding, business behavior, and outbound encoding when they are distinct jobs
- ensure inbound and outbound types match between adjacent handlers
- keep TLS, HTTP, WebSocket, compression, and custom codecs in a documented order
- close channels intentionally and report whether the close is graceful, error-driven, or remote-initiated

Do not bury unrelated application behavior inside a `ChannelHandler`. If the handler starts owning routing, persistence, auth, or domain transformations, split those responsibilities and hand the higher-level behavior to the appropriate workflow.

## ByteBuffer And Framing

When working with `ByteBuffer`:

- track reader and writer index behavior
- parse partial input safely
- avoid assuming a full frame arrives in one read
- avoid copying buffers unless ownership, lifetime, or Foundation interop requires it
- bound frame sizes before allocating or accumulating untrusted input
- test malformed, partial, empty, oversized, and multi-frame input

For custom protocols, define the frame shape before coding:

- delimiter, length-prefix, fixed width, or protocol-specific framing
- maximum frame size
- encoding and decoding errors
- close behavior after malformed input
- whether back-pressure should pause reads or fail the connection

## Back-Pressure And Nonblocking I/O

Before changing flow control, identify which side is producing faster than the other side can consume.

Check:

- `autoRead` behavior
- explicit reads
- write buffering and flush timing
- promise completion and error propagation
- streaming response or request body lifecycle
- file, database, HTTP client, or subprocess work that may block an event loop

Do not run blocking filesystem, network, crypto, compression, process, sleep, or database work directly on an event loop. Use framework-provided async APIs, NIO nonblocking APIs, or an explicit offload path that the repository already accepts.

## Testing

Prefer the smallest test that proves the NIO behavior:

- pure parser or encoder test for deterministic frame transformations
- `EmbeddedChannel` test for channel handlers, pipeline order, inbound/outbound behavior, and error propagation
- bootstrap integration test for socket binding, TLS, HTTP, or cross-channel behavior
- Linux or container validation only when platform behavior is the risk
- runtime `curl`, TCP, or protocol-client check only when the behavior cannot be proven in tests

Tests should cover partial frames, multiple frames in one read, malformed input, back-pressure behavior, close behavior, and promise failure paths when those cases are relevant.

## Handoffs

Use `vapor-server-workflow` when the task is really about Vapor routes, middleware, commands, server configuration, Fluent, or Vapor auth.

Use `hummingbird-server-workflow` when the task is really about Hummingbird routing, middleware, request contexts, application lifecycle, or framework tests.

Use `openapi-rpc-workflow` when the task is really about API contracts, generated handlers, JSON-RPC, gRPC, or MCP-style boundaries.

Use `observability-tracing-workflow` when the task is primarily about logs, metrics, tracing, spans, propagation, or production diagnostics.

Use `docker-workflow` or `fly-io-deployment-workflow` when the failure is caused by Linux runtime, container entry point, port binding, health checks, image architecture, or hosted deployment configuration.

## Output Shape

Return:

1. `NIO shape`: package root, target, NIO products, event-loop owner, bootstrap, channels, pipeline handlers, buffers, and test surface.
2. `Docs used`: SwiftNIO, SwiftPM, Vapor, Hummingbird, deployment, or observability docs consulted.
3. `Behavior`: protocol, pipeline, frame shape, event-loop flow, back-pressure, errors, and close behavior.
4. `Command path`: exact build, test, run, or diagnostic commands run or recommended.
5. `Validation`: parser tests, `EmbeddedChannel` tests, integration checks, logs, or runtime results.
6. `Handoffs`: framework, API contract, persistence, observability, Docker, Fly.io, or deployment follow-up when the task crosses this skill's boundary.

## Guardrails

- Do not add direct SwiftNIO code when Vapor, Hummingbird, or another accepted framework API fits the job clearly.
- Do not block event loops.
- Do not create hidden global event-loop groups or shut down event-loop groups owned by callers.
- Do not assume an inbound read contains a whole protocol frame.
- Do not ignore failed futures, promises, writes, flushes, channel closes, or async task cancellation.
- Do not claim SwiftNIO behavior from memory when current official docs or source can be checked.
