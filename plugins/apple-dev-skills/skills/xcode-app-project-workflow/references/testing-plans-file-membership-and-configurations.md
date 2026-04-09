# Testing Plans, File Membership, and Build Configurations

## Swift Testing, XCTest, and XCUITest

- Prefer Swift Testing for modern unit-style test surfaces, including suites, tags, parameterized tests, and direct async coverage.
- Keep XCTest for Apple tooling or dependency constraints that still require it, and keep XCTest-specific helpers scoped to that surface instead of mixing frameworks casually.
- Use XCUITest for UI automation and prefer explicit wait APIs such as `waitForExistence(timeout:)`, `waitForNonExistence(timeout:)`, and related state waits instead of fixed sleeps.

## Test plans

- Version `.xctestplan` files when the project needs repeatable configurations for environment variables, launch arguments, localization, sanitizers, diagnostics, or code coverage.
- Inspect available plans with `xcodebuild -scheme <Scheme> -showTestPlans`.
- Run a specific plan with `xcodebuild -scheme <Scheme> -testPlan <Plan> test`.
- Use configuration filtering such as `-only-test-configuration` and `-skip-test-configuration` when the plan defines multiple named configurations.

## File addition and target membership

- Adding files to a repository directory does not guarantee that Xcode will add them to the project, target, build phases, or bundled resources automatically.
- After filesystem edits, verify that source files, resources, asset catalogs, storyboards, test files, and supporting files all have the intended project and target membership.
- When no safe Xcode-aware mutation tool is available, ask the user to add or reconcile project membership through Xcode instead of guessing.

## Debug and Release

- Use Debug builds for the normal edit-build-run loop.
- Validate Release builds explicitly when optimization, launch behavior, watchdog timing, or packaging can change runtime behavior.
- Treat tagged releases as a signal to build and validate both Debug and Release paths, and when shipping artifacts verify the Release behavior without relying on a debugger attachment.
