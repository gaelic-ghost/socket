---
name: safari-extension-control-workflow
description: Guide macOS Safari integration decisions across Safari Web Extensions, Safari Web Inspector Extensions, Safari App Extensions, SafariServices APIs, content blockers, extension messaging, and app-to-Safari control surfaces. Use when the user wants a Mac app to extend, message, open, inspect, debug, or coordinate with Safari without confusing WebExtension, Web Inspector, native extension, content blocker, authentication, or AppleScript-style automation paths.
---

# Safari Extension Control Workflow

## SwiftData And SwiftUI Rule

When a task combines SwiftData with SwiftUI, keep SwiftData directly coupled to SwiftUI through Apple's data-driven path: `modelContainer`, environment `modelContext`, `@Query`, SwiftData model objects, and bindings. Do not add repositories, stores, service layers, DTO mirrors, view-model caches, wrapper objects, or other abstraction layers between SwiftData and SwiftUI. If this skill is not the right owner for SwiftData-backed SwiftUI work, hand off to `apple-dev-skills:swiftui-app-architecture-workflow` instead of inventing an intermediate data layer.

## Purpose

Guide Safari integration work for macOS apps, with enough platform awareness to choose the right Safari extension or SafariServices surface before implementation starts.

This skill owns the decision between Safari Web Extensions, Safari Web Inspector Extensions, Safari App Extensions, content blockers, SafariServices APIs, app-to-extension messaging, and limited external automation paths. It is not a generic browser-extension guide and it is not a replacement for `xcode-build-run-workflow` or `xcode-testing-workflow`.

## When To Use

- Use this skill when the user wants a macOS app to extend Safari, communicate with Safari content, or coordinate native app state with a Safari extension.
- Use this skill when choosing between a Safari Web Extension, Safari Web Inspector Extension, Safari App Extension, Safari content blocker, `SFSafariApplication`, `SFSafariExtensionManager`, `SFSafariViewController`, `ASWebAuthenticationSession`, AppleScript, Shortcuts, or URL-opening behavior.
- Use this skill when the work involves WebExtension manifests, Web Inspector developer-tool panels, native messaging, app groups, injected scripts, toolbar items, content blockers, Safari profiles, temporary extension loading, unsigned extension testing, or App Store distribution.
- Use this skill when a user says they want to "control Safari" from a Mac app and the first job is distinguishing supported SafariServices control from broader GUI or scripting automation.
- Recommend `explore-apple-swift-docs` when the user primarily needs direct Apple documentation lookup rather than integration-shape guidance.
- Recommend `xcode-build-run-workflow` when the next step is target setup, build settings, entitlements, signing, file membership, running the containing app, or guarded Xcode project mutation.
- Recommend `xcode-testing-workflow` when the next step is repeatable XCTest, XCUITest, extension-state checks, or test-plan work.
- Recommend `swiftui-app-architecture-workflow` when the Safari work is settled and the remaining question is native app scene, command, focus, or settings structure.

## Single-Path Workflow

1. Classify the Safari integration request:
   - WebExtension-compatible browser feature
   - Web Inspector developer-tool feature
   - macOS-only Safari App Extension feature
   - declarative content blocking
   - containing app to extension messaging
   - extension to webpage or injected-script messaging
   - app-initiated Safari window, tab, or extension-state operation
   - authentication, reading list, associated-domain, or in-app Safari content
   - external automation outside SafariServices
2. Apply the Apple docs gate before recommending shape:
   - read the relevant SafariServices, Safari Web Extension, Safari App Extension, App Extension, or AuthenticationServices documentation first
   - state the documented behavior or platform limit being relied on
   - if Apple docs and the current code disagree, stop and surface that conflict
   - if no relevant Apple documentation can be found, say that explicitly before proceeding
3. Choose the supported integration surface:
   - Safari Web Extension for cross-browser-style JavaScript, HTML, CSS, manifest, browser APIs, iOS, visionOS, Mac web apps, or extension portability
   - Safari Web Inspector Extension for developer-facing tools that extend Safari Web Inspector rather than user-facing browsing behavior
   - Safari App Extension for macOS-only native extension behavior that uses SafariServices classes and can share data with a containing Mac app
   - Content blocker when the feature is declarative blocking and does not need to inspect page content or run arbitrary page logic
   - `SFSafariApplication` and related Safari App Extension proxies only for supported Safari extension interactions such as opening windows, sending app-to-extension messages, or working with Safari windows, tabs, pages, and toolbar items from the extension context
   - `SFSafariExtensionManager` for extension state checks before UI or feature claims
   - `ASWebAuthenticationSession` for SSO-style browser authentication rather than embedding or automating Safari
   - external automation only when the user explicitly needs behavior outside SafariServices and has accepted automation, permissions, fragility, and user-visible side effects
4. Plan data flow and permissions:
   - keep app, extension, and JavaScript contexts explicit
   - use app groups for shared app and extension data when Apple requires a shared container
   - keep message names typed or centralized in code and document payload shapes
   - model profile-aware behavior when Safari profile identifiers are exposed
   - avoid logging sensitive URLs, cookies, page text, tokens, or browsing history
