---
name: choose-platform-integration
description: Choose a supported chat, calling, business-messaging, or collaboration integration shape before implementation. Use for Discord, Telegram, Slack, Teams, WhatsApp Business, SMS/MMS/RCS, Google Meet, iMessage collaboration, and Apple VoIP requests.
---

# Choose Platform Integration

## Purpose

Choose the real platform surface before code, credentials, or a shared abstraction are added. The result is a documented integration shape and one implementation handoff, not a fictional universal bot SDK.

## Workflow

1. Classify the request as a server bot, workspace app, business messaging agent, meeting add-on, native Messages extension, VoIP calling app, or Mac operator workflow.
2. Identify the user, installation, identity, inbound-event, outbound-response, and hosting model.
3. Check current official platform docs for availability, policy, review, consent, and SDK lifecycle.
4. Select the owning platform workflow and then the owning stack workflow.
5. Define the minimum secure event contract before implementation: verified source, acknowledgement deadline, idempotency key, retry behavior, state owner, audit boundary, and human handoff.

## Routing

- Discord: installed app and HTTP/Gateway interactions; use `discord-app-workflow`.
- Telegram: Bot API, webhook or polling, optional Mini App; use `telegram-bot-workflow`.
- Slack: workspace OAuth app, Events API, interactivity, or Socket Mode; use `slack-app-workflow`.
- Teams: Teams SDK or Microsoft 365 Agents SDK; use `teams-agent-workflow`.
- WhatsApp, SMS, MMS, or RCS: business-messaging route; use `whatsapp-business-workflow` or `sms-mms-rcs-workflow`.
- Google Meet: add-on, REST conference/artifact integration, or explicitly preview media access; use `google-meet-collaboration-workflow`.
- Apple: CallKit/PushKit/AVFAudio/App Intents, Messages extension, or Shared with You; use `apple-communication-workflow`.
- Signal: report that no official bot route is supported; do not substitute account automation.

## Output

Return the selected surface, reasons, documented constraints, credential and data boundary, implementation owner, validation plan, and rejected alternatives. Stop if the requested platform capability is unsupported or needs a product-policy decision.
