---
name: avaudio-engine-workflow
description: Guide AVAudioEngine implementation and repair for Apple apps and packages, including node graph ownership, AVAudioNode attachment, input and output nodes, player scheduling, taps, AVAudioFormat, format conversion, manual rendering, offline processing, AVAudioUnit hosting, and real-time audio callback safety. Use when fixing broken engine graphs or modernizing custom audio processing.
---

# AVAudio Engine Workflow

## Purpose

Guide `AVAudioEngine` graph design and repair. This skill owns audio-node ownership, graph construction, connection formats, typed AVFAudio buffer and format surfaces, taps, manual rendering, offline processing, Audio Unit hosting through `AVAudioUnit`, and real-time safety boundaries.

It is not the app audio-session workflow, not the AVFoundation capture or asset workflow, and not a low-level Core Audio C API repair workflow except where AVAudioEngine wraps the lower-level behavior.

## When To Use

- Use this skill when code creates, connects, mutates, starts, stops, or repairs an `AVAudioEngine` graph.
- Use this skill for `AVAudioPlayerNode`, `AVAudioInputNode`, `AVAudioOutputNode`, `AVAudioMixerNode`, `AVAudioSourceNode`, `AVAudioSinkNode`, taps, `AVAudioFormat`, manual rendering, offline processing, `AVAudioUnit`, Audio Unit instantiation, and render-block safety.
- Use this skill when existing code crashes from unattached nodes, format mismatches, missing input or output hardware, illegal graph mutation, callback allocation, actor isolation mistakes, or UI work inside real-time audio paths.
- Recommend `avfaudio-session-workflow` when the primary problem is category, route, permission, interruption, or activation policy.
- Recommend `coreaudio-modernization-repair-workflow` when the primary problem is legacy `AudioQueue`, `AudioUnit`, `AudioConverter`, pointer, callback, or `OSStatus` code outside AVAudioEngine.

## Single-Path Workflow

1. Classify the engine request:
   - playback graph
   - input capture or tap
   - processing chain or effects
   - source or sink node
   - manual rendering or offline processing
   - Audio Unit hosting
   - repair of an existing graph
2. Apply the Apple docs gate:
   - read current AVFAudio docs for the relevant engine, node, format, or rendering behavior
   - state the documented graph, format, or real-time behavior relied on
   - apply `../../shared/references/apple-media-type-ownership.md` before introducing custom graph, buffer, format, or unit-hosting abstractions
3. Map the graph:
   - engine owner and lifetime
   - attached nodes
   - connection order
   - bus formats and conversion points
   - start, schedule, stop, and teardown lifecycle
   - real-time and non-real-time boundaries
4. Repair common failure modes:
   - node used before `attach(_:)`
   - exact format mismatch where no mixer or output conversion applies
   - input or output node used when hardware is unavailable
   - graph mutation that breaks mixer or channel-count assumptions
   - render callback that allocates, locks, logs, awaits, or touches UI
   - hand-rolled format or buffer structs replacing `AVAudioFormat`, `AVAudioPCMBuffer`, `AVAudioFile`, `AVAudioConverter`, or `AudioStreamBasicDescription` while still configuring Apple audio APIs
   - completion handlers that mutate engine state from an arbitrary thread without a clear hop
5. Return one recommendation with:
   - graph class
   - documented Apple behavior relied on
   - graph ownership and connection plan
   - format and rendering plan
   - repair findings
   - validation and handoff expectation

## Inputs

- `request`: optional free-text engine task.
- `graph_goal`: optional goal such as `playback`, `record`, `tap`, `process`, `source-node`, `sink-node`, `manual-rendering`, `offline-processing`, `audio-unit`, or `repair`.
- `platform_context`: optional platform emphasis such as `ios`, `macos`, or `mixed-apple`.
- Defaults:
  - docs-first guidance always applies
  - prefer Apple and Swift media types unless `../../shared/references/apple-media-type-ownership.md` identifies a concrete escape hatch
  - prefer AVAudioEngine and AVAudioUnit surfaces before lower-level callback APIs when they honestly fit
  - keep real-time render paths free of actor hops, locks, allocation, logging, and UI work

## Outputs

- `status`
  - `success`: an engine design or repair path is ready
  - `handoff`: another Apple Dev skill owns the next step
  - `blocked`: graph ownership, format, or runtime evidence is too unclear
- `path_type`
  - `primary`: the recommendation uses current AVFAudio surfaces
  - `fallback`: the recommendation requires lower-level Core Audio analysis
- `output`
  - resolved engine request class
  - documented Apple behavior relied on
  - graph ownership and node connection plan
  - format and callback-safety findings
  - repair steps
  - validation and handoff expectation

## Guards and Stop Conditions

- Do not hide engine ownership behind a broad audio manager unless one owner must coordinate multiple independent graphs or lifetimes.
- Do not replace `AVAudioEngine`, `AVAudioNode`, `AVAudioFormat`, `AVAudioPCMBuffer`, `AVAudioFile`, `AVAudioConverter`, or `AVAudioUnit` with custom wrappers or generic structs unless the Apple type boundary remains inspectable.
- Do not claim audio graph, route, latency, underrun, or callback safety is verified without runtime evidence.
- Do not put Swift concurrency, logging, allocation, blocking I/O, locks, or UI work in real-time render callbacks.
- Do not silently migrate low-level Core Audio code to AVAudioEngine when the existing code depends on behavior AVAudioEngine does not expose.
- Stop with `blocked` when the graph cannot be reconstructed from the code or the failure requires live hardware evidence.

## Fallbacks and Handoffs

- Recommend `avfaudio-session-workflow` for app-level audio intent, permission, route, interruption, or activation policy.
- Recommend `coreaudio-modernization-repair-workflow` for legacy Core Audio, Audio Toolbox, or `OSStatus` work.
- Recommend `coremedia-timing-samplebuffer-workflow` for timestamp or sample-buffer synchronization problems.
- Recommend `xcode-build-run-workflow` for build, run, entitlements, device setup, and runtime diagnostics.
- Recommend `xcode-testing-workflow` for test design, repeatable engine checks, or regression coverage.
- Recommend `explore-apple-swift-docs` when more docs lookup is the next honest step.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` exists to preserve the repo-wide customization-file contract, but this workflow defines no runtime-enforced knobs.

## References

### Workflow References

- `references/engine-graph-and-repair.md`
- `references/realtime-rendering-safety.md`
- `references/customization-flow.md`

### Support References

- Use `../../shared/references/apple-media-type-ownership.md` for the shared Apple media type and framework-selection contract.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Xcode-project baseline policy for apps that host audio engines.

### Script Inventory

- `scripts/customization_config.py`
