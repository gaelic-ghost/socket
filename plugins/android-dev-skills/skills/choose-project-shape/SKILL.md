---
name: choose-project-shape
description: Choose the right Android project, app, library, module, language, UI, build, test, lint, signing, release, or dependency-maintenance shape before implementation. Use when Android work needs routing across Kotlin, Java, Gradle, Android Gradle Plugin, Compose, XML views, emulator-aware validation, release readiness, or server-side JVM handoffs.
license: PolyForm-Noncommercial-1.0.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: android-planning
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(java:*) Bash(./gradlew:*) Bash(gradle:*) Bash(adb:*) Bash(aapt:*) Bash(aapt2:*)
---

# Choose Android Project Shape

## Purpose

Pick the smallest correct Android-owned shape before code changes begin.

The practical decision is whether the work belongs in an Android app, Android library, multi-module Android project, Kotlin-first implementation, Java-only maintenance, UI workflow, Gradle/AGP maintenance pass, test/lint pass, release-readiness pass, or a handoff to server-side JVM guidance.

## Source Check

Use repo-local files, checked-out dependency sources, and Dash.app docsets opportunistically when they cover the exact Android-adjacent surface, especially Gradle, Java, or command-line reference material. Treat current official Android and Google documentation as authoritative for Android-specific behavior, APIs, release policy, permissions, privacy, Play delivery, and version-sensitive guidance:

- [Android Developers documentation](https://developer.android.com/docs)
- [Android build and Android Gradle Plugin documentation](https://developer.android.com/build)
- [Jetpack Compose documentation](https://developer.android.com/compose)
- [Gradle User Manual](https://docs.gradle.org/current/userguide/userguide.html)
- [Kotlin documentation](https://kotlinlang.org/docs/home.html)
- [Java documentation](https://docs.oracle.com/en/java/)

Translate documentation into the concrete module, command, or implementation decision it changes.

## Classification Workflow

1. Inspect the repository shape:
   - `settings.gradle`, `settings.gradle.kts`, `build.gradle`, `build.gradle.kts`
   - `gradle/libs.versions.toml`, `gradle.properties`, `gradlew`
   - `AndroidManifest.xml`
   - `src/main/java`, `src/main/kotlin`, `src/main/res`
   - `src/test`, `src/androidTest`
   - Compose markers such as `androidx.compose`, `@Composable`, or Compose compiler configuration
   - XML view markers such as `layout/`, AppCompat, fragments, view binding, or data binding
   - CI, signing, lint, release, and Play delivery files
2. Identify the user-visible job:
   - Android app
   - Android library
   - multi-module Android project
   - Kotlin-first app or library
   - Java-only app or library
   - mixed Kotlin and Java app
   - Compose UI implementation
   - XML/AppCompat UI implementation
   - AndroidX library maintenance
   - Gradle/AGP, dependency, test, lint, signing, or release work
3. Route non-Android JVM work away from this plugin:
   - backend services
   - shared non-Android JVM libraries
   - server frameworks
   - Maven or SBT backend workflows
4. Choose language posture:
   - Preserve existing repository language choices.
   - Prefer Kotlin for new Android work when no repo default conflicts.
   - Preserve Java-only Android codebases unless the user asks for migration.
   - Ask before large Kotlin/Java migrations.
   - Explain interop when APIs cross Kotlin and Java.
5. Choose validation:
   - Gradle wrapper commands from the affected module first.
   - `test`, `lint`, `assemble`, `bundle`, or connected-device tasks only when they match the change.
   - Emulator/device validation as a handoff to the Android testing plugin, not duplicated here.

## Recommendations

### Android App

Use app guidance when the change affects activities, fragments, services, receivers, resources, UI, manifests, permissions, signing, packaging, or Play release behavior.

Handoff:

- `android-dev:build-kotlin-android` for Kotlin-first implementation
- `android-dev:java-android-workflow` for Java-only or Kotlin/Java interop work
- `android-dev:testing-lint-workflow` for tests and lint
- `android-dev:release-readiness-workflow` for release checks

### Android Library

Use library guidance when the output is an Android artifact consumed by apps or other Android modules. Keep public APIs, resources, manifests, and binary compatibility explicit.

### Gradle Or AGP Maintenance

Use `android-dev:gradle-agp-workflow` when build files, plugin versions, namespaces, variants, flavors, version catalogs, dependency resolution, generated sources, or Android SDK settings own the work.

### UI Implementation

Use `android-dev:build-kotlin-android` for common Compose and XML UI tasks. Keep future specialized Compose or XML skills as expansion points, not blockers for ordinary UI edits.

## Output Shape

Return:

1. `Chosen shape`: app, library, multi-module project, Kotlin implementation, Java maintenance, UI task, build task, test/lint task, release task, or handoff.
2. `Android owner`: module, package, source set, manifest, resources, or release surface.
3. `Language posture`: Kotlin-first, Java-only, mixed, or migration decision needed.
4. `Build owner`: Gradle wrapper, AGP version, affected modules, and variants.
5. `Validation path`: exact commands and any emulator/device handoff.
6. `Next skill`: the next Android or server-side JVM skill to use.

## Guardrails

- Do not make backend JVM work Android-owned just because it uses Gradle or Java.
- Do not rewrite Java Android code to Kotlin without user intent.
- Do not add new modules, flavors, or architecture layers without naming the near-term problem they solve.
- Do not start emulator, device, Play, or publish workflows by default.
- Do not trust Dash coverage for Android-specific behavior unless coverage and freshness are verified.
