# PhotosUI Selection and Authorization

## Picker-First Selection

Use SwiftUI `PhotosPicker`/`photosPicker` or `PHPickerViewController` when the app needs only items the user explicitly chooses. Configure matching filters, maximum selection count, selection behavior/order, preferred item encoding, and the intended photo library. A system picker is the privacy-preserving selection boundary; do not request broad library access solely to recreate it.

Keep each `PhotosPickerItem` or `PHPickerResult` tied to the current selection generation. Load only supported transferable/content types, model progress and cancellation, and discard results from obsolete selections. `PhotosPickerItem.loadTransferable` and item-provider loads may require iCloud/network work and can fail or be cancelled.

Picker results are selected content handles, not proof of a PhotoKit `PHAsset`. Use an asset identifier only when the documented picker configuration/result provides one and the app already has the authorization needed to fetch it.

## Authorization

Choose `PHAccessLevel.addOnly` for saving without browsing and `.readWrite` for actual library reading, limited selection management, observation, organization, or editing. Check `PHPhotoLibrary.authorizationStatus(for:)` and request authorization for the same level.

Handle every `PHAuthorizationStatus`:

- `.notDetermined`: explain the feature at the moment of need, then request once.
- `.restricted`: explain that system policy prevents access.
- `.denied`: preserve nonlibrary app behavior and offer the documented settings route when useful.
- `.limited`: operate only on visible assets, do not fetch or organize user albums, and use the documented limited-library management UI when user intent requires it.
- `.authorized`: use only the access needed by the feature.

Treat `.readWrite` as the requested access level and `.authorized` as the status required for full-library album browsing and organization. A `.limited` result is intentionally narrower: keep picker and selected-asset behavior available, explain why an album feature needs broader access, and offer the documented settings or limited-library management route rather than attempting album fetches or change requests that require the full library.

Provide the correct usage description for each requested access level. Authorization is not permission to copy unrelated metadata, upload media, or retain selected content indefinitely.
