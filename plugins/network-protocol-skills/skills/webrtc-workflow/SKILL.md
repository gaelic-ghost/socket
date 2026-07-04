---
name: webrtc-workflow
description: Plan, implement, test, and diagnose WebRTC work, including W3C and IETF source checks, browser and native runtime support, signaling boundaries, ICE/STUN/TURN, DTLS, SRTP, SDP offer/answer, tracks, transceivers, data channels, media devices, permissions, NAT traversal, SFU/MCU decisions, and handoffs to web, mobile, server, or deployment plugins.
---

# WebRTC Workflow

## Purpose

Use this skill when a task needs real-time browser or native media, peer connection behavior, data channels, NAT traversal, or WebRTC signaling. Keep signaling, media transport, application state, and deployment roles separate.

## Source Check

Check current sources before claiming behavior:

- [W3C WebRTC](https://www.w3.org/TR/webrtc/)
- [RFC 8825: Real-Time Protocols for Browser-Based Applications](https://datatracker.ietf.org/doc/rfc8825/)
- [RFC 8831: WebRTC Data Channels](https://datatracker.ietf.org/doc/rfc8831/)
- [RFC 8445: Interactive Connectivity Establishment](https://datatracker.ietf.org/doc/rfc8445/)

Also check browser compatibility, native SDK docs, SFU/MCU docs, and deployment provider docs because behavior often depends on runtime and network shape.

## Planning Workflow

1. Inspect the feature:
   - audio, video, screen sharing, camera capture, data channel, file transfer, game state, remote control, or mixed
   - browser, iOS/macOS, Android, desktop native, server-side media, or headless runtime
   - peer-to-peer, SFU, MCU, broadcast, recording, transcription, or relay topology
   - permissions, device selection, codecs, simulcast/SVC, bandwidth adaptation, and privacy needs
2. Separate responsibilities:
   - signaling channel: offer/answer exchange, trickle ICE, room/session state, auth, retries, and reconnection
   - media/data transport: peer connection, tracks, transceivers, DTLS/SRTP, SCTP data channels, congestion, and stats
   - NAT traversal: STUN, TURN, ICE candidates, relay policy, and corporate/mobile network constraints
   - application behavior: UI state, moderation, recording, storage, payments, analytics, and notifications
3. Choose topology:
   - peer-to-peer for small direct calls when NAT and scale fit
   - SFU for multi-party calls, server-side forwarding, selective subscription, recording, or moderation
   - MCU when server-side compositing is required and latency/cost tradeoffs are accepted
   - WebSocket or HTTP for signaling; do not confuse signaling with media transport
   - MoQ or HTTP streaming only when the media distribution problem is not conversational WebRTC
4. Route implementation to stack plugins:
   - `web-dev-skills` for browser UI and TypeScript integration
   - `apple-dev-skills` or `android-dev-skills` for native app integration
   - `server-side-swift`, `python-skills`, `server-side-jvm`, or `rust-skills` for signaling services, SFU integration, or backend work
   - `cloud-deployment-skills` for TURN, UDP, firewall, autoscaling, media servers, and hosting constraints

## Diagnostics

Gather evidence from:

- browser WebRTC internals, stats, and network panels
- native SDK logs and permission state
- signaling logs with offer/answer and ICE candidate flow
- STUN/TURN reachability and credentials
- SFU/MCU room, track, and subscription logs
- packet capture only when logs cannot identify the failing hop

Name the failing layer: permissions, media capture, signaling, SDP, ICE, DTLS, SRTP, data channel, codec negotiation, SFU, TURN, firewall, or UI state.

## Output Shape

Return:

1. `WebRTC shape`: media, data channel, or mixed; browser, native, server, or mixed.
2. `Topology`: peer-to-peer, SFU, MCU, broadcast, recording, or fallback.
3. `Boundaries`: signaling, media/data transport, NAT traversal, app state, and deployment owner.
4. `Evidence`: docs, code, logs, WebRTC stats, TURN/STUN checks, or browser/native runtime observations.
5. `Validation`: local call, multi-peer test, device/browser matrix, network path, media quality, stats, or manual gaps.
6. `Handoffs`: web, mobile, backend, cloud, MoQ, or diagnostics workflow.

## Guardrails

- Do not treat WebRTC signaling as the media transport.
- Do not skip TURN planning for user-facing calls across real networks.
- Do not claim codec, permission, or browser behavior without current runtime/source checks.
- Do not replace WebRTC with MoQ for conversational media unless the product requirements explicitly fit that tradeoff.
