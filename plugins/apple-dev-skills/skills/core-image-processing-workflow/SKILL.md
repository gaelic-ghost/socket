---
name: core-image-processing-workflow
description: Guide Core Image implementation and repair across CIImage processing graphs, CIContext rendering, built-in and custom filters, RAW development, color management, HDR, regions of interest, Core Video and Metal destinations, and performance diagnostics. Use when Apple-platform image work changes, generates, composites, or renders pixels rather than decoding files or recognizing image content.
---

# Core Image Processing Workflow

## Purpose

Guide Core Image processing and rendering without turning `CIImage` into a bitmap wrapper or mixing transformation with file decoding, visual recognition, or display-container ownership. Preserve Core Image, Core Graphics, Core Video, and Metal types until an explicit output boundary.

## When To Use

- Use for Core Image filter chains, compositing, RAW development, custom kernels, color or HDR processing, render destinations, and Core Image performance or correctness repair.
- Recommend `apple-image-representation-workflow` when decoding, encoding, metadata, or platform image-container behavior is primary.
- Recommend the Vision workflow when the requested outcome is recognition or analysis rather than pixel transformation.

## Single-Path Workflow

1. Classify the request:
   - built-in filter chain
   - compositing, masking, scaling, or geometry
   - RAW development
   - custom kernel or processor
   - color, HDR, or alpha repair
   - render destination or interop
   - performance or correctness diagnosis
2. Apply the Apple docs gate:
   - read current Core Image documentation before proposing implementation changes
   - state the documented behavior relied on
   - apply `../../shared/references/apple-image-type-ownership.md`
   - use `references/core-image-processing-and-rendering.md` for graph, context, color, render, and performance decisions
   - use `references/core-image-diagnostics-and-handoffs.md` for repair probes and ownership handoffs
3. Define the graph and ownership:
   - identify the source image, extent, orientation state, color space, alpha semantics, and dynamic range
   - build immutable `CIImage` transformations and keep mutable `CIFilter` instances task-local
   - choose one deliberately scoped, reusable `CIContext`
   - select the output bounds, format, color space, and destination before rendering
4. Repair common failure modes:
   - treating `CIImage` as already-rendered pixels
   - creating a new `CIContext` per frame or filter application
   - sharing mutable `CIFilter` instances across concurrent work
   - losing orientation, extent, alpha, color-space, HDR, or auxiliary-data meaning during conversion
   - forcing CPU readback between Core Image, Core Video, and Metal without a concrete boundary
   - rendering infinite or unexpectedly expanded extents without an explicit crop
   - using Core Image as a recognition framework instead of handing analysis to Vision
5. Return one recommendation with:
   - processing class and documented behavior
   - source and output type ownership
   - graph, context, color, extent, and render-destination plan
   - concurrency, cancellation, memory, and performance plan
   - repair findings and runtime validation handoff

## Inputs

- `request`: image-processing task or code under repair.
- `processing_goal`: `filter`, `composite`, `raw`, `kernel`, `color`, `hdr`, `render`, `interop`, or `repair`.
- `platform_context`: `ios`, `ipados`, `macos`, `tvos`, `visionos`, or `mixed-apple`.
- Defaults:
  - prefer current Xcode or Apple documentation
  - preserve `CIImage`, `CIContext`, `CIFilter`, `CIFormat`, `CGColorSpace`, `CVPixelBuffer`, `IOSurface`, and Metal types
  - preserve lazy evaluation until a real render boundary
  - prefer Core Image before a custom Metal pipeline when Core Image expresses the requirement

## Outputs

- `status`: `success`, `handoff`, or `blocked`.
- `path_type`: `primary` when Core Image owns the operation, `fallback` when another framework owns the next step.
- `output`: documented behavior, graph and type ownership, render plan, diagnostics, validation, and handoff.

## Guards and Stop Conditions

- Do not claim a `CIImage` is rendered pixel storage; it describes an image and its processing recipe until rendered.
- Do not create generic image managers, filter coordinators, or custom pixel wrappers when framework types and direct composition express the requirement.
- Do not share mutable `CIFilter` state across concurrent tasks.
- Do not silently discard orientation, scale, metadata, color space, alpha, dynamic range, extent, or auxiliary data.
- Do not claim GPU, Metal, HDR, RAW, real-time, or zero-copy behavior is verified without runtime or profiling evidence.
- Stop when the source representation, output destination, color requirements, or device capability needed for a correct recommendation is unavailable.

## Fallbacks and Handoffs

- Recommend `apple-image-representation-workflow` for Image I/O decode/encode, metadata, `CGImage`, `NSImage`, `NSImageRep`, `NSBitmapImageRep`, or `UIImage` ownership.
- Recommend `vision-image-analysis-workflow` for recognition, detection, tracking, segmentation, or feature analysis.
- Recommend `camera-capture-depth-workflow` for camera and depth capture.
- Recommend `avfoundation-media-pipeline-workflow` for capture-session, reader, writer, export, or video pipeline ownership.
- Recommend `video-codec-processing-workflow` for low-level codec and pixel-buffer work.
- Recommend `xcode-build-run-workflow` for project integration, Metal toolchain, build, run, device, or Instruments follow-through.
- Recommend `xcode-testing-workflow` for fixtures, image comparisons, performance baselines, or regression tests.
- Recommend `explore-apple-swift-docs` when documentation lookup is the real need.

## Customization

Use `references/customization-flow.md`. This workflow defines no runtime-enforced knobs.

## References

- `references/core-image-processing-and-rendering.md`
- `references/core-image-diagnostics-and-handoffs.md`
- `references/customization-flow.md`
- `../../shared/references/apple-image-type-ownership.md`
- Recommend `references/snippets/apple-xcode-project-core.md` for reusable Xcode-project policy.

## Script Inventory

- `scripts/customization_config.py`
