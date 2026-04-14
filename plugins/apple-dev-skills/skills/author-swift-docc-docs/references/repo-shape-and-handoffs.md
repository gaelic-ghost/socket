# Repo Shape And Handoffs

## Repo Shapes

- `swift-package`
  - likely signals: `Package.swift`, package-local `.docc` catalogs, SwiftPM-owned source layout
- `xcode-app-framework`
  - likely signals: `.xcodeproj`, `.xcworkspace`, target-owned `.docc` catalogs, Xcode-managed app or framework layout

## Handoff Rules

- Use `explore-apple-swift-docs` when the request is mainly documentation lookup.
- Use `swift-package-build-run-workflow` when a Swift package repo needs generation, export, or build-oriented DocC follow-through.
- Use `xcode-build-run-workflow` when an Xcode app or framework repo needs generation, export, `Product > Build Documentation`, `xcodebuild docbuild`, or project-integrity follow-through.

## Phase-One Tutorial Rule

- Recognize tutorial-shaped requests.
- Keep tutorial handling shallow in phase one.
- Route directive-deep or interactive-tutorial mechanics to the fuller DocC references unless a later skill revision intentionally deepens that surface.
