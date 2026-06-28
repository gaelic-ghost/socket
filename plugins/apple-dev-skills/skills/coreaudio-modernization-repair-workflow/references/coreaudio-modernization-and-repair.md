# Core Audio Modernization And Repair

Use current Core Audio, Audio Toolbox, Core Audio Types, and AVFAudio documentation first. Use archive docs only to understand legacy code.

Framework choice:

- Use AVAudioSession and AVAudioApplication for app audio intent, permissions, activation, routes, and interruptions.
- Use AVAudioEngine, AVAudioNode, AVAudioFormat, AVAudioFile, AVAudioPCMBuffer, AVAudioConverter, and AVAudioUnit for modern graph, file, buffer, converter, processing, and unit-hosting work when those APIs expose the needed behavior.
- Use AVFoundation for capture, playback, asset loading, readers, writers, export, transcode, and sample-buffer append ownership.
- Use Core Media when timing, sample buffers, format descriptions, attachments, clocks, timebases, or synchronization are the real problem.
- Keep Core Audio or Audio Toolbox when the code needs low-level `AudioUnit`, `AudioQueue`, `AudioConverterRef`, `AudioStreamBasicDescription`, `AudioBufferList`, `AudioTimeStamp`, real-time callback, workgroup, codec, file, or device behavior that the higher-level frameworks do not expose.

Retention criteria:

- Keep low-level Core Audio when the code needs behavior not exposed by AVFAudio.
- Keep low-level code when it is a narrow, stable, tested wrapper around a required device, unit, converter, or format behavior.
- Migrate when the code duplicates AVAudioEngine, AVAudioUnit, AVAudioFile, AVAudioConverter, or AVAudioSession behavior without adding needed control.

Type ownership:

- Keep `AudioStreamBasicDescription`, `AudioStreamPacketDescription`, `AudioComponentDescription`, `AudioBufferList`, `AudioTimeStamp`, `AudioUnit`, `AudioQueueRef`, `AudioConverterRef`, and `OSStatus` visible at the low-level boundary.
- Wrap retained low-level APIs behind one narrow Swift entry point, but do not erase the operation, format, component, callback ownership, or `OSStatus` cause from diagnostics.
- Convert `OSStatus` to Swift errors only after attaching the operation name, relevant format or component, and a likely inspection point.
- Use custom Swift structs only for validated summaries, fixture data, or app-domain intent; do not use them as a replacement for Core Audio structures that still configure C APIs.

Repair checklist:

- Decode or name `OSStatus` values with the operation that produced them.
- Keep `AudioStreamBasicDescription` construction centralized and inspectable.
- Make pointer and callback ownership explicit.
- Preallocate callback state and keep render callbacks real-time safe.
- Wrap retained low-level code behind one narrow entry point.
- Remove duplicate legacy and modern codepaths after cleanup unless the user explicitly approves a transition period.

Bad shapes:

- A callback captures a Swift object whose lifetime is shorter than the audio unit or queue.
- Bare `OSStatus` integers are logged without operation, format, component, or likely cause.
- Audio Queue and AVAudioEngine code both attempt to own the same playback lifecycle.
