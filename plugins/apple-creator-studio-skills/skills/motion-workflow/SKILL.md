---
name: motion-workflow
description: Guide safe Motion projects, compositions, behaviors, keyframes, generators, titles, effects, Final Cut Pro templates, publishing, render/export, and source-project preservation. Use when a user needs to create, inspect, edit, publish, or deliver a Motion project or Final Cut Pro template without losing the editable source.
---

# Motion Workflow

Use this skill for Motion app operation and Final Cut Pro template authoring, not Core Animation, AVFoundation, or custom graphics-code work.

## Source Check

Open Motion Help or search the local Tips/Help Viewer catalog for `Motion`. Confirm the guide matches the installed app/version before relying on project-type, publish, template, or render behavior. Read `references/project-template-and-render-contract.md` before changing a source project, publishing a template, or rendering an artifact.

## Workflow

1. Classify the task: composition, Final Cut title/effect/generator/transition, source-project repair, behavior/keyframe animation, parameter publishing, media replacement, render/export, or Final Cut Pro handoff.
2. Establish the artifact contract: editable source location, project type, resolution/frame rate/duration/color space, media policy, intended published parameters/category, render format, destination, overwrite rule, and receiving app/version.
3. Inspect before action: project type, current preset/timing/color state, selected layers/groups/behaviors/keyframes, source-media links, template publish state, and output destination.
4. Preserve the source project. Duplicate or use a new project before changing a reusable template, replacing media, flattening/rebuilding layers, or publishing a revision that can replace an installed Final Cut Pro template.
5. Keep parameters and timing intentional. Expose only user-meaningful Final Cut Pro controls, use clear names/defaults/ranges, and distinguish an editable Motion source from a rendered deliverable or published template.
6. Confirm immediately before replacing media, deleting layers/assets, publishing/updating a Final Cut Pro template, rendering/exporting, or overwriting a source/delivery/template revision. State the exact target, destination, category, name, and recovery path.
7. Verify in the relevant surface: inspect Motion project state, reopen a render, or confirm that the intended Final Cut Pro template category/controls load correctly. For delivery, inspect name, location, duration, dimensions, codec/container, alpha/color, and audio where applicable.

## Guards

- Do not publish a template merely to test whether Final Cut Pro sees it; use a disposable name/category or obtain confirmation.
- Do not replace linked media, remove layers, or flatten source state without a source-preservation decision.
- Do not claim template parameter behavior, alpha, color, timing, or Final Cut Pro availability without observed evidence.
- Do not silently inherit a high-resolution, high-frame-rate, or long-duration project preset when the target is unspecified.
- Hand custom graphics, rendering, video, or image processing code to `apple-dev-skills`.

## Handoffs

- `final-cut-pro-workflow` for receiving, placing, and verifying a published Motion template in an edit.
- `compressor-workflow` for final delivery packaging after a Motion render exists.
- `apple-dev-skills:core-animation-layer-workflow`, `core-image-processing-workflow`, or `avfoundation-media-pipeline-workflow` for code-level implementation.
