---
name: conversation-state-human-handoff
description: Plan conversation identity, state, consent, escalation, transcript, and human-handoff behavior for bots and business messaging agents.
---

# Conversation State And Human Handoff

## Purpose

Design a narrow, explainable conversation boundary. Platforms identify people, installations, channels, and conversations differently, so normalize only the application facts needed for the product; do not erase platform identity or policy distinctions.

## Workflow

1. Identify the platform-native sender, conversation, installation or tenant, message, and consent identifiers.
2. State which identifiers are durable, which can change, and which are sensitive.
3. Define the minimal state required for the user experience: task progress, user preference, handoff status, and delivery context.
4. Specify an explicit escalation path: trigger, acknowledgement, operator queue or destination, visible transition, return-to-automation rule, and unavailable-hours behavior.
5. Apply platform and product consent/retention rules before storing transcripts, media, model inputs, or contact data.
6. Test interruption, duplicate delivery, human takeover, failed escalation, opt-out, deletion, and resumed conversation behavior.

## Guards

- Do not map identities across platforms as though they represent the same authenticated person without an explicit account-linking flow.
- Do not let an AI response conceal that a human has joined or left when the platform has a representative-state mechanism.
- Do not introduce repositories, managers, or state mirrors into an app without a concrete ownership need.
