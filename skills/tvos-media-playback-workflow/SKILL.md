---
name: tvos-media-playback-workflow
description: "Guide tvOS media playback: AVKit-first player choice, custom escalation, remote commands, Now Playing, and validation. Use for AVPlayerViewController, MPRemoteCommandCenter, playback focus, or media-control boundaries."
---

# tvOS Media Playback Workflow

## Purpose

Guide the tvOS media-control contract. This skill starts with AVKit's system
player, makes custom-player escalation evidence-based, and keeps remote command
routing, player state, and Now Playing information under one explicit owner.
It does not replace general AVFoundation pipelines, Core Media timing, audio
session policy, or Xcode execution workflows.

## When To Use

- Use this skill for `AVPlayerViewController`, system-player adoption, AVKit
  playback UI, custom info tabs, overlays, content proposals, HLS
  interstitials, Picture in Picture, and playback-focused tvOS design.
- Use this skill for `MPRemoteCommandCenter`, remote transport commands,
  `MPNowPlayingInfoCenter`, custom player controls, command enablement, and
  Apple TV media-state ownership.
- Use this skill when a product believes it needs a custom player; first decide
  whether AVKit's system player satisfies the actual requirement.
- Use this skill for remote/controller command validation, post-playback focus
  restoration, and device-only playback capability gates.
- Recommend `tvos-app-experience-workflow` for browsing UI, focus layout,
  remote-first app navigation, Large Text, TVMLKit migration, or general tvOS
  platform constraints.
- Recommend `avfoundation-media-pipeline-workflow` for general asset loading,
  capture, readers, writers, export, transcode, and playback-pipeline repair.

## Single-Path Workflow

1. Classify the playback request:
   - system player adoption
   - AVKit extension or supporting content
   - custom-player justification
   - remote command or Now Playing state
   - HLS/interstitial/continuity feature
   - runtime validation or repair
2. Apply the Apple docs gate:
   - read current AVKit, AVFoundation, MediaPlayer, and release-note evidence
   - state the documented behavior relied on before recommending a control path
   - version-qualify beta APIs and device-specific behavior
3. Prefer the system player:
   - choose `AVPlayerViewController` when its controls and supported extension
     points satisfy the requirement
   - name the concrete unavailable product behavior before choosing custom UI
   - keep the custom path responsible for every relevant remote command and
     media-state transition
4. Establish one media-control owner:
   - player lifecycle and current item
   - command enablement and `MPRemoteCommandCenter` handlers
   - `MPNowPlayingInfoCenter` state
   - interruption/end-of-item behavior and focus restoration
5. Return one recommendation with:
   - player choice and documented rationale
   - command/state ownership
   - feature and device gates
   - remote validation matrix and handoff

## Inputs

- `request`: optional free-text playback task.
- `playback_goal`: optional `system-player`, `custom-player`, `remote-command`,
  `now-playing`, `hls`, `interstitial`, `overlay`, `proposal`, `continuity`, or
  `validation`.
- `player_context`: optional current player, UI customization, media type, and
  command requirement.
- `target_context`: optional Apple TV model, tvOS/Xcode version, controller,
  and physical-device availability.
- Defaults:
  - docs-first guidance always applies
  - prefer `AVPlayerViewController` over a custom player
  - one explicit owner manages player state, commands, and Now Playing state

## Outputs

- `status`
  - `success`: a playback ownership recommendation is ready
  - `handoff`: another workflow owns the actual next step
  - `blocked`: the required device, entitlement, stream, or framework evidence
    is missing
- `path_type`
  - `primary`: AVKit system-player or documented extension path
  - `fallback`: custom-player or device-only feature path
- `output`
  - resolved player path
  - documented Apple behavior relied on
  - command and state ownership
  - capability/beta gate
  - validation matrix and handoff

## Guards and Stop Conditions

- Do not start with custom playback controls when `AVPlayerViewController`
  satisfies the product requirement.
- Do not treat a custom player as cosmetic: it must support applicable remote
  commands, media-control state, interruption/end behavior, and focus return.
- Do not scatter `MPRemoteCommandCenter` handlers, player state, or
  `MPNowPlayingInfoCenter` updates across unrelated views.
- Do not claim HLS, interstitial, Picture in Picture, Continuity Camera,
  controller, remote, or system-media-control behavior is verified without
  relevant runtime evidence.
- Do not run general media type, timing, capture, reader/writer, export, or
  audio-session work through this skill when an existing specialist owns it.
- Stop with `blocked` when the requested behavior depends on unavailable stream,
  account, hardware, signed entitlement, or physical-device evidence.

## Fallbacks and Handoffs

- Recommend `tvos-app-experience-workflow` for app navigation, focus layout,
  Large Text, remote-first browsing UI, and TVMLKit migration.
- Recommend `avfoundation-media-pipeline-workflow` for assets, capture, player
  pipeline, reader/writer, export, or transcode ownership.
- Recommend `coremedia-timing-samplebuffer-workflow` for timestamps, timebases,
  format descriptions, and sample-buffer synchronization.
- Recommend `avfaudio-session-workflow` for audio intent, routes,
  interruptions, microphone permission, and audio-session behavior.
- Recommend `xcode-build-run-workflow` for project/device deployment and
  `xcode-testing-workflow` for repeatable playback/runtime verification.
- Recommend `explore-apple-swift-docs` when current AVKit or tvOS docs lookup
  is the real task.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` preserves the shared customization-file
contract. This first version has no runtime-enforced knobs.

## References

### Workflow References

- `references/system-player-and-remote-commands.md`
- `references/playback-validation-and-handoffs.md`
- `references/customization-flow.md`

### Support References

- Recommend `avfoundation-media-pipeline-workflow` for general media-pipeline
  shape and `coremedia-timing-samplebuffer-workflow` for typed timing behavior.
- Recommend `explore-apple-swift-docs` for current framework availability and
  release-note evidence.

### Script Inventory

- `scripts/customization_config.py`
