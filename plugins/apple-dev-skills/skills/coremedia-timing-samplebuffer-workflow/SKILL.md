---
name: coremedia-timing-samplebuffer-workflow
description: Guide Core Media timing and sample-buffer implementation and repair, including CMTime, CMTimeRange, CMClock, CMTimebase, CMFormatDescription, CMSampleBuffer, attachments, readiness, presentation and decode timestamps, dropped buffers, AVSampleBufferDisplayLayer, AVSampleBufferRenderSynchronizer, and synchronization diagnostics. Use when media bugs involve timestamps, sample buffers, timing drift, or format descriptions.
---

# Core Media Timing Sample Buffer Workflow

## Purpose

Guide Core Media timing and sample-buffer repair. This skill owns the precise media-time and sample payload boundary: `CMTime`, time ranges, clocks, timebases, format descriptions, sample buffers, attachments, readiness, presentation and decode timestamps, synchronization, and diagnostic probes.

It is not the AVFoundation pipeline owner, not the AVAudioEngine graph owner, and not a generic media-player workflow.

## When To Use

- Use this skill when code manipulates `CMTime`, `CMTimeRange`, `CMClock`, `CMTimebase`, `CMFormatDescription`, `CMSampleBuffer`, attachments, sample readiness, timestamps, dropped buffers, `AVSampleBufferDisplayLayer`, or `AVSampleBufferRenderSynchronizer`.
- Use this skill when existing media code drifts, drops frames or buffers, appends invalid samples, loses format descriptions, confuses decode and presentation time, mishandles host time, or cannot explain synchronization failures.
- Recommend `avfoundation-media-pipeline-workflow` when the primary problem is capture, playback, reader, writer, export, or asset loading.
- Recommend `avaudio-engine-workflow` when the primary problem is engine graph rendering rather than sample-buffer timing.

## Single-Path Workflow

1. Classify the timing request:
   - time math
   - sample-buffer creation or inspection
   - format description
   - attachments or dropped buffers
   - display layer or render synchronizer
   - writer or reader timestamp repair
   - audio/video synchronization
2. Apply the Apple docs gate:
   - read current Core Media or AVFoundation sample-buffer documentation first
   - state the documented timing or sample-buffer behavior relied on
   - apply `../../shared/references/apple-media-type-ownership.md` before converting Core Media values to raw numbers, dictionaries, or app-specific sample wrappers
3. Inspect timing invariants:
   - validity, timescale, epoch, and numeric value
   - presentation timestamp, decode timestamp, and duration
   - time range start and end
   - format description presence and media type
   - readiness and dropped-buffer flags
   - host clock or audio clock relationship
4. Repair common failure modes:
   - invalid `CMTime` treated as zero
   - mismatched timescales or lossy conversion hidden in helpers
   - missing or wrong `CMFormatDescription`
   - `CMSampleBuffer`, `CMFormatDescription`, attachments, readiness, or dropped-buffer metadata hidden behind opaque dictionaries before diagnostics
   - presentation and decode timestamps swapped or flattened
   - sample-buffer append without readiness or writer back-pressure
   - video synchronized to host time when audio-clock sync is required
5. Return one recommendation with:
   - timing class
   - documented Apple behavior relied on
   - invariant checks
   - repair findings
   - diagnostic probes
   - validation and handoff expectation

## Inputs

- `request`: optional free-text timing or sample-buffer task.
- `timing_goal`: optional goal such as `time-math`, `sample-buffer`, `format-description`, `attachments`, `dropped-buffer`, `display-layer`, `render-synchronizer`, `writer`, `reader`, or `repair`.
- `media_context`: optional context such as `audio`, `video`, `metadata`, `captions`, or `mixed-media`.
- Defaults:
  - docs-first guidance always applies
  - prefer Apple and Swift media types unless `../../shared/references/apple-media-type-ownership.md` identifies a concrete escape hatch
  - keep exact timing values inspectable
  - prefer explicit invariants over helper code that hides timestamp behavior

## Outputs

- `status`
  - `success`: a timing or sample-buffer recommendation is ready
  - `handoff`: another Apple Dev skill owns the next step
  - `blocked`: sample data or timing evidence is insufficient
- `path_type`
  - `primary`: current Core Media or AVFoundation docs cover the recommendation
  - `fallback`: runtime instrumentation or pipeline handoff is needed
- `output`
  - resolved timing class
  - documented Apple behavior relied on
  - timing and sample-buffer invariants
  - repair findings
  - diagnostic probes
  - validation and handoff expectation

## Guards and Stop Conditions

- Do not hide `CMTime` validity, timescale, duration, presentation timestamp, or decode timestamp behind vague time helper names.
- Do not replace `CMTime`, `CMTimeRange`, `CMClock`, `CMTimebase`, `CMFormatDescription`, `CMSampleBuffer`, `CMSampleTimingInfo`, attachments, or readiness metadata with raw numbers, strings, or dictionaries until the framework invariants have been inspected and the conversion boundary is documented.
- Do not claim drift, synchronization, dropped-buffer, or writer timing repair is verified without runtime evidence or inspected sample buffers.
- Do not silently absorb capture, export, player, reader, or writer ownership that belongs to the AVFoundation pipeline workflow.
- Do not recommend changing timestamps before identifying whether the source, transform, writer, display, or synchronizer owns the bug.
- Stop with `blocked` when there is no sample, timestamp, format-description, or log evidence to inspect.

## Fallbacks and Handoffs

- Recommend `avfoundation-media-pipeline-workflow` for capture, asset, reader, writer, export, and player ownership.
- Recommend `video-codec-processing-workflow` for VideoToolbox sessions, codec properties, hardware policy, pixel-buffer pools, and encode/decode callbacks while keeping timing and format-description repair here.
- Recommend `avaudio-engine-workflow` for engine rendering and audio-processing graphs.
- Recommend `avfaudio-session-workflow` for route, interruption, permission, or app audio policy.
- Recommend `xcode-build-run-workflow` for runtime probes, device capture, and app execution.
- Recommend `xcode-testing-workflow` for repeatable sample fixtures and timing regression tests.
- Recommend `explore-apple-swift-docs` when more docs lookup is the next honest step.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` exists to preserve the repo-wide customization-file contract, but this workflow defines no runtime-enforced knobs.

## References

### Workflow References

- `references/time-samplebuffer-and-repair.md`
- `references/diagnostics-and-handoffs.md`
- `references/customization-flow.md`

### Support References

- Use `../../shared/references/apple-media-type-ownership.md` for the shared Apple media type and framework-selection contract.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Xcode-project baseline policy for sample-buffer apps.

### Script Inventory

- `scripts/customization_config.py`
