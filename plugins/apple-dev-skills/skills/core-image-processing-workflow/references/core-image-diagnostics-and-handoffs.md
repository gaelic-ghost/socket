# Core Image Diagnostics and Handoffs

## Diagnostic Inventory

Record the operation, source type, source extent, output bounds, orientation, working and output color spaces, `CIFormat`, alpha policy, destination type, context backend, cancellation state, and measured duration. An operator-facing failure should identify the filter or render operation, destination, likely mismatch, and next value to inspect.

## Common Failures

- Empty output: inspect extent, crop intersection, transforms, and input availability.
- Unexpected memory growth: inspect repeated context creation, unbounded extents, full-resolution intermediates, cache behavior, and concurrent in-flight renders.
- Color shift: inspect embedded source profile, working color space, output color space, destination attachments, and display/export color management.
- Dark or fringed edges: inspect alpha presence and premultiplication across inputs, kernels, and output.
- Stale or nondeterministic filters: inspect shared mutable `CIFilter` instances and parameter mutation across tasks.
- Slow video processing: inspect CPU readbacks, context creation, pixel-format conversions, command-buffer boundaries, and work performed after a frame is already obsolete.

## Validation

Use representative source fixtures for orientation, wide color, alpha, HDR, RAW, large dimensions, and unusual extents. Compare output dimensions, properties, color behavior, and perceptual or numeric pixels at the level appropriate to the operation. Profile release builds on representative devices before claiming real-time or GPU performance.

Hand file decoding, metadata, and platform representations to `apple-image-representation-workflow`; recognition to Vision; capture to AVFoundation; low-level codecs to VideoToolbox; project execution and Instruments to Xcode workflows.
