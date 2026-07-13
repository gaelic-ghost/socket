# Apple Creator Studio Skills Plugin Plan

This plan records the durable shape for a Socket-hosted `apple-creator-studio-skills` plugin: operator guidance for people and agents using Apple’s creative applications.

## Recommendation

Create a separate `apple-creator-studio-skills` child plugin for the initial slice: `compressor-workflow`, `logic-pro-workflow`, and `mainstage-workflow`, with `garageband-workflow` as its companion-app extension.

This is a durable building-block change. It gives creative-app operation a clear install, documentation, validation, and ownership boundary without turning `apple-dev-skills` into a catch-all for both media-code implementation and professional-app operation.

The simpler extension path—adding these workflows to `apple-dev-skills`—was considered first. It would be misleading: that plugin owns Swift, Xcode, Apple frameworks, and low-level media-code behavior; Creator Studio skills own libraries, projects, presets, app UI, exports, performance rigs, source artifacts, and human-in-the-loop Computer Use. Keeping the boundaries separate makes requests easier to route and preserves the existing AVFoundation, AVFAudio, Core Media, Core Audio, and VideoToolbox owners.

## Product Boundary

Apple Creator Studio currently includes Final Cut Pro, Logic Pro, Pixelmator Pro, Motion, Compressor, and MainStage. It also provides subscription-only premium features and content in Keynote, Pages, Numbers, and Freeform. Existing one-time-purchase versions of the six Mac creative apps remain usable. [Apple Creator Studio](https://support.apple.com/en-us/125029)

This plugin covers the six dedicated creative applications as operator workflows. It does not automatically absorb productivity-app work, image-code implementation, audio-code implementation, generic video processing, or generic desktop automation.

GarageBand is not an Apple Creator Studio subscription app. It remains a worthwhile companion workflow for accessible music capture and project handoff into Logic Pro, but must be represented accurately in plugin metadata and user-facing wording.

## Ownership And Handoffs

| Request | Owner | Reason |
| --- | --- | --- |
| Edit a Final Cut library, construct a Motion template, transcode in Compressor, mix in Logic, prepare a MainStage concert, or preserve Pixelmator source layers | `apple-creator-studio-skills` | The task is application operation and creative-artifact safety. |
| Implement Swift media capture, playback, export, audio graphs, sample timing, codecs, image processing, or photo-library access | `apple-dev-skills` | The task is Apple framework or Xcode code behavior. |
| Make a deterministic command-line conversion where Compressor’s app path is unavailable or unsuitable | A separate `ffmpeg` or shell workflow | Do not claim a stable Compressor CLI contract without verified current behavior. |
| Automate windows, inspect menus, or drive the app after a user authorizes interaction | The applicable Creator Studio skill plus Computer Use | The creative-app skill owns the decision and safety contract; Computer Use owns UI interaction. |
| Prepare assets in Acorn or RetroBatch | Future `mac-image-workflows` candidate | Those apps are not Creator Studio apps and should not be hidden within an Apple subscription plugin. |

## Design Principles

- Write for both a creator operating the app and an agent helping through Computer Use.
- Preserve source media, project files, libraries, sessions, patches, and layered documents by default.
- Treat render, export, batch submission, external-device changes, library consolidation, relinking, deletion, and publishing as confirmation checkpoints.
- Use the real visible app state as the source of truth. Inspect before acting; do not rely on fixed screen coordinates, assumed panel layouts, or stale menu paths.
- Put app-version, macOS-version, device, plug-in, media, codec, and destination assumptions in the run record when they affect a result.
- Give every workflow one clear artifact contract: inputs, source-preservation policy, target output, destination, and verification method.
- Keep help text concise and procedural. Store app-specific command tables, export settings, and fixture details in skill references, not in a giant shared overview.
- Use official Apple Help, release notes, and support material first. Treat product behavior as version-sensitive and refresh the documentation anchors before adding a new app feature claim.

## Computer Use Contract

Each skill must include these agent-facing rules:

1. Inspect the active app, document, project/library/session state, selected item, and destination before editing.
2. State the proposed mutation in plain language before performing an action that can overwrite, delete, relink, change a live patch, start an expensive render, or publish/share an artifact.
3. Use a visible save-as/copy/duplicate path or a user-confirmed backup when the application supports it and the task risks source loss.
4. Confirm the exact output name, format, destination, and overwrite behavior immediately before exporting, transcoding, bouncing, rendering, or sharing.
5. Verify the resulting artifact in the app or Finder with the concrete condition that matters: a completed job, expected duration/resolution/codec, audible stem, loaded patch, preserved source layer, or readable project.
6. Stop rather than improvising when a modal warning, missing media, missing plug-in, account prompt, permission prompt, unfamiliar destructive dialog, or mismatched project version changes the operation.
7. Keep live MainStage performance surfaces especially conservative: no device routing, patch selection, concert save, or playback/record action without an explicit user-visible checkpoint.

Computer Use is a UI-driving aid, not a promise that every task is safe to run unattended. Skills should describe a human-readable manual route even when the agent can operate the app.

## Shared Artifact Convention

Every workflow should ask for or establish this minimum record:

- source artifact and its location;
- working copy or source-preservation decision;
- app and version; macOS version when it changes behavior;
- intended deliverable and target audience/platform;
- output directory and overwrite policy;
- required constraints: duration, sample rate, resolution, color/HDR, loudness, file size, codec, captioning, stems, or performance hardware;
- verification evidence and any remaining uncertainty.

Never rely on a machine-local path in shipped documentation or plugin metadata. Paths may appear only in a user’s current interactive task or in untracked fixture instructions.

## Skill Inventory

### Initial Slice

#### `compressor-workflow`

Guide media import, presets, settings, destinations, batches, watch-folder decisions, Final Cut Pro/Motion handoff, submission, job monitoring, and verified delivery artifacts.

Primary use cases:

- make a share-ready deliverable from a known source;
- choose or safely customize a preset for a target platform;
- set batch destinations and prevent source/output confusion;
- diagnose a failed, stalled, or unexpected transcode from visible job evidence;
- send Final Cut Pro or Motion work through Compressor deliberately;
- verify codec, resolution, duration, audio, and destination after completion.

Not owned:

- low-level codec code or VideoToolbox session configuration;
- a guaranteed CLI interface;
- replacing a user’s encoding judgment when target delivery requirements are unknown.

Primary source: [Compressor User Guide](https://support.apple.com/guide/compressor/imf-package-fields-cpsra358c67e/mac).

#### `logic-pro-workflow`

Guide projects, audio/MIDI device preflight, recording, editing, arrangement, session-player decisions, routing, mixing, export/bounce, stem delivery, and safe Logic/MainStage handoffs.

Primary use cases:

- begin or stabilize a production session without losing existing media;
- configure an interface, input, monitoring, tempo, and project rate intentionally;
- record or edit audio/MIDI while preserving takes and recoverability;
- organize tracks, buses, plug-ins, automation, and gain staging into a comprehensible mix;
- bounce a master or stems with an explicit deliverable contract;
- prepare a Logic patch/project handoff for MainStage only after device and live-performance constraints are clear.

Not owned:

- custom audio-engine programming;
- unattended recording or destructive session cleanup;
- assertions about plug-in availability without inspecting the actual project and installed system.

Primary source: [Logic Pro User Guide for Mac](https://support.apple.com/en-gb/guide/logicpro/welcome/mac).

#### `mainstage-workflow`

Guide concert/set/patch structure, audio and MIDI device configuration, channel-strip and plug-in routing, mappings, rehearsal checks, backup copies, and explicit live-performance confirmation gates.

Implement with a real device and rehearsal fixture, but keep all live-performance mutations behind visible user checkpoints. Apple’s support resource provides the [MainStage User Guide and release notes](https://support.apple.com/en-us/docs/software/134085).

### Companion-App Extension

#### `garageband-workflow`

Own beginner-friendly project setup, capture, arrangement, Apple Loops, automation, soundtrack work, safe export, and explicit GarageBand-to-Logic Pro handoffs. Keep it outside Creator Studio subscription claims.

### Follow-Up Creator Studio Skills

#### `final-cut-pro-workflow`

Own Final Cut library safety, import and media organization, proxy/optimized media decisions, edit structures, captions, roles, titles/effects handoffs, color/export decisions, sharing, and relink/recovery guidance.

Start only after Compressor proves the export and output-verification contract. [Final Cut Pro User Guide for Mac](https://support.apple.com/guide/final-cut-pro/welcome-ver92663661d/mac)

#### `motion-workflow`

Own Motion project setup, behaviors/keyframes, generators, titles, effects, template publication for Final Cut Pro, parameter exposure, render/export, and source-project preservation.

Start after the Final Cut and Compressor handoff contracts are proven. [Motion User Guide](https://support.apple.com/guide/motion/welcome/mac)

#### `pixelmator-pro-workflow`

Own document/layer preservation, nondestructive editing decisions, color/profile-aware output, export variants, asset naming, and handoffs to Final Cut Pro, Motion, and other creative-app surfaces.

Start after confirming Mac/iPad feature boundaries and durable source-versus-delivery conventions.

## Future Mac Image Workflows Plugin Candidate

Acorn and RetroBatch should remain separate from Creator Studio for now. The likely future home is `mac-image-workflows`, but it should only be created when common work justifies it.

Potential skills:

- `acorn-workflow`: layers, selections, non-destructive source policy, batch-safe exports, and reproducible image edits.
- `retrobatch-workflow`: input sets, filters, naming templates, metadata policy, batch previews, destination safety, queue completion, and sampled output verification.
- `mac-image-asset-handoff`: a narrow shared workflow for source assets, variants, color profiles, format decisions, naming, metadata, and transfer into video/app-icon/web surfaces.

Do not include Pixelmator Pro in that plugin. It belongs with Creator Studio because its project, install, and support surface is part of the Apple collection. Do not include Core Image, Image I/O, or app image-code tasks there; those belong in `apple-dev-skills`.

Decision checkpoint: create `mac-image-workflows` only when at least two independent app workflows have reusable references, fixture needs, validation contracts, and user-facing value. Otherwise retain the plan without an empty install surface.

## First Implementation Sequence

### Slice 0: Shared Preparation

- Confirm the exact plugin path and local validation convention by following the closest existing child-plugin shape.
- Record the application versions available on the validation Mac; do not place machine-local paths in the repository.
- Collect official Apple Help anchors and current release notes for Compressor and Logic Pro.
- Define disposable fixture inputs: a short licensed or self-created video/audio source, a simple Logic project, expected export contracts, and an untracked local output directory.
- Define how a run records source preservation, output location, complete-job status, and artifact verification.

### Slice 1: `compressor-workflow`

- Initialize the new skill using the standard skill scaffold only after the child-plugin directory is deliberately created.
- Write a compact `SKILL.md` covering request classification, preflight, source-preserving job setup, preset/destination selection, submission, monitoring, verification, recovery, and handoffs.
- Add only the references that make the workflow repeatable: job/preset/destination decision table, failure/recovery states, and artifact-verification checklist.
- Keep a clear fallback boundary: use a separate command-line encoding workflow when an actual reproducible CLI contract is required; do not misrepresent the installed Compressor app as a supported CLI tool.
- Validate with at least one controlled transcode and one destination/preset inspection pass. Capture app version and actual output evidence.

### Slice 2: `logic-pro-workflow`

- Write a compact `SKILL.md` for project preflight, audio/MIDI device state, project settings, recording/arrangement, routing/mix decisions, bounce/stem output, verification, and MainStage handoff.
- Add references for session ownership, recording safety, routing/bus checklist, delivery decision table, and recovery states for missing media/device/plug-in warnings.
- Require explicit confirmation before recording, replacing takes, changing audio devices, freezing/flattening, destructive editing, or bouncing over an existing file.
- Validate with a disposable Logic project: inspect configuration, make a non-destructive edit, create a defined output, and verify it opens/plays as expected.

### Slice 3: `mainstage-workflow`

- Write a compact `SKILL.md` for concert/set/patch structure, audio/MIDI device preflight, channel strips, mappings, rehearsal, backup, and live-performance confirmation gates.
- Add references for device/routing state, concert backup, patch-change safety, rehearsal checklist, and recovery from missing device or plug-in conditions.
- Require explicit confirmation before changing selected patches, audio/MIDI routing, mappings, concert files, playback, or recording on a live-performance surface.
- Validate with a disposable rehearsal concert and real available audio/MIDI evidence; do not alter an active performance configuration during validation.

### Slice 4: Plugin Packaging And Release Readiness

- Add child `AGENTS.md`, `.codex-plugin/plugin.json`, authored `skills/`, and only required test/validation files.
- Add the root marketplace entry only after Compressor, Logic Pro, and MainStage are real, validated skill folders.
- Update root README, roadmap, active-skill inventory, plugin metadata, and tests in the same pass.
- Run child validation, root metadata validation, and focused fixture checks serially.

### Slice 5: Follow-Up Apps

- Add Final Cut Pro and Motion together when their cross-app project/template/export flow has a tested fixture.
- Add Pixelmator Pro only after Mac/iPad scope and source-layer preservation are proven.
- Keep GarageBand handoff behavior under the same fixture gate as the rest of the plugin and do not claim full project parity with Logic Pro without an observed handoff.

## Validation Strategy

- Validate every new skill folder with the standard skill validator.
- Add focused repository tests that inspect required frontmatter, reference links, metadata/skill inventory agreement, and safety-language requirements without attempting to automate professional creative apps in CI.
- Run deterministic repository checks serially: child checks first, then root metadata validation.
- Forward-test each skill through a disposable fixture task with a fresh agent context after its initial draft. Do not pass the intended solution or hidden fixture result to the tester.
- Treat visual/manual app verification as an explicit evidence type. Record the app version, the operation, the output artifact, and any limitation rather than asserting that a UI flow is stable across all releases.

## Open Questions

- What initial visual identity should the plugin use: consistent with Apple Dev Skills, or a distinct creative-suite mark?
- Should the first release offer Mac-only guidance, or provide iPad-specific Final Cut Pro and Logic Pro paths immediately where Apple’s help distinguishes them?
- Which real first fixtures best fit Gale’s creative work: screen-recording delivery, a short educational video package, a nightcore/remix Logic session, or a simple MainStage rehearsal project?
- Should the first Compressor release include a project-local helper for artifact inspection, or keep output verification manual/standard-tool based until a deterministic need recurs?
- Does Pixelmator Pro belong in the first Creator Studio release after the two initial skills, or should it wait until the Acorn/RetroBatch decision establishes a stronger image-workflow boundary?

## Non-Goals

- Do not bundle Apple apps, paid content, plug-ins, codecs, media, third-party presets, or license-restricted documentation.
- Do not create a generic “Creative Studio automation” skill that obscures app-specific safety and artifact contracts.
- Do not treat a Computer Use action as verification; require observed state or an inspected output artifact.
- Do not promise that all app operations are scriptable, stable across versions, or safe without human review.
- Do not modify a user’s source project/library/session in a training or validation pass.
