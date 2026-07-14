---
name: communication-notifications-workflow
description: Implement Apple communication and Time Sensitive notifications with intent donation, Focus behavior, and a bounded Notification Service Extension processing path.
metadata:
  hermes:
    category: apple-development
    tags: [notifications, communication, focus, time-sensitive, nse]
---

# Communication Notifications Workflow

## Purpose

Deliver calling and messaging notifications with accurate people and
conversation context, while keeping Focus behavior, interruption level, and
Notification Service Extension processing within their documented boundaries.

## Workflow

1. Confirm that the notification represents a real person-to-person
   communication or incoming call; do not use communication presentation to
   promote unrelated activity.
2. Configure the required push, communication-notification, Time Sensitive,
   and Siri/intent capabilities only when the feature qualifies.
3. Donate the applicable message or call intent and set the needed
   `NSUserActivityTypes` entry for the supported communication surface.
4. Add a Notification Service Extension only when an alert payload needs bounded
   enrichment, decryption, attachment download, or communication-content update.
5. Send alert payloads with `mutable-content: 1`; return the best available
   content before the extension expires. Silent, sound-only, and badge-only
   pushes do not invoke the extension.
6. Treat Time Sensitive delivery and Focus status as user-controlled system
   behavior, not a guarantee that a notification will interrupt someone.

## Data And Safety Boundaries

- Keep push payloads privacy-minimal; decrypt or fetch sensitive display data
  only when needed and tolerate extension timeout.
- Do not make notification filtering a hidden policy engine. The extension may
  transform this app's incoming alert, not inspect or filter other apps' alerts.
- Provide a plain fallback title/body if enrichment fails.

## Validation

Validate on physical devices with notification permission, Focus modes,
communication metadata, Time Sensitive settings, extension timeout fallback,
network loss, and redacted-lock-screen behavior.

## References

- [Handling Communication Notifications and Focus Status Updates](https://developer.apple.com/documentation/UserNotifications/handling-communication-notifications-and-focus-status-updates)
- [Modifying content in newly delivered notifications](https://developer.apple.com/documentation/usernotifications/modifying-content-in-newly-delivered-notifications)
