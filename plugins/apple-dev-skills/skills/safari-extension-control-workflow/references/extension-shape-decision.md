# Safari Extension Shape Decision

## Documented Anchors

- Apple Safari Services: https://developer.apple.com/documentation/safariservices/
- Safari Web Extensions: https://developer.apple.com/documentation/SafariServices/safari-web-extensions
- Creating a Safari Web Extension: https://developer.apple.com/documentation/safariservices/creating-a-safari-web-extension
- Safari App Extensions: https://developer.apple.com/documentation/safariservices/safari_app_extensions
- Safari app extension Info.plist keys: https://developer.apple.com/documentation/safariservices/using-safari-app-extension-default-keys
- Content blockers: https://developer.apple.com/documentation/safariservices/creating-a-content-blocker

## Decision Rules

- Choose a Safari Web Extension when the core behavior is browser-extension-shaped: JavaScript, HTML, CSS, a manifest, browser extension APIs, content scripts, background scripts, toolbar UI, permissions, and portability to or from Chrome, Firefox, or Edge extension formats.
- Choose a Safari App Extension when the feature is macOS-only and needs native SafariServices app-extension objects such as `SFSafariExtensionHandler`, `SFSafariApplication`, `SFSafariWindow`, `SFSafariTab`, `SFSafariPage`, or toolbar-item callbacks.
- Choose a content blocker when the feature can be expressed as declarative blocking rules. Do not upgrade a content blocker to a Web Extension or App Extension unless the feature needs messaging, content scripts, arbitrary JavaScript, app data, or native UI.
- Choose `ASWebAuthenticationSession` when the user needs browser-backed authentication or SSO. Do not frame authentication as "controlling Safari" unless Safari extension behavior is actually involved.
- Choose `SFSafariViewController` only for supported in-app Safari-style browsing contexts on platforms where Apple documents it. For macOS app control of the Safari app, use documented Safari extension or automation surfaces instead.

## Platform Boundaries

- Safari Web Extensions are available beyond macOS, including iOS and visionOS, and can also be used in Mac web apps on supported macOS versions.
- Safari App Extensions are macOS-only.
- Safari content blockers can be useful on iOS and macOS, but they are intentionally narrower than Web Extensions or App Extensions.
- When a user asks for one codebase across Safari and other browsers, bias toward Safari Web Extensions unless a native macOS-only requirement is central.
- When a user asks for tight integration with a Mac app and Safari windows or pages, evaluate Safari App Extensions first, then decide whether a Web Extension with native messaging is enough.

## Anti-Patterns

- Do not recommend Safari App Extensions only because the containing app is native. If the browser-facing behavior is portable WebExtension work, use the Web Extension model.
- Do not recommend a Safari Web Extension when the feature requires native Safari App Extension callback objects that WebExtension APIs do not expose.
- Do not treat content blockers as a privacy-invasive inspection surface; their strength is declarative matching, not page introspection.
- Do not assume the containing app can silently enable an extension. Users manage extension enablement in Safari.
