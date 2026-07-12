# Image I/O Decoding, Encoding, and Metadata

## Source Inspection

Create a `CGImageSource` from the URL, data, or incremental provider appropriate to the input. Before decoding, inspect the type, image count, per-image properties, dimensions, orientation, embedded profile, frame timing, and auxiliary-data inventory needed by the task.

Use incremental sources for progressive data arrival. Update the source as data arrives and mark the final update accurately. Treat incomplete frames as provisional and keep cancellation and byte ownership explicit.

## Thumbnail and Decode Policy

Use Image I/O source thumbnail options when the requested result is a bounded thumbnail or preview. Configure maximum pixel size, transform policy, and cache behavior deliberately. Avoid decoding a large full-resolution raster only to scale it down immediately afterward.

Apply orientation at one named boundary. Do not both transform during thumbnail creation and carry the original orientation as if pixels remained unrotated.

## Metadata and Auxiliary Images

Keep source properties and `CGImageMetadata` typed. Separate preservation, modification, removal, and privacy-sanitization policies. GPS, camera, timestamp, author, and editing properties may be sensitive; never copy them accidentally merely because pixel output is allowed.

Inventory depth, disparity, gain maps, portrait-effects mattes, semantic mattes, and other auxiliary data before export. Copy or transform them only when the destination supports them and the relationship to the primary image remains valid.

## Destination Lifecycle

Choose the destination type identifier and image count up front. Add each image or frame with its intended properties and metadata, add supported auxiliary data deliberately, then require `CGImageDestinationFinalize` to return success. A destination object or partially written data value is not proof of a valid encoded image.

For animated or multi-frame output, preserve frame ordering, durations, loop properties, dimensions, color policy, and format-specific constraints. Validate by opening the encoded result as a new source and checking the properties that matter.
