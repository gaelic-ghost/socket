# Apple Media Type Ownership

Use Apple and Swift media types as the default representation for Apple media work. Reach for custom wrappers, strings, dictionaries, raw numeric timing, or framework-neutral structs only after naming the concrete reason the framework type is unsuitable for the app, package, test, or persistence boundary.

## Default Type Choices

- Use `AVAudioSession.Category`, `AVAudioSession.Mode`, `AVAudioSession.CategoryOptions`, `AVAudioSession.RouteSharingPolicy`, `AVAudioSessionRouteDescription`, and `AVAudioSessionPortDescription` for app audio intent, route, permission, interruption, and policy decisions.
- Use `AVAudioEngine`, `AVAudioNode`, `AVAudioInputNode`, `AVAudioOutputNode`, `AVAudioMixerNode`, `AVAudioPlayerNode`, `AVAudioSourceNode`, `AVAudioSinkNode`, `AVAudioFormat`, `AVAudioFile`, `AVAudioPCMBuffer`, `AVAudioConverter`, and `AVAudioUnit` for modern audio graph, file, buffer, conversion, and unit-hosting work.
- Use `AVCaptureSession`, `AVCaptureDevice`, `AVCaptureInput`, `AVCaptureOutput`, `AVCaptureConnection`, `AVPlayer`, `AVPlayerItem`, `AVAsset`, `AVAssetTrack`, `AVAsyncProperty`, `AVAssetReader`, `AVAssetReaderOutput`, `AVAssetWriter`, `AVAssetWriterInput`, and writer receiver types for capture, playback, asset loading, reader, writer, export, and transcode ownership.
- Use `CMTime`, `CMTimeRange`, `CMTimeMapping`, `CMClock`, `CMTimebase`, `CMFormatDescription`, `CMSampleBuffer`, `CMSampleTimingInfo`, `CMBlockBuffer`, `CMAttachment`, and Core Media attachments for media timing, sample payload, format, readiness, synchronization, and diagnostic evidence.
- Use `AudioStreamBasicDescription`, `AudioStreamPacketDescription`, `AudioComponentDescription`, `AudioBuffer`, `AudioBufferList`, `AudioTimeStamp`, `AudioUnit`, `AudioQueueRef`, `AudioConverterRef`, and `OSStatus` when the code genuinely needs lower-level Core Audio or Audio Toolbox behavior that AVFAudio does not expose.

## Framework Choice

- Choose AVFAudio session APIs for app-level audio intent: category, mode, options, activation, deactivation, permission, route, interruption, Bluetooth, AirPlay, and capture-session audio-session interaction.
- Choose AVAudioEngine and adjacent AVFAudio types for modern audio graphs, taps, player scheduling, source or sink nodes, file playback, format conversion, manual rendering, offline processing, and Audio Unit hosting through `AVAudioUnit`.
- Choose AVFoundation for media capture, playback, asset inspection, async asset loading, asset reader/writer loops, export, transcode, and sample-buffer append back-pressure.
- Choose Core Media when the bug or design turns on timestamps, time ranges, clocks, timebases, format descriptions, sample buffers, attachments, readiness, dropped buffers, or synchronization.
- Choose Core Audio or Audio Toolbox only for low-level device, unit, queue, converter, stream-description, buffer-list, callback, real-time thread, or `OSStatus` behavior that AVFAudio or AVFoundation cannot express.

## Escape Hatches

Custom types are acceptable when they preserve rather than replace the Apple media type boundary:

- persistence or wire formats that cannot store framework objects directly
- stable test fixtures or snapshot records that serialize inspected framework values
- app-domain models that add meaning outside the media framework, such as user intent, project structure, or editing decisions
- small value types that hold a validated subset of framework data while keeping conversion points explicit
- platform-independent planning docs or APIs that intentionally defer Apple-specific execution to an adapter

When using an escape hatch, document the source Apple type, the destination shape, the conversion point, and any precision, attachment, format-description, timing, route, or lifecycle information that is intentionally lost.

## Review Checks

- Do not convert `CMTime`, timestamps, durations, or time ranges to `Double` or `TimeInterval` until a UI, persistence, or reporting boundary actually needs that representation.
- Do not model media type, route, category, mode, output destination, sample readiness, or writer state as free-form strings when Apple provides typed constants or enums.
- Do not hide `CMSampleBuffer`, `CMFormatDescription`, attachments, or dropped-buffer flags behind opaque payload dictionaries before the timing and format invariants have been inspected.
- Do not replace `AVAudioFormat` or `AudioStreamBasicDescription` with hand-rolled format structs in code that must still configure Apple audio APIs.
- Do not bridge Core Audio pointers, callbacks, `AudioBufferList`, or `OSStatus` behind generic Swift errors until the low-level operation, ownership, format, and likely cause are still visible in diagnostics.
- Do not keep duplicate AVFAudio and Core Audio codepaths after modernization unless Gale explicitly approves a transition period.
