# Apple Xcode Project Core AGENTS Snippet

Use this snippet in repository `AGENTS.md` files when you want baseline standards for an existing native Apple app project managed through Xcode.

## General Swift Baseline

- For any Swift, Apple-framework, Apple-platform, SwiftUI, SwiftData, Observation, AppKit, UIKit, Foundation-on-Apple, or Xcode-related task, read the relevant Apple documentation first before planning, proposing, or making changes.
- Use Xcode MCP `DocumentationSearch` or Xcode-local documentation first for Apple-owned SDK, framework, lifecycle, and Xcode behavior; use Dash MCP or Dash HTTP next when installed local package docs or multi-ecosystem docs are a better fit; use open source Swift project repositories, generated DocC, or release notes when the relevant Swift package or tool is open source and available there; use official Apple web docs only when the page content is actually readable through a capable source. Generic no-JS web search/open results, snippets, metadata shells, or bare Apple Developer URLs are not enough evidence that Apple docs were read.
- Before proposing an architecture or implementation, state the documented API behavior, lifecycle rule, or workflow requirement being relied on.
- Do not rely on memory, habit, or analogy as the primary source when Apple documentation exists.
- If Apple documentation and the current code disagree, stop and report the conflict before continuing.
- If no relevant Apple documentation can be found, say that explicitly before proceeding.
- Prefer the simplest correct Swift that is easiest to read, reason about, and maintain.
- Treat idiomatic Swift, Cocoa conventions, and modern Swift features as tools in service of readability, not as goals by themselves.
- Do not add ceremony, abstraction, or boilerplate just to make code look more architectural, more generic, or more "Swifty".
- Strongly prefer synthesized, implicit, and framework-provided behavior over custom code.
- Prefer synthesized conformances (`Codable`, `Equatable`, `Hashable`, etc.) whenever they satisfy the actual requirements.
- Prefer memberwise and otherwise synthesized initializers, default property values, and framework defaults over handwritten setup code.
- Do not add `CodingKeys`, manual `Codable` methods, custom initializers, wrappers, helper types, protocols, coordinators, or extra layers unless they are required by a concrete constraint or they make the final code clearly easier to understand.
- Prefer applicable existing framework or platform error types before inventing custom error wrappers or error hierarchies.
- Prefer direct, simple error flows and small focused error enums only when they materially improve understanding.
- Prefer stable, source-of-truth naming across layers when the data and meaning have not changed.
- Treat naming consistency as a reliability feature: if the same data still serves the same purpose, keep the same name.
- Do not rename fields just to match local style conventions when the external schema is already clear and stable.
- Do not use automatic case-conversion strategies such as `.convertFromSnakeCase` or `.convertToSnakeCase` unless the project explicitly wants that behavior and it clearly improves readability overall.
- When an API, cloud service, or wire format already provides clear names, preserve those names directly in Swift models and nearby code unless the meaning actually changes or a concrete collision must be resolved.
- Preserve raw wire and persistence shapes by default; do not add DTO, domain, or view-model conversion layers unless meaning actually changes or a concrete boundary requires it.
- Treat redundant wrappers, rename-and-copy layers, and duplicated logic as anti-patterns by default.
- This guidance is optimized for an advanced Swift reader and may prefer dense but readable modern Swift over beginner-style explicitness.
- Prefer explicit names that are consistent, unambiguous, and easy to scan at the call site.
- For public Swift APIs, treat streamlined, compact, ergonomic call sites as the only acceptable default; do not grow method families, overload sets, or loosely typed entry points when one clear typed API can express the operation.
- Prefer optional parameters with explicit default values over additional methods or overloads whenever the difference is optional behavior on the same operation.
- When a public function, initializer, or method reaches four or more arguments or parameters, strongly prefer a named typed `struct` request, options, or configuration value so call sites stay readable and future additions do not multiply overloads.
- Prefer enums, enum cases with associated values, and narrow typed values over strings, booleans, sentinel values, or parallel parameters whenever the domain has a closed or meaningful set of choices.
- Prefer compact syntax when it improves local reasoning, including shorthand syntax, ternary expressions, trailing closures, enums, `switch`, `map`, `filter`, `forEach`, async iteration, `AsyncSequence`, `AsyncStream`, and `AsyncAlgorithms`.
- Prefer explicit default values at initialization when they reduce optional-handling clutter and keep the code easier to follow.
- When lines, chains, or expressions get long, prefer chopping them down into a clean vertical, top-down structure with straight visual flow.
- Do not force value types by default, protocols at seams, actors by default, or other pattern slogans when a plainer concrete implementation is easier to reason about.
- Keep code compliant with Swift 6 language mode.
- Keep strict concurrency checking enabled.
- Prefer modern structured concurrency (`async`/`await`, task groups, actors) over legacy async patterns when it keeps the flow clearer and more direct.
- Make async code cancellation-aware and keep actor or task boundaries explicit instead of hiding them behind detached tasks or queue wrappers.
- Prefer clear `Sendable` boundaries for values that cross task or actor isolation, and keep unchecked sendability exceptional and justified locally.
- Prefer Swift Testing (`import Testing`) as the default test framework, and use XCTest only when a dependency or platform constraint requires it.
- Prefer Swift Testing for unit-style and package-style test surfaces in modern Xcode projects, including suites, tags, parameterized tests, and direct async tests.
- Use XCTest when the platform surface, dependency graph, or Apple tooling still expects it, and keep XCTest and Swift Testing responsibilities clearly separated when both coexist.
- Use XCUITest for UI automation, and prefer explicit element wait APIs such as `waitForExistence(timeout:)`, `waitForNonExistence(timeout:)`, and related state waits over fixed sleeps.
- Keep `.xctestplan` files versioned when test configurations, diagnostics, sanitizers, locale coverage, or selective plan execution matter, and inspect or run them explicitly with `xcodebuild -showTestPlans` and `xcodebuild -testPlan ...`.
- Prefer normal Xcode and XCTest parallel execution for ordinary Swift Testing, XCTest, and XCUITest runs when the project, scheme, destination, and test plan support it. Do not serialize regular tests just because they use Swift, XCTest, async tests, UI automation, or `.xctestplan` matrices.
- Treat tests that load large local AI or ML models, especially models over 500 million parameters, as heavy system-resource tests. Run those tests sequentially, one at a time.
- Prefer first-party and top-tier Swift ecosystem packages from Apple, `swiftlang`, the Swift Server Work Group, and similarly trusted core Swift projects when they simplify the code and make it easier to reason about.
- Commonly approved examples include `swift-configuration` and `swift-async-algorithms` when they reduce bespoke code and improve readability.
- For Apple app projects, prefer Apple-native logging facilities first and allow Swift Logging where it makes the project API clearer.
- Prefer Swift OpenTelemetry for telemetry and instrumentation when telemetry is needed, and prefer existing ecosystem integrations over bespoke wrappers.
- Prefer a checked-in repo-root `.swiftformat` file as the default Swift formatting source of truth, and prefer a pre-commit hook that formats staged Swift sources and then verifies them with `swiftformat --lint` before commit.
- Treat SwiftLint as an optional complementary signal layer for clarity, safety, and maintainability after SwiftFormat owns formatting shape.
- Keep automation and CI commands deterministic, non-interactive, and explicit about toolchain, platform, and configuration assumptions.

