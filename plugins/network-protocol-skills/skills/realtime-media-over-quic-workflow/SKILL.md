---
name: realtime-media-over-quic-workflow
description: Plan, evaluate, and diagnose Media over QUIC or MoQ work, including draft-state checks, relay/client/server topology, publish/subscribe object flow, media packaging, live latency, reliability tradeoffs, authorization/privacy drafts, qlog or protocol evidence, and fallback routing to WebRTC, HLS/DASH, HTTP streaming, or stack-specific implementation plugins.
---

# Realtime Media Over QUIC Workflow

## Purpose

Use this skill for Media over QUIC work where MoQ terminology, relay topology, media-object delivery, or draft-aware experimentation is central. Treat MoQ as draft-driven until current IETF status proves otherwise.

## Source Check

Start with the [IETF MoQ working group documents](https://datatracker.ietf.org/wg/moq/documents/). Check the current active drafts before giving production guidance, especially:

- `draft-ietf-moq-transport`
- streaming format drafts such as `draft-ietf-moq-msf`, `draft-ietf-moq-cmsf`, or related packaging drafts when media format matters
- security, authorization, privacy, relay, qlog, and extension drafts when those behaviors are in scope

State the exact draft names and dates used. If the implementation targets a library, relay, CDN, browser experiment, or product preview, check its current docs or source too.

## Planning Workflow

1. Inspect the media job:
   - live streaming, contribution, relay/CDN distribution, watch party, camera feed, generated media, telemetry plus media, or experiment
   - latency budget, viewer count, publisher count, reliability, ordering, object lifetime, rewind, caching, and fanout needs
   - media format, packaging, timestamps, encryption, authorization, and privacy requirements
   - existing WebRTC, HLS, DASH, LL-HLS, WebSocket, or HTTP streaming path
2. Decide whether MoQ fits:
   - fits when object-oriented low-latency media distribution, relay subscriptions, and QUIC transport properties are the core problem
   - does not fit by default for stable browser conferencing, ordinary app chat, file downloads, simple event streams, or production video delivery with mature HLS/DASH requirements
3. Separate roles:
   - publisher, subscriber, relay, catalog/discovery, auth service, media packager, player, and observability owner
   - do not make one service own relay, auth, media packaging, storage, and player behavior without a concrete reason
4. Design fallback:
   - WebRTC for browser/native real-time calls and peer/media interactivity
   - HLS/DASH or LL-HLS for broad production video playback
   - WebSocket or SSE for non-media app events
   - HTTP/3 or direct QUIC only when the transport itself is the experiment

## Validation

Use evidence that matches the claim:

- draft version and implementation commit/version
- relay/publisher/subscriber logs
- qlog or protocol event output
- measured startup, live edge, and rebuffer behavior
- object loss, ordering, and retransmission behavior
- authorization and encryption checks
- player compatibility and fallback behavior

If validation requires a real network, media device, CDN, relay, or browser experiment that is not available, report that as a manual validation gap.

## Output Shape

Return:

1. `MoQ fit`: yes, no, experiment-only, or mixed.
2. `Draft state`: exact IETF drafts and dates checked.
3. `Topology`: publisher, relay, subscriber, packager, player, auth, and observability roles.
4. `Media behavior`: latency, reliability, ordering, packaging, encryption, authorization, and fallback.
5. `Implementation owner`: stack plugin, relay/library, client, deployment, or docs-only plan.
6. `Validation`: logs, qlog, media metrics, compatibility checks, or manual gaps.

## Guardrails

- Do not present MoQ as a stable production default while the relevant behavior is still draft-driven.
- Do not use MoQ as a synonym for WebRTC, HTTP/3, or generic QUIC.
- Do not skip fallback planning for user-facing media.
- Do not claim relay/CDN behavior without implementation-specific evidence.
