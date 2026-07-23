# Playback Validation and Handoffs

## Remote Validation Matrix

| Surface | Evidence |
| --- | --- |
| System-player baseline | Verify the AVKit path before accepting a custom-player escalation. |
| Transport | Play/Pause, select, scrub, skip, previous/next, and command enablement match the active media item. |
| Navigation | Menu/Back exits or dismisses predictably and returns focus to an intentional browse control. |
| System state | Now Playing metadata and system media controls reflect item, position, rate, and terminal state. |
| Alternate input | Test controller support whenever claimed; test remote behavior on physical Apple TV for hardware-dependent flows. |
| Lifecycle | Exercise buffering, interruption, error, item replacement, end-of-item, and app/background transitions supported by the product. |
| Feature path | Validate HLS/interstitial/overlay/proposal/Continuity behavior on the required device and account/stream configuration. |

## Handoffs

Use `avfoundation-media-pipeline-workflow` for AVAsset loading, player-item
pipeline behavior, capture, reader/writer, export, and transcode work. Use
`coremedia-timing-samplebuffer-workflow` for timing and sample-buffer evidence,
and `avfaudio-session-workflow` for app audio policy. Use
`xcode-testing-workflow` to design or execute repeatable runtime verification;
manual device evidence remains necessary for remote and hardware-only behavior.
