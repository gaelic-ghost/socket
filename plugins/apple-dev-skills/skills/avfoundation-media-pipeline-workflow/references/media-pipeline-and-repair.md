# Media Pipeline And Repair

Use current AVFoundation documentation before changing capture, playback, reader, writer, or export code. Start from:

- `AVCaptureSession`: configuration, inputs, outputs, and blocking `startRunning()`.
- `AVPlayer` and `AVPlayerItem`: playback status and automatically loaded asset keys.
- `AVAsset` and `AVURLAsset`: lightweight creation and async property loading.
- `AVAssetReader` and `AVAssetWriter`: pipeline ownership and append loops.
- `AVAssetWriterInput`: readiness, real-time input, and finished-state handling.

Type ownership:

- Keep capture state in `AVCaptureSession`, `AVCaptureDevice`, `AVCaptureInput`, `AVCaptureOutput`, and `AVCaptureConnection` terms until a UI or persistence boundary needs a smaller app model.
- Keep playback state in `AVPlayer`, `AVPlayerItem`, `AVAsset`, `AVAssetTrack`, and `AVAsyncProperty` terms instead of replacing readiness, duration, tracks, or metadata with untyped dictionaries.
- Keep reader and writer loops expressed through `AVAssetReader`, `AVAssetReaderOutput`, `AVAssetWriter`, `AVAssetWriterInput`, receiver/adaptor types, and `CMSampleBuffer` so readiness, media type, timing, and failure state stay visible.
- Use Core Media types for timing and sample payload facts inside AVFoundation pipelines; hand off to `coremedia-timing-samplebuffer-workflow` when the bug is really timestamp, format-description, attachment, or timebase behavior.
- Introduce custom wrapper types only for app-domain intent, serialization, or UI-facing summaries, and document which AVFoundation or Core Media type they summarize.

Repair checklist:

- Move blocking capture-session start and stop work onto a serial session queue.
- Keep session configuration on a consistent owner instead of mutating inputs and outputs from unrelated views.
- Use Swift concurrency asset loading for modern Swift clients.
- Keep player state observation separate from asset inspection and export policy.
- Model cancellation and teardown before adding retry loops.
- Reject stringly typed media kind, route, writer state, or capture state when Apple already exposes a typed surface.
- Treat sample-buffer timestamp issues as a Core Media handoff after identifying the pipeline stage that produced or consumed the bad timing.

Bad shapes:

- A view object that owns session setup, delegate callbacks, writer loops, player state, and UI updates.
- A writer loop that appends whenever data appears without checking readiness or final failure state.
- "Fixing" capture by adding sleeps around start/stop instead of using a queue and lifecycle boundary.
