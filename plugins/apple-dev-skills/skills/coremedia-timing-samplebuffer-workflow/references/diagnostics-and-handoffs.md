# Diagnostics And Handoffs

Core Media repair is evidence-heavy. Prefer small probes over broad rewrites.

Useful diagnostics:

- sample presentation timestamp, decode timestamp, duration, and output presentation time
- format description media type and extensions
- sample attachments and dropped-buffer reasons
- writer input readiness and final error
- synchronizer rate and current time
- control timebase clock and host-time relationship

Keep diagnostics typed:

- print `CMTime` value, timescale, flags, epoch, and validity before converting to seconds
- print `CMSampleTimingInfo` presentation timestamp, decode timestamp, and duration separately
- print `CMFormatDescription` media type and relevant extensions instead of only a codec label
- print attachment keys and dropped-buffer reasons before deciding whether a buffer can be treated as ordinary media
- print the source clock or timebase relationship when diagnosing drift or audio/video synchronization

Hand off to `avfoundation-media-pipeline-workflow` when:

- the owner of capture, reader, writer, export, or player state is unclear
- the append loop ignores writer back-pressure
- asset loading is deprecated or blocking

Hand off to Xcode execution skills when:

- sample buffers need to be captured live
- drift needs to be measured over time
- display-layer or render-synchronizer behavior needs a running app
