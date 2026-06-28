---
name: avfaudio-session-workflow
description: Guide AVFAudio audio-session implementation and repair for Apple apps, including AVAudioSession categories, modes, options, activation, deactivation, record permission, interruptions, route changes, Bluetooth, AirPlay, capture-session interaction, and user-friendly audio diagnostics. Use when the user needs to design, modernize, or fix app audio behavior rather than build or test an Xcode project.
---

# AVFAudio Session Workflow

## Purpose

Guide Apple app audio-session design and repair. This skill owns the app-level audio intent boundary: what the app tells the system it wants to do with audio, when it activates that intent, how it responds to interruption and route changes, how it preserves typed AVFAudio policy surfaces, and how it explains failures.

It is not the audio-engine graph workflow, not the AVFoundation media-pipeline workflow, not the Core Media timing workflow, and not the Xcode execution workflow.

## When To Use

- Use this skill when configuring or repairing `AVAudioSession`, `AVAudioApplication`, `AVAudioApplication.requestRecordPermission`, recording permission, categories, modes, options, `AVAudioSession.RouteSharingPolicy`, activation, deactivation, interruptions, route changes, Bluetooth, AirPlay, speaker routing, or capture-session audio-session behavior.
- Use this skill when existing audio code plays from the wrong route, fails silently, captures silence, interrupts other audio incorrectly, fails around calls, ignores headphones disconnects, or logs vague audio errors.
- Recommend `avaudio-engine-workflow` when the primary issue is an `AVAudioEngine` graph, node connection, tap, render callback, manual rendering, or format conversion.
- Recommend `avfoundation-media-pipeline-workflow` when the primary issue is capture, playback, media assets, readers, writers, export, or sample-buffer append policy.
- Recommend `coremedia-timing-samplebuffer-workflow` when the primary issue is timestamps, timebases, `CMSampleBuffer`, or media synchronization.
- Recommend `xcode-build-run-workflow` or `xcode-testing-workflow` when the next step is build, run, entitlement, `Info.plist`, simulator, device, or test execution.

## Single-Path Workflow

1. Classify the audio-session request:
   - playback-only behavior
   - recording or play-and-record behavior
   - capture-session audio interaction
   - route, Bluetooth, AirPlay, or speaker behavior
   - interruption or route-change handling
   - permission or privacy gate
   - repair of an existing implementation
2. Apply the Apple docs gate:
   - read current AVFAudio or AVFoundation documentation first
   - use archive material only for legacy migration context
   - state the documented behavior relied on before recommending design or repair
   - apply `../../shared/references/apple-media-type-ownership.md` before introducing string-backed audio policy, route, category, mode, or permission models
   - stop if current docs and code disagree in a way that changes the recommendation
3. Choose the app-audio policy:
   - category, mode, route-sharing policy, and options
   - activation and deactivation point
   - permission request and denial behavior
   - interruption and route-change observers
   - capture-session automatic audio-session configuration stance
4. Repair common failure modes:
   - missing microphone usage description or permission path
   - category, mode, route, permission, or output policy modeled as free-form strings instead of `AVAudioSession` and `AVAudioApplication` types
   - using `overrideOutputAudioPort` when `defaultToSpeaker` is the durable intent
   - leaving other apps interrupted after deactivation instead of using `notifyOthersOnDeactivation` when appropriate
   - treating denied permission as a hardware failure
   - ignoring headphones disconnect privacy expectations
   - allowing `AVCaptureSession` to mutate shared audio-session state unexpectedly
5. Return one recommendation with:
   - request class
   - documented Apple behavior relied on
   - chosen category, mode, options, and activation lifecycle
   - permission, route, and interruption plan
   - repair findings
   - one execution or testing handoff when runtime validation is required

## Inputs

- `request`: optional free-text audio-session task.
- `platform_context`: optional platform emphasis such as `ios`, `ipados`, `macos`, `watchos`, `tvos`, `visionos`, or `mixed-apple`.
- `audio_goal`: optional goal such as `playback`, `recording`, `play-and-record`, `capture`, `spoken-audio`, `bluetooth`, `airplay`, or `repair`.
- Defaults:
  - docs-first guidance always applies
  - prefer Apple and Swift media types unless `../../shared/references/apple-media-type-ownership.md` identifies a concrete escape hatch
  - prefer current AVFAudio behavior over archive-era Audio Session Programming Guide text
  - prefer framework-owned behavior over custom route managers or broad audio coordinators

## Outputs

- `status`
  - `success`: an audio-session recommendation or repair path is ready
  - `handoff`: another Apple Dev skill owns the next step
  - `blocked`: the request lacks enough platform, goal, or code context
- `path_type`
  - `primary`: current AVFAudio or AVFoundation docs cover the recommendation
  - `fallback`: archive or legacy behavior is used only to explain old code
- `output`
  - resolved audio-session class
  - documented Apple behavior relied on
  - category, mode, option, activation, and deactivation guidance
  - permission, route, and interruption plan
  - repair findings
  - validation and handoff expectation

## Guards and Stop Conditions

- Do not treat audio-session state as a global dumping ground for unrelated playback, recording, engine, and capture responsibilities.
- Do not replace `AVAudioSession` category, mode, options, route-sharing, route, port, or permission surfaces with stringly typed policy models unless the conversion boundary is explicit and framework state remains inspectable.
- Do not claim runtime route, Bluetooth, AirPlay, microphone, speaker, or interruption behavior is verified without device, simulator, or manual validation evidence.
- Do not use archive-era guidance to override current AVFAudio documentation.
- Do not recommend broad custom route managers unless a documented framework behavior cannot express the app's real intent.
- Stop with `blocked` when the requested route or permission behavior requires a live device, external accessory, or system setting that is not available.

## Fallbacks and Handoffs

- Recommend `explore-apple-swift-docs` when more current docs lookup is the real need.
- Recommend `avaudio-engine-workflow` for engine graph, tap, render, manual-rendering, or format work.
- Recommend `avfoundation-media-pipeline-workflow` for capture, playback, reader, writer, export, or asset-loading work.
- Recommend `coremedia-timing-samplebuffer-workflow` for sample-buffer timing and synchronization.
- Recommend `xcode-build-run-workflow` for entitlements, `Info.plist`, target membership, build, run, or device setup.
- Recommend `xcode-testing-workflow` for repeatable test plans, interruption test design, or runtime verification.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` exists to preserve the repo-wide customization-file contract, but this workflow defines no runtime-enforced knobs.

## References

### Workflow References

- `references/session-policy-and-repair.md`
- `references/validation-and-handoffs.md`
- `references/customization-flow.md`

### Support References

- Use `../../shared/references/apple-media-type-ownership.md` for the shared Apple media type and framework-selection contract.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Xcode-project baseline policy for audio-session apps.

### Script Inventory

- `scripts/customization_config.py`
