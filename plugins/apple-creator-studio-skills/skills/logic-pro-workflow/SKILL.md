---
name: logic-pro-workflow
description: Guide safe Logic Pro projects, audio and MIDI device preflight, recording, arrangement, routing, mixing, bounce and stem delivery, and MainStage handoffs. Use when a user needs to operate or stabilize a Logic Pro session while preserving recordings, takes, project media, and delivery artifacts.
---

# Logic Pro Workflow

Use this skill for Logic Pro app/session operation. Hand custom audio-engine or Apple audio-framework code to `apple-dev-skills`.

## Source Check

Open Logic Pro Help or search the local Tips/Help Viewer catalog for `Logic Pro`, then confirm the guide matches the installed app/version. Read `references/session-and-delivery-contract.md` before recording, routing, freezing, bouncing, or replacing session material.

## Workflow

1. Classify the task: project setup, device/input issue, recording, MIDI/audio editing, arrangement, routing/mix, stem/master bounce, missing media/plug-in, or MainStage handoff.
2. Establish the session contract: project location, source-preservation decision, tempo/key/sample-rate intent, device/input/monitoring requirements, target deliverable, output location, and overwrite rule.
3. Inspect the project before changing it: project settings, tracks, selected channel strips, routing, automation, plug-in state, audio/MIDI device state, existing takes, unresolved warnings, and current output settings.
4. Preserve recordings and project media. Create a copy or use an explicit non-destructive path before replacing takes, flattening/freeze-related changes, destructive edits, track deletion, or broad routing changes.
5. Configure only the required audio/MIDI path. State the device, input, output, monitoring, and latency consequence. Get confirmation immediately before recording or changing audio-device/routing state that could disrupt the session.
6. Make arrangement, mix, or routing changes with clear ownership: tracks feed buses, buses feed outputs, and any plug-in/automation change has a stated audible or delivery purpose.
7. Before bouncing, state master-versus-stems, range, format, sample rate/bit depth, normalization/dither policy when relevant, destination, exact file names, and overwrite behavior. Get confirmation before writing outputs.
8. Verify the bounce or stems: files exist in the intended directory, play/open correctly, meet the requested duration/range and format, and preserve the source project.

## Guards

- Do not begin recording, replace takes, change audio devices, freeze/flatten, delete tracks, or overwrite a bounce without a visible user confirmation.
- Do not claim an interface, plug-in, input, or MIDI controller is available without inspecting the current session/system state.
- Do not hide a broad routing change behind vague “cleanup”; describe the affected tracks, buses, and outputs.
- Do not recommend loudness, normalization, dither, or mastering settings without knowing the delivery target.
- Do not substitute this skill for AVAudioEngine, Core Audio, Audio Unit, or file-processing implementation guidance.

## Handoffs

- `mainstage-workflow` for rehearsal concert, set, patch, mapping, and live-performance preparation.
- `compressor-workflow` for video/audio delivery packaging after a final export or bounce exists.
- `apple-dev-skills:avaudio-engine-workflow`, `avfaudio-session-workflow`, or `coreaudio-modernization-repair-workflow` for code-level audio behavior.
