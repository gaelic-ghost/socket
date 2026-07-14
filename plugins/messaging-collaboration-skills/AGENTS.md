# AGENTS.md

This file refines the Socket root guidance for `messaging-collaboration-skills`.

## Scope

- This child plugin is the decision and workflow layer for chat, business messaging, meeting collaboration, iMessage collaboration, and Apple VoIP integrations.
- `skills/` is the authored source of truth. The plugin is guidance-only; do not bundle an MCP server, daemon, credential store, client SDK, or provider-neutral runtime without an explicit later approval.
- Every new or materially changed skill must explicitly record whether it is eligible for the shared Hermes skill-tap export or remains Codex-only by design. Any future `.mcp.json` must ship with its checked-in Hermes `mcp_servers` translation and inventory entry; any real Hermes runtime behavior requires a separately designed native Hermes plugin, never a manifest shim.
- Route server implementation to the chosen stack plugin, Apple work to `apple-dev-skills`, Android work to `android-dev-skills`, and transport problems to `network-protocol-skills`.

## Platform Rules

- Check current official documentation before asserting supported capabilities, policy windows, product availability, consent requirements, or SDK status.
- Treat Signal as unsupported for official bot development. Do not recommend unofficial account automation as an equivalent workaround.
- Treat iMessage as a Messages extension and Shared with You collaboration surface, not a server-side bot API. For interactive iMessage collaboration, define participant-visible versioned message/session state and recipient reconstruction behavior.
- Treat Communication Notifications, Time Sensitive notifications, Focus behavior, and Notification Service Extensions as separate user-controlled or bounded system contracts; never imply an NSE can inspect or filter other apps' notifications.
- Treat PushToTalk as its own channel and system-controls framework. Keep channel membership, transport, audio, encryption, recording, and retention as explicit app/backend responsibilities.
- Treat CallKit or LiveCommunicationKit as the system calling layer, PushKit as real incoming-call delivery, AVFAudio as audio policy, and SIP/WebRTC as separate transport choices. Use App Intents for app-owned discoverability or Shortcuts only; use the documented Siri/Intents call or message domains where applicable.
- Treat default messaging, calling, dialer, and carrier messaging as separate iOS/iPadOS roles with distinct entitlements and regional availability. Where no documented macOS default role exists, build an app-owned macOS client without claiming control of Apple Messages, Phone, carrier messaging, or system call routing.
- Treat the macOS Phone and Messages apps as user-operated surfaces. Do not claim they expose a general automation API, and do not recommend a third-party MCP product without first checking its source, privacy model, authorization scope, and live behavior.
- For Apple VoIP, keep CallKit call actions, PushKit notification handling, AVFAudio session policy, network media, and app UI as explicit separate responsibilities. Do not add a broad call manager or global coordinator unless a real codebase demonstrates the missing ownership boundary.
- For business messaging, include consent, opt-out, sender/brand verification, template or policy-window requirements, rate limits, delivery states, and human escalation when those apply.
- Webhook examples must verify authenticity, acknowledge within platform deadlines, make event handling idempotent, and describe retry and duplicate-delivery behavior.

## Validation

```bash
uv run python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/<skill-name>
uv run scripts/validate_socket_metadata.py
uv run scripts/export_hermes_skills.py
uv run scripts/validate_hermes_compatibility.py
```
