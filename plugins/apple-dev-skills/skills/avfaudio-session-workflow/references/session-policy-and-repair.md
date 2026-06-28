# Session Policy And Repair

Use current AVFAudio documentation before proposing changes. Start from:

- `AVAudioSession`: app audio intent, categories, modes, route-sharing policy, options, activation, and deactivation.
- `AVAudioApplication`: modern app-level recording permission APIs.
- `Handling audio interruptions`: interruption notifications and resume policy.
- `Responding to audio route changes`: route-change notifications and headphones-disconnect privacy behavior.
- `AVCaptureSession` audio-session properties when capture code changes the shared app audio session.

Type ownership:

- Keep category, mode, options, route-sharing policy, route descriptions, port descriptions, and permission surfaces in AVFAudio or AVFoundation terms until a UI or persistence boundary requires a smaller app model.
- Use `AVAudioSession.Category`, `AVAudioSession.Mode`, `AVAudioSession.CategoryOptions`, `AVAudioSession.RouteSharingPolicy`, `AVAudioSessionRouteDescription`, and `AVAudioSessionPortDescription` instead of free-form strings for app audio policy.
- Use `AVAudioApplication.requestRecordPermission` for app recording permission and `AVCaptureDevice.authorizationStatus(for: .audio)` when capture-device authorization is the real question.
- Introduce app-specific policy types only when they add domain meaning, such as "voice note capture" or "speakerphone call mode", and keep the conversion to AVFAudio category, mode, options, and activation explicit.

Repair checklist:

- Name the app's real audio goal first: playback, record, play-and-record, spoken audio, capture, call-adjacent, Bluetooth, AirPlay, or background-compatible behavior.
- Check microphone usage strings before treating silent input as a device failure.
- Use `AVAudioApplication.requestRecordPermission` for app recording permission and `AVCaptureDevice.authorizationStatus(for: .audio)` for capture-device authorization when capture APIs are involved.
- Pick category, mode, route-sharing policy, and options as one policy, not as scattered calls from views, players, and capture delegates.
- Deactivate with `notifyOthersOnDeactivation` when the app interrupted other audio and wants the system to notify interrupted sessions.
- Treat headphones disconnect as a user privacy signal for playback apps.
- Decide whether `AVCaptureSession` may automatically configure the app audio session; if not, own `usesApplicationAudioSession` and related properties deliberately.

Bad shapes:

- "Fixing" audio by retrying `setActive(true)` without identifying category, route, or permission state.
- Treating `overrideOutputAudioPort(.speaker)` as durable speakerphone policy when the category option should express that intent.
- Logging "audio failed" without the operation, category, mode, route, permission state, and likely cause.
