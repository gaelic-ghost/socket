---
name: choose-network-transport
description: Choose the right application transport or real-time protocol before implementation. Use when Codex needs to route work across plain HTTP routes, HTTP/2, HTTP/3, QUIC, WebSocket, WebTransport-adjacent designs, WebRTC media or data channels, Media over QUIC, gRPC, RPC, streaming APIs, mobile app networking, browser networking, server frameworks, deployment proxies, or protocol diagnostics.
---

# Choose Network Transport

## Purpose

Choose the smallest transport that fits the feature before code changes start. The practical decision is whether the work needs request/response HTTP, bidirectional messages, browser media, low-latency object delivery, direct QUIC behavior, or a higher-level framework route.

## Source Check

Check repo-local docs and current protocol sources before making claims:

- [RFC 9000: QUIC](https://datatracker.ietf.org/doc/rfc9000/)
- [RFC 9114: HTTP/3](https://datatracker.ietf.org/doc/rfc9114/)
- [W3C WebRTC](https://www.w3.org/TR/webrtc/)
- [RFC 8825: Real-Time Protocols for Browser-Based Applications](https://datatracker.ietf.org/doc/rfc8825/)
- [IETF MoQ working group documents](https://datatracker.ietf.org/wg/moq/documents/)

State whether the chosen protocol is stable, draft-driven, browser-dependent, platform-dependent, or blocked by deployment infrastructure.

## Classification Workflow

1. Inspect the feature:
   - client runtime: browser, Apple app, Android app, CLI, backend service, embedded device, or server-to-server
   - payload shape: request/response, events, streams, media frames, files, game state, telemetry, commands, or arbitrary bytes
   - latency, reliability, ordering, congestion, and back-pressure needs
   - network reality: proxies, CDN, firewalls, NAT, mobile networks, UDP availability, TLS termination, and HTTP version support
   - existing stack plugins that own implementation details
2. Choose the candidate:
   - plain HTTP routes for simple request/response APIs, CRUD, webhooks, and service commands
   - Server-Sent Events for one-way server-to-browser event streams where HTTP infrastructure matters more than bidirectional transport
   - WebSocket for widely deployed bidirectional app messages when media, NAT traversal, and multiplexed streams are not the core job
   - HTTP/3 when the app benefits from QUIC-backed HTTP semantics, modern CDN/browser support, reduced head-of-line blocking, or migration from HTTP/2
   - direct QUIC only when the application must own streams, datagrams, connection migration, or transport behavior below HTTP
   - WebRTC for browser or native real-time audio, video, screen sharing, data channels, NAT traversal, and peer/media topology work
   - Media over QUIC when the work is low-latency media distribution, relay/subscription/object delivery, or draft experimentation where MoQ terminology is central
   - gRPC or RPC when typed service contracts, generated clients, streaming RPCs, or internal service boundaries are the dominant need
3. Reject overbuilt options:
   - do not choose QUIC only because HTTP/3 exists
   - do not choose WebRTC for ordinary app messages that a WebSocket or HTTP route can handle
   - do not choose MoQ for general video chat, conferencing, or stable production media unless the draft and implementation risk is explicit
   - do not choose MCP, custom RPC, or a bespoke protocol when a plain route is clearer
4. Route implementation to the owning stack plugin.

## Handoffs

- Use `http3-quic-workflow` for HTTP/3, QUIC, ALPN, Alt-Svc, UDP, proxy, or transport-version work.
- Use `webrtc-workflow` for WebRTC media, data channels, signaling, ICE, TURN, browser/native constraints, or peer/media topology.
- Use `realtime-media-over-quic-workflow` for Media over QUIC or MoQ draft-driven media distribution.
- Use `network-protocol-diagnostics` when the task begins with logs, packet captures, browser failures, proxy behavior, TLS, CDN, or NAT traversal.
- Use stack plugins for implementation: `server-side-swift`, `rust-skills`, `python-skills`, `server-side-jvm`, `web-dev-skills`, `apple-dev-skills`, `android-dev-skills`, and `cloud-deployment-skills`.

## Output Shape

Return:

1. `Chosen transport`: HTTP, SSE, WebSocket, HTTP/3, direct QUIC, WebRTC, MoQ, gRPC/RPC, or mixed.
2. `Why`: concrete feature and deployment evidence.
3. `Maturity`: RFC-backed, W3C-backed, draft-driven, browser-dependent, platform-dependent, or infrastructure-gated.
4. `Implementation owner`: stack plugin, framework, package, service, or client surface.
5. `Validation`: exact build, test, browser, runtime, trace, curl, qlog, packet-capture, or deployment check.
6. `Handoffs`: next skill or plugin to use.
