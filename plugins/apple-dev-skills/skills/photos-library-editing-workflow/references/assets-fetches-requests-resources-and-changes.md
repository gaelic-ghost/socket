# Assets, Fetches, Requests, Resources, and Changes

## Fetch and Change Ownership

Keep `PHAsset`, `PHAssetCollection`, `PHCollectionList`, `PHFetchOptions`, and `PHFetchResult` typed. Use local identifiers for durable references but re-fetch and handle deletion, limited-library visibility changes, and inaccessible assets.

Register a `PHPhotoLibraryChangeObserver` only for the lifecycle that consumes changes. In `photoLibraryDidChange`, request `PHChange` details for the exact fetch result or object, replace the stored fetch result with `fetchResultAfterChanges`, and apply incremental inserts, removals, moves, and changes only when incremental details are available. Move UI publication onto the required UI isolation boundary.

## Image and Video Requests

Use `PHImageManager` or `PHCachingImageManager` with explicit target size, content mode, delivery mode, resize mode, version, network-access policy, progress handler, and cancellation. Keep `PHImageRequestID`; cancel obsolete requests and inspect result info for cancellation, error, degraded/intermediate results, and source behavior.

Cache only the visible/prefetch window and stop caching assets that leave it. Do not cache an unbounded library or assume a requested asset is local.

## Asset Resources

Use `PHAssetResource.assetResources(for:)` and `PHAssetResourceManager` when exact resource identity matters. Distinguish original, full-size, adjusted, paired-video, adjustment-base, photo, video, audio, and RAW-related resource types according to current documentation.

Configure `PHAssetResourceRequestOptions.isNetworkAccessAllowed`, progress, cancellation, and destination lifecycle. Preserve original versus adjusted intent, Live Photo photo/video pairing, RAW-plus-processed relationships, metadata policy, filenames/UTTypes, and export errors. A displayed `UIImage` or thumbnail is not an original asset export.
