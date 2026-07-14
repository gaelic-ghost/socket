---
name: webhook-and-event-lifecycle
description: Design and repair secure inbound events, webhooks, interactions, retries, acknowledgements, and delivery observability for messaging and collaboration platforms.
---

# Webhook And Event Lifecycle

## Purpose

Make inbound messaging events trustworthy, prompt, idempotent, and diagnosable. This skill owns the event boundary; it does not own application business logic, persistent conversation policy, or a platform transport implementation.

## Workflow

1. Read current official delivery and signature-verification documentation for the selected platform.
2. Capture the platform's request signature, timestamp/replay guard, response deadline, retry policy, event ID, ordering guarantees, and rate limits.
3. Verify authenticity before parsing or enqueueing work. Reject an invalid request with a descriptive operator-facing log that identifies the platform, validation stage, and likely cause without exposing secrets.
4. Deduplicate on the platform event identity before side effects. Persist an explicit processing state when retries can outlive a request.
5. Acknowledge on time, then execute slow work through the selected app runtime. Use platform-native deferred responses where they exist.
6. Record correlation IDs, delivery outcome, retry count, and a privacy-safe error summary. Do not log raw message content or tokens by default.

## Required Output

Document the request verifier, acknowledgement path, duplicate rule, retry and failure behavior, ordering assumption, response/update path, and targeted replay test. Hand service implementation to the chosen server stack skill.

## Guards

- Do not use a shared webhook wrapper merely because multiple providers use HTTP.
- Do not acknowledge an event as successful before a required signature or idempotency check.
- Do not claim a webhook works without a platform test delivery, local signed fixture, or observed request trace.
