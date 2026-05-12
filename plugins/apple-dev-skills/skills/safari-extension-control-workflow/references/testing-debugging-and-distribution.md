# Testing, Debugging, And Distribution

## Documented Anchors

- Running your Safari Web Extension: https://developer.apple.com/documentation/safariservices/running-your-safari-web-extension
- Troubleshooting your Safari Web Extension: https://developer.apple.com/documentation/safariservices/safari_web_extensions/troubleshooting_your_safari_web_extension
- Troubleshooting your Safari App Extension: https://developer.apple.com/documentation/safariservices/troubleshooting-your-safari-app-extension
- Distributing your Safari Web Extension: https://developer.apple.com/documentation/safariservices/distributing-your-safari-web-extension
- Packaging a Web Extension for Safari: https://developer.apple.com/documentation/safariservices/packaging-a-web-extension-for-safari
- Packaging and distributing Safari Web Extensions with App Store Connect: https://developer.apple.com/documentation/safariservices/packaging-and-distributing-safari-web-extensions-with-app-store-connect
- Adding a web development tool to Safari Web Inspector: https://developer.apple.com/documentation/safariservices/adding-a-web-development-tool-to-safari-web-inspector

## Debugging Order

1. Verify the containing app builds and embeds the extension target.
2. Verify signing, entitlements, app groups, and bundle identifiers.
3. Verify Safari sees the extension and the user has enabled it.
4. Verify host permissions or website access permissions.
5. Verify the right Safari profile or Mac web app context is enabled.
6. Inspect Web Inspector logs, injected-script logs, system logs, and extension errors.
7. Only then debug higher-level app or page behavior.

## macOS Web Extension Development

- Temporary extension loading is useful for quick macOS Safari checks, but it is not a substitute for an Xcode project when testing iOS, app-extension messaging, native app coordination, or distribution.
- Unsigned extension testing requires Safari developer settings and resets when Safari quits.
- Use the containing macOS app install path when validating real app-extension packaging behavior.

## Web Inspector Extension Development

- Treat Safari Web Inspector Extensions as developer-tool panels that extend Web Inspector, not as ordinary end-user extension UI.
- Verify Web Inspector developer features before debugging the extension itself.
- Validate the Web Inspector panel loads before testing inspected-page data exchange.
- Keep console and diagnostic output clear about whether a failure is in the Web Inspector extension UI, inspected-page messaging, the containing app, or native messaging.

## Safari App Extension Debugging

- Use `pluginkit` to verify whether Safari can see the app extension when visibility is in doubt.
- Verify allowed URL patterns and website access permissions before debugging injected-script logic.
- Keep native extension logs clear about which callback, page, profile, and message failed.

## Distribution Boundaries

- App Store distribution requires the extension to be packaged with an app and reviewed as part of the app submission path.
- For Safari Web Extensions, decide early whether the source of truth is an existing cross-browser extension, a new Xcode template project, or a temporary macOS Safari folder during early evaluation.
- Do not claim a WebExtension is production-ready until signing, packaging, permission prompts, App Store Connect metadata, and Safari enablement paths have been exercised.
