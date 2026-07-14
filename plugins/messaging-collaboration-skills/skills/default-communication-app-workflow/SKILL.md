---
name: default-communication-app-workflow
description: Plan iOS and iPadOS default messaging, calling, dialer, and carrier messaging app roles while separating documented system integrations from an app-owned macOS companion implementation.
metadata:
  hermes:
    category: apple-development
    tags: [default-app, messaging, calling, dialer, rcs, sms, mms]
---

# Default Communication App Workflow

## Purpose

Choose the documented default-app role before building routing, UI, account, or
transport logic. A default messaging app, default calling app, default dialer,
and default carrier messaging app are separate products with different system
contracts.

## iOS And iPadOS Roles

1. **Default instant messaging app:** requires the Default Messaging App
   entitlement and `im:` URL handling. It receives a recipient address, not
   arbitrary message body content; provide `sms:` fallback only when the app
   cannot handle the recipient.
2. **Default calling app:** requires real VoIP capability, the Default Calling
   App entitlement, `voip` background mode, and CallKit or
   LiveCommunicationKit. Handle `tel:` routing and offer an explicit system
   fallback when VoIP cannot complete.
3. **Default dialer:** uses LiveCommunicationKit for cellular conversation
   initiation and has a separate Default Dialer App entitlement. Treat EU
   account/device requirements as release gates, not implementation details.
4. **Default carrier messaging app:** uses TelephonyMessagingKit for SMS, MMS,
   and RCS. Keep its entitlement, carrier behavior, user data, and EU
   availability separate from internet messaging.

## macOS Boundary

Do not claim a corresponding documented macOS default messaging or calling-app
role without current Apple evidence. When building for macOS, implement an
app-owned messaging/calling client, account setup, local notifications,
contacts/share integrations where available, and companion continuity behavior.
That client must not imply access to Apple Messages, Phone, carrier SMS/MMS/RCS,
or system call routing.

## Validation And Release Gates

Validate default-role selection, URL routing, unavailable-recipient and
transport fallback, entitlement/provisioning state, privacy disclosures,
physical-device behavior, regional availability, and App Review evidence. Keep
each role's capability inventory in the app project; do not silently enable an
entitlement because another communication role needs it.

## References

- [Preparing your app to be the default messaging app](https://developer.apple.com/documentation/messages/preparing-your-app-to-be-the-default-messaging-app)
- [Preparing your app to be the default calling app](https://developer.apple.com/documentation/callkit/preparing-your-app-to-be-the-default-calling-app)
- [Preparing your app to be the default dialer app](https://developer.apple.com/documentation/livecommunicationkit/preparing-your-app-to-be-the-default-dialer-app)
- [Creating a carrier messaging app](https://developer.apple.com/documentation/availability/creating-a-carrier-messaging-app)
