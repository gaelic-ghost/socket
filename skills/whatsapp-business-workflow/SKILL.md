---
name: whatsapp-business-workflow
description: Plan and validate official WhatsApp Business messaging integrations, including onboarding, webhooks, conversation policy, templates, consent, and provider boundaries.
---

# WhatsApp Business Workflow

## Workflow

1. Confirm the current official WhatsApp Business Platform path or the chosen approved provider before implementation. Record who owns the business account, phone number, webhook, and credentials.
2. Recheck current Meta policy for user opt-in, template approval, conversation windows, message categories, and regional restrictions. These rules are release-sensitive and must not be copied from memory.
3. Verify webhook authenticity, deduplicate status/message events, and separate inbound message handling from delivery/read-status processing.
4. Treat a WhatsApp phone identity, application account, user consent, template, and conversation window as explicit data inputs.
5. Design opt-out, human escalation, media retention, and failure fallback before adding AI-generated replies.
6. Validate with an approved test environment, observed webhook signatures, template state, inbound/outbound behavior, delivery status, and stop/escalation paths.

## Provider Boundary

An approved CPaaS provider can simplify transport but does not remove WhatsApp business policy obligations. Keep provider-specific types and credentials at the provider boundary; do not convert this skill into a universal WhatsApp client.
