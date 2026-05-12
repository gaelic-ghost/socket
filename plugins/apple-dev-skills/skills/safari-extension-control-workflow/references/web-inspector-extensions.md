# Safari Web Inspector Extensions

## Documented Anchors

- Adding a web development tool to Safari Web Inspector: https://developer.apple.com/documentation/safariservices/adding-a-web-development-tool-to-safari-web-inspector
- Creating Safari Web Inspector extensions: https://developer.apple.com/documentation/safariservices/creating-safari-web-inspector-extensions
- WWDC22 Create Safari Web Inspector Extensions: https://developer.apple.com/videos/play/wwdc2022/10100/
- WWDC22 What's new in Safari and WebKit: https://developer.apple.com/videos/play/wwdc2022/10048/

## When To Choose This Path

Choose a Safari Web Inspector Extension when the product is a developer tools feature that belongs inside Safari Web Inspector. This is different from an ordinary Safari Web Extension that customizes web browsing for end users.

Good fits include:

- inspecting page state with custom developer UI
- adding debugging or analysis panels to Web Inspector
- porting an existing browser developer-tools extension to Safari
- augmenting Safari's built-in inspecting, testing, and debugging tools

Poor fits include:

- changing normal user-facing webpage behavior
- blocking ads or trackers
- adding an end-user toolbar popup
- automating Safari windows or tabs from a native app
- replacing Xcode, system logs, or native app debugging for the containing app

## Implementation Shape

- Treat the Web Inspector tool as part of a Safari Web Extension project.
- Keep the developer-tool UI and inspected-page communication separate from ordinary content scripts or toolbar behavior.
- Verify whether the tool depends on browser developer-tools APIs that Safari supports before assuming a Chrome or Firefox developer-tools extension will port cleanly.
- Keep any inspected-page data handling privacy-aware. Developer tools can expose sensitive page data during debugging, so logs and persisted diagnostics should be deliberate.

## Validation

- Enable Safari developer features and unsigned extension support when using Apple's sample or local development flow.
- Confirm the Web Inspector panel appears in Safari Web Inspector before debugging the inspected-page integration.
- Validate inspected-page messaging separately from the containing app or native messaging behavior.
- Use `xcode-build-run-workflow` when Xcode target setup, signing, or extension packaging is the blocker.
- Use `xcode-testing-workflow` when the work needs repeatable verification around Web Inspector UI availability or inspected-page behavior.
