# Vision Coordinates, Live Frames, and Diagnostics

## Coordinate Pipeline

Inventory source pixels, orientation, mirroring, region of interest, normalized Vision output, crop behavior, preview or image-view content mode, and final view coordinates. Use Vision conversion functions for normalized image locations where applicable, then apply UI framework transforms. Validate all four corners and at least one nonsquare image rather than trusting one portrait fixture.

## Live Scheduling

Give every frame a sequence number or presentation timestamp. Use a bounded newest-frame or explicitly queued policy based on product semantics. For camera overlays, stale accuracy is usually worse than an intentionally dropped frame. Do not create an unbounded Task for every sample buffer. Cancel work where the request supports it and discard results that no longer match the current frame or stream generation.

## Diagnostics

Log the request type, API family, revision when applicable, source dimensions and orientation, region of interest, frame identity, elapsed time, cancellation state, observation count/types, and the exact transform stage that failed. Explain likely causes such as unsupported revision, wrong orientation, mismatched crop, insufficient pixels, obsolete frame, or unavailable compute stage.

Validate with known fixtures for orientations, mirroring, aspect ratios, empty scenes, multiple observations, low confidence, and cancellation. Use physical devices and representative streams before claiming throughput or real-time behavior.
