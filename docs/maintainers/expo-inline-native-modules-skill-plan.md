# Expo Inline Native Modules Skill Plan

This plan records a proposed Socket-hosted skill for Expo SDK 56+ inline native modules and `expo-type-information`.

The skill should help agents work at the React Native native boundary without treating Expo projects like ordinary web projects. It should be narrow, current-docs-first, and explicit about the experimental status of the SDK 56 inline module surface.

## Intent

Add a `web-dev-skills` skill that helps agents do six things:

- decide whether Expo inline modules are the right shape for a requested native feature
- inspect an existing Expo app before changing app config, generated native projects, or generated TypeScript files
- add or update Swift and Kotlin inline modules in watched TypeScript or JavaScript project directories
- use `expo-type-information` for Swift-backed TypeScript interface generation when the host environment supports it
- choose the right validation path across Expo Go, development builds, CNG/prebuild, local native builds, and TypeScript checks
- hand off Apple-platform design, Swift availability, Xcode validation, and signing-sensitive work to `apple-dev-skills`

This should be a companion guidance skill, not a runtime plugin. Do not bundle Expo, EAS, SourceKitten, native build tooling, an MCP server, a template feed, or generated sample apps in the first version.

## Proposed Skill

### `web-dev-skills:expo-inline-native-modules-workflow`

Use this when a task mentions Expo SDK 56+ inline modules, custom Swift or Kotlin inside an Expo app, `expo-type-information`, generated TypeScript interfaces for Expo modules, `requireNativeModule`, `requireNativeView`, Expo Modules API native views, or moving a native Expo module from standalone package boilerplate into the app tree.

The skill should route the agent through:

1. current official Expo documentation lookup
2. live project inspection
3. SDK and workflow gate checks
4. implementation shape selection
5. native module and generated interface handling
6. validation and risk reporting

## Freshness Policy

Inline modules and `expo-type-information` are new in Expo SDK 56 and are likely to change frequently.

The skill must require agents to refresh official Expo documentation before making claims or edits involving:

- inline module availability, configuration keys, naming rules, or watched directory restrictions
- `expo-type-information` command names, generated file names, type inference modes, or setup requirements
- Expo SDK version gates, React Native version alignment, New Architecture assumptions, or Expo Go support
- CNG, prebuild, dev-client, local build, or EAS behavior

As of the checked documentation on 2026-06-04:

- Expo inline modules are experimental and available in Expo SDK 56 and later.
- Inline modules let Swift and Kotlin module files live inside configured project directories instead of a standalone Expo module package.
- `expo.experiments.inlineModules` enables the feature, and `expo.experiments.inlineModules.watchedDirectories` controls where inline modules can be discovered.
- A watched directory must live inside a TypeScript or JavaScript project with a `package.json` ancestor, cannot be the whole project directory or an ancestor of it, cannot be nested inside another watched directory entry, and cannot include special characters such as spaces, parentheses, or `$`.
- App config changes for inline modules require `npx expo prebuild` before they affect native projects.
- The inline module file name must match the native module name, and module names must be unique in the app.
- `expo-type-information` is available for SDK 56 and later, works only on macOS, and depends on SourceKitten.
- `inline-modules-interface` creates two files for each Swift inline module: a regenerated `Module.generated.ts` file and a stable `Module.tsx` file that is not regenerated if changed.
- Type inference defaults to `SIMPLE_INFERENCE`; `PREPROCESS_AND_INFERENCE` can fail on some modules, so the skill should fall back to `SIMPLE_INFERENCE` or `NO_INFERENCE` when needed.

Treat these notes as a snapshot, not permanent truth. The skill should cite official docs in implementation-time replies whenever the facts matter.

## Documentation Sources

Use official Expo documentation first:

