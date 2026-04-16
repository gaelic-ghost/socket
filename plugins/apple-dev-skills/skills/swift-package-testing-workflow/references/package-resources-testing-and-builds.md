# Package Resources, Testing, and Build Configurations

## Resources

- Keep package resources under the owning target tree, commonly `Sources/<TargetName>/Resources` or `Tests/<TargetName>Tests/Resources`.
- Use `Resource.process(...)` when platform-aware processing or optimization is desired.
- Use `Resource.copy(...)` when the original bytes or directory layout must survive exactly as authored.
- Use `Resource.embedInCode(...)` when embedding data directly into generated code is the right tradeoff for the package surface.
- Use `exclude` intentionally when files live under a target directory but should not be bundled.
- Load bundled resources through `Bundle.module` and prefer typed wrappers only when they make call sites clearer.

## Metal and Apple-managed build assets

- Precompiled Metal artifacts such as `.metallib` files can be distributed as package resources and loaded from `Bundle.module`.
- Prefer `.copy(...)` for `.metallib` and similar precompiled binary assets when exact distribution matters.
- If the work requires compiling Metal shaders, validating Apple-platform bundle integration, or confirming the active Apple-managed Metal toolchain, hand off to `xcode-build-run-workflow`.
- In those cases, inspect the active developer directory and toolchain first, then validate with package-oriented `xcodebuild` commands instead of assuming plain `swift build` is sufficient.

## Swift Testing, XCTest, and test plans

- Prefer Swift Testing for new package tests, including `@Test`, suites, tags, and parameterized coverage.
- Prefer direct async tests in Swift Testing, and use `confirmation(...)` for event-driven asynchronous behavior instead of fixed sleeps.
- Keep XCTest only when a dependency, legacy test surface, or Apple tooling constraint still requires it.
- When package-facing Xcode integration uses `.xctestplan` files, keep them versioned and exercise them explicitly with `xcodebuild -showTestPlans` and `xcodebuild -testPlan ...`.
- Keep UI automation, runtime accessibility verification, and deeper Xcode-native `.xctestplan` matrix work in `xcode-testing-workflow`.

## Accessibility-related test boundaries

- Package-side tests can validate semantic formatting, model-derived accessible strings, or other non-UI logic that feeds accessibility behavior.
- Do not pretend package tests replace runtime UI accessibility verification.
- Hand off to `apple-ui-accessibility-workflow` when the real question is semantic accessibility design, and hand off to `xcode-testing-workflow` when the real question is runtime UI verification.

## Debug and Release

- Use `swift build` and `swift test` as the normal first-pass validation path.
- Use `xcodebuild` when schemes, destinations, configurations, test plans, or Apple-managed SDK and toolchain behavior matter.
- Validate Release builds intentionally when optimization or packaging can change behavior.
- Treat tagged releases as a cue to verify both the everyday Debug path and the Release artifact path before publishing.
