# Compressed Samples, Diagnostics, and Performance

## Compressed Samples

Keep `CMVideoFormatDescription`, codec subtype, dimensions, extensions, parameter sets, NAL-unit header length, and format changes explicit. Preserve `CMSampleBuffer` presentation/decode timestamps, duration, data buffer, sample sizes, attachments, sync/dependency flags, and readiness.

Do not infer keyframe status only from position in a GOP. Inspect the documented sample attachments/dependencies and codec output. Hand exact timing and synchronization repair to `coremedia-timing-samplebuffer-workflow`.

## Diagnostics

For every failure record operation, session type, codec, dimensions/profile, property or frame identity, input/output format descriptions, pixel format, timestamps, callback status, info flags, `OSStatus` numeric value and readable interpretation when available, hardware-request/actual state, and next probe.

Distinguish unsupported codec/property, invalid session, bad data, format change, allocation failure, source-lifetime error, callback failure, dropped frame, delayed output, pool pressure, and teardown races.

## Performance

Measure session creation/prepare, first-frame latency, steady-state encode/decode duration, end-to-end frame age, throughput, in-flight depth, output delay/reordering, dropped frames, pool allocation, memory, CPU/GPU/media-engine use, energy, and thermal behavior in release builds on representative devices.

Bound in-flight frames and buffers. Real-time pipelines should degrade or drop according to explicit product policy rather than grow unbounded. Offline pipelines should preserve correctness and cancellation while using controlled parallelism.
