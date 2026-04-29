# AGENTS.md

## Apple / Xcode Project Workflow

- Use `xcode-build-run-workflow` for normal Xcode build, run, diagnostics, preview, file-membership, and guarded mutation work inside this existing project.
- Use `xcode-testing-workflow` when the task is primarily about Swift Testing, XCTest, XCUITest, `.xctestplan`, flaky tests, retries, or test diagnosis.
- Use `apple-ui-accessibility-workflow` when the task is primarily about SwiftUI accessibility semantics, Apple UI accessibility review, accessibility tree shaping, or UIKit/AppKit accessibility bridge behavior.
- Use `sync-xcode-project-guidance` when the repo guidance for this project drifts and needs to be refreshed or merged forward.
- Re-run `sync-xcode-project-guidance` after substantial Xcode-workflow or plugin updates so local guidance stays aligned.
- Use `scripts/repo-maintenance/validate-all.sh` for local maintainer validation, `scripts/repo-maintenance/sync-shared.sh` for repo-local sync steps, and `scripts/repo-maintenance/release.sh --mode standard --version vX.Y.Z` from a feature branch or worktree for protected-main releases.
- Do not run the standard release workflow from `main`; let it validate, bump versions, tag, push the branch and tag, open the release PR, watch CI, address valid PR comments or record out-of-scope concerns in `ROADMAP.md`, merge to protected `main`, fast-forward local `main`, and clean up stale branches.
- Treat `scripts/repo-maintenance/config/profile.env` as the installed `maintain-project-repo` profile marker, and keep it on the `xcode-app` profile for native Apple app repos.
- Read relevant Apple documentation before proposing or making Xcode, SwiftUI, lifecycle, architecture, or build-configuration changes.
- Prefer Dash or local Apple docs first, then official Apple docs when local docs are insufficient.
- Prefer the simplest correct Swift that is easiest to read and reason about.
- Prefer synthesized and framework-provided behavior over extra wrappers and boilerplate.
- For public Swift APIs, treat streamlined, compact, ergonomic call sites as the only acceptable default; prefer optional parameters with explicit default values over additional methods or overloads when the difference is optional behavior on the same operation.
- When a public function, initializer, or method reaches four or more arguments or parameters, strongly prefer a named typed `struct` request, options, or configuration value so call sites stay readable and future additions do not multiply overloads.
- Prefer enums, enum cases with associated values, and narrow typed values over strings, booleans, sentinel values, or parallel parameters whenever the domain has a closed or meaningful set of choices.
- Keep data flow straight and dependency direction unidirectional.
- Treat the `.xcworkspace` or `.xcodeproj` as the source of truth for app integration, schemes, and build settings.
- Prefer Xcode-aware tooling or `xcodebuild` over ad hoc filesystem assumptions when project structure or target membership is involved.
- If this repo is XcodeGen-backed, treat `project.yml`, `project.yaml`, and any included XcodeGen specs as the source of truth for generated targets, schemes, build settings, packages, and file membership.
- For XcodeGen-backed projects, edit the spec set and rerun `xcodegen generate` instead of hand-editing generated `.pbxproj` files.
- After regenerating an XcodeGen project, review both the spec diff and generated `.xcodeproj` diff, then validate the affected scheme with explicit `xcodebuild` commands.
- Prefer Swift Testing for modern unit-style tests, keep XCTest where Apple tooling or dependencies still require it, and use XCUITest with explicit element wait APIs instead of fixed sleeps.
- Keep `.xctestplan` files versioned when the project depends on repeatable test-plan configurations, and inspect or run them explicitly with `xcodebuild -showTestPlans` and `xcodebuild -testPlan ...`.
- Prefer a checked-in repo-root `.swiftformat` file as the Swift formatting source of truth.
- Prefer a pre-commit hook such as `scripts/repo-maintenance/hooks/pre-commit.sample` that formats staged Swift sources and then verifies them with `swiftformat --lint` before commit.
- Treat SwiftLint as an optional complementary signal layer for clarity, safety, and maintainability after SwiftFormat owns formatting shape.
- Treat accessibility semantics and Apple UI accessibility review as a separate concern from UI automation; use `apple-ui-accessibility-workflow` for the semantic side and `xcode-testing-workflow` for runtime verification and XCUITest follow-through.
- When scripts add files on disk, verify project membership, target membership, build phases, and resource inclusion afterward; files existing in the directory tree alone are not enough.
- Validate both Debug and Release paths when behavior can diverge, and treat tagged releases as a cue to build and verify Release artifacts in addition to the everyday Debug flow.
- Never edit `.pbxproj` files directly. If a project-file change is needed and no safe project-aware tool is available, stop and make that change through Xcode instead.
- Validate Xcode-project changes with explicit `xcodebuild` commands when build or test integrity matters.
