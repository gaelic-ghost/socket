---
name: apple-communication-workflow
description: Route an Apple communication request to iMessage collaboration, communication notifications, Push to Talk, VoIP calling, default-app, or macOS companion workflows before implementation.
---

# Apple Communication Workflow

## Purpose

Route an Apple communication feature to the documented framework and dedicated
workflow that owns it. This is a decision and handoff skill; use
`apple-dev-skills` for implementation, build, and device validation.

## Supported Lanes

- **iMessage app and collaboration:** a Messages extension creates interactive,
  app-specific messages; Shared with You connects app-owned collaboration
  metadata to system surfaces.
- **Communication notification:** a Notification Service Extension enriches a
  mutable remote alert before delivery; communication and Time Sensitive
  behavior require the applicable capability and intent integration.
- **Push to Talk:** PushToTalk owns system controls and channel events while the
  app owns the backend, audio transport, and channel membership.
- **VoIP calling:** CallKit or LiveCommunicationKit owns system call UI and
  transactions; PushKit handles arrival; AVFAudio owns audio policy; SIP or
  WebRTC remains a transport decision.
- **Default app:** iOS/iPadOS default messaging, calling, dialer, and carrier
  messaging roles have distinct entitlements, routing, and regional limits.
- **macOS companion:** when there is no documented macOS default-app role, build
  an app-owned client and integrations rather than claiming control of Phone or
  Messages.

## Workflow

1. Use Xcode DocumentationSearch before planning Apple behavior; confirm framework availability and capability requirements.
2. Route to exactly one detailed workflow: `imessage-app-and-collaboration-workflow`, `communication-notifications-workflow`, `push-to-talk-workflow`, `voip-sip-calling-workflow`, or `default-communication-app-workflow`.
3. For Phone or Messages MCP evaluation, inspect public source, supported API, requested permissions, storage, authentication, audit behavior, and live test evidence before recommending it. Never authorize or automate personal calls/messages without the user's explicit instruction.
4. Hand implementation to the relevant Apple framework and Xcode validation workflows.

## Output

Return the lane, detailed workflow, documented behavior, required
targets/capabilities or privacy keys, data and authorization boundary,
validation device requirement, and owning Apple skill. Clearly call out the
difference between a documented iOS/iPadOS default-app role and an app-owned
macOS companion implementation.
