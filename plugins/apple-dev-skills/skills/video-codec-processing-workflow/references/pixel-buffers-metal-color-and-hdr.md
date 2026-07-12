# Pixel Buffers, Metal, Color, and HDR

## Pixel Buffers and Pools

Preserve `CVPixelBuffer` dimensions, pixel format, plane count, bytes per row for each plane, extended pixels, attachments, IOSurface state, and pool provenance. Use `CVPixelBufferPool` for bounded compatible allocation and surface pool-exhaustion or allocation-threshold behavior rather than silently allocating unrelated buffers.

Balance `CVPixelBufferLockBaseAddress` and unlock with matching flags. Treat planar formats as planes; do not assume one contiguous packed address. Keep the buffer alive through CPU, codec, Core Image, Vision, or GPU consumption.

## Metal and IOSurface

Use `CVMetalTextureCacheCreateTextureFromImage` to create compatible texture views and obtain the Metal texture from `CVMetalTexture`. Preserve plane selection, Metal pixel format, dimensions, storage lifetime, command-buffer synchronization, and cache lifecycle.

IOSurface-backed buffers can enable shared storage, but a compatible buffer does not prove an end-to-end zero-copy path. Check pixel-format compatibility and profile for conversions, staging, synchronization, or CPU readback before using that claim.

## Color and HDR

Preserve Core Video attachments for color primaries, transfer function, YCbCr matrix, chroma location, clean aperture, pixel aspect ratio, mastering/display metadata, content-light metadata, and other format-specific signal properties. Keep attachments synchronized with `CMVideoFormatDescription` extensions and output container/sample metadata.

Do not label output HDR merely because the pixel format has high bit depth. Verify transfer function, primaries, matrix/range, metadata, codec/profile, container, display/export path, and observed result. Preserve alpha only with a codec/profile/pixel format and consumer that support it.
