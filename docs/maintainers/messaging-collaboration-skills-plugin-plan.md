# Messaging Collaboration Skills Plugin Plan

## Intent

`messaging-collaboration-skills` helps Codex choose, build, test, and maintain user-facing communication integrations without treating distinct platform policies as one interchangeable chat API. It covers server bots, workspace apps, business messaging agents, meeting add-ons, iMessage collaboration, Apple notification and Push to Talk experiences, native VoIP calling, and documented default-app roles.

The first release is a companion guidance plugin. It does not ship an MCP server, a webhook relay, a credential store, a daemon, a provider-neutral client library, or a Mac Phone/Messages automation bridge.

That deliberately small shape unlocks two immediate use cases: an agent can correctly select and bootstrap a platform integration, and it can hand the resulting implementation to the owning server, web, Android, or Apple workflow. It removes the current duplication of rediscovering platform identity, webhook, consent, and human-handoff constraints. The simpler alternative—adding only platform bookmarks—was considered, but would not give Codex a shared decision path or safe implementation boundaries.

## Packaging Direction

Package this as the independent Socket child plugin at `plugins/messaging-collaboration-skills/`. Its root owns the Codex-facing manifest, authored `skills/`, local `AGENTS.md`, and branded assets. Socket's root marketplace lists it as a normal local child plugin.

The plugin must remain a guidance surface until two real projects demonstrate a repeated, compatible need for executable shared support. If that happens, assess a narrow reference library or MCP bridge in a separate design decision; do not retrofit a universal SDK into these skills.

## Codex And Hermes Compatibility

Every new or materially changed Messaging Collaboration skill must carry an
explicit Codex-and-Hermes compatibility decision in the same pass. The Codex
plugin manifest remains the Socket install surface; a portable `SKILL.md` may
also be exported through the root Hermes skill tap, but that export must be
recorded in the shared inventory and grouped in `skills.sh.json`. Do not present
the Codex manifest as a Hermes plugin.

If a later phase adds a `.mcp.json`, add its checked-in Hermes `mcp_servers`
translation and inventory entry at the same time. Do not copy user configuration,
secrets, or machine-local paths into Socket. If a future runtime feature needs a
Hermes tool, hook, command, or namespaced runtime behavior, design a real native
Hermes plugin with its own lifecycle and validation; otherwise mark the surface
host-specific by design. This first guidance-only release has no MCP or native
Hermes plugin requirement.

## Platform Boundary Map

| Surface | Supported integration shape | Explicit boundary |
| --- | --- | --- |
| Discord | Installed app, HTTP/Gateway interaction bot, Activity | Commands and interaction responses are not generic webhooks. |
| Telegram | HTTPS Bot API, webhook or polling, Mini App | A bot cannot initiate a private conversation before the user starts or adds it. |
| Slack | Workspace app with OAuth, Events API, interactivity, Socket Mode | Workspace scopes and installation are core product behavior. |
| Teams | Teams SDK or Microsoft 365 Agents SDK bot/agent | Microsoft Entra and tenant deployment are first-class boundaries. |
| WhatsApp | WhatsApp Business Platform or an approved provider | Business onboarding, templates, policy windows, and verification must be rechecked at implementation time. |
| SMS/MMS/RCS | Carrier/CPaaS or RCS for Business agent | Consent, sender registration, regional rules, and fallback are required design inputs. |
| Google Meet | Add-on, REST conference/artifact integration, Media API preview | Meet is collaboration/conferencing, not a generic chat-bot target. |
| iMessage and Messages collaboration | Messages app extension and Shared with You collaboration | No general server-side iMessage bot API. |
| Apple Phone and VoIP | CallKit or LiveCommunicationKit, PushKit, AVFAudio, documented Siri/Intents call surfaces, SIP/WebRTC transport | The macOS Phone app is an operator surface, not an automation API. |
| Signal | No official bot workflow | Do not route users to unofficial account automation as a supported Signal integration. |

## Apple Communication Scope

The Apple workflow has three independent lanes:

1. **VoIP calling app** — CallKit or LiveCommunicationKit owns native call UI and action transactions; PushKit is the incoming-call wakeup boundary; AVFAudio owns the active call audio-session policy; use App Intents only for app-owned discoverability/Shortcuts and the documented Siri/Intents call surface where it applies.
2. **iMessage user app and collaboration** — Messages extensions create interactive messages and versioned, participant-visible `MSMessage`/`MSSession` state; Shared with You Core connects a first-party app's collaboration metadata to Messages, Mail, and FaceTime. These are complementary, not interchangeable.
3. **Communication notification and Push to Talk** — UserNotifications and a Notification Service Extension enrich this app's alert payload; communication and Time Sensitive behavior require the applicable capability and intent integration. PushToTalk owns system channel controls while the app owns identity, transport, and media.
4. **VoIP, SIP, and default roles** — CallKit or LiveCommunicationKit owns system calling integration, PushKit owns real incoming-call arrival, AVFAudio owns audio policy, and SIP/WebRTC is an independent signaling/media transport choice. Default messaging, calling, dialer, and carrier messaging roles have separate entitlements and availability.
5. **macOS client and third-party MCP products** — where Apple documents no macOS default messaging or calling role, build an app-owned macOS client with only the supported client, notification, contact, share, and continuity integrations. A skill must not claim an Apple-provided Messages or Phone control API, must never automate a user's personal messages or calls without explicit authorization, and must require a source, privacy, capability, and live-behavior review before recommending an external MCP package.

