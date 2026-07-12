# Creation, Collections, and Nondestructive Editing

## Transactional Changes

Perform library mutations inside `PHPhotoLibrary.performChanges` or its documented async equivalent. Create assets with `PHAssetCreationRequest` and explicit resource types/options. Create or modify albums with `PHAssetCollectionChangeRequest`. Use placeholders only inside the change transaction, retain local identifiers when needed, and fetch the committed object after successful completion.

Do not update application success state before the transaction completes. Report the operation, access level, resource/collection intent, error, likely cause, and next probe. Handle partial input preparation outside the transaction so the change block stays deterministic and does not perform arbitrary network or long-running work.

## Nondestructive Editing

Request `PHContentEditingInput` with explicit version/network policy. Inspect existing `PHAdjustmentData`; use it only when the app can handle its format identifier and version. Otherwise request or use the appropriate rendered/full-size input according to product intent.

Create `PHContentEditingOutput` from the input. Write the rendered image or audiovisual output to the provided URL and set new `PHAdjustmentData` that records enough versioned parameters to reproduce or revise the edit. Commit the content editing output through a `PHAssetChangeRequest` transaction.

Keep original media preserved by PhotoKit's nondestructive model. Define how the app handles previous adjustments from itself and other editors, Live Photos, paired resources, orientation, color/HDR, metadata, cancellation, temporary files, and cleanup.

## Validation

Test add-only, read/write, limited, denied, restricted, iCloud-only, degraded, cancellation, deletion, changed-library, original/adjusted resource, Live Photo, RAW-plus-processed, transaction failure, and adjustment-version paths on suitable devices/accounts. Do not claim simulator fixtures prove a user's real iCloud Photos behavior.
