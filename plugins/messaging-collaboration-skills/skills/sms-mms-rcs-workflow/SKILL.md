---
name: sms-mms-rcs-workflow
description: Plan, build, and validate consent-aware SMS, MMS, and RCS business messaging agents, including sender setup, webhooks, rich content, delivery, and fallback.
---

# SMS MMS RCS Workflow

## Workflow

1. Classify the requirement as SMS/MMS, RCS for Business, a CPaaS multi-channel route, or an Android/iOS app compose/OTP feature. These are not equivalent APIs.
2. Define sender ownership, country/carrier coverage, registration and verification, consent evidence, opt-out/help handling, content class, rate limits, and fallback before sending any message.
3. For RCS for Business, model an agent with an external trigger, HTTP API, webhook responses, device capability check, rich-card fallback, and SMS fallback for unsupported recipients.
4. Verify inbound signatures, deduplicate events, track delivery states, and prevent a retry from becoming a duplicate user notification.
5. Keep OTP use limited to an authorized authentication flow; do not treat a client-side SMS/RCS retriever as permission to read ordinary user messages.
6. Validate a test sender, inbound reply, opt-out, unreachable recipient, fallback, media behavior, and delivery failure path in the intended region.

## Sources And Handoffs

Use [RCS for Business](https://developers.google.com/business-communications/rcs-business-messaging/guides/get-started/how-it-works) for Google's direct route. A provider route may use [Twilio Programmable Messaging](https://www.twilio.com/docs/messaging), but it must retain the provider's sender and consent requirements. Hand Android app work to `android-dev-skills` and backend work to the selected server skill.
