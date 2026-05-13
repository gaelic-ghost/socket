# SafariServices Control Surfaces

## Documented Anchors

- `SFSafariApplication`: https://developer.apple.com/documentation/safariservices/sfsafariapplication
- `SFSafariApplication.openWindow(with:)`: https://developer.apple.com/documentation/safariservices/sfsafariapplication/openwindow%28with%3Acompletionhandler%3A%29
- `SFSafariApplication.dispatchMessage`: https://developer.apple.com/documentation/safariservices/sfsafariapplication/dispatchmessage%28withname%3Atoextensionwithidentifier%3Auserinfo%3Acompletionhandler%3A%29
- `SFSafariExtensionManager.getStateOfSafariExtension`: https://developer.apple.com/documentation/safariservices/sfsafariextensionmanager/getstateofsafariextension%28withidentifier%3Acompletionhandler%3A%29
- `SFSafariExtensionState`: https://developer.apple.com/documentation/safariservices/sfsafariextensionstate
- `SFSafariWindow`: https://developer.apple.com/documentation/safariservices/sfsafariwindow

## Supported Control Model

SafariServices provides specific proxy objects and extension-management APIs. Treat those APIs as scoped capabilities, not as general ownership of Safari.

- `SFSafariExtensionManager` answers whether an embedded Safari app or web extension is enabled.
- `SFSafariApplication.openWindow(with:)` can open an HTTP or HTTPS URL in a new Safari window.
- `SFSafariApplication.dispatchMessage(withName:toExtensionWithIdentifier:userInfo:)` sends a message from the containing app to its Safari App Extension and may launch the user's default Safari variant to deliver it.
- `SFSafariWindow`, `SFSafariTab`, and `SFSafariPage` are proxy objects used in Safari App Extension workflows for supported window, tab, page, and toolbar interactions.

## Control Boundary

- If the user wants to open a page, use `NSWorkspace` or `SFSafariApplication.openWindow(with:)` depending on whether the target is just opening a URL or coordinating with a Safari App Extension.
- If the user wants to read or modify page content, use a Safari Web Extension content script or a Safari App Extension injected script, depending on the chosen extension model.
- If the user wants to send native app state into Safari, use the documented messaging model for the chosen extension shape.
- If the user wants to enumerate or manipulate unrelated user Safari state, stop and check whether SafariServices exposes that exact behavior. If it does not, discuss external automation explicitly.

## External Automation Fallbacks

External automation includes AppleScript, Shortcuts, UI automation, accessibility automation, and app-specific scripting. Use it only when the user explicitly wants behavior outside documented SafariServices or extension capabilities.

Before implementation, state:

- the permission prompt or accessibility automation requirement
- whether the action is visible to the user
- which Safari or macOS version behavior is assumed
- what breaks if Safari is closed, has multiple profiles, uses Safari Technology Preview, or changes UI labels
- how the app will report failure in a human-readable way
