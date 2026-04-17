# AGENTS.md

## Swift Package Workflow

- Use `swift build` and `swift test` as the default first-pass validation commands for this package.
- Use `bootstrap-swift-package` when a new Swift package repo still needs to be created from scratch.
- Use `sync-swift-package-guidance` when the repo guidance for this package drifts and needs to be refreshed or merged forward.
- Re-run `sync-swift-package-guidance` after substantial package-workflow or plugin updates so local guidance stays aligned.
- Use `swift-package-build-run-workflow` for manifest, dependency, plugin, resource, Metal-distribution, build, and run work when `Package.swift` is the source of truth.
- Use `swift-package-testing-workflow` for Swift Testing, XCTest holdouts, `.xctestplan`, fixtures, and package test diagnosis.
- Use `scripts/repo-maintenance/validate-all.sh` for local maintainer validation, `scripts/repo-maintenance/sync-shared.sh` for repo-local sync steps, and `scripts/repo-maintenance/release.sh` for releases.
- Treat `scripts/repo-maintenance/config/profile.env` as the installed profile marker for this repo-maintenance toolkit surface, and keep it on the `swift-package` profile for plain package repos.
- Read relevant SwiftPM, Swift, and Apple documentation before proposing package-structure, dependency, manifest, concurrency, or architecture changes.
- Prefer Dash or local Swift docs first, then official Swift or Apple docs when local docs are insufficient.
- Prefer the simplest correct Swift that is easiest to read and reason about.
- Prefer synthesized and framework-provided behavior over extra wrappers and boilerplate.
- Keep data flow straight and dependency direction unidirectional.
- Treat `Package.swift` as the source of truth for package structure, targets, products, and dependencies.
- Prefer `swift package` subcommands for structural package edits before manually editing `Package.swift`.
- Edit `Package.swift` intentionally and keep it readable; agents may modify it when package structure, targets, products, or dependencies need to change, and should try to keep package graph updates consolidated in one change when possible.
- Keep `Package.swift` explicit about its package-wide Swift language mode. On current Swift 6-era manifests, prefer `swiftLanguageModes: [.v6]` as the default declaration and treat `swiftLanguageVersions` as a legacy alias used only when an older manifest surface requires it.
- Avoid adding unnecessary dependency-provenance detail or switching to branch/revision-based requirements unless the user explicitly asks for that level of control.
- Treat `Package.resolved` and similar package-manager outputs as generated files; do not hand-edit them.
- Prefer Swift Testing by default unless an external constraint requires XCTest.
- Use `apple-ui-accessibility-workflow` when the package work crosses into SwiftUI accessibility semantics, Apple UI accessibility review, or UIKit/AppKit accessibility bridge behavior.
- Keep package resources under the owning target tree, declare them intentionally with `Resource.process(...)`, `Resource.copy(...)`, `Resource.embedInCode(...)`, and load them through `Bundle.module`.
- Keep test fixtures as test-target resources instead of relying on the working directory.
- Bundle precompiled Metal artifacts such as `.metallib` files as explicit resources when they ship with the package, and prefer `xcode-build-run-workflow` when shader compilation or Apple-managed Metal toolchain behavior matters.
- Validate both Debug and Release paths when optimization or packaging differences matter, and treat tagged releases as a cue to verify the Release artifact path before publishing.
- Prefer `xcode-build-run-workflow` or `xcode-testing-workflow` only when package work needs Xcode-managed SDK, toolchain, or test behavior.
- Keep runtime UI accessibility verification and XCUITest follow-through in `xcode-testing-workflow` rather than treating package-side testing as a substitute for live UI verification.
