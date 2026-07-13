---
name: mainstage-workflow
description: Guide safe MainStage concert, set, patch, channel-strip, audio and MIDI device, mapping, rehearsal, backup, and live-performance preparation. Use when a user needs to prepare or troubleshoot MainStage while avoiding surprise routing, patch, playback, recording, or concert-file changes.
---

# MainStage Workflow

Use this skill for MainStage app operation and rehearsal preparation. Treat an active performance configuration as high risk.

## Source Check

Search the local Tips/Help Viewer catalog for `MainStage` or open MainStage Help. Confirm the guide matches the installed app/version. Read `references/concert-safety-contract.md` before changing concert, set, patch, device, mapping, playback, or recording state.

## Workflow

1. Classify the request: inspect, rehearsal preparation, concert/set/patch organization, audio/MIDI device setup, channel-strip routing, mapping, missing device/plug-in repair, backup, or live-performance issue.
2. Establish the performance contract: whether the configuration is live, rehearsal-only, or disposable; available audio/MIDI hardware; intended inputs/outputs; selected concert/set/patch; backup location; and what must not change.
3. Inspect before action: active mode, selected set/patch, concert path, audio device, MIDI devices/controllers, channel strips, output routing, mappings, missing plug-ins/media, and current playback/record state.
4. Preserve the concert. For configuration changes, use a duplicate or explicit backup. Do not save over an active performance file without confirmation.
5. Confirm immediately before changing selected patches, audio or MIDI devices, channel-strip output routes, mappings, playback, recording, or concert file state. State the user-visible effect and recovery path.
6. Prepare one rehearsal path: verify audio input/output, MIDI response, patch selection, mappings, level/mute behavior, and any backing-track/transport behavior using observed device evidence.
7. Report the ready/not-ready state with the specific concert/set/patch, connected devices, tested routes, untested components, backup status, and next safe action.

## Guards

- Never validate against a live show without explicit confirmation at the moment of the potentially disruptive action.
- Do not change a concert, patch, mapping, or audio/MIDI device merely to see what happens.
- Do not claim hardware routing, controller response, latency, or sound-check readiness without observed device evidence.
- Do not perform unattended playback, recording, or device reconfiguration.
- Do not treat missing plug-ins/media as something to replace automatically; identify the exact dependency and stop for direction.

## Handoffs

- `logic-pro-workflow` for Logic session/bounce preparation before a MainStage handoff.
- `apple-dev-skills:avfaudio-session-workflow` or `avaudio-engine-workflow` for application-code audio routing or engine issues.
- `apple-dev-skills:xcode-build-run-workflow` only when MainStage-related work actually concerns an Apple app or plug-in project build/run surface.
