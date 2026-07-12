# Apple Image Type Ownership

Use the framework type that still carries the information the next operation needs. Do not normalize Apple image values into a generic image, raw byte array, dictionary, or app-specific wrapper merely to make unlike operations look uniform.

## Framework Values

- `CGImageSource` and `CGImageDestination` own encoded source and destination lifecycles, type identifiers, frames, properties, metadata, thumbnails, and auxiliary data.
- `CGImage` owns concrete raster pixels plus dimensions, bit layout, color space, alpha information, provider, interpolation intent, and decode information.
- `CIImage` owns a lazy image recipe, extent, properties, and processing inputs; it is not proof that pixels have been rendered.
- `NSImage` owns macOS display-oriented image behavior and may contain several `NSImageRep` values with different sizes, scales, color spaces, or vector/raster forms.
- `UIImage` owns UIKit display semantics including scale, orientation, rendering mode, and an underlying `CGImage` or `CIImage` when available.
- `CVPixelBuffer` owns frame-oriented pixel storage, pixel format, planes, attachments, pool provenance, and hardware/media interoperability.

## Required Conversion Ledger

Before conversion, record which of these are present and which the destination can preserve:

- encoded format and original bytes
- pixel dimensions and logical size
- orientation and coordinate convention
- scale
- color profile, working color space, transfer function, primaries, and dynamic range
- alpha and premultiplication
- metadata and privacy-sensitive properties
- animation frames, durations, and loop behavior
- depth, disparity, gain maps, portrait or semantic mattes, and other auxiliary images
- lazy graph, raster storage, buffer-pool, IOSurface, or Metal interoperability

Name every intentional loss. If the requirement does not permit the loss, keep the original representation or choose another destination.

## Direct Composition

- Decode or inspect with Image I/O, then create the concrete processing or display type the next operation requires.
- Process with Core Image and render only at a concrete output boundary.
- Draw a `CGImage` with Core Graphics or place it into the platform image container needed for UI display.
- Keep `CVPixelBuffer` and IOSurface-backed data in their media/GPU path when a CPU bitmap round trip adds no value.
- Preserve original encoded data separately when an edit or export must retain properties that the rendered representation cannot carry.

## Escape Hatches

Convert to an app, persistence, test, wire, or cross-platform type only after naming the concrete boundary, the fields preserved, the fields lost, and the reverse-conversion policy. Do not keep parallel framework and wrapper codepaths after the boundary is typed and proven.
