---
name: apple-image-representation-workflow
description: Guide Apple image decoding, encoding, metadata, thumbnails, multi-frame sources, and representation bridging across Image I/O, Core Graphics, AppKit NSImage and NSImageRep, UIKit UIImage, Core Image, and Core Video. Use when image work involves files, data, representations, orientation, scale, color, metadata, or conversion rather than pixel effects or visual recognition.
---

# Apple Image Representation Workflow

## Purpose

Guide image source, destination, representation, and conversion work without flattening distinct Apple image types into a generic wrapper. Keep file encoding, rendered pixels, processing recipes, platform display containers, metadata, and auxiliary images visibly separate.

## When To Use

- Use for Image I/O sources and destinations, metadata, thumbnails, incremental loading, multi-frame images, `CGImage`, `NSImage`, `NSImageRep`, `NSBitmapImageRep`, `UIImage`, and representation conversion.
- Recommend `core-image-processing-workflow` when filters, compositing, RAW development, custom kernels, or rendering are primary.
- Recommend the Vision workflow when the requested outcome is recognition or analysis rather than representation ownership.

## Single-Path Workflow

1. Classify the request:
   - source inspection or decoding
   - incremental loading or thumbnailing
   - metadata or auxiliary data
   - destination encoding or multi-frame output
   - Core Graphics raster ownership
   - AppKit representation or drawing
   - UIKit image display ownership
   - conversion or repair
2. Apply the Apple docs gate:
   - read current Image I/O, Core Graphics, AppKit, or UIKit documentation first
   - state the documented behavior relied on
   - apply `../../shared/references/apple-image-type-ownership.md`
   - use `references/image-io-decoding-encoding-and-metadata.md` for source and destination work
   - use `references/apple-image-representations-and-bridging.md` for type selection and conversion
3. Preserve source meaning:
   - inspect type, frame count, dimensions, properties, orientation, color profile, alpha, dynamic range, and auxiliary data before conversion
   - choose decode-time thumbnailing or incremental loading when the workload requires it
   - identify whether metadata and original encoded bytes must survive
4. Choose the representation:
   - `CGImage` for concrete raster pixels and Core Graphics drawing
   - `CIImage` for a lazy processing graph
   - `NSImage` and `NSImageRep` for macOS display-oriented multi-representation behavior
   - `UIImage` for UIKit display semantics including scale and orientation
   - `CVPixelBuffer` for frame-oriented media and hardware interop
5. Encode deliberately:
   - choose destination type, frame count, properties, metadata policy, orientation policy, color profile, compression, and auxiliary-data policy
   - add every image or frame
   - require successful `CGImageDestinationFinalize` before claiming output exists
6. Return one recommendation with source facts, chosen types, conversion losses, decode/encode plan, memory and cancellation policy, diagnostics, and validation.

## Inputs

- `request`: image representation, decode, encode, metadata, or conversion task.
- `representation_goal`: `inspect`, `decode`, `thumbnail`, `incremental`, `metadata`, `encode`, `appkit`, `uikit`, `bridge`, or `repair`.
- `platform_context`: `ios`, `ipados`, `macos`, `tvos`, `watchos`, `visionos`, or `mixed-apple`.

## Outputs

- `status`: `success`, `handoff`, or `blocked`.
- `path_type`: `primary` when image representation owns the work, `fallback` when processing, analysis, capture, or codecs own it.
- `output`: documented behavior, source inventory, selected representation, conversion-loss ledger, decode/encode plan, diagnostics, and validation.

## Guards and Stop Conditions

- Do not assume `NSImage` contains one fixed bitmap; it can own multiple representations and select among them for drawing.
- Do not assume `UIImage`, `NSImage`, `CGImage`, and `CIImage` preserve the same orientation, scale, metadata, color, or rendering semantics.
- Do not fully decode large images merely to produce a small thumbnail when Image I/O thumbnailing fits the requirement.
- Do not discard source metadata, ICC profiles, animation frames, depth, disparity, gain maps, mattes, or other auxiliary data silently.
- Do not claim an encoded destination succeeded before finalization returns success.
- Do not invent image repositories, managers, or mirrored metadata models when Image I/O properties and framework values express the boundary.
- Stop when required source bytes, format support, destination policy, or preservation requirements are unavailable.

## Fallbacks and Handoffs

- Recommend `core-image-processing-workflow` for filters, RAW development, compositing, color processing, custom kernels, or rendering.
- Recommend `vision-image-analysis-workflow` for recognition and analysis.
- Recommend `appkit-app-architecture-workflow` for broader macOS view, controller, window, or application ownership.
- Recommend `avfoundation-media-pipeline-workflow` for assets, capture, video, readers, writers, or export.
- Recommend `photos-library-editing-workflow` for PhotoKit and PhotosUI ownership after Milestone 61 ships.
- Recommend `xcode-build-run-workflow` for target resources, build, run, device, or profiling follow-through.
- Recommend `xcode-testing-workflow` for image fixtures, metadata round trips, comparison tests, or performance baselines.
- Recommend `explore-apple-swift-docs` when documentation lookup is the real need.

## Customization

Use `references/customization-flow.md`. This workflow defines no runtime-enforced knobs.

## References

- `references/image-io-decoding-encoding-and-metadata.md`
- `references/apple-image-representations-and-bridging.md`
- `references/customization-flow.md`
- `../../shared/references/apple-image-type-ownership.md`
- Recommend `references/snippets/apple-xcode-project-core.md` for reusable Xcode-project policy.

## Script Inventory

- `scripts/customization_config.py`
