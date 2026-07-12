# Compression, Decompression, and Session Lifecycle

## Compression

Use `VTCompressionSessionCreate` with explicit dimensions, codec type, encoder specification when required, source image-buffer attributes, output callback, and session owner. Inspect available encoders and supported properties before selecting profiles or controls. Set properties through VideoToolbox and check every `OSStatus`; a property dictionary key existing in an SDK does not prove the selected encoder accepts it.

Configure real-time policy, average bitrate, data-rate limits, keyframe interval, frame reordering, expected frame rate, profile/level, entropy mode, quality, and pixel-transfer behavior only when supported and required. Call `VTCompressionSessionPrepareToEncodeFrames` when appropriate, then submit frames with exact presentation timestamps, durations, frame properties, and source lifetime.

Use `VTCompressionSessionCompleteFrames` to drain through the intended timestamp. For multipass work, preserve `VTMultiPassStorage`, begin/end pass flags, further-pass requests, and final completion. Multipass is an offline policy, not a free quality toggle for real-time streams.

## Decompression

Create `VTDecompressionSession` from a valid compressed `CMVideoFormatDescription`, decoder specification, output image-buffer attributes, and callback/handler. Keep parameter sets and format changes explicit. Submit complete compressed samples with decode flags and inspect returned info flags and asynchronous output status.

Call `VTDecompressionSessionFinishDelayedFrames` when draining reordered output and wait for asynchronous frames when the lifecycle requires it. Invalidate the session once after all owned work is complete.

## Hardware Evidence

Use enable/require hardware specification keys only according to product fallback policy. After creation, inspect `kVTCompressionPropertyKey_UsingHardwareAcceleratedVideoEncoder` or `kVTDecompressionPropertyKey_UsingHardwareAcceleratedVideoDecoder` where documented. Requested hardware is not proof of actual hardware use; record creation outcome, actual property, codec/profile, device/OS, and measured behavior.
