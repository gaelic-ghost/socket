---
name: avfoundation-media-pipeline-workflow
description: Guide AVFoundation media-pipeline implementation and repair, including AVCaptureSession, capture queues, AVPlayer, AVAsset async loading, AVAssetReader, AVAssetWriter, export, transcode, sample-buffer append back-pressure, and capture or playback ownership boundaries. Use when fixing or modernizing Apple media capture, playback, loading, reader, writer, or export code.
---

# AVFoundation Media Pipeline Workflow

## Purpose

Guide AVFoundation capture, playback, asset loading, reader, writer, export, and sample-buffer pipeline design and repair. This skill owns media-pipeline shape, typed AVFoundation surface choice, and back-pressure policy, while leaving app audio-session policy, engine graphs, Core Media timing internals, and Xcode execution to their owning skills.

## When To Use

- Use this skill for `AVCaptureSession`, capture inputs and outputs, capture queues, `AVPlayer`, `AVPlayerItem`, `AVAsset`, `AVURLAsset`, `AVAsyncProperty`, async asset loading, `AVAssetReader`, `AVAssetWriter`, export, transcode, and sample-buffer append loops.
- Use this skill when existing code blocks the main thread, uses deprecated AVAsset synchronous properties, misuses `loadValuesAsynchronously(forKeys:)`, appends sample buffers without back-pressure, confuses capture authorization with microphone permission, or mixes capture, UI, writer, and player ownership in one object.
- Recommend `avfaudio-session-workflow` when the primary problem is app audio intent, routes, interruptions, or microphone permission.
- Recommend `coremedia-timing-samplebuffer-workflow` when the primary issue is sample-buffer timestamps, format descriptions, timebases, clocks, or synchronization.
- Recommend `camera-capture-depth-workflow` when the primary issue is camera discovery, device controls, formats, rotation, photo capture, depth, calibration, synchronized camera outputs, or computational capture.

## Single-Path Workflow

1. Classify the media pipeline:
   - capture setup
   - player or playback state
   - asset inspection or async loading
   - reader or writer loop
   - export or transcode
   - sample-buffer append or back-pressure
   - repair of an existing implementation
2. Apply the Apple docs gate:
   - read current AVFoundation documentation for the pipeline surface
   - state the documented behavior relied on before recommending changes
   - apply `../../shared/references/apple-media-type-ownership.md` before introducing custom media wrappers, raw numeric timing, strings, or dictionaries
3. Choose the pipeline owner and queues:
   - capture-session configuration owner
   - serial capture session queue
   - player item and UI update boundary
   - async asset loading boundary
   - reader and writer queue
   - cancellation and teardown path
4. Repair common failure modes:
   - `AVCaptureSession.startRunning()` on the main queue
   - deprecated synchronous AVAsset property reads in Swift clients
   - callback-based asset loading left in otherwise async Swift code
   - writer loops that ignore `isReadyForMoreMediaData`
   - raw strings, dictionaries, or custom structs replacing `AVAsset`, `AVAssetTrack`, `AVPlayerItem`, `AVCaptureConnection`, `AVAssetReaderOutput`, `AVAssetWriterInput`, `CMSampleBuffer`, or writer receiver types without a documented boundary reason
   - capture authorization, recording permission, and `Info.plist` gates collapsed together
   - sample-buffer timing issues that need Core Media handoff
5. Return one recommendation with:
   - pipeline class
   - documented Apple behavior relied on
   - owner, queue, and async-loading plan
   - back-pressure and cancellation plan
   - repair findings
   - validation and handoff expectation

## Inputs

- `request`: optional free-text media task.
- `pipeline_goal`: optional goal such as `capture`, `playback`, `asset-loading`, `reader`, `writer`, `export`, `transcode`, `sample-buffer-append`, or `repair`.
- `platform_context`: optional platform emphasis such as `ios`, `macos`, or `mixed-apple`.
- Defaults:
  - docs-first guidance always applies
  - prefer Apple and Swift media types unless `../../shared/references/apple-media-type-ownership.md` identifies a concrete escape hatch
  - prefer Swift concurrency asset loading for modern Swift clients
  - keep blocking session and media work off the main queue

## Outputs

- `status`
  - `success`: a media pipeline recommendation or repair path is ready
  - `handoff`: another Apple Dev skill owns the next step
  - `blocked`: pipeline ownership or runtime evidence is too unclear
- `path_type`
  - `primary`: current AVFoundation docs cover the recommendation
  - `fallback`: a lower-level timing or audio repair workflow is needed
- `output`
  - resolved pipeline class
  - documented Apple behavior relied on
  - owner, queue, loading, and back-pressure plan
  - repair findings
  - validation and handoff expectation

## Guards and Stop Conditions

- Do not run capture sessions, media loading, export, or writer loops on the main queue when docs identify the operation as blocking or asynchronous.
- Do not replace AVFoundation or Core Media pipeline types with custom wrappers, strings, dictionaries, or raw numeric timing unless the conversion boundary and lost media information are explicit.
- Do not claim capture, playback, export, camera, microphone, or route behavior is verified without runtime evidence.
- Do not silently absorb Core Media timestamp, sample-buffer readiness, or timebase repair.
- Do not collapse UI state, capture configuration, writer loops, and player ownership into one object unless the code is deliberately tiny and no persistent boundary is needed.
- Stop with `blocked` when the requested behavior depends on unavailable camera, microphone, file, route, or device evidence.

## Fallbacks and Handoffs

- Recommend `avfaudio-session-workflow` for app audio intent, microphone permission, interruptions, routes, or capture-session audio-session interaction.
- Recommend `camera-capture-depth-workflow` for camera devices, controls, photo features, depth, calibration, synchronized outputs, and capability diagnostics.
- Recommend `coremedia-timing-samplebuffer-workflow` for `CMTime`, format descriptions, sample-buffer attachments, dropped buffers, or synchronization.
- Recommend `video-codec-processing-workflow` for low-level VideoToolbox compression/decompression, codec properties, hardware policy, pixel-buffer pools, and per-frame callbacks.
- Recommend `photos-library-editing-workflow` for PhotosUI selection, PhotoKit asset/resource requests, library saves, and content editing.
- Recommend `avaudio-engine-workflow` for engine graph, tap, or audio processing work.
- Recommend `xcode-build-run-workflow` for build, run, target, entitlement, `Info.plist`, or device follow-through.
- Recommend `xcode-testing-workflow` for repeatable media tests, fixtures, or runtime verification planning.
- Recommend `explore-apple-swift-docs` when docs lookup is the real need.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` exists to preserve the repo-wide customization-file contract, but this workflow defines no runtime-enforced knobs.

## References

### Workflow References

- `references/media-pipeline-and-repair.md`
- `references/async-loading-and-backpressure.md`
- `references/customization-flow.md`

### Support References

- Use `../../shared/references/apple-media-type-ownership.md` for the shared Apple media type and framework-selection contract.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Xcode-project baseline policy for media apps.

### Script Inventory

- `scripts/customization_config.py`