## SwiftUI and State Architecture

- Treat SwiftUI views as component UI: keep them small, composable, reusable, and easy to scan from top to bottom.
- Choose and record one explicit three-letter uppercase prefix for every app or package. Prefix project-owned Swift files and primary declarations; exempt only `Package.swift`, externally generated Swift, and vendored third-party Swift.
- Never use `+` in project-owned Swift filenames. Concatenate the owner and concern so Xcode navigation, rename, and refactoring keep one consistent grammar.
- Name views `GEAWhateverView.swift`, paired `@Observable final class` view models `GEAWhateverViewModel.swift`, and extracted modifiers `GEAWhateverViewModifier.swift`.
- Give independently editable or previewable view components their own files. Small private computed view properties or helper views may remain while they do not clutter focused editing or previews.
- Prefix extracted child components with their complete composition owner, such as `GEASettingsSheetToggleCard.swift`.
- Extract a custom `ViewModifier` after more than eight chained modifiers, or earlier when a coherent chain is reusable or obscures the view body.
- Prefer straight, top-down data flow with state owned at the narrowest view, scene, or app boundary that matches the behavior.
- Do not build monolithic views, monolithic controllers, or broad shared mutable state when a smaller component boundary would be clearer.
- Keep updates to view-driving state minimal and localized.
- Prefer durable identity for types that drive SwiftUI state and view updates.
- Treat `App` as the application entry and scene composition boundary, `Scene` as the container for scene-specific lifecycle and environment, and `View` as the component rendering layer.
- Every native app target must have exactly one app lifecycle entry point: one `@main` app type, one `main.swift`, or the platform-equivalent single launch entry. Do not add alternate app entry points, second `@main` types, duplicate `main.swift` files, target-specific app entry files, or parallel app structs for variants. When launch behavior must differ by platform, configuration, or feature flag, keep the single entry point and use Swift conditional compilation or ordinary runtime conditionals inside that boundary.
- Use app-level lifecycle concerns at the `App` boundary, scene lifecycle concerns at the `Scene` boundary, and view-local active or presentation behavior inside views.
- Use `@Binding` to pass a focused writable piece of parent-owned state into a child view.
- Use `@Bindable` when working with an observable model that should project bindings to its mutable properties in a view.
- Use the dedicated SwiftData workflow for persistence architecture and its direct SwiftUI integration path.
- Prefer environment values for shared context that truly belongs to the surrounding hierarchy, not as a dumping ground for unrelated dependencies.
- Prefer key-path-based APIs, predicates, and sort descriptors when they keep data access direct and readable.
- Extract repeated chains of view modifiers into custom view modifiers early when that reduces clutter and clearly matches a view or family of views.

