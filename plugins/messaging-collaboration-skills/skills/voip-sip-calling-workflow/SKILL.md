---
name: voip-sip-calling-workflow
description: Build a native Apple VoIP calling app by separating CallKit or LiveCommunicationKit, PushKit, AVFAudio, SIP or WebRTC transport, and call-state ownership.
metadata:
  hermes:
    category: apple-development
    tags: [voip, sip, callkit, pushkit, audio, webrtc]
---

# VoIP SIP Calling Workflow

## Purpose

Build an Apple VoIP calling app without conflating system call presentation,
audio-session activation, signaling, media transport, and account state.

## Architecture

- **System integration:** use CallKit or LiveCommunicationKit for call actions,
  system UI, and system coordination.
- **Wake-up:** use PushKit VoIP notifications only for a real incoming call that
  is promptly reported through the supported calling framework.
- **Audio:** use AVFAudio/AVAudioSession for activation, route changes,
  interruptions, Bluetooth, and media permissions.
- **Signaling and media:** choose SIP, WebRTC, or another documented transport
  based on interoperability, NAT traversal, codec, security, and backend needs.
  SIP is a protocol lane, not an Apple calling UI API.
- **App state:** own account identity, call state, reconnection, recording,
  retention, emergency-call policy, and end-to-end encryption explicitly.

## Workflow

1. Define incoming, outgoing, answer, decline, end, hold, mute, transfer, and
   failure state transitions before integrating UI.
2. Report incoming calls to the system promptly, then start media only after the
   calling framework and audio system permit it.
3. Design a transport adapter behind explicit call-state inputs and outputs;
   never let SIP registration or WebRTC callbacks become the global UI owner.
4. Decide the fallback behavior separately for VoIP failure and cellular calling.
5. Route default-calling or default-dialer eligibility to
   `default-communication-app-workflow`.

## Validation

Test physical-device incoming/outgoing calls, background arrival, lock screen,
audio route and interruption changes, reconnect, duplicate pushes, signaling
failure, media failure, and user-visible fallback.

## References

- [Making and receiving VoIP calls](https://developer.apple.com/documentation/callkit/making-and-receiving-voip-calls)
- [CallKit](https://developer.apple.com/documentation/callkit)
- [Initiating VoIP conversations with LiveCommunicationKit](https://developer.apple.com/documentation/livecommunicationkit/initiating-voip-conversations-with-livecommunicationkit)
