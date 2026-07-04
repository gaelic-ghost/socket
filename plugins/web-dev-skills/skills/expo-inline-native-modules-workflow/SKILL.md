---
name: expo-inline-native-modules-workflow
description: Work at the Expo SDK 56+ inline native module boundary with current Expo docs, live project inspection, TypeScript interface generation, and explicit Apple Dev Skills handoffs.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients changing Expo apps that use or may use inline Swift or Kotlin modules, expo-type-information, Expo Modules API native views, CNG, development builds, and prebuild validation.
metadata:
  owner: gaelic-ghost
  repo: web-dev-skills
  category: expo-native-boundary
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(npx:*) Bash(pnpm:*) Bash(npm:*) Bash(yarn:*) Bash(bun:*) Bash(which:*)
---

# Expo Inline Native Modules Workflow

## Purpose

Guide Expo app changes that cross from TypeScript or JavaScript into app-specific Swift or Kotlin native code.

This workflow keeps inline modules narrow and project-local. It helps decide whether an inline module is the right shape, inspect the app before touching native or generated files, configure discovery, generate TypeScript interfaces where supported, and pick validation that matches the app's Expo workflow.

## When To Use

- Use this skill when a task mentions Expo SDK 56 or later inline modules.
- Use this skill when adding custom Swift or Kotlin inside an Expo app tree.
- Use this skill when using `expo-type-information` or generated TypeScript interfaces for Swift Expo modules.
- Use this skill when a task mentions `requireNativeModule`, `requireNativeView`, Expo Modules API native views, or moving a native Expo module from standalone package boilerplate into the app tree.
- Use the broader Expo Modules workflow for standalone reusable Expo modules, package publishing, and module templates.
- Use Apple Dev Skills for Swift API design, Apple framework behavior, Xcode project validation, simulators, signing, capabilities, entitlements, App Store behavior, and Apple platform availability claims.

## Freshness Gate

Inline modules and `expo-type-information` are experimental and may change quickly. Refresh official Expo documentation before making claims or edits involving:

- inline module availability, configuration keys, naming rules, watched directory restrictions, or generated native project behavior
- `expo-type-information` commands, generated file names, type inference modes, or setup requirements
- Expo SDK gates, React Native alignment, New Architecture assumptions, Expo Go support, CNG, prebuild, dev-client, local native builds, or EAS behavior

Use repo-local Expo files, checked-out dependency sources, Dash MCP or Dash HTTP for installed Expo or React Native docsets, and then official Expo documentation when Dash/local coverage is missing, stale, or insufficient for the current experimental SDK behavior:

