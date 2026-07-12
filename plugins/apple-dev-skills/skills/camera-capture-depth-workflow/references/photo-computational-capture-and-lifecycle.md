# Photo, Computational Capture, and Lifecycle

## Photo Configuration

Configure `AVCapturePhotoOutput` capabilities before creating per-capture `AVCapturePhotoSettings`. Keep the settings unique per request and retain the delegate through the complete photo capture callback sequence.

Choose processed codec, RAW pixel format, bracket settings, flash, quality prioritization, preview format, depth delivery, Live Photo movie URL, portrait-effects matte, semantic segmentation mattes, and supported computational features from the output's current capabilities. Do not request mutually incompatible settings or assume enabling an output feature makes every settings instance use it.

Use `maxPhotoQualityPrioritization` and per-request `photoQualityPrioritization` deliberately. Treat responsive capture, fast capture prioritization, deferred photo delivery, zero shutter lag, spatial video, and cinematic features as independently capability-gated behavior with their documented lifecycle and quality tradeoffs. Current Xcode documentation establishes spatial video capture through compatible device formats and movie-file output; do not infer a spatial-photo API without a current documentation anchor.

## Typed Results

Keep `AVCapturePhoto` as the result owner until file data, pixel buffers, metadata, depth, mattes, calibration, and capture errors have been inspected. Preserve the relationship among the primary image, RAW representation, Live Photo movie, depth, portrait-effects matte, and semantic mattes through orientation and export.

## Session Lifecycle and Pressure

Observe session start/stop state, interruptions and reasons, runtime errors, media-services reset, device disconnection, subject-area changes, and system pressure. Explain which notification or property changed, the affected device/session/output, the likely cause, and whether to wait, rebuild, reduce quality/frame rate, switch devices, or ask the user to act.

Handle authorization denial separately from missing hardware. Never retry a denied permission as if the camera were temporarily unavailable. Do not restart blindly after every runtime error; rebuild only when the documented error and current session state require it.
