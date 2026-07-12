# Core Image Processing and Rendering

## Processing Graph

`CIImage` represents an immutable, lazily evaluated image recipe. Compose filters, transforms, crops, blends, masks, generators, and kernels as images; render only when a display, file, pixel buffer, IOSurface, or Metal consumer needs concrete output.

Track the source extent throughout the graph. Generators and some effects can produce infinite or expanded extents. Crop deliberately before allocation or export when the intended output is finite.

Use current typed filter APIs where available. Keep mutable `CIFilter` instances local to one task or isolation domain; do not share them concurrently.

## Context Ownership

`CIContext` owns expensive rendering state, caches, and GPU resources. Reuse a deliberately scoped context for a view, renderer, or background processing boundary instead of constructing one per frame. Choose CPU, Metal, or other documented context behavior from the actual interoperability and profiling requirement.

Do not call context cache-clearing methods as routine lifecycle management. Use them only when a measured memory or resource condition justifies the tradeoff.

## Color, Alpha, and Dynamic Range

Inventory the input profile and intended output before choosing working and output color spaces. Keep the working color space explicit when color fidelity or cross-source compositing matters. Do not treat a nil color-space option as a harmless performance toggle without checking the documented color-management effect.

Preserve alpha semantics and premultiplication. Record the selected `CIFormat`, output color space, and destination attachment policy for HDR or extended-range output. Validate the entire display or export path; a high-range intermediate does not prove a high-range result.

## Render Destinations

- Use `createCGImage` when the next boundary needs a concrete Core Graphics image.
- Render to `CVPixelBuffer` for media pipelines that already own compatible buffers and attachments.
- Render to an IOSurface or Metal texture when the consuming pipeline uses that storage and avoids an unnecessary CPU readback.
- Supply explicit bounds and color space. Treat allocation size, pixel format, row layout, and destination lifetime as part of the render contract.

## RAW and Custom Processing

Use `CIRAWFilter` for supported RAW development and preserve source metadata needed to configure it. Use `CIKernel`, `CIColorKernel`, `CIWarpKernel`, `CIBlendKernel`, or `CIImageProcessorKernel` only when built-in filters and composition cannot express the operation. State why a custom kernel or processor is required and profile it on representative hardware.
