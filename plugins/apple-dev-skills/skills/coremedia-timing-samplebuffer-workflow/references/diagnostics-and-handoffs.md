# Diagnostics And Handoffs

Core Media repair is evidence-heavy. Prefer small probes over broad rewrites.

Useful diagnostics:

- sample presentation timestamp, decode timestamp, duration, and output presentation time
- format description media type and extensions
- sample attachments and dropped-buffer reasons
- writer input readiness and final error
- synchronizer rate and current time
- control timebase clock and host-time relationship

Hand off to `avfoundation-media-pipeline-workflow` when:

- the owner of capture, reader, writer, export, or player state is unclear
- the append loop ignores writer back-pressure
- asset loading is deprecated or blocking

Hand off to Xcode execution skills when:

- sample buffers need to be captured live
- drift needs to be measured over time
- display-layer or render-synchronizer behavior needs a running app