## Phase 1: Cross-Platform Foundations

- `messaging:choose-platform-integration`: classify the desired surface, scope, user identity, installation, deployment, and runtime owner before implementation.
- `messaging:webhook-and-event-lifecycle`: model signature verification, idempotency, acknowledgement deadlines, retries, ordering, rate limits, observability, and secret handling.
- `messaging:conversation-state-human-handoff`: define per-platform identity mapping, durable state, consent, escalation, transcript boundaries, and operator-visible failures.
- `messaging:apple-communication-workflow`: choose among CallKit/LiveCommunicationKit, PushKit, AVFAudio, documented Siri/Intents call or messaging surfaces, Messages extensions, Shared with You, and Mac operator/discovery surfaces.

Phase 1 exit criteria: a new integration can be accurately routed without introducing a universal runtime abstraction, and Apple calling/Messages requests are separated into documented supported lanes.

## Phase 2: Supported Platform Workflows

- `messaging:discord-app-workflow`
- `messaging:telegram-bot-workflow`
- `messaging:slack-app-workflow`
- `messaging:teams-agent-workflow`
- `messaging:whatsapp-business-workflow`
- `messaging:sms-mms-rcs-workflow`
- `messaging:google-meet-collaboration-workflow`

Phase 2 exit criteria: each workflow starts from official current documentation, identifies the correct app identity and inbound event model, covers authentication/installation/consent, and hands implementation to an owning Socket stack plugin without inventing an SDK.

## Deferred Phases

### Phase 2.5: Apple Communication Systems

- `messaging:imessage-app-and-collaboration-workflow`: build iMessage extensions, interactive message/session state, and Shared with You without suggesting server-side personal-message access.
- `messaging:communication-notifications-workflow`: model Communication Notifications, Time Sensitive policy, Focus behavior, intent donation, and bounded Notification Service Extension enrichment/fallback.
- `messaging:push-to-talk-workflow`: plan PushToTalk channels, ephemeral APNs PTT delivery, audio session ownership, and app-owned backend/media behavior.
- `messaging:voip-sip-calling-workflow`: separate CallKit/LiveCommunicationKit, PushKit, AVFAudio, SIP/WebRTC signaling and media, and call-state ownership.
- `messaging:default-communication-app-workflow`: distinguish iOS/iPadOS default messaging, calling, dialer, and carrier-messaging roles from an app-owned macOS companion/client implementation.

Phase 2.5 exit criteria: each Apple communication lane names its documented system contract, app-owned responsibilities, entitlement or capability gate, physical-device validation, and macOS boundary without claiming an undocumented default-app or automation role.

### Phase 3: Executable Reference Work

Only after repeated implementation evidence, assess narrow helpers for webhook verification fixtures, event replay tests, or platform-local samples. Do not create a shared service unless its ownership, credentials, state, and failure behavior are proven common across at least two live consumers.

The current proof targets and agent-integration boundaries are maintained in the
[Phase 3 readiness plan](./messaging-collaboration-phase-3-readiness-plan.md).

### Phase 4: MCP Evaluation And Operator Workflows

Evaluate external messaging MCP products by source, supported API, data access, authorization model, auditability, and runtime proof. A bundled MCP server remains out of scope until a concrete, maintainable operator need is approved.

### Phase 5: Expansion And Release Maintenance

Consider Google Chat, Zoom, Matrix, customer-support systems, carrier-specific routes, and verified provider adapters. Recheck platform policies, availability, and SDK lifecycle before each expansion.

## Documentation And Validation

- Use current official platform documentation before making implementation claims.
- Use Xcode DocumentationSearch or other local Apple documentation sources first for Apple behavior.
- Keep secrets out of repository files and examples.
- Run the skill quick validator for every new `SKILL.md` and Socket metadata validation after marketplace or manifest edits.
- For every changed skill, record whether it is exported through the Hermes tap or intentionally remains Codex-only; for every future MCP declaration, add and validate its Hermes translation in the same pass.
- Export the portable Messaging Collaboration skills through the Hermes tap, keep their grouping inventory current, and validate the generated export before release.
- Add root README and ROADMAP inventory language in the same pass as an installable plugin.

## Release Decision

After Phases 1 and 2 validate, release this as a Socket minor version because it adds a new installable plugin and a substantive new capability surface. Phases 3 through 5 require a separate discussion before implementation.
