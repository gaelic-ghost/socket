---
name: video-codec-processing-workflow
description: Guide VideoToolbox compression and decompression, codec-session creation and properties, encoder/decoder selection, hardware capability, real-time and multipass policy, Core Video pixel buffers and pools, Metal and IOSurface interop, Core Media compressed samples and format descriptions, color/HDR attachments, OSStatus diagnostics, and performance repair. Use when low-level per-frame codec control is primary.
---

# Video Codec Processing Workflow

## Purpose

Guide low-level Apple video encode, decode, and pixel-buffer work while keeping ordinary reader/writer/export pipelines with AVFoundation and exact compressed sample timing with Core Media.

## When To Use

- Use for `VTCompressionSession`, `VTDecompressionSession`, codec properties, hardware selection, compressed callbacks, pixel-buffer pools, color/HDR attachments, multipass, latency, or codec `OSStatus` repair.
- Recommend `avfoundation-media-pipeline-workflow` when `AVAssetReader`, `AVAssetWriter`, export, or general transcode behavior expresses the requirement.
- Recommend `coremedia-timing-samplebuffer-workflow` when timestamps, format descriptions, sample dependencies, or synchronization are the primary bug.

## Single-Path Workflow

1. Classify the request:
   - compression or decompression
   - real-time or offline encode
   - hardware encoder/decoder selection
   - bitrate, keyframes, reordering, latency, profile, or entropy policy
   - multipass encoding
   - pixel-buffer allocation, pool, planes, or Metal/IOSurface interop
   - compressed sample, parameter-set, color/HDR, or attachment repair
   - lifecycle, callback, `OSStatus`, or performance diagnosis
2. Apply the Apple docs gate:
   - read current VideoToolbox, Core Video, and Core Media documentation for the codec and platform
   - state the documented behavior relied on
   - apply `../../shared/references/apple-media-type-ownership.md`
   - prefer AVFoundation unless the requirement needs low-level codec selection, latency, per-frame control, hardware policy, or callback access
3. Establish the media contract:
   - codec, dimensions, profile/level, frame rate, timescale, pixel format, color primaries, transfer function, YCbCr matrix, dynamic range, alpha, bitrate, latency, and destination
   - input/output `CMVideoFormatDescription`, parameter sets, `CMSampleBuffer`, `CVPixelBuffer`, attachments, and timing ownership
4. Configure and prepare one session owner:
   - inspect encoder/decoder availability and supported property dictionaries
   - create the session with explicit specifications and image-buffer attributes
   - set only supported properties and check every `OSStatus`
   - prepare the compression session when appropriate
5. Submit and drain:
   - preserve frame identity, presentation timestamp, duration, and source lifetime
   - handle asynchronous callback status, info flags, delayed frames, dropped frames, dependencies, and output format changes
   - complete/finish delayed frames, end passes, wait for asynchronous work where required, then invalidate exactly once
6. Return the documented behavior, AVFoundation-versus-VideoToolbox decision, capability evidence, session and buffer contract, color/timing policy, diagnostics, profiling evidence, and handoffs.

## Inputs

- `request`: codec, buffer, or compressed-sample task.
- `codec_goal`: `encode`, `decode`, `hardware`, `realtime`, `multipass`, `pixel-buffer`, `color`, `hdr`, `interop`, or `repair`.
- `media_context`: codec, dimensions, pixel formats, frame rate/timing, latency, color/HDR, and destination requirements.
- `platform_context`: Apple platform, deployment target, intended devices, and GPU/media consumers.

## Outputs

- `status`: `success`, `handoff`, or `blocked`.
- `path_type`: `primary` for low-level codec work, `fallback` for AVFoundation, Core Media timing, Core Image, Metal, or execution.
- `output`: documented behavior, framework decision, capability/session/buffer contract, lifecycle, diagnostics, performance evidence, and handoffs.

## Guards and Stop Conditions

- Do not use VideoToolbox merely because the pipeline handles video; prefer AVFoundation when it expresses the real reader/writer/export requirement.
- Do not set codec properties without checking supported-property and codec/session availability.
- Do not claim hardware acceleration from a requested specification; inspect the actual session property and measure runtime behavior.
- Do not call a Core Video/Metal/IOSurface path zero-copy without proving compatible storage, formats, synchronization, and absence of hidden conversion or readback.
- Do not lose `CMTime`, `CMVideoFormatDescription`, parameter sets, sample attachments, dependency flags, color/HDR attachments, alpha, or pixel-buffer pool provenance.
- Do not read/write pixel-buffer base addresses outside balanced lock/unlock calls or assume contiguous memory for planar formats.
- Do not collapse an `OSStatus` into a vague codec failure; report operation, codec, property/frame, status value, likely cause, and next probe.
- Stop when codec support, format descriptions, pixel format/color contract, source lifetime, or representative-device evidence is unavailable.

## Fallbacks and Handoffs

- Recommend `avfoundation-media-pipeline-workflow` for readers, writers, export, asset loading, playback, and general transcode pipelines.
- Recommend `coremedia-timing-samplebuffer-workflow` for sample timing, format descriptions, attachments, dependency flags, synchronization, and display layers.
- Recommend `core-image-processing-workflow` for image processing/rendering and Metal only for advanced custom GPU compute or rendering.
- Recommend `camera-capture-depth-workflow` for camera devices, capture formats, photo/video controls, and depth.
- Recommend `xcode-build-run-workflow` for build, run, hardware/device logs, VideoToolbox availability probes, or Instruments.
- Recommend `xcode-testing-workflow` for encoded fixtures, round trips, corruption tests, color/HDR checks, and performance baselines.
- Recommend `explore-apple-swift-docs` for current codec or media-buffer research.

## Customization

Use `references/customization-flow.md`. This workflow defines no runtime-enforced knobs.

## References

- `references/compression-decompression-and-session-lifecycle.md`
- `references/pixel-buffers-metal-color-and-hdr.md`
- `references/compressed-samples-diagnostics-and-performance.md`
- `references/customization-flow.md`
- `../../shared/references/apple-media-type-ownership.md`
- Recommend `references/snippets/apple-xcode-project-core.md` for reusable Xcode-project policy.

## Script Inventory

- `scripts/customization_config.py`
