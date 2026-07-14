---
name: apple-communication-workflow
description: Choose and plan Apple communication features across CallKit, PushKit, AVFAudio, App Intents phone schemas, Messages extensions, Shared with You collaboration, and Mac Phone or Messages operator surfaces.
---

# Apple Communication Workflow

## Purpose

Route an Apple communication feature to the documented framework that owns it. This is a decision and handoff skill; use `apple-dev-skills` for implementation, build, and device validation.

## Supported Lanes

- **VoIP calling app:** CallKit reports and receives system call actions; PushKit handles VoIP notification delivery; AVFAudio configures live-call audio; App Intents can expose a real calling app's calling actions to system experiences.
- **iMessage app:** a Messages extension creates interactive, app-specific messages in a user conversation.
- **Collaboration:** Shared with You Core connects app-owned collaboration metadata and settings to Messages, Mail, and FaceTime.
- **Mac operator surfaces:** Phone and Messages are user-operated apps. Treat external MCP products as optional discovery targets, not native APIs.

## Workflow

1. Use Xcode DocumentationSearch before planning Apple behavior; confirm framework availability and capability requirements.
2. For a VoIP app, separate CallKit call transactions, PushKit arrival, AVFAudio route/interruption policy, network media, app state, and UI. CallKit acceptance is not permission to begin media before the system activates audio.
3. For a Messages extension, design an interactive user action and app-specific message payload; do not imply unattended server access to iMessage conversations.
4. For collaboration, use the app's real collaboration identity and `SWCollaborationCoordinator`; do not introduce a duplicate collaboration store just for Messages.
5. For Phone or Messages MCP evaluation, inspect public source, supported API, requested permissions, storage, authentication, audit behavior, and live test evidence before recommending it. Never authorize or automate personal calls/messages without the user's explicit instruction.
6. Hand implementation to CallKit/PushKit, AVFAudio, App Intents, Messages, Shared with You, or Xcode validation workflows as applicable.

## Output

Return the lane, documented behavior, required targets/capabilities or privacy keys, data and authorization boundary, validation device requirement, and the owning Apple skill. Clearly call out any unsupported macOS Phone/Messages automation request.
