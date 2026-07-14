# AGENTS.md

This file refines the Socket root guidance for `messaging-collaboration-skills`.

## Scope

- This child plugin is the decision and workflow layer for chat, business messaging, meeting collaboration, iMessage collaboration, and Apple VoIP integrations.
- `skills/` is the authored source of truth. The plugin is guidance-only; do not bundle an MCP server, daemon, credential store, client SDK, or provider-neutral runtime without an explicit later approval.
- Route server implementation to the chosen stack plugin, Apple work to `apple-dev-skills`, Android work to `android-dev-skills`, and transport problems to `network-protocol-skills`.

## Platform Rules

- Check current official documentation before asserting supported capabilities, policy windows, product availability, consent requirements, or SDK status.
- Treat Signal as unsupported for official bot development. Do not recommend unofficial account automation as an equivalent workaround.
- Treat iMessage as a Messages extension and Shared with You collaboration surface, not a server-side bot API.
- Treat the macOS Phone and Messages apps as user-operated surfaces. Do not claim they expose a general automation API, and do not recommend a third-party MCP product without first checking its source, privacy model, authorization scope, and live behavior.
- For Apple VoIP, keep CallKit call actions, PushKit notification handling, AVFAudio session policy, network media, and app UI as explicit separate responsibilities. Do not add a broad call manager or global coordinator unless a real codebase demonstrates the missing ownership boundary.
- For business messaging, include consent, opt-out, sender/brand verification, template or policy-window requirements, rate limits, delivery states, and human escalation when those apply.
- Webhook examples must verify authenticity, acknowledge within platform deadlines, make event handling idempotent, and describe retry and duplicate-delivery behavior.

## Validation

```bash
uv run python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/<skill-name>
uv run scripts/validate_socket_metadata.py
```
