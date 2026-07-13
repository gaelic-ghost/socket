---
name: garageband-workflow
description: Guide safe GarageBand projects, audio and MIDI recording, Apple Loops, arrangement, automation, movie soundtrack work, export, and Logic Pro handoffs. Use when a user needs to operate GarageBand while preserving recordings, tracks, project media, and final delivery artifacts.
---

# GarageBand Workflow

Use this skill for GarageBand app operation. GarageBand is a companion workflow, not an Apple Creator Studio subscription-app claim.

## Source Check

Search the local Tips/Help Viewer catalog for `GarageBand` or open GarageBand Help. Confirm the guide matches the installed app/version. Read `references/project-and-handoff-contract.md` before recording, replacing regions, changing audio devices, exporting, or moving work into Logic Pro.

## Workflow

1. Classify the task: project setup, device/input issue, recording, software instrument/MIDI, Apple Loops, arrangement, automation, movie soundtrack, mix, export, missing content, or Logic Pro handoff.
2. Establish the project contract: project location, source-preservation decision, tempo/key/sample-rate intent, device/input/monitoring requirements, target deliverable, output location, and overwrite rule.
3. Inspect before changing: project settings, tracks, regions/takes, selected track controls, automation, plug-in state, audio/MIDI device state, existing media, unresolved warnings, and export state.
4. Preserve recordings and project media. Use an explicit copy or non-destructive path before replacing recordings, deleting tracks/regions, flattening project decisions, or making broad routing changes.
5. Configure only the needed audio/MIDI path. State the device, input, output, monitoring, and likely interruption consequence. Get confirmation immediately before recording or changing an audio-device/routing state.
6. Make arrangement, loop, automation, or mix changes with a stated purpose. Do not replace a region, take, or loop selection merely to experiment unless the user has approved that edit.
7. Before exporting or sharing, state the range, output type, quality settings, output name, destination, overwrite behavior, and whether the result is a review mix, final audio file, or a movie soundtrack. Get confirmation before writing output.
8. Verify the resulting artifact exists in the intended directory, opens or plays, matches the intended range/format, and leaves the source project intact. For Logic Pro handoffs, state what transferred and what still needs inspection in Logic.

## Guards

- Do not claim GarageBand belongs to Apple Creator Studio; it is an adjacent companion app.
- Do not begin recording, replace takes/regions, change audio devices, delete content, or overwrite an export without a visible user confirmation.
- Do not claim an interface, plug-in, input, or MIDI controller is available without inspecting the actual project/system state.
- Do not promise a lossless GarageBand-to-Logic transfer without checking the available project/export handoff route and the specific project content.
- Hand custom audio-engine, Core Audio, or Audio Unit code to `apple-dev-skills`.

## Handoffs

- `logic-pro-workflow` when a GarageBand project or export needs more advanced recording, routing, editing, mixing, mastering, or stem delivery.
- `compressor-workflow` for final audio/video packaging after GarageBand creates the source deliverable.
- `apple-dev-skills:avaudio-engine-workflow`, `avfaudio-session-workflow`, or `coreaudio-modernization-repair-workflow` for application-code audio behavior.