## Xcode Workspace and Project Baseline

- Treat the `.xcworkspace` or `.xcodeproj` as the source of truth for Apple platform app integration, schemes, build settings, destinations, and target membership.
- Prefer edits through Xcode-aware project structure and keep project file changes intentional and reviewed closely.
- Use the standard top-level Xcode app repository layout when creating or normalizing native app repos: `Sources/`, `Tests/`, `Shared/`, `Extensions/`, `Configurations/`, `Scripts/`, and `Packages/`.
- `Sources/` owns the main app target implementation and app-owned resources/support files. `Tests/` owns all test targets. `Shared/` owns reusable source intended to be compiled into the app and extension targets. `Extensions/` owns extension target roots, one folder per extension. `Configurations/` owns `.xcconfig` layers. `Scripts/` owns project-local automation and build helper scripts. `Packages/` owns local Swift packages only when a real package boundary is justified.
- Keep those top-level roots stable. Do not invent parallel names such as `AppSources`, `TestSources`, `Config`, `BuildScripts`, or `LocalPackages` for ordinary Xcode app repos unless the existing repo already has a deliberate, documented convention.
- Inside `Sources/`, use this strict app structure by default: `Views/`, `Models/`, and `Services/`. Do not create a root `Controllers/` directory.
- `Sources/Views/` owns SwiftUI views and UIKit/AppKit view surfaces. Use `Sources/Views/Shared`, `Sources/Views/macOS`, and `Sources/Views/iOS` so shared, macOS-specific, and iOS/iPadOS-specific UI have clear homes.
- Use bare prefixed names such as `GEAWhatever.swift` for runtime/domain values. Reserve `GEAWhateverModel.swift` for persistence, and use `GEAWhateverRecord.swift` or `GEAWhateverDTO.swift` only for genuinely additional representations.
- `Sources/Models/` owns Core Data and SwiftData persistence models plus additional record or transfer representations.
- `Sources/Services/` owns app-wide and boundary-facing services. Use `Consumed/` for external services the app calls, `Internal/` for services owned only by the app, and `Provided/` for services the app exposes to extensions, helpers, plugins, integrations, or other clients.
- Name services `GEAWhateverService.swift`; they manage the matching runtime/domain value `GEAWhatever`. `GEAAppService.swift` may manage `GEA`, while `GEAApp.swift` is the lifecycle-entry special case.
- Use `xcodebuild` for Apple platform integration validation, including scheme, destination or SDK, and configuration-specific build or test runs.
- Keep `xcodebuild` invocations reproducible in automation by passing explicit schemes, destinations or SDKs, and configurations when relevant.
- For Codex GUI worktree-first Xcode repos, use a portable `.codex/environments/*.toml` local environment file when the repo wants shared app setup or action buttons. Start from `apple-dev-skills/templates/codex-local-environments/xcode-project.toml`, keep paths repo-relative, and prefer `-derivedDataPath ./DerivedData` or another ignored repo-local build directory instead of user-global DerivedData.
- When scripts or terminal workflows add files on disk, verify that Xcode project membership, target membership, build-phase membership, and resource-bundle inclusion all match the intended result; files appearing in the directory tree alone are not enough.
- Direct filesystem edits outside `.pbxproj` are generally safe when Xcode is closed or when the current project is not open in Xcode, but still verify that the Xcode project picks up the intended files and memberships afterward.
- Prefer Debug builds for everyday edit-build-test loops, but validate Release builds explicitly when optimization, packaging, launch behavior, watchdog timing, or deployment realism matters.
- Treat tagged releases as a signal to validate both the normal Debug path and a Release artifact path, and when shipping apps or deliverables test the Release behavior without relying on an attached debugger.
- Prefer direct filesystem edits in Xcode-managed scope only when the workflow already accounts for project-file and scheme integrity.
- Never edit `.pbxproj` files directly. If a project-file change is needed and no safe project-aware tool is available, stop and ask for an Xcode-mediated project change instead. When `.pbxproj` is tracked and Xcode, XcodeGen, or another project-aware workflow legitimately changes it, treat that diff as critical project state: review it, stage it, and commit it with the branch before any push, merge, release, or cleanup.