5. Plan validation:
   - verify extension visibility and enabled state before debugging feature logic
   - test unsigned-extension setup separately from signed distribution setup
   - validate the containing app install path, Safari Settings state, profile state, and Web Inspector or system logs when relevant
   - run Xcode build, signing, entitlements, target membership, or UI validation through the Xcode skills
6. Return one recommendation path with:
   - chosen Safari surface
   - documented Apple behavior relied on
   - native app, extension, JavaScript, and Safari ownership boundaries
   - messaging and shared-data plan
   - validation plan
   - one handoff if the work should move into docs lookup, Xcode execution, testing, SwiftUI architecture, or external automation

## Inputs

- `request`: optional free-text Safari integration request.
- `platform_context`: optional emphasis such as `macos`, `ios`, `visionos`, `mac-web-app`, or `mixed-apple`.
- `extension_shape`: optional explicit shape such as `web-extension`, `app-extension`, `content-blocker`, `unknown`, or `no-extension`.
- `control_goal`: optional explicit goal such as `open-url`, `open-window`, `send-message`, `read-page-state`, `modify-page`, `block-content`, `authenticate`, or `automate-ui`.
- Defaults:
  - docs-first guidance always applies
  - prefer Safari Web Extensions for portable browser-extension behavior
  - prefer Safari Web Inspector Extensions only for developer tools that live inside Safari Web Inspector
  - prefer Safari App Extensions only when the macOS-only native extension model is the real requirement
  - prefer SafariServices and AuthenticationServices over GUI scripting when the documented API surface covers the job

## Outputs

- `status`
  - `success`: the request belongs to this workflow and a Safari integration recommendation is ready
  - `handoff`: the request belongs to another Apple Dev skill after Safari-aware classification
  - `blocked`: the request lacks enough context or relies on unsupported Safari behavior
- `path_type`
  - `primary`: the recommendation uses a documented SafariServices, Web Extension, Web Inspector Extension, App Extension, content blocker, or authentication path
  - `fallback`: the recommendation depends on external automation because the documented Safari API surface does not cover the requested behavior
- `output`
  - resolved Safari integration class
  - chosen Safari surface
  - documented Apple behavior relied on
  - app, extension, JavaScript, and Safari ownership boundaries
  - messaging and shared-data plan
  - validation plan
  - recommended skill or automation handoff when needed

## Guards and Stop Conditions

- Do not claim a Mac app can freely inspect or control arbitrary Safari windows, tabs, cookies, page content, or user browsing state unless the documented SafariServices, extension, or automation surface actually supports it.
- Do not use AppleScript, Shortcuts, UI automation, accessibility automation, or browser GUI scripting as the first recommendation when a supported SafariServices or extension path exists.
- Do not collapse Safari Web Extension native messaging, Safari App Extension injected-script messaging, and app-group shared storage into one vague "bridge"; name the exact contexts and transport.
- Do not recommend a Safari App Extension for portable WebExtension behavior unless a macOS-only native extension requirement is explicit.
- Do not recommend a Safari Web Extension for arbitrary native control of Safari outside the browser-extension permission model.
- Do not recommend a Safari Web Inspector Extension for ordinary end-user browser customization; Web Inspector extensions are developer tools.
- Stop with `blocked` when the feature requires user-private Safari data or privileged browser control that Apple does not expose through the documented APIs and the user has not explicitly opted into external automation.

## Fallbacks and Handoffs

- Recommend `explore-apple-swift-docs` when the real need is direct Apple docs lookup for SafariServices, Web Extensions, App Extensions, Web Inspector Extensions, or AuthenticationServices.
- Recommend `xcode-build-run-workflow` when the next step is creating targets, adding entitlements, wiring app groups, signing, running the containing app, or debugging build/install state.
- Recommend `xcode-testing-workflow` when the next step is repeatable test design or extension-state verification.
- Recommend `swiftui-app-architecture-workflow` when Safari integration shape is settled and the native app shell needs scene, command, focus, settings, or menu ownership guidance.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Xcode-project policy for a repo that will own the containing app and extension targets.
- Treat external automation as a conscious fallback, not the default. When it is requested, state the user-visible permissions, fragility, and Safari-version sensitivity before implementation.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` exists to preserve the repo-wide customization-file contract, but the first version of this skill defines no runtime-enforced knobs.

Keep the first release focused on the documented Safari surface decision. If future iterations add deterministic checks for manifests, entitlements, or app-group configuration, document the knobs before runtime behavior depends on them.

## References

### Workflow References

- `references/extension-shape-decision.md`
- `references/web-inspector-extensions.md`
- `references/safari-services-control-surfaces.md`
- `references/messaging-shared-data-and-permissions.md`
- `references/testing-debugging-and-distribution.md`
- `references/customization-flow.md`

### Support References

- Recommend `explore-apple-swift-docs` when the user needs current Apple docs before a Safari implementation choice.
- Recommend `xcode-build-run-workflow` when the user needs target, signing, entitlements, build, run, or install follow-through.
- Recommend `xcode-testing-workflow` when the user needs repeatable extension-state or Safari UI verification.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Xcode project guidance for containing-app and extension-target work.

### Script Inventory

- `scripts/customization_config.py`
