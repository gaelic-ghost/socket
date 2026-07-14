# Messaging Collaboration Phase 3 Readiness Plan

## Decision

Phase 3 remains a readiness and evidence pass until the reference consumers
below demonstrate a repeated implementation need. Do not create a
provider-neutral messaging SDK, universal webhook runtime, shared credential
store, or Messages automation bridge first.

A helper may graduate into Phase 3 only when at least two real consumers need
the same narrowly defined behavior and can share the same privacy, credential,
failure, and validation contract.

## Reference Consumers

### iMessage Collaboration App

Build an iOS/iPadOS app with an iMessage extension for a user-driven,
participant-visible collaborative activity. `MSMessage` carries versioned,
app-defined state; `MSSession` coordinates updates; the containing app or a
server owns durable state, account authorization, merge rules, and recovery.
Use Shared with You only when the app owns the shared item and collaboration
metadata.

This is not a server-side iMessage bot and does not grant access to a person's
Messages history or unattended sending. Validate with two accounts/devices,
stale state, missing app account, backend outage, and participant rejoin.

### Push-To-Talk App With Hummingbird Lambda

Build a channel-based Apple PushToTalk client with app-owned identity,
membership, media transport, encryption, retention, and moderation. The client
uses `PTChannelManager` for system controls and channel lifecycle, waits for the
framework to activate audio before recording, and treats Core Bluetooth accessory
events as user-initiated transmission triggers only.

Bootstrap the backend as a fresh Hummingbird Lambda application through the
official `hb` CLI. Its narrow jobs are channel authorization, participant state,
short-lived APNs PTT-token registration, PTT notification dispatch, and a
health/audit surface. It is not the media relay unless a later transport decision
explicitly requires that. Keep APNs credentials and channel tokens server-side;
send PTT pushes using the documented `pushtotalk` type and `.voip-ptt` topic.

Validate physical-device channel join/leave, token rotation, PTT push delivery,
Bluetooth/wired-headset trigger behavior, audio interruption and route changes,
half-duplex handoff, and backend unavailable/recovery states.

### Default Messaging App Exploration

Build an iOS/iPadOS app-owned instant-messaging service that can opt into the
documented default messaging role. It must use its own identity, conversation,
delivery, and retention model. The `im:` URL route supplies a recipient address;
it is not an API to send or read iMessage content.

Treat carrier SMS/MMS/RCS as a separate discovery lane. TelephonyMessagingKit
and the Default Carrier Messaging App role have distinct eligibility, privacy,
and EU availability constraints. Do not imply that the default instant-messaging
role can send iMessage, read Apple Messages, or automatically gain RCS access.

Validate `im:` routing, unavailable-recipient fallback, entitlement and
provisioning behavior, Siri/Apple Intelligence message-domain integration, and
regional carrier-messaging gates independently.

### Discord Personal Projects

Use Fizze Assistant as the first real bot reference: a private Swift Gateway bot
that combines realtime events with Discord HTTP commands and keeps its local
state deliberately small. Build the next projects as distinct consumers:

- a user-installed app with installation and private-channel command boundaries;
- an HTTP interaction/webhook integration that validates signatures and responds
  within Discord's deadline; and
- a Gateway bot when realtime guild events or long-lived state are required.

Do not derive a shared Discord runtime until these projects identify a common
contract beyond routine REST/Gateway plumbing.

## Supported Hook Inventory

| Hook | Supported use | Boundary |
| --- | --- | --- |
| Messages extension | User-driven interactive iMessage payload and session | No inbox/history or unattended iMessage bot access. |
| Shared with You | App-owned shared item and collaboration metadata | Not a Messages transcript API. |
| Default messaging | App-owned instant messaging through `im:` routing | Does not control iMessage or carrier messaging. |
| Carrier messaging | SMS/MMS/RCS through TelephonyMessagingKit when eligible | Separate entitlement and EU availability gate. |
| Communication notifications/NSE | This app's alert enrichment, intent donation, and Focus-aware presentation | NSE cannot inspect or filter other apps' notifications. |
| App extension targets | Containing-app extension lifecycle, app groups, entitlements, activation, and process isolation | Each extension point has its own host contract. |
| PushToTalk and accessories | System PTT controls; Core Bluetooth, headset, or CarPlay transmission triggers | App owns transport/media; wait for system audio activation. |
| Group Activities | Synchronize an app-defined SharePlay activity over FaceTime/Messages | No public remote-screen-control or FaceTime-control API. |
| App Intents | Expose app-owned actions/data to Siri, Shortcuts, Spotlight, Apple Intelligence | Never exposes another app's private messages. |
| User-owned Mac/VPS | Run the user's own client, agent bridge, webhook receiver, or backend | Access only data and APIs the user/app explicitly owns and authorizes. |

## Agent Integration Contract

Agents may act through a user-owned app's App Intents, explicit in-app actions,
Shortcuts, authenticated server APIs, Discord interactions/webhooks, or a
user-owned Mac/VPS bridge for that app's own data. Every mutation needs an
identity, authorization scope, audit event, user-visible result, and failure
path. Do not present private Apple Messages/FaceTime/Phone state as an agent
integration surface without a documented API and explicit authorization.

## Phase 3 Helper Gate

Candidate helpers must satisfy every condition before implementation:

1. Two reference consumers need the same behavior without platform-specific policy differences.
2. The helper has one owner and no credentials or user-message content by default.
3. Its failure behavior, idempotency/retry contract, and audit data can be specified and tested independently.
4. A fixture can prove it against the real platform contract.

Initial candidates to evaluate, not implement yet: signed Discord interaction or
webhook verification fixtures, platform-local event replay fixtures, and PTT
channel/auth state test fixtures.

## Sources

- [Messages](https://developer.apple.com/documentation/messages)
- [Default messaging app](https://developer.apple.com/documentation/messages/preparing-your-app-to-be-the-default-messaging-app)
- [Carrier messaging app](https://developer.apple.com/documentation/availability/creating-a-carrier-messaging-app)
- [Creating a Push to Talk app](https://developer.apple.com/documentation/pushtotalk/creating-a-push-to-talk-app)
- [Group Activities](https://developer.apple.com/documentation/groupactivities/groupactivity)
- [Messages App Intents domain](https://developer.apple.com/documentation/appintents/app-schema-domain-messages)
- [Discord interactions and commands](https://docs.discord.com/developers/platform/interactions)
- [Discord Gateway](https://docs.discord.com/developers/events/gateway)
- [Hummingbird server workflow](../../plugins/server-side-swift/skills/hummingbird-server-workflow/SKILL.md)