## XcodeGen and Build Configuration Defaults

- For new Xcode app, framework, and workspace repositories, prefer an XcodeGen-backed project by default unless the user explicitly asks for a hand-managed Xcode project or the repository has a concrete reason to avoid a generator dependency.
- If the repo contains `project.yml`, `project.yaml`, or clearly named included XcodeGen spec files, treat the XcodeGen spec set as the source of truth for generated project structure.
- For XcodeGen-backed repos, make target membership, resource membership, schemes, Swift package declarations, test-plan references, project references, build configurations, configuration-file wiring, generation options, and project-level settings in the XcodeGen specs instead of editing the generated `.pbxproj`.
- Before running `xcodegen generate`, inspect the current git diff for generated `.xcodeproj` or `.pbxproj` changes. Treat existing project-file diffs as intentional user or Xcode GUI changes by default, not disposable generator drift.
- When Xcode GUI changes added build settings, signing settings, capabilities, `Info.plist` build setting overrides, file membership, scheme changes, or entitlement wiring to `.pbxproj`, preserve the user intent by moving each intentional value to the owning tracked source first: XcodeGen spec for structure, `.xcconfig` for build settings, `.entitlements` for entitlement keys, `Info.plist` for plist keys, `.xcscheme` or scheme spec for scheme behavior, and `.xctestplan` for test-plan content.
- Only regenerate after that promotion is complete, then review the generated project diff to confirm XcodeGen preserved the intended behavior instead of deleting it. If the owning tracked file is ambiguous, stop and ask before regenerating.
- For new XcodeGen-backed app scaffolds, start from the maintained `apple-dev-skills/templates/xcodegen/` templates when available instead of inventing a fresh project-spec shape from memory.
- Keep `minimumXcodeGenVersion` on a recent validated release for new scaffolds. Prefer updating the template and validation together when the repo intentionally raises the baseline.
- For Xcode 16 or newer project formats, prefer XcodeGen `syncedFolder` roots at the broad top-level directory boundary so file creation, deletion, and organization stay synchronized between Xcode and the filesystem without hand-listing every source file in YAML.
- Do not fragment ordinary XcodeGen source roots by subdirectory. A standard app target gets one `Sources` source entry that includes all app source, resource, support, generated plist, entitlement, and nested feature folders, plus one `Shared` source entry when shared app/extension code exists. A standard test target gets one `Tests` source entry that includes all test subdirectories. Extension targets use one `Extensions/<ExtensionName>` source entry per extension target. If a project has another separate top-level logical root, use one top-level entry for that root, not one entry per child folder.
- Never split `Sources/App`, `Sources/Resources`, `Sources/Support`, feature folders, or `Tests/<TargetName>Tests` into separate XcodeGen source entries unless a specific non-ordinary file or folder truly needs custom compiler flags, build-phase routing, destination filters, or target membership that cannot be represented from the broad root.
- If `syncedFolder` behaves poorly for a repo, fall back to the same broad top-level recursive paths such as `Sources`, `Tests`, or `Resources` with explicit `includes` and `excludes`; do not fall back to subdirectory-level fragmentation or one YAML entry per ordinary source file.
- Keep XcodeGen specs readable as project structure, not as a dumping ground for every build setting. Use `configs`, `configFiles`, `targets`, `schemes`, `packages`, `projectReferences`, `targetTemplates`, and `schemeTemplates` deliberately so future edits have an obvious owner.
- Prefer explicit top-level schemes for app scaffolds once scheme behavior matters. Put build, run, test, profile, analyze, archive, environment variables, command-line arguments, and test-plan references in the scheme spec rather than relying on hidden generated defaults.
- Prefer external `.xcconfig` files as the default home for nontrivial build settings. Keep build settings in XcodeGen inline settings only when they are small, local, and clearer there.
- Use `.xcconfig` files for settings that vary by Debug, Release, CI, local development, signing, bundle identity, compiler flags, Swift settings, deployment variants, or environment-specific behavior.
- Keep configuration layering explicit. Prefer a small shared base config, target-level configs for app/test/extension identity, then per-configuration configs that include the narrower target config and override only what changes.
- In XcodeGen specs, wire build configurations to their matching `.xcconfig` files instead of duplicating the same settings across generated project objects.
- Prefer checked-in external `.entitlements` files for app, extension, and capability-bearing targets, with `CODE_SIGN_ENTITLEMENTS` declared in the owning target's `.xcconfig`. Let Xcode capabilities update the entitlement plist when possible, then review and commit the entitlement diff; keep XcodeGen responsible for wiring the file, not regenerating its contents from inline YAML.
- Do not assume Xcode's Build Settings UI writes edited values back into `.xcconfig` files. When a build setting should remain tracked in `.xcconfig`, inspect the generated project diff after GUI changes and move intentional build-setting overrides from `.pbxproj` back into the owning `.xcconfig` before regenerating.
- Keep secrets, personal team IDs, local machine paths, provisioning profiles, API tokens, and private signing material out of committed `.xcconfig` files. Use build settings only for non-secret configuration values, safe placeholders, references to externally supplied values, or local developer placeholders that are safe to commit.
- Before changing generated project structure, inspect the root spec plus any `include` entries so the edit lands in the owning spec rather than duplicating settings in the wrong file. Remember that included specs merge into the root spec, and local overrides may intentionally replace arrays or maps.
- After changing XcodeGen specs, `.xcconfig` files, or entitlement-file wiring, run `xcodegen generate` from the spec root, or `xcodegen generate --spec <path>` when the project uses a non-default spec path.
- If the spec uses environment variables or generation hooks, preserve and document the required environment before regenerating so CI and other contributors can reproduce the project.
- Review the spec diff, `.xcconfig` diff, and generated `.xcodeproj` diff after regeneration. Generated `.pbxproj` changes are acceptable output when they come from XcodeGen, but they should still be reviewed for unintended target, scheme, signing, package, build-setting, or file-membership churn.
- Validate regenerated projects with explicit `xcodebuild` commands for the affected scheme, destination or SDK, and configuration.
- For existing hand-managed Xcode projects, do not migrate to XcodeGen or externalize build settings into `.xcconfig` files unless the user explicitly asks for that migration. When they do, treat it as a project-structure migration with before/after validation.
