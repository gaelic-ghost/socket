---
name: final-cut-pro-workflow
description: Guide safe Final Cut Pro libraries, events, projects, media imports, proxy and optimized-media decisions, timeline edits, roles, captions, shares, and Compressor/Motion handoffs. Use when a user needs to inspect, edit, repair, export, or hand off a Final Cut Pro project while preserving source media and existing libraries.
---

# Final Cut Pro Workflow

Use this skill for Final Cut Pro app operation, not AVFoundation or custom media-code work.

## Source Check

Open Final Cut Pro Help or search the local Tips/Help Viewer catalog for `Final Cut Pro`. Confirm the guide matches the installed app/version before relying on an import, library, proxy, share, or relink path. Read `references/library-and-delivery-contract.md` before changing a library, event, project, media relationship, or delivery artifact.

## Workflow

1. Classify the task: inspection, library/event organization, import, proxy or optimized-media decision, edit, captions/roles, missing-media repair, Motion handoff, share/export, Compressor delivery, or output verification.
2. Establish the artifact contract: library/project path, source-media policy, managed-versus-external media state, intended timeline/range, target platform, format, roles/captions, destination, overwrite rule, and deliverable owner.
3. Inspect before action: selected library/event/project, active timeline, media locations, missing-media/proxy state, render/share state, connected storage, selected ranges, and existing destination contents.
4. Preserve source state. Use a duplicate library/project or explicit backup before consolidation, relinking, deleting generated files, changing media location, or making wide timeline changes. Do not infer that a generated proxy, optimized copy, or render file is safe to remove.
5. Make the smallest correct edit. Keep project, event, library, media, and role boundaries clear; explain any tradeoff in proxy quality, optimized-media storage, color/HDR, captions, or sharing settings.
6. Confirm immediately before importing into a managed library, relinking, consolidating, deleting generated/original media, modifying a shared timeline, rendering, sharing, exporting, or replacing an existing delivery. State the exact source/range, destination, name, format, and overwrite behavior.
7. Verify the result: inspect library/project state after edits, or inspect the exported artifact for name, location, duration, dimensions, codec/container, audio, captions/roles, color/HDR, and target playback where required.

## Guards

- Do not open, modify, consolidate, or repair an unfamiliar library as a probe.
- Do not confuse deleting generated media with a harmless operation; inspect whether original, optimized, proxy, render, or cache assets are selected.
- Do not relink or reveal missing media by guessing a replacement path.
- Do not claim a Motion template is installed or a Compressor delivery is valid until the receiving app or output artifact has been checked.
- Hand source-code media processing, codecs, and application implementation to `apple-dev-skills`.

## Handoffs

- `motion-workflow` for titles, effects, generators, and transitions authored for Final Cut Pro.
- `compressor-workflow` for an explicit delivery preset, batch, and artifact verification after Final Cut Pro creates the source master.
- `apple-dev-skills:avfoundation-media-pipeline-workflow` or `video-codec-processing-workflow` for code-level media handling.
