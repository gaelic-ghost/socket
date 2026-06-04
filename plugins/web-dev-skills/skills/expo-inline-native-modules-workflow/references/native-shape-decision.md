# Native Shape Decision

Use this table after inspecting the live Expo app and refreshing official Expo documentation. Choose the smallest native shape that matches the requested behavior and the repo's workflow.

| Shape | Choose when | Avoid when | Usually affects | Validate or hand off next |
| --- | --- | --- | --- | --- |
| Inline native module | Native code is app-specific, small, and can live in configured app source directories | The module needs reuse, package versioning, an example app, or independent tests | Expo config, watched source directory, Swift/Kotlin module files, TypeScript wrapper files | This skill for boundary and validation path; Apple Dev Skills for Swift/Xcode/signing; official Android/Kotlin or repo-local guidance for Android-specific behavior. |
| Standalone or local Expo module | Native code should be reusable, package-shaped, independently tested, or published | The feature is tiny and only belongs to one app | `modules/`, `expo-module.config.json`, native module package files, TypeScript package exports | Built-in `expo-module` skill for implementation; this skill only for choosing not to inline. |
| Config plugin | The change customizes generated native project configuration rather than exposing a JS-callable native API | The feature needs runtime Swift/Kotlin functions or a native view | Expo config, config plugin files, Info.plist, AndroidManifest, Gradle, pods, entitlements, generated project settings | Built-in Expo module/config plugin guidance plus Apple Dev Skills for Apple-specific generated-project behavior. |
| Existing package configuration | A maintained Expo or React Native package already exposes the requested native capability or config surface | Custom native code is genuinely required or package behavior is insufficient | Package config, app config, dependency versions, lockfiles | Built-in Expo package, upgrade, and dev-client guidance as appropriate. |
| Direct native project edit | The app is bare, brownfield, or repo-local guidance treats native directories as source of truth | The app relies on CNG/prebuild and native directories are generated artifacts | `ios/`, `android/`, Xcode project files, Gradle files, native source | Apple Dev Skills for Apple work; official Android/Kotlin or repo-local guidance for Android work; this skill should only document why direct native ownership is intentional. |

## Decision Checklist

1. Inspect `package.json`, Expo config, lockfile, `ios/`, `android/`, `eas.json`, and existing native or generated TypeScript files.
2. Confirm whether the app is Expo Go only, development-build based, CNG/prebuild, checked-in native, bare, or mixed.
3. Decide whether the request is a JS-callable native API, a native view, generated project configuration, dependency configuration, or direct native project work.
4. State the chosen shape and why it is a durable building-block change, local implementation detail, or conscious stopgap.
5. Route implementation and validation to the owning workflow before running package-manager, prebuild, native build, or EAS commands.

## Source Refresh

Use official Expo documentation before relying on inline-module, type-generation, CNG, or development-build details:

- [Expo inline modules reference](https://docs.expo.dev/modules/inline-modules-reference/)
- [Expo type generation reference](https://docs.expo.dev/modules/type-generation-reference/)
- [Expo Modules API overview](https://docs.expo.dev/modules/overview/)
- [Development builds](https://docs.expo.dev/develop/development-builds/introduction/)