- [Expo inline modules reference](https://docs.expo.dev/modules/inline-modules-reference/)
- [Expo type generation reference](https://docs.expo.dev/modules/type-generation-reference/)
- [Expo Modules API overview](https://docs.expo.dev/modules/overview/)
- [Expo Modules API reference](https://docs.expo.dev/modules/module-api/)
- [Continuous Native Generation](https://docs.expo.dev/workflow/continuous-native-generation/)
- [Development builds](https://docs.expo.dev/develop/development-builds/introduction/)
- [create-expo-module](https://docs.expo.dev/more/create-expo-module/)
- [Expo SDK 56 changelog](https://expo.dev/changelog/sdk-56)
- [Native code in Expo SDK 56 blog post](https://expo.dev/blog/native-code-expo-sdk-56)

Use official Apple documentation or the `apple-dev-skills` workflows for Swift, Xcode, Apple framework, signing, simulator, App Store, or platform-availability claims. Use official Android, Kotlin, or React Native documentation when the Android side requires behavior that Expo's docs do not fully specify.

## Project Inspection Contract

Before editing an Expo app, the skill should inspect:

- `package.json`
- lockfile and package manager
- `app.json`, `app.config.js`, `app.config.ts`, or equivalent Expo config
- installed `expo`, `react`, and `react-native` versions
- whether `ios/` and `android/` directories exist
- whether the project appears to use CNG, bare native directories, or a mixed/manual native workflow
- `eas.json` when EAS or development builds are part of validation
- `tsconfig.json` and TypeScript check scripts
- existing Swift, Kotlin, Expo Modules API, config plugin, or generated TypeScript interface files

Do not run `npx expo prebuild --clean`, native builds, EAS builds, or package installation until the agent has identified the likely side effects and the user's request authorizes that level of change.

## Decision Rules

Use inline modules when:

- the native code is app-specific
- the feature can live cleanly inside the app's source tree
- the module does not need to be published as a reusable package
- the app already uses Expo SDK 56+ or the task explicitly includes an SDK upgrade
- the user accepts the experimental SDK 56 inline module status

Prefer a local or standalone Expo module when:

- the module should be reused across apps
- the native surface needs an example app, independent tests, or package-level versioning
- the native code has enough size or complexity that colocating it with app route files would hide ownership
- the team needs a more established Expo Modules API package shape

Prefer a config plugin or existing package configuration when:

- the requested work is native project configuration rather than a JS-callable native API
- the native change belongs in generated project customization, entitlements, Info.plist, AndroidManifest, Gradle, Pods, targets, or app delegates
- the change needs to survive CNG/prebuild without manual native directory edits

Prefer direct native project work only when:

- the project is intentionally bare or brownfield
- repo-local guidance says native directories are source of truth
- the user explicitly asks for manual native project edits

## Workflow

### Phase 1: Refresh and Inspect

1. Refresh official Expo docs for inline modules and type generation.
2. Inspect the live project files listed in the project inspection contract.
3. Identify whether the app uses Expo Go only, development builds, CNG, checked-in native directories, or a bare/brownfield native workflow.
4. Report the intended edit scope before making native, generated, or package-manager changes.

### Phase 2: Choose the Native Shape

1. Decide between inline module, standalone Expo module, config plugin, existing Expo package, or direct native edit.
2. Explain the practical effect of the choice in plain language.
3. If the scope requires a new module boundary, state whether it is a durable building-block change, local implementation detail, or conscious stopgap.
4. For Swift/iOS work, route platform API design and Xcode validation through `apple-dev-skills`.

### Phase 3: Configure Inline Module Discovery

1. Add or update `expo.experiments.inlineModules` only when SDK and workflow gates pass.
2. Set `watchedDirectories` to specific project source directories such as `app` or `src`.
3. Avoid watched directory entries that are whole-project roots, parent directories, nested duplicates, or paths with special characters.
4. Preserve existing Expo config structure and formatting.

### Phase 4: Add Native Code

1. Keep Swift and Kotlin module file names aligned with module names.
2. Keep module names unique across the app.
3. Prefer small native modules with one obvious JS-facing job.
4. For views, distinguish `requireNativeView` usage from ordinary `requireNativeModule` usage.
5. Keep platform-specific behavior explicit; do not imply iOS validation proves Android behavior or Android validation proves iOS behavior.

### Phase 5: Generate TypeScript Interfaces

1. Install or use `expo-type-information` only in SDK 56+ projects.
2. On macOS, verify SourceKitten availability before running generation.
3. Use `inline-modules-interface` for inline Swift module generation.
4. Treat `Module.generated.ts` as volatile generated output.
5. Treat `Module.tsx` as the stable editable wrapper surface.
6. Prefer default or simple inference first; fall back if preprocessing fails.
7. Do not hand-edit generated output except as an explicitly temporary diagnostic step.

### Phase 6: Validate

Choose validation based on the project:

- run package-manager install or sync only when dependencies changed
- run the repo's TypeScript check when available
- run `npx expo-doctor` after Expo dependency or config changes
- run `npx expo prebuild` when app config changes must synchronize native projects
- run `npx expo run:ios` or `npx expo run:android` only when local native build validation is appropriate and authorized
- use a development build when custom native code is required at runtime
- use EAS build only when the user requests cloud/device/store validation or repo-local guidance requires it

Respect the machine-wide rule that build and test commands must be serialized. Do not run Expo, Xcode, Gradle, SwiftPM, TypeScript, or package-manager validation concurrently.

## Skill Content Shape

The first implementation slice should add:

- `plugins/web-dev-skills/skills/expo-inline-native-modules-workflow/SKILL.md`
- `plugins/web-dev-skills/skills/expo-inline-native-modules-workflow/agents/openai.yaml`
- references for workflow policy and validation matrix if the `SKILL.md` gets too large
- updated `plugins/web-dev-skills/.codex-plugin/plugin.json` metadata
- updated `plugins/web-dev-skills/AGENTS.md` with Expo/React Native guidance boundaries
- root marketplace metadata updates if the plugin is still placeholder-only
- root README and roadmap updates only when the user-facing catalog surface changes

Keep examples minimal in the first slice. Prefer workflow guidance over copied code templates because Expo SDK 56 inline modules are experimental.

## Validation for Socket Implementation

For the Socket skill implementation pass:

1. Run root metadata validation:

   ```bash
   uv run scripts/validate_socket_metadata.py
   ```

2. Run child-local validation if `web-dev-skills` gains tests or a validator.
3. Inspect the final diff for generated or copied documentation drift.
4. Do not publish, tag, release, or run marketplace upgrade unless Gale explicitly asks for the release workflow.

## Open Questions

- Should this remain under `web-dev-skills`, or should Socket eventually grow a mobile-focused `expo-skills` or `react-native-skills` plugin if more RN workflows accumulate?
- Should the first skill include Android/Kotlin examples, or keep examples Swift-first because `expo-type-information` currently generates TypeScript from Swift modules?
- Should a later version include a small Expo sample app for smoke testing, or should the skill stay documentation-only until Expo stabilizes inline modules?

For now, keep it in `web-dev-skills` as a narrow native-boundary workflow. Revisit the plugin boundary only if Socket accumulates several Expo, React Native, Android, and mobile release skills that no longer fit a web-dev bucket cleanly.
