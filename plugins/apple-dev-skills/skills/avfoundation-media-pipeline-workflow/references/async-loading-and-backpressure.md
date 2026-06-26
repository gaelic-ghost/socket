# Async Loading And Backpressure

Modern Swift AVFoundation code should avoid deprecated synchronous asset properties.

Use async property loading when inspecting assets:

- `try await asset.load(.duration)`
- `try await asset.load(.tracks)`
- `try await asset.load(.metadata)`
- tuple loading when several properties are needed together

Repair deprecated shapes:

- Replace synchronous property reads on `AVAsset`, `AVAssetTrack`, and `AVMetadataItem` in Swift clients.
- Replace `loadValuesAsynchronously(forKeys:)` when the deployment target and code shape support Swift concurrency.
- Batch related property loads so AVFoundation can optimize the request.

Writer back-pressure:

- Check `isReadyForMoreMediaData` or use the modern receiver API where appropriate.
- Keep `expectsMediaDataInRealTime` aligned with whether the source is live.
- Mark inputs finished exactly once.
- Surface writer failure with the input, file URL or destination kind, media type, and likely timing or disk cause.
