---
name: imessage-app-and-collaboration-workflow
description: Build an iMessage app or collaboration feature with Messages extensions, interactive message sessions, and Shared with You without implying server-side access to personal conversations.
metadata:
  hermes:
    category: apple-development
    tags: [imessage, messages, collaboration, shared-with-you]
---

# iMessage App And Collaboration Workflow

## Purpose

Build a user-driven iMessage app or an app-owned collaboration feature. This
workflow covers Messages extensions and Shared with You, not a general iMessage
bot or access to a person's Messages history.

## Choose The Surface

1. Use a **Messages extension** for an interactive composer experience, custom
   text/sticker/media insertion, or an interactive `MSMessage` in a specific
   conversation.
2. Use `MSSession` when participants update an app-defined interactive message;
   define the app's session state, merge rules, and stale-update behavior.
3. Use **Shared with You** when an app owns the shared item and its
   collaboration metadata; use the app's real identity and coordinator rather
   than creating a Messages-specific copy of collaboration state.
4. Use an app-owned iOS or macOS client when the feature needs a standalone
   conversation list, account system, or collaboration workspace. Do not claim
   that this grants access to Apple Messages conversations.

## Required Boundaries

- An iMessage app acts through a person in a Messages conversation. It does not
  provide unattended server-side iMessage sending or inbox automation.
- Keep message payloads small, versioned, and app-specific. Authenticate or
  authorize any server-backed state independently of the message payload.
- Treat iMessage app availability as iOS/iPadOS. Messages content may be viewed
  on other Apple platforms, but do not claim a macOS iMessage-app extension
  surface.
- Preserve participant consent, deletion behavior, collaboration membership,
  and user-visible failure recovery.

## Validation

Test the extension with two independent accounts or devices, including initial
insert, update, re-open, stale session data, unavailable backend, and a
participant who lacks the containing app's account. Test Shared with You with
the app's real shared-item identity and ensure it never exposes unrelated
private content.

## References

- [Messages framework](https://developer.apple.com/documentation/messages)
- [iMessage apps and stickers](https://developer.apple.com/imessage/)
- [Shared with You](https://developer.apple.com/documentation/sharedwithyou)
