# Privacy, Validation, Signing, and Distribution

## Privacy

Inventory the data visible to the system host, extension, containing app, shared container, and any server separately. Ask whether the feature works with less data, shorter retention, fewer logs, and no background collection. Explain user-visible activation or configuration requirements without implying that an installed extension is automatically enabled.

## Validation

Validate the target in layers: extension-point configuration and `Info.plist`; target membership and embedding; per-target entitlements; signing; clean install and enablement; host activation; core behavior; interruption and restart; privacy-sensitive log review; and the real distribution artifact. Extract framework-independent logic into a testable shared target only when that ownership is already justified.

## Distribution

Development signing proves only a development path. For macOS, route release signing, notarization, Gatekeeper, and artifact evidence to `macos-distribution-workflow`. For all platforms, use the extension point’s current distribution requirements and validate the user-facing install path.

## Sources

- [Entitlements](https://developer.apple.com/documentation/bundleresources/entitlements)
- [Configuring the macOS App Sandbox](https://developer.apple.com/documentation/xcode/configuring-the-macos-app-sandbox)
- [Signing Mac software with Developer ID](https://developer.apple.com/documentation/security/signing-mac-software-with-developer-id)
