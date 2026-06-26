# Core Audio Modernization And Repair

Use current Core Audio, Audio Toolbox, Core Audio Types, and AVFAudio documentation first. Use archive docs only to understand legacy code.

Retention criteria:

- Keep low-level Core Audio when the code needs behavior not exposed by AVFAudio.
- Keep low-level code when it is a narrow, stable, tested wrapper around a required device, unit, converter, or format behavior.
- Migrate when the code duplicates AVAudioEngine, AVAudioUnit, AVAudioFile, AVAudioConverter, or AVAudioSession behavior without adding needed control.

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
