# Validation Matrix

Use this matrix after refreshing the official Expo inline modules and type generation references. Pick the narrowest validation that proves the changed surface, then broaden only when the change crosses into native runtime behavior.

## Changed Surface Matrix

| Changed surface | Minimum validation | Broaden when | Notes |
| --- | --- | --- | --- |
| Expo config only | Inspect config shape and run `npx expo-doctor` when Expo config or dependencies changed | App config must update generated native projects | Run `npx expo prebuild` only after explaining generated-project side effects. |
| `expo.experiments.inlineModules` or watched directories | Inspect SDK gate, config shape, and watched path rules; run `npx expo-doctor` | Native projects must reflect the config | Watched directories should be specific app source directories, not the project root or nested duplicates. |
| Swift inline module | TypeScript check plus Swift/iOS validation chosen through Apple Dev Skills | The module must run on device or simulator | `expo-type-information` can help with Swift-backed TypeScript interfaces, but Xcode and Apple API claims belong to Apple Dev Skills. |
| Kotlin inline module | TypeScript check plus Android validation appropriate to the project | The module must run on emulator or device | Do not imply iOS validation proves Android behavior. |
| Native view | TypeScript check plus platform-specific runtime validation | The view affects layout, gestures, accessibility, or platform UI behavior | Use `requireNativeView` for native views and validate each target platform separately. |
| Generated TypeScript interface | Confirm generated files and run the repo TypeScript check | Generated wrappers changed runtime imports or public JS API | Treat `Module.generated.ts` as volatile and `Module.tsx` as the stable editable wrapper. |
| Dependency or lockfile changed | Package-manager install/sync, then TypeScript check and `npx expo-doctor` | Native dependency affects pods, Gradle, dev builds, or runtime native code | Do not run installs unless dependency changes are intended and authorized. |
| CNG/prebuild workflow | `npx expo prebuild` only when config changes must update native projects | Clean regeneration is required and authorized | Prefer ordinary prebuild before `--clean`; clean prebuild can discard manual native edits. |
| Checked-in `ios/` or `android/` | Inspect native ownership before changing files | Native source of truth is manual or mixed | Preserve repo-local native workflow; avoid generated rewrites unless requested. |
| Expo Go workflow | `npx expo start` or existing repo start command when no custom native code is needed | Custom native code is required at runtime | Inline/native modules require a development build or native runtime, not plain Expo Go. |
| Development build | Use built-in `expo-dev-client` guidance for build/distribution path | Native code must be tested on physical device, TestFlight, or shared dev client | This skill chooses the boundary; dev-client workflows own distribution details. |
| Local native build | Run `npx expo run:ios` or `npx expo run:android` only when authorized | Native runtime behavior must be proven locally | Serialize with Xcode, Gradle, TypeScript, and package-manager checks. |
| EAS build | Use EAS only when user requests cloud/device/store validation or repo guidance requires it | Release, device fleet, credentials, or CI validation is in scope | EAS can touch credentials, remote build state, and project metadata; do not run casually. |

## High-Side-Effect Commands

| Command | Why it matters | Before running |
| --- | --- | --- |
| Package-manager install or sync | Changes dependency graph, lockfiles, and native dependency resolution | Confirm dependency changes are intended and the repo package manager is known. |
| `npx expo prebuild` | Regenerates or updates native project files from Expo config | Explain which config change needs native-project sync. |
| `npx expo prebuild --clean` | Deletes and regenerates native project directories | Confirm there are no manual native edits to preserve, or get explicit approval to discard/regenerate. |
| `npx expo run:ios` | Builds native iOS app and can invoke Xcode tooling | Use Apple Dev Skills for Xcode, simulator, signing, and Apple-platform validation details. |
| `npx expo run:android` | Builds native Android app and can invoke Gradle/emulator tooling | Confirm Android local build validation is appropriate and serialize with other build commands. |
| EAS build commands | Use remote build resources, project credentials, and account state | Require explicit user intent for cloud/device/store validation. |

## Source Refresh

Use official Expo documentation before relying on SDK 56 inline-module or type-generation details:

- [Expo inline modules reference](https://docs.expo.dev/modules/inline-modules-reference/)
- [Expo type generation reference](https://docs.expo.dev/modules/type-generation-reference/)
- [Continuous Native Generation](https://docs.expo.dev/workflow/continuous-native-generation/)
- [Development builds](https://docs.expo.dev/develop/development-builds/introduction/)
