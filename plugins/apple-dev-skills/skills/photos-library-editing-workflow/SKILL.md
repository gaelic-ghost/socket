---
name: photos-library-editing-workflow
description: Guide privacy-preserving PhotosUI media selection and PhotoKit authorization, limited-library access, assets, collections, fetches, change observation, image/video requests, caching, iCloud delivery, asset resources, creation transactions, albums, content editing, adjustment data, nondestructive edits, cancellation, and diagnostics. Use when selecting user media or reading, saving, observing, organizing, exporting, or editing the Apple Photos library.
---

# Photos Library and Editing Workflow

## Purpose

Guide PhotosUI selection and PhotoKit library work while requesting the narrowest access, preserving typed asset/resource identity, and keeping image processing and video pipelines with their owning frameworks.

## When To Use

- Use for `PhotosPicker`, `PHPickerViewController`, `PHPhotoLibrary`, assets, fetches, collections, image/resource requests, changes, creation, albums, or nondestructive editing.
- Prefer PhotosUI when the app only needs media the user explicitly selects.
- Use PhotoKit authorization only for concrete library read, add, observe, organize, or edit behavior.

## Single-Path Workflow

1. Classify the request:
   - user-selected image/video through PhotosUI
   - add-only save
   - read/write or limited-library browse
   - asset/collection fetch and change observation
   - image, video, Live Photo, data, or resource request
   - iCloud-backed delivery, progress, cancellation, or caching
   - asset/album creation or transactional change
   - content-editing input/output and adjustment data
   - privacy, lifecycle, or correctness repair
2. Apply the Apple docs gate:
   - read current PhotosUI, PhotoKit, SwiftUI, and Core Transferable documentation for the platform
   - state the documented behavior relied on
   - check API/platform availability before making macOS, iOS, iPadOS, or visionOS claims
3. Choose the narrowest access:
   - use `PhotosPicker` or `PHPickerViewController` for explicit user selection when broad library access is unnecessary
   - use `.addOnly` when the app only saves into Photos
   - use `.readWrite` only for fetch, limited-library, organization, observation, or edit requirements
   - handle `.notDetermined`, `.restricted`, `.denied`, `.authorized`, and `.limited` distinctly
4. Preserve typed identity and lifecycle:
   - keep `PhotosPickerItem`, `PHPickerResult`, `PHAsset`, `PHAssetCollection`, `PHFetchResult`, `PHAssetResource`, request IDs, placeholders, and adjustment data typed
   - attach asynchronous results to the current selection, asset local identifier, request ID, fetch result, or edit generation
   - cancel obsolete loads and ignore stale callbacks
5. Perform changes transactionally:
   - create `PHAssetCreationRequest`, asset/collection change requests, and placeholders only inside `PHPhotoLibrary.performChanges`
   - surface transaction errors and fetch created objects after commit when needed
6. Return documented behavior, picker-versus-library decision, authorization/purpose-string policy, asset/resource identity, request/cancellation and iCloud policy, transactional/editing plan, diagnostics, validation, and handoffs.

## Inputs

- `request`: Photos selection, library, resource, save, or edit task.
- `photos_goal`: `pick`, `add`, `browse`, `fetch`, `observe`, `request`, `resource`, `create`, `album`, `edit`, or `repair`.
- `platform_context`: Apple platform, deployment target, UI framework, and Photos availability.
- `privacy_context`: required access level, user explanation, metadata policy, network/iCloud policy, retention, and export behavior.

## Outputs

- `status`: `success`, `handoff`, or `blocked`.
- `path_type`: `primary` for PhotosUI/PhotoKit, `fallback` for image decode/process, video, UI architecture, or execution.
- `output`: documented behavior, access decision, identity/lifecycle, request/change/edit plan, diagnostics, validation, and handoffs.

## Guards and Stop Conditions

- Do not request PhotoKit read/write authorization when a system picker or add-only access fulfills the feature.
- Do not treat `.limited` as fully authorized or as denial; operate on the visible library and provide the documented management path when appropriate.
- Do not mirror the entire library into app-owned state or introduce a Photos repository when `PHFetchResult`, local identifiers, change details, and picker bindings express the requirement.
- Do not assume a picker item, asset, or resource is local; model iCloud/network delivery, progress, cancellation, and failure explicitly.
- Do not treat degraded or opportunistic image callbacks as final, and do not let stale request callbacks overwrite a newer selection.
- Do not silently substitute adjusted content for original resources, flatten Live Photos, discard RAW/paired resources, or copy metadata without an explicit policy.
- Do not claim a library change succeeded before `performChanges` completes successfully.
- Do not destructively replace edited content when PhotoKit's content-editing and adjustment-data contract requires nondestructive output.
- Stop when authorization, selected item, resource identity, network policy, or required runtime evidence is unavailable.

## Fallbacks and Handoffs

- Recommend `apple-image-representation-workflow` for Image I/O decode/encode, metadata inspection, thumbnails, and image representations.
- Recommend `core-image-processing-workflow` for image effects, color, RAW processing, masks, and rendering.
- Recommend `avfoundation-media-pipeline-workflow` for video assets, playback, export, reader/writer, and transcode pipelines.
- Recommend `video-codec-processing-workflow` for low-level compression/decompression or pixel-buffer behavior.
- Recommend `swiftui-app-architecture-workflow` or `appkit-app-architecture-workflow` for broader UI ownership while keeping direct picker bindings and PhotoKit state here.
- Recommend `xcode-build-run-workflow` for purpose strings, target integration, build, run, physical-library testing, logging, or profiling.
- Recommend `xcode-testing-workflow` for authorization matrices, picker/load fakes, resource fixtures, change-detail tests, and edit round trips.
- Recommend `explore-apple-swift-docs` for current PhotosUI or PhotoKit research.

## Customization

Use `references/customization-flow.md`. This workflow defines no runtime-enforced knobs.

## References

- `references/photosui-selection-and-authorization.md`
- `references/assets-fetches-requests-resources-and-changes.md`
- `references/creation-collections-and-nondestructive-editing.md`
- `references/customization-flow.md`
- Recommend `references/snippets/apple-xcode-project-core.md` for reusable Xcode-project policy.

## Script Inventory

- `scripts/customization_config.py`
