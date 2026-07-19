---
name: operate-hermes-agent-gateway
description: Configure, run, secure, and troubleshoot Hermes Agent messaging gateways, platform adapters, webhooks, API server, long-lived profiles, and remote deployments across built-in and custom channels.
metadata:
  hermes:
    category: agent-portability
    tags: [hermes, messaging, gateway, webhooks, api-server]
---

# Operate Hermes Agent Gateway

Treat the messaging gateway as a long-running service with external identities, inbound events, persistent sessions, and delivery obligations.

## Define the Deployment

1. Name the platform or API surface.
2. Name the Hermes profile that owns its config, credentials, memory, sessions, skills, and gateway state.
3. Choose the host and terminal backend.
4. Define authorized users, chats, workspaces, or webhook senders before enabling actions.
5. Define delivery behavior for replies, media, scheduled work, and failures.
6. Define process supervision and logs through Hermes-supported or OS-supported service paths; do not invent a second gateway manager.

## Keep Gateway Surfaces Distinct

- Messaging gateway: `hermes gateway` and its platform adapters.
- API server: OpenAI-compatible HTTP endpoint hosted by the gateway.
- Webhooks: inbound event routes that trigger agent work.
- TUI gateway: JSON-RPC host protocol, not the messaging service.
- Nous Tool Gateway: hosted tool backends, not message transport.

## Configure Safely

- Use a dedicated profile when a bot identity or authorization boundary differs.
- Keep platform tokens and API server keys in private configuration.
- Bind local dashboards and APIs to localhost by default.
- Require explicit authentication and network controls before exposing an API or dashboard beyond localhost.
- Use platform allowlists and Hermes user authorization; do not rely on obscurity or a private-looking channel name.
- Prefer containerized or managed terminal backends for unattended public gateways.
- Preserve per-platform toolset differences rather than enabling every local tool everywhere.

## Validate Before Unattended Operation

1. Start the intended profile and gateway in the foreground.
2. Confirm platform authentication and connection state.
3. Send a harmless message from an authorized identity.
4. Confirm session routing and response delivery.
5. Confirm an unauthorized identity is rejected or constrained as designed.
6. Exercise one harmless tool allowed on that platform.
7. Confirm logs redact secrets and identify the profile/platform/session on failure.
8. Only then move to the approved long-running service path.

## Build a New Platform Adapter

Hand extension work to `build-hermes-agent-extensions`. A platform adapter is a specialized plugin registered through the gateway platform interface, not a general plugin disguised as a messaging integration. Cover configuration, auth, inbound normalization, outbound delivery, media, slash commands, session keys, authorization, and tests.

## Troubleshoot by Path

Check:

1. process and profile;
2. platform credentials;
3. network connection or webhook reachability;
4. authorization;
5. inbound event normalization;
6. session routing;
7. model/provider and tool availability;
8. outbound formatting and delivery;
9. retry, rate-limit, and shutdown behavior.

Read [references/gateway-surface-map.md](references/gateway-surface-map.md) for deployment shapes, integration boundaries, and official sources.