- [Inline modules reference](https://docs.expo.dev/modules/inline-modules-reference/)
- [Type generation reference](https://docs.expo.dev/modules/type-generation-reference/)
- [Expo Modules API overview](https://docs.expo.dev/modules/overview/)
- [Expo Modules API reference](https://docs.expo.dev/modules/module-api/)
- [Continuous Native Generation](https://docs.expo.dev/workflow/continuous-native-generation/)
- [Development builds](https://docs.expo.dev/develop/development-builds/introduction/)
- [create-expo-module](https://docs.expo.dev/more/create-expo-module/)
- [Expo SDK 56 changelog](https://expo.dev/changelog/sdk-56)
- [Native code in Expo SDK 56](https://expo.dev/blog/native-code-expo-sdk-56)

When Swift, Xcode, signing, simulator, or Apple framework facts matter, route through Apple Dev Skills and official Apple documentation instead of relying on Expo guidance alone.

## References

Use the focused reference tables when choosing a native shape or validation path:

- [Native shape decision](./references/native-shape-decision.md)
- [Validation matrix](./references/validation-matrix.md)

These references are local workflow aids, not permanent API references. Refresh official Expo docs before using SDK-version-sensitive details.

## Inspection Contract

Before editing an Expo app, inspect the live project:

1. `package.json`, the lockfile, and package-manager conventions.
2. `app.json`, `app.config.js`, `app.config.ts`, or equivalent Expo config.
3. Installed `expo`, `react`, and `react-native` versions.
4. Whether `ios/` and `android/` directories exist.
5. Whether the app appears to use Expo Go only, CNG/prebuild, checked-in native directories, development builds, or a bare/brownfield workflow.
6. `eas.json` when EAS or development builds are part of validation.
7. `tsconfig.json` and TypeScript check scripts.
8. Existing Swift, Kotlin, Expo Modules API, config plugin, generated TypeScript interface, and native view files.

Report the intended edit scope before changing native code, generated TypeScript, package dependencies, Expo config, or generated native projects.

Do not run `npx expo prebuild --clean`, native builds, EAS builds, or package installation until the likely side effects are identified and the user's request authorizes that level of change.

## Danger Commands

Treat these commands as high-side-effect operations. Do not run them until the intended side effects are clear and the user's request authorizes that level of change:

- package-manager install or sync commands that change dependencies or lockfiles
- `npx expo prebuild`, because it updates generated native projects from Expo config
- `npx expo prebuild --clean`, because it deletes and regenerates native project directories
- `npx expo run:ios` and `npx expo run:android`, because they run local native build toolchains
- EAS build commands, because they use remote build resources, credentials, and account/project state

Use [Validation matrix](./references/validation-matrix.md) before choosing one of these commands.

## Handoff Map

- Use this skill to decide the native boundary, inspect the live Expo app, choose validation scope, and report native-boundary risk.
- Use the built-in `expo-module` skill for standalone or local Expo module implementation.
- Use the built-in `expo-dev-client` skill for development build distribution and dev-client setup.
- Use the built-in `upgrading-expo` skill for Expo SDK upgrades and dependency-alignment work.
- Use Apple Dev Skills for Swift API design, Apple framework behavior, Xcode validation, simulators, signing, capabilities, entitlements, App Store behavior, and Apple platform availability claims.

## Native Shape Decision

Prefer an inline module when:

- the native code is app-specific
- the feature can live cleanly in the app source tree
- the module does not need package-level versioning, an example app, or reuse across apps
- the app already uses Expo SDK 56 or later, or the task explicitly includes an SDK upgrade
- the user accepts the experimental inline module status

Prefer a local or standalone Expo module when:

- the module should be reused across apps
- the module needs independent tests, an example app, package metadata, or package-level versioning
- the native surface is large enough that colocating it with route or app source files would hide ownership

Prefer a config plugin or existing package configuration when:

- the requested change is native project configuration rather than a JS-callable API
- the native change belongs in generated project customization such as Info.plist, AndroidManifest, Gradle, Pods, targets, entitlements, app delegates, or capabilities
- the change needs to survive CNG/prebuild without manual native directory edits

Prefer direct native project edits only when the project is intentionally bare or brownfield, repo-local guidance says native directories are source of truth, or the user explicitly asks for manual native project work.

If the choice creates a new native boundary, describe it plainly as a durable building-block change, a local implementation detail, or a conscious stopgap, and name what practical work it unlocks.

## Workflow

### 1. Refresh And Inspect

1. Refresh the official Expo inline modules and type generation references.
2. Inspect the live project files from the inspection contract.
3. Identify the app workflow: Expo Go only, development build, CNG/prebuild, checked-in native directories, bare native, or mixed/manual.
4. State the intended edit scope before changing config, native files, generated files, dependencies, or native projects.

### 2. Configure Discovery

1. Add or update `expo.experiments.inlineModules` only when SDK and workflow gates pass.
2. Set `watchedDirectories` to specific source directories such as `app` or `src`.
3. Avoid watched entries that are the whole project root, parent directories, nested duplicates, outside JavaScript or TypeScript projects, or paths with special characters.
4. Preserve the existing Expo config format and comments where practical.
5. After config changes, explain that prebuild is required before generated native projects reflect the new config.

### 3. Add Native Code

1. Keep Swift and Kotlin module filenames aligned with module names.
2. Keep native module names unique across the app.
3. Prefer small modules with one obvious JavaScript-facing job.
4. Use `requireNativeModule` for modules and `requireNativeView` for native views.
5. Keep platform differences explicit; iOS validation does not prove Android behavior, and Android validation does not prove iOS behavior.
6. Route Apple API, Swift availability, Xcode, simulator, and signing-sensitive decisions through Apple Dev Skills.

### 4. Generate TypeScript Interfaces

1. Use `expo-type-information` only in SDK 56 or later projects.
2. On macOS, verify SourceKitten availability before running generation.
3. Use `inline-modules-interface` for Swift inline modules.
4. Treat `Module.generated.ts` as regenerated output.
5. Treat `Module.tsx` as the stable editable wrapper surface.
6. Prefer default or simple inference first; fall back to simpler inference when preprocessing fails.
7. Do not hand-edit generated output except as an explicitly temporary diagnostic step.

### 5. Validate

Choose validation from the project shape and changed surface:

- run package-manager install or sync only when dependencies changed
- run the repo's TypeScript check when available
- run `npx expo-doctor` after Expo dependency or config changes
- run `npx expo prebuild` when app config changes must synchronize native projects
- run `npx expo run:ios` or `npx expo run:android` only when local native build validation is appropriate and authorized
- use a development build when custom native code must run at runtime
- use EAS only when the user requests cloud, device, or store validation, or repo-local guidance requires it

Run Expo, Xcode, Gradle, SwiftPM, TypeScript, and package-manager validation serially. Do not run build or test tools concurrently.

## Output Shape

Return:

1. `Decision`: inline module, standalone module, config plugin, existing package, or direct native edit.
2. `Changed surfaces`: config, native files, TypeScript wrappers, generated files, dependencies, or native projects.
3. `Validation`: exact commands run and what passed or was skipped.
4. `Native boundary risk`: experimental Expo status, platform coverage gaps, generated-file caveats, and any Apple Dev Skills handoff.
