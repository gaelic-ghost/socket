# Testing Plans, File Membership, and Build Configurations

## Swift Testing, XCTest, and XCUITest

- Prefer Swift Testing for modern unit-style test surfaces, including suites, tags, parameterized tests, and direct async coverage.
- Keep XCTest for Apple tooling or dependency constraints that still require it, and keep XCTest-specific helpers scoped to that surface instead of mixing frameworks casually.
- Use XCUITest for UI automation and prefer explicit wait APIs such as `waitForExistence(timeout:)`, `waitForNonExistence(timeout:)`, and related state waits instead of fixed sleeps.
- Keep deeper UI automation mechanics in `references/xcuitest-and-xcuiautomation.md` instead of overloading this summary file.

## Test scheduling and live TTS model pressure

- Prefer normal Xcode and XCTest parallel execution for ordinary Swift Testing, XCTest, and XCUITest runs when the project, scheme, destination, and test plan support it. Do not serialize regular tests just because they use Swift, XCTest, async tests, UI automation, or `.xctestplan` matrices.
- Treat tests that load large local AI or ML models, especially models over 500 million parameters, as heavy system-resource tests. Run those tests sequentially, one at a time, and do not run them concurrently with other build, test, simulator, or model-loading work.
- Before starting a heavy model-loading test run on Gale's machine, call `unload_models` on the live TTS service so routine speech output is not competing for memory and accelerator resources.
- After the heavy model-loading test run ends, call `reload_models` on the live TTS service, even when the test run fails or is interrupted.
- If `unload_models` or `reload_models` is unavailable, blocked, or fails, report that explicitly before continuing with or claiming completion of the heavy test run.

## Test plans

- Version `.xctestplan` files when the project needs repeatable configurations for environment variables, launch arguments, localization, sanitizers, diagnostics, or code coverage.
- Inspect available plans with `xcodebuild -scheme <Scheme> -showTestPlans`.
- Run a specific plan with `xcodebuild -scheme <Scheme> -testPlan <Plan> test`.
- Use configuration filtering such as `-only-test-configuration` and `-skip-test-configuration` when the plan defines multiple named configurations.
- Keep the richer `.xctestplan` decision model in `references/xctestplan-configurations-and-matrix.md`.

## Accessibility verification

- Runtime accessibility verification belongs here when the next honest step is XCUITest, simulator or device follow-through, screenshots, attachments, or plan-driven matrix coverage.
- Accessibility semantics and implementation review belong to `apple-ui-accessibility-workflow`.
- Keep the runtime verification details in `references/ui-accessibility-verification.md`.

## File addition and target membership

- Adding files to a repository directory does not guarantee that Xcode will add them to the project, target, build phases, or bundled resources automatically.
- After filesystem edits, verify that source files, resources, asset catalogs, storyboards, test files, and supporting files all have the intended project and target membership.
- When no safe Xcode-aware mutation tool is available, ask the user to add or reconcile project membership through Xcode instead of guessing.

## Debug and Release

- Use Debug builds for the normal edit-build-run loop.
- Validate Release builds explicitly when optimization, launch behavior, watchdog timing, or packaging can change runtime behavior.
- Treat tagged releases as a signal to build and validate both Debug and Release paths, and when shipping artifacts verify the Release behavior without relying on a debugger attachment.
