# DocC Execution Surfaces And Handoffs

- Stay in this skill for content authoring and review; those tasks do not require repository classification.
- Use `swift-package-build-run-workflow` when the requested operation is SwiftPM DocC generation or package build follow-through.
- Use `xcode-build-run-workflow` for `Product > Build Documentation`, `xcodebuild docbuild`, scheme-bound generation, archive export, or Xcode project-integrity follow-through.
- Use `explore-apple-swift-docs` when the request is primarily documentation lookup.
- Apply `../../../shared/execution-surface-routing.md`: co-located Xcode and SwiftPM files are normal and never require an opt-in.

Tutorial-shaped requests remain a light authoring review unless the fuller DocC directive references are consulted.
