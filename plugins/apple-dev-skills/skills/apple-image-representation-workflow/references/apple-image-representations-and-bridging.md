# Apple Image Representations and Bridging

## Choose by Responsibility

- Use `CGImage` when the next operation needs stable raster pixels, Core Graphics drawing, masking, cropping, or image-provider access.
- Use `CIImage` when the next operation builds or renders a Core Image processing graph.
- Use `NSImage` when AppKit must select or draw among platform image representations.
- Use `NSImageRep` and `NSBitmapImageRep` when macOS code needs representation-specific dimensions, pixels, color space, encoding, or representation selection.
- Use `UIImage` for UIKit image display semantics, including logical scale, orientation, rendering mode, and underlying image source.
- Use `CVPixelBuffer` for captured, decoded, encoded, analyzed, or GPU-consumed frames where buffer attachments and hardware interoperability matter.

## AppKit Representation Rules

An `NSImage` can contain multiple raster, PDF, vector, symbol, or custom representations. Its logical size is not proof of one representation's pixel dimensions. Inspect `representations`, select or request the best representation for the destination, and avoid locking focus merely to force a bitmap when direct representation or Core Graphics drawing works.

When exporting through `NSBitmapImageRep`, define the raster dimensions, color space, alpha, and output properties rather than assuming the current screen scale is the desired file resolution.

## UIKit Representation Rules

Preserve `UIImage.scale` and `UIImage.imageOrientation` when display semantics matter. Creating a `UIImage` from a `CGImage` or `CIImage` can add orientation and scale semantics that are not baked into the underlying pixels. Decide whether to preserve metadata orientation or normalize pixels, and do it once.

## Conversion Review

For every bridge, record the source and destination type, whether rendering or decoding occurs, whether pixels are copied, and which orientation, scale, metadata, color, alpha, HDR, animation, and auxiliary-data values survive. Keep original encoded bytes when lossless round-trip requirements exceed the destination representation.
