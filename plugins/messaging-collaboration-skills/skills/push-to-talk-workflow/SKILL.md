---
name: push-to-talk-workflow
description: Build an Apple Push to Talk channel experience with system controls, ephemeral PTT pushes, audio-session ownership, and an app-owned communication backend.
metadata:
  hermes:
    category: apple-development
    tags: [push-to-talk, ptt, audio, apns, channels]
---

# Push To Talk Workflow

## Purpose

Build a walkie-talkie-style application using PushToTalk. The framework supplies
system controls and channel lifecycle; the app still owns identity, membership,
audio transport, encryption, moderation, and backend behavior.

## Workflow

1. Model a channel with stable app-owned identity, membership authorization,
   transmission mode, and explicit join/leave lifecycle.
2. Use `PTChannelManager` and its delegate for system-visible channel state and
   begin/end transmission events. Treat half-duplex and full-duplex as product
   decisions, not interchangeable audio modes.
3. Configure the app's audio session only in response to the applicable PTT
   lifecycle event; preserve interruptions, Bluetooth routing, and privacy
   indicators.
4. Use the channel's ephemeral push token only for that channel lifetime. Send
   APNs PTT pushes with `pushtotalk`, the `.voip-ptt` topic suffix, immediate
   priority, and no stale-delivery window when the event is time-sensitive.
5. Keep transport, codec, encryption, recording, retention, and moderation as
   explicit app/backend responsibilities.

## Validation

Validate on physical iPhone/iPad hardware with multiple participants, lock
screen controls, join/leave churn, token rotation, delayed audio, interruptions,
Bluetooth accessories, denied microphone permission, and expired-channel push
delivery.

## References

- [Creating a Push to Talk app](https://developer.apple.com/documentation/pushtotalk/creating-a-push-to-talk-app)
- [Push to Talk framework](https://developer.apple.com/documentation/pushtotalk)
