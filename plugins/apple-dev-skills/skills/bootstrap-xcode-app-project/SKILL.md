---
name: bootstrap-xcode-app-project
description: Bootstrap a new native Apple app project for macOS, iOS, or iPadOS when the user wants to start, begin, create, or bootstrap an Xcode app project. Use for new SwiftUI-first app repositories on macOS, with optional XcodeGen generation preference and repo-baseline setup guidance. Do not use for plain Swift packages, libraries, or tools that are not native Apple apps.
---

# Bootstrap Xcode App Project

## Purpose

Create a new native Apple app repository from nothing to a usable baseline on disk. The first implementation prioritizes a deterministic `XcodeGen` path for SwiftUI app projects and a guarded planning path for the standard Xcode-created-project flow. `scripts/run_workflow.py` is the runtime entrypoint, and `scripts/bootstrap_xcode_app_project.py` is the current implementation core for XcodeGen-backed scaffold creation plus `maintain-project-repo` installation with the `xcode-app` profile.

## Companion Plugin Requirement

This skill can be discovered from a standalone `apple-dev-skills` install, but its mutating bootstrap path installs repo-maintenance files through the companion [`productivity-skills`](https://github.com/gaelic-ghost/productivity-skills) plugin. If the companion `maintain-project-repo` runner is missing, tell the user to install `productivity-skills` alongside `apple-dev-skills`, or add the [`socket`](https://github.com/gaelic-ghost/socket) marketplace with `codex plugin marketplace add gaelic-ghost/socket` and then install or enable both `apple-dev-skills` and `productivity-skills` from the Socket catalog.

## When To Use

- Use this skill when the user wants to start, begin, create, or bootstrap one new macOS, iOS, or iPadOS app project on macOS.
- Use this skill when the user explicitly asks for a new Xcode app, a native Apple app, or a new SwiftUI app repository.
- Use this skill when the user wants a reproducible app-project generator flow and prefers `XcodeGen`.
- Use this skill when a brand-new app repo should also get baseline repo guidance such as `AGENTS.md`.
- Do not use this skill for ordinary collaboration inside an existing Xcode project.
- Do not use this skill to bootstrap an Apps/Packages workspace with more than one app project; use `bootstrap-xcode-workspace` first and let it route each child app here.
- Do not use this skill for plain Swift packages, libraries, or tools that are not native Apple apps.
- Recommend `bootstrap-swift-package` when the user wants a regular SwiftPM package instead of a native Apple app.
- Recommend `xcode-build-run-workflow` when the project already exists and the task is execution, diagnostics, docs lookup, mutation, build, run, or preview work inside that existing project.
- Recommend `xcode-testing-workflow` when the project already exists and the task is primarily about Swift Testing, XCTest, XCUITest, `.xctestplan`, or test diagnosis.

## Single-Path Workflow

1. Collect the required inputs:
   - `name`
   - `destination`
   - `platform`
   - `ui_stack`
   - `project_generator`
   - optional `bundle_identifier`
   - optional `org_identifier`
   - optional `skip_validation`
   - optional `dry_run`
2. Classify the request as a native Apple app bootstrap request before continuing:
   - continue only for `project_kind=app`
   - stop if the request is actually a Swift package, library, or tool bootstrap
3. Apply the Apple docs gate before recommending project structure or implementation guidance:
   - read the relevant Apple documentation first
   - use Xcode MCP `DocumentationSearch` first for Apple-owned SDK, framework, lifecycle, and Xcode project-creation behavior
   - use the Dash.app MCP second when its installed docsets cover the question; use Dash HTTP only when that MCP is unavailable or incomplete
   - use checked-out source, generated DocC, GitHub/source repositories, release notes, and readable online documentation only after those local MCP paths; generic no-JS web search/open results, snippets, metadata shells, or bare URLs are not enough
   - state the documented behavior being relied on before design or implementation guidance
   - current documented anchors for this workflow include:
     - Apple's Xcode project-creation guidance: [Creating an Xcode project for an app](https://developer.apple.com/documentation/xcode/creating_an_xcode_project_for_an_app)
     - SwiftUI app lifecycle guidance through the `App` protocol: [App](https://developer.apple.com/documentation/swiftui/app)
     - scene composition guidance through `Scene` and `WindowGroup`: [Scene](https://developer.apple.com/documentation/swiftui/scene) and [WindowGroup](https://developer.apple.com/documentation/swiftui/windowgroup)
   - if the docs and the current code or planned scaffold conflict, stop and report that conflict
   - if no relevant Apple docs can be found, say that explicitly before proceeding
4. Apply the shared Swift policy before giving implementation guidance:
   - apply the detailed local policy in `references/snippets/apple-xcode-project-core.md`
   - preserve its simplicity-first, shape-preserving, and anti-ceremony Swift guidance
5. Run `scripts/run_workflow.py` to normalize inputs, load customization state, and select the supported bootstrap path.
6. Resolve the generator path:
   - prefer `xcodegen` by default for new app projects unless the user explicitly prefers the standard Xcode project-creation flow
   - use `xcode` only when the user explicitly prefers the standard Xcode project-creation flow
   - treat `ask` as a legacy explicit-blocking value only when the user or customization state supplies it intentionally
7. Create the project:
   - for `xcodegen`, let `scripts/bootstrap_xcode_app_project.py` generate the repo scaffold from `templates/xcodegen/swiftui-app/`, including `project.yml`, checked-in `.xcconfig` files, source files, tests, and `AGENTS.md`, then run `xcodegen generate`
   - create the standard top-level Xcode app layout: `Sources/`, `Tests/`, `Shared/`, `Extensions/`, `Configurations/`, `Scripts/`, and `Packages/`
   - create `Sources/Resources/Localizable.xcstrings` for every app target by default; the generated XcodeGen app target owns the broad synced `Sources` root, so the catalog is a tracked project resource without a separate source entry
   - keep app-owned implementation/resources/support under `Sources/`, tests under `Tests/`, reusable app/extension source under `Shared/`, extension target roots under `Extensions/`, `.xcconfig` layers under `Configurations/`, project-local automation under `Scripts/`, and justified local Swift package boundaries under `Packages/`
   - inside `Sources/`, create the strict app structure: `Views/Shared`, `Views/macOS`, `Views/iOS`, `Models`, `Services/Consumed`, `Services/Internal`, and `Services/Provided`
   - require an explicit `--file-prefix` containing three uppercase letters after offering reasonable initials-based suggestions
   - create `GEAApp.swift` as the lifecycle entry and `GEA.swift` as the application runtime/domain value; do not generate an umbrella `GEAAppService.swift`
   - create prefixed, self-contained SwiftUI views such as `GEAContentView.swift`, using component-local `@State` and `@Observable` state only when direct state is not sufficient; add a concrete feature service only when the new app has a real capability that needs one
   - prefix every project-owned Swift file except `Package.swift`, externally generated Swift, and vendored third-party Swift; never generate `+` filenames
   - install `.codex/environments/xcode-project.toml` from `templates/codex-local-environments/xcode-project.toml` and replace the scheme placeholder with the generated app target name
   - keep the generated `project.yml` aligned with the current XcodeGen project spec concepts: project `options`, `configs`, `configFiles`, targets, sources, schemes, packages, project references, test-plan references, and `minimumXcodeGenVersion`; when this app is opened from a workspace, set `options.schemePathPrefix: "../"` in the owning spec
   - keep the generated `minimumXcodeGenVersion` on the recent validated baseline declared by the templates; when the baseline is raised, update the templates, docs, and tests together
   - use exactly one top-level `Sources` entry for the app target, exactly one top-level `Shared` entry for shared app/extension source, and exactly one top-level `Tests` entry for the test target when the generated project format is Xcode 16 or newer; prefer `type: syncedFolder` on those broad roots, and use the same broad roots with explicit `includes` and `excludes` as the fallback when synchronized folders are not appropriate
   - never split ordinary generated app project paths into separate XcodeGen source entries such as `Sources/App`, `Sources/Resources`, `Sources/Support`, feature subfolders, or `Tests/<AppName>Tests`; extension targets may use one `Extensions/<ExtensionName>` entry per extension target
   - create exactly one app lifecycle entry point for the app target; do not create alternate `@main` app types, duplicate `main.swift` files, target-specific app entry files, or parallel app structs for variants; keep platform or configuration differences inside the single entry point with Swift conditional compilation or runtime conditionals
   - keep nontrivial build settings in external `.xcconfig` files by default, using shared, target-level, and per-configuration layers wired through the XcodeGen spec instead of duplicating settings inline
   - install a checked-in external app entitlement plist and wire it through `CODE_SIGN_ENTITLEMENTS` in the app `.xcconfig` so capability changes have a real tracked file owner instead of living only in generated project state
   - for `xcode`, use a guarded guidance path for now instead of pretending the repo supports full GUI automation already
8. Validate the scaffold:
   - verify the expected app files exist
   - verify the standard top-level directories exist
   - verify the strict app source directories exist under `Sources/Views`, `Sources/Models`, and `Sources/Services`
   - verify the app entry point, runtime/domain value, and shared content view use the strict naming contract without a generated ViewModel or umbrella app service
   - verify `.swiftformat` exists
   - verify `Sources/Resources/Localizable.xcstrings` exists and that the generated target's broad `Sources` root includes it as a resource
   - verify `AGENTS.md` exists when enabled
   - verify `.codex/environments/xcode-project.toml` exists and uses the generated app target name for Codex GUI actions
   - verify generated guidance says tracked `.pbxproj` changes must be reviewed, staged, and committed before push, merge, release, or cleanup
   - verify generated guidance says Xcode Build Settings UI edits may need to be moved from generated project overrides back into the owning `.xcconfig`
   - verify `Scripts/repo-maintenance/hooks/pre-commit.sample` exists
   - verify `Scripts/repo-maintenance/validate-all.sh` and `Scripts/repo-maintenance/release.sh` exist
   - verify branch protection, when enabled, requires the GitHub Actions check context `validate` rather than `Validate Repo Maintenance / validate`
   - when a GitHub remote is created or already exists, route repository
     settings audit or mutation through `productivity-skills:maintain-github-repository`
     instead of embedding a separate Xcode-specific baseline
   - if validation is enabled, verify project generation and basic project introspection succeeded
9. Hand off existing-project work cleanly:
   - recommend `sync-xcode-project-guidance` when the repo guidance should be refreshed or merged after creation
   - recommend `xcode-build-run-workflow` for normal Xcode build or run collaboration after bootstrap and guidance sync
   - recommend `xcode-testing-workflow` for test-focused collaboration after bootstrap and guidance sync

## Inputs

- `name`: required; app project name and repo directory name.
- `destination`: parent directory for the new app repo.
- `project_kind`: defaults to `app`; any non-app value blocks the workflow.
- `platform`: `macos`, `ios`, or `ipados`.
- `ui_stack`: `swiftui`, `uikit`, or `appkit`.
- `project_generator`: `ask`, `xcode`, or `xcodegen`.
- `bundle_identifier`: optional explicit bundle identifier.
- `org_identifier`: optional organization identifier used to derive a bundle identifier when `bundle_identifier` is omitted.
- `skip_validation`: optional flag to skip post-generation verification.
- `dry_run`: optional flag to resolve inputs and emit the planned execution contract without creating files.
- Defaults:
  - runtime entrypoint: executable `scripts/run_workflow.py`
  - `project_kind` defaults to `app`
  - `destination` defaults to `.`
  - `platform` defaults to `ask` unless explicitly set
  - `ui_stack` defaults to `swiftui`
  - `project_generator` defaults to `xcodegen`
  - `copy_agents_md` defaults to `true`
  - Codex GUI local environments are installed from `templates/codex-local-environments/xcode-project.toml` into `.codex/environments/xcode-project.toml`
  - validation runs unless `--skip-validation` is passed
  - `maintain-project-repo` installs `Scripts/repo-maintenance/` on successful mutating runs

## Outputs

- `status`
  - `success`: bootstrap completed on the supported path
  - `blocked`: prerequisites, unsupported selections, or safety rules prevented completion
  - `failed`: the implementation path started but did not complete successfully
- `path_type`
  - `primary`: the documented supported path completed
  - `fallback`: a guided fallback or non-mutating plan was returned instead
- `output`
  - resolved project path
  - normalized inputs
  - resolved bundle identifier
  - generator path
  - installed `.codex/environments/xcode-project.toml`
  - installed default String Catalog path
  - installed `maintain-project-repo` paths
  - validation result
  - one concise next step or handoff

## Guards and Stop Conditions

- Stop with `blocked` if `name` is missing.
- Stop with `blocked` if `project_kind` is not `app`.
- Stop with `blocked` if the platform cannot be resolved safely.
- Stop with `blocked` if `project_generator=ask` and the request intentionally asks not to choose the default generator.
- Stop with `blocked` if `ui_stack` is not supported by the current implementation path.
- Stop with `blocked` if the target directory already exists and contains non-ignorable files.
- Stop with `blocked` if `project_generator=xcodegen` and `xcodegen` is not available on `PATH`.
- Stop with `blocked` if the user chose the standard Xcode flow and the repo cannot safely automate that path yet.

## Fallbacks and Handoffs

- Preferred implementation path in the first iteration is `XcodeGen` plus generated scaffold files.
- Use the standard Xcode-created-project path only as a guided fallback for now.
- After a successful XcodeGen bootstrap, treat `project.yml` as the editable source for generated project structure and regenerate with `xcodegen generate` after project-spec changes.
- After a successful bootstrap, hand off to `sync-xcode-project-guidance` for repo-guidance alignment when needed, then to `xcode-build-run-workflow` for build, run, diagnostics, mutation, preview, and docs work.
- After a successful bootstrap, hand off to `xcode-testing-workflow` for Swift Testing, XCTest, XCUITest, `.xctestplan`, and test diagnosis work.
- After a successful bootstrap, use `Scripts/repo-maintenance/validate-all.sh` for local maintainer validation and `Scripts/repo-maintenance/release.sh --mode standard --version vX.Y.Z` from a feature branch or worktree for protected-main releases.
- After a successful bootstrap, configure protected branches to require `validate` for the managed repo-maintenance workflow; GitHub exposes that job check context directly rather than the workflow title plus job string.
- When the app repository is published to GitHub, use
  `productivity-skills:maintain-github-repository` to audit repository features,
  merge modes, security automation, sign-off policy, and branch protection.
- Recommend `bootstrap-swift-package` directly when the task is really package bootstrap.
- Recommend `sync-xcode-project-guidance` when the repo already exists and only needs repo-guidance or documentation alignment.

## Customization

- Use `references/customization-flow.md`.
- `scripts/customization_config.py` stores and reports customization state.
- `scripts/run_workflow.py` loads runtime-safe defaults from customization state before invoking the supported implementation path.
- Current runtime-enforced knobs include the default platform, bundle-ID prefix, and `AGENTS.md` copy behavior. Project kind, UI stack, generator choice, and validation policy now live as fixed workflow behavior or explicit invocation inputs.
- Run the Python wrapper and customization entrypoints through `uv`, because they rely on inline `PyYAML` script metadata rather than a repo-global Python environment.
- In consuming repos, the supported path is `uv run scripts/run_workflow.py ...` and `uv run scripts/customization_config.py ...`; do not assume plain `python` or `python3` will have the needed YAML dependency installed.

## References

### Workflow References

- `references/project-generators.md`
- `references/xcodegen-synced-folder-and-config-notes.md`
- `references/platform-matrix.md`

### Contract References

- `references/automation-prompts.md`
- `references/customization-flow.md`

### Support References

- `assets/AGENTS.md`
- Recommend `references/snippets/apple-xcode-project-core.md` when the new app repo should start with reusable Xcode-project baseline policy content next to the generated `AGENTS.md`.
- `references/snippets/apple-xcode-project-core.md`
- `templates/xcodegen/swiftui-app/project.yml.tmpl`
- `templates/xcodegen/swiftui-app/Configurations/*.xcconfig.tmpl`

### Script Inventory

- `scripts/run_workflow.py`
- `scripts/bootstrap_xcode_app_project.py`
- `scripts/customization_config.py`
