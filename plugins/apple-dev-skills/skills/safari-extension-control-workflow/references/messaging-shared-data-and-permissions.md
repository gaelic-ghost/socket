# Messaging, Shared Data, And Permissions

## Documented Anchors

- Safari Web Extension app and JavaScript messaging: https://developer.apple.com/documentation/safariservices/messaging-between-the-app-and-javascript-in-a-safari-web-extension
- Messaging a Web Extension's native app: https://developer.apple.com/documentation/safariservices/messaging-a-web-extensions-native-app
- Safari App Extension injected-script messaging: https://developer.apple.com/documentation/safariservices/passing-messages-between-safari-app-extensions-and-injected-scripts
- `SFSafariPage.dispatchMessageToScript`: https://developer.apple.com/documentation/safariservices/sfsafaripage/dispatchmessagetoscript%28withname%3Auserinfo%3A%29
- Managing Safari Web Extension permissions: https://developer.apple.com/documentation/safariservices/managing-safari-web-extension-permissions

## Contexts To Name Explicitly

For every Safari integration, name the participating contexts:

- containing macOS app
- native app extension
- WebExtension JavaScript background or service worker context
- content script or injected script
- webpage
- Safari profile or Mac web app context when relevant

## Web Extension Messaging

Safari Web Extension messaging is split across sandboxed parts: the app, extension, and JavaScript files. Use native messaging when JavaScript needs to communicate with the containing app, and use app groups when the app and extension need shared persisted data.

Keep message contracts narrow:

- centralize message names
- document payload keys and scalar types
- reject unknown message names
- return descriptive errors for missing permissions, disabled extension state, missing app group data, or unsupported pages
- avoid passing sensitive page data unless the user explicitly granted the relevant extension permission

## Safari App Extension Messaging

Safari App Extension messaging uses Safari-specific injected-script APIs. Injected scripts can send messages to the app extension, and the app extension can dispatch messages back to a page script through `SFSafariPage`.

Keep the distinction clear:

- webpage JavaScript is not the same as the injected script context
- injected scripts communicate through the `safari` namespace Apple documents for Safari App Extensions
- containing-app messages to the extension use `SFSafariApplication.dispatchMessage`
- extension-side dispatch to the injected script context uses `SFSafariPage.dispatchMessageToScript`

## Permission And Privacy Rules

- Treat browsing history, cookies, tokens, page text, URLs, and profile identifiers as sensitive by default.
- Prefer least-privilege host permissions in WebExtension manifests.
- For Safari profiles, keep profile-specific state separate when Apple exposes a profile identifier.
- Keep App Group identifiers explicit and consistent across the containing app and extension.
- Do not store page content or URL history in shared containers unless the user-facing feature clearly requires it.
