---
name: gradle-agp-workflow
description: Inspect and maintain Android Gradle and Android Gradle Plugin workflows, including Gradle wrapper policy, AGP and Kotlin plugin versions, Java toolchains, Android SDK settings, namespaces, variants, flavors, signing config, version catalogs, dependencies, generated sources, build cache boundaries, and targeted assemble, test, lint, or bundle tasks.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Gradle-backed Android projects.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: android-build
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(java:*) Bash(./gradlew:*) Bash(gradle:*)
---

# Android Gradle And AGP Workflow

## Purpose

Keep Android build, dependency, variant, and packaging work grounded in the repository's real Gradle and Android Gradle Plugin configuration.

The practical decision is which Gradle files own the change, which Android modules and variants are affected, and which command proves the change without relying on machine-global state.

## Source Check

Use repo-local Gradle files, checked-out dependency sources, and Dash.app Gradle or Java docsets opportunistically. Use official documentation as authority for Android-specific and version-sensitive behavior:

- [Android build documentation](https://developer.android.com/build)
- [Android Gradle Plugin release notes](https://developer.android.com/build/releases/gradle-plugin)
- [Gradle User Manual](https://docs.gradle.org/current/userguide/userguide.html)
- [Gradle Java Toolchains](https://docs.gradle.org/current/userguide/toolchains.html)
- [Kotlin Gradle plugin documentation](https://kotlinlang.org/docs/gradle.html)

Translate documentation into concrete Gradle files, module names, variants, and commands.

## Inspection Workflow

1. Identify the Gradle owner:
   - `settings.gradle` or `settings.gradle.kts`
   - root `build.gradle` or `build.gradle.kts`
   - module `build.gradle` or `build.gradle.kts`
   - `gradle/libs.versions.toml`
   - `gradle.properties`
   - `gradle/wrapper/gradle-wrapper.properties`
2. Identify Android plugin shape:
   - `com.android.application`
   - `com.android.library`
   - `com.android.test`
   - Kotlin Android plugin aliases or IDs
3. Inspect toolchain and SDK policy:
   - AGP version
   - Gradle wrapper version
   - Kotlin plugin version
   - Java toolchain or source/target compatibility
   - `compileSdk`, `minSdk`, and target SDK policy
4. Inspect variants and packaging:
   - build types
   - product flavors
   - signing configs
   - namespace and application ID
   - app bundles, APKs, ProGuard/R8, and generated outputs
5. Inspect dependencies:
   - version catalogs
   - plugin management
   - dependency constraints
   - repositories
   - generated sources, annotation processors, KSP, KAPT, or codegen plugins

## Command Selection

Prefer repository wrappers and narrow module tasks:

```bash
./gradlew :app:assembleDebug
./gradlew :app:testDebugUnitTest
./gradlew :app:lintDebug
./gradlew :app:bundleRelease
```

Use the repository's documented commands when they differ. Run one Gradle command at a time.

## Dependency Rules

- Use fetchable repositories or package registries only.
- Do not commit machine-local SDK, Gradle, Maven, or file dependency paths.
- Preserve version catalog and plugin-management patterns.
- Keep dependency updates separate from feature work when the update has broad risk.
- Do not raise AGP, Gradle, Kotlin, Java, compile SDK, min SDK, or target SDK without explaining compatibility impact and validation.

## Failure Triage

Classify failures by phase:

- wrapper or Gradle startup
- plugin resolution
- SDK or toolchain selection
- dependency resolution
- manifest merge
- resource processing
- compile or KSP/KAPT/code generation
- unit test
- lint
- package, bundle, signing, or R8

Report the command, module, variant, phase, first meaningful error, likely cause, and smallest next check.

## Output Shape

Return:

1. `Build owner`: Gradle wrapper, AGP, Kotlin plugin, Java toolchain, and Android SDK policy.
2. `Affected modules`: module names, plugins, source sets, and variants.
3. `Dependency decision`: add, update, preserve, or remove.
4. `Packaging impact`: build types, flavors, signing, bundle, APK, R8, or no packaging impact.
5. `Validation path`: exact commands.
6. `Risk`: toolchain, dependency, generated-source, variant, signing, or release risk.

## Guardrails

- Do not run Gradle commands concurrently.
- Do not use machine-global Gradle when `./gradlew` exists.
- Do not change SDK, AGP, Gradle, Kotlin, or Java versions as drive-by cleanup.
- Do not make server-side JVM build decisions inside Android-owned modules.
- Do not start release publishing from a build-tooling pass.
