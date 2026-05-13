# Safari Extension Shape Decision

## Documented Anchors

- Apple Safari Services: https://developer.apple.com/documentation/safariservices/
- Safari Web Extensions: https://developer.apple.com/documentation/SafariServices/safari-web-extensions
- Creating a Safari Web Extension: https://developer.apple.com/documentation/safariservices/creating-a-safari-web-extension
- Safari App Extensions: https://developer.apple.com/documentation/safariservices/safari_app_extensions
- Safari app extension Info.plist keys: https://developer.apple.com/documentation/safariservices/using-safari-app-extension-default-keys
- Content blockers: https://developer.apple.com/documentation/safariservices/creating-a-content-blocker
- Adding a web development tool to Safari Web Inspector: https://developer.apple.com/documentation/safariservices/adding-a-web-development-tool-to-safari-web-inspector
- Creating Safari Web Inspector extensions: https://developer.apple.com/documentation/safariservices/creating-safari-web-inspector-extensions
- Underpass explanation of Safari extension types: https://underpassapp.com/news/2023-4-24.html

## Decision Rules

- Choose a Safari Web Extension when the core behavior is browser-extension-shaped: JavaScript, HTML, CSS, a manifest, browser extension APIs, content scripts, background scripts, toolbar UI, permissions, and portability to or from Chrome, Firefox, or Edge extension formats.
- Choose a Safari Web Inspector Extension when the user is building a developer-facing Web Inspector tool. Keep this separate from ordinary Web Extensions that affect browsing behavior for end users.
- Choose a Safari App Extension when the feature is macOS-only and needs native SafariServices app-extension objects such as `SFSafariExtensionHandler`, `SFSafariApplication`, `SFSafariWindow`, `SFSafariTab`, `SFSafariPage`, or toolbar-item callbacks.
- Choose a content blocker when the feature can be expressed as declarative blocking rules. Do not upgrade a content blocker to a Web Extension or App Extension unless the feature needs messaging, content scripts, arbitrary JavaScript, app data, or native UI.
- Choose `ASWebAuthenticationSession` when the user needs browser-backed authentication or SSO. Do not frame authentication as "controlling Safari" unless Safari extension behavior is actually involved.
- Choose `SFSafariViewController` only for supported in-app Safari-style browsing contexts on platforms where Apple documents it. For macOS app control of the Safari app, use documented Safari extension or automation surfaces instead.

## Platform Boundaries

- Safari Web Extensions are available beyond macOS, including iOS and visionOS, and can also be used in Mac web apps on supported macOS versions.
- Safari App Extensions are macOS-only.
- Safari content blockers can be useful on iOS and macOS, but they are intentionally narrower than Web Extensions or App Extensions.
- Safari Web Inspector Extensions are Safari Web Extension-based developer tools for Web Inspector. Treat them as inspection, testing, and debugging tools, not as a general page-customization path.
- When a user asks for one codebase across Safari and other browsers, bias toward Safari Web Extensions unless a native macOS-only requirement is central.
- When a user asks for tight integration with a Mac app and Safari windows or pages, evaluate Safari App Extensions first, then decide whether a Web Extension with native messaging is enough.

## Practical Differences

- Safari Web Extensions are the best fit for cross-browser-style extension code, but they still need Apple packaging and distribution. Do not imply they can ship as loose extension archives to Safari users.
- Safari App Extensions can use JavaScript and style sheets, but their SafariServices API is different from the cross-browser WebExtensions API. Code sharing with Chrome, Firefox, or Edge is usually harder.
- Safari App Extensions can provide native Mac UI inside Safari, which is a real reason to choose them when the feature is Mac-only.
- Content blockers have no JavaScript execution path and do not receive page-content or URL-load telemetry from Safari. Their privacy posture is part of the feature, not an implementation inconvenience.
- On Mac, extension types can look similar in Safari Settings. Use capability clues instead of user-facing labels alone: content blockers have no page-permission prompts, Web Extensions use website access permissions, App Extensions can expose native Mac UI, and obsolete `.safariextz` extensions should not be considered for new work.
- Safari 17 and later brought Safari App Extensions into the same per-site permission model family as Safari Web Extensions. Do not assume older "enabled means all websites" behavior when giving current guidance.

## Anti-Patterns

- Do not recommend Safari App Extensions only because the containing app is native. If the browser-facing behavior is portable WebExtension work, use the Web Extension model.
- Do not recommend Safari Web Inspector Extensions for end-user customization, content blocking, or normal toolbar extension features.
- Do not recommend a Safari Web Extension when the feature requires native Safari App Extension callback objects that WebExtension APIs do not expose.
- Do not treat content blockers as a privacy-invasive inspection surface; their strength is declarative matching, not page introspection.
- Do not assume the containing app can silently enable an extension. Users manage extension enablement in Safari.
- Do not propose `.safariextz` for new work. That format is obsolete.
