---
name: coreaudio-modernization-repair-workflow
description: Guide legacy Core Audio and Audio Toolbox modernization and repair, including AudioUnit, AudioQueue, AudioConverter, AudioStreamBasicDescription, AudioComponentDescription, OSStatus diagnostics, callback lifetime, pointer ownership, Swift bridging, and migration decisions toward AVFAudio when appropriate. Use when fixing low-level Apple audio implementations or deciding whether to keep or replace legacy Core Audio code.
---

# Core Audio Modernization Repair Workflow

## Purpose

Guide low-level Core Audio and Audio Toolbox repair. This skill owns the legacy and escape-hatch boundary: when to keep C APIs, when to isolate them, when to migrate toward AVFAudio, and how to make old callback, pointer, buffer, format, and `OSStatus` code understandable and safer without erasing the Apple type boundary.

It is not the default audio recommendation when AVFAudio covers the job.

## When To Use

- Use this skill when code uses `AudioUnit`, `AudioQueue`, `AudioConverter`, `AudioComponentDescription`, `AudioStreamBasicDescription`, `AudioBufferList`, render callbacks, `OSStatus`, unsafe pointers, or archive-era Core Audio patterns.
- Use this skill when existing code has opaque `OSStatus` failures, pointer lifetime bugs, callback crashes, hand-rolled format structs, unsafe Swift bridging, or low-level audio code that might be replaceable with AVAudioEngine or AVAudioSession.
- Recommend `avaudio-engine-workflow` when the same job can be modeled as an AVAudioEngine graph or `AVAudioUnit` host.
- Recommend `avfaudio-session-workflow` when the real issue is audio-session policy, route, permission, or interruption behavior.

## Single-Path Workflow

1. Classify the low-level audio request:
   - Audio Unit hosting or rendering
   - Audio Queue playback or recording
   - Audio Converter or format conversion
   - stream description or buffer layout
   - `OSStatus` diagnosis
   - callback, pointer, or lifetime repair
   - migration to AVFAudio
2. Apply the Apple docs gate:
   - read current Core Audio, Audio Toolbox, AVFAudio, or Core Audio Types docs first
   - use archive docs only to understand legacy code, not to override current guidance
   - state the documented behavior or legacy context relied on
   - apply `../../shared/references/apple-media-type-ownership.md` before hiding Core Audio structures, pointers, callbacks, or `OSStatus` values behind generic Swift wrappers
3. Decide retention versus migration:
   - keep low-level code only when it exposes needed behavior that AVFAudio does not cover
   - wrap retained low-level code behind a narrow boundary with explicit ownership
   - migrate to AVAudioEngine, AVAudioUnit, AVAudioFile, AVAudioConverter, or AVAudioSession when current APIs cover the job
4. Repair common failure modes:
   - `OSStatus` logged as an integer with no operation or likely cause
   - callbacks retaining invalid object pointers
   - allocation, locking, logging, or actor hops in render callbacks
   - mismatched `AudioStreamBasicDescription`
   - unsafe `AudioBufferList` memory ownership
   - `AudioComponentDescription`, `AudioStreamBasicDescription`, `AudioBufferList`, `AudioTimeStamp`, or `OSStatus` replaced with generic structs or errors before the low-level operation remains diagnosable
   - duplicate low-level and AVFAudio codepaths left behind after modernization
5. Return one recommendation with:
   - low-level request class
   - documented behavior or archive context relied on
   - retention or migration decision
   - boundary and ownership plan
   - repair findings
   - validation and handoff expectation

## Inputs

- `request`: optional free-text low-level audio task.
- `legacy_surface`: optional surface such as `audio-unit`, `audio-queue`, `audio-converter`, `stream-description`, `buffer-list`, `osstatus`, `callback`, or `repair`.
- `migration_goal`: optional goal such as `keep-low-level`, `wrap`, `migrate-to-avaudioengine`, `migrate-to-avaudiosession`, or `undecided`.
- Defaults:
  - docs-first guidance always applies
  - prefer Apple and Swift media types unless `../../shared/references/apple-media-type-ownership.md` identifies a concrete escape hatch
  - current docs outrank archive docs for modern recommendations
  - prefer AVFAudio when it honestly covers the behavior

## Outputs

- `status`
  - `success`: a modernization or repair path is ready
  - `handoff`: another Apple Dev skill owns the next step
  - `blocked`: the low-level behavior or failure evidence is too unclear
- `path_type`
  - `primary`: current Core Audio, Audio Toolbox, or AVFAudio docs cover the recommendation
  - `fallback`: archive docs explain legacy behavior only
- `output`
  - resolved low-level surface
  - documented behavior or archive context relied on
  - retention or migration decision
  - callback, pointer, format, and `OSStatus` repair findings
  - validation and handoff expectation

## Guards and Stop Conditions

- Do not preserve duplicate legacy and modern codepaths after cleanup unless the user explicitly approves that compromise.
- Do not recommend low-level C APIs by default when AVFAudio exposes the behavior directly.
- Do not hide `AudioUnit`, `AudioQueueRef`, `AudioConverterRef`, `AudioComponentDescription`, `AudioStreamBasicDescription`, `AudioBufferList`, `AudioTimeStamp`, or `OSStatus` behind generic Swift wrappers until ownership, format, operation, and likely failure cause remain inspectable.
- Do not claim render-callback, underrun, device, or format repair is verified without runtime evidence.
- Do not log bare `OSStatus` values without operation context and at least one likely cause or inspection point.
- Stop with `blocked` when the existing low-level code cannot be inspected enough to know whether migration is safe.

## Fallbacks and Handoffs

- Recommend `avaudio-engine-workflow` for AVAudioEngine graph repair, `AVAudioUnit` hosting, and modern processing chains.
- Recommend `avfaudio-session-workflow` for app audio-session policy, route, interruption, or permission behavior.
- Recommend `coremedia-timing-samplebuffer-workflow` when the failure is sample timing or media synchronization.
- Recommend `xcode-build-run-workflow` for build, run, device, Instruments, Audio MIDI Setup, or runtime diagnostics.
- Recommend `xcode-testing-workflow` for repeatable regression tests around audio conversion, fixtures, or wrapper behavior.
- Recommend `explore-apple-swift-docs` when more current or archive docs lookup is the next honest step.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` exists to preserve the repo-wide customization-file contract, but this workflow defines no runtime-enforced knobs.

## References

### Workflow References

- `references/coreaudio-modernization-and-repair.md`
- `references/legacy-archive-boundary.md`
- `references/customization-flow.md`

### Support References

- Use `../../shared/references/apple-media-type-ownership.md` for the shared Apple media type and framework-selection contract.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Xcode-project baseline policy for low-level audio apps.

### Script Inventory

- `scripts/customization_config.py`
