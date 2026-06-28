---
name: build-kotlin-android
description: Implement Kotlin-first Android app or library changes, including activities, fragments, services, receivers, Compose UI, XML/AppCompat UI, AndroidX, lifecycle-aware coroutines, state, persistence touchpoints, resources, accessibility labels, navigation touchpoints, tests, lint, and validation while preserving repo conventions.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Kotlin-first Android projects.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: android-implementation
allowed-tools: Read Edit Bash(rg:*) Bash(git:*) Bash(./gradlew:*) Bash(gradle:*)
---

# Build Kotlin Android

## Purpose

Implement Kotlin-first Android changes while preserving the repository's architecture, UI system, resources, and validation path.

The skill should be deep enough for common Compose and XML UI work without pretending to replace future specialized UI skills.

## Source Check

Use repo-local Android files, checked-out dependency sources, and Dash.app docsets opportunistically when they cover exact Gradle, Java, or local command questions. Use official documentation as authority for Android APIs, Compose, AndroidX, lifecycle, resources, accessibility, and version-sensitive behavior:

- [Android Developers documentation](https://developer.android.com/docs)
- [Jetpack Compose documentation](https://developer.android.com/compose)
- [Android app architecture guide](https://developer.android.com/topic/architecture)
- [Kotlin documentation](https://kotlinlang.org/docs/home.html)
- [AndroidX documentation](https://developer.android.com/jetpack/androidx)

Translate documentation into repository-specific code, resource, lifecycle, or validation decisions.

## Implementation Workflow

1. Inspect existing conventions:
   - package structure and module boundaries
   - activities, fragments, services, receivers, workers, or navigation owners
   - Compose versus XML/AppCompat ownership
   - ViewModel, state holder, repository, dependency injection, persistence, and background-work patterns
   - resource naming, theming, strings, dimensions, and accessibility conventions
   - existing tests and lint baselines
2. Preserve architecture:
   - keep UI, state, domain, persistence, and platform boundaries consistent
   - add shared helpers only when they remove real duplication or match an existing local pattern
   - avoid new architecture layers unless the current shape cannot support the requested work
3. Implement common Compose tasks:
   - compose screens from small functions with explicit state and callbacks
   - preserve state hoisting and unidirectional data flow
   - update previews when the repo already uses them
   - use modifiers, lists, forms, theming, and semantics consistently
   - keep navigation touchpoints aligned with existing navigation owners
4. Implement common XML/AppCompat tasks:
   - update layouts, resources, themes, strings, and accessibility labels together
   - use view binding or data binding only when the repo already does
   - keep RecyclerView, adapter, fragment, and activity wiring aligned with existing code
   - avoid mixing Compose into XML screens unless the repo already has an interop pattern or the user approves it
5. Implement platform work:
   - keep lifecycle-aware coroutines scoped correctly
   - keep permissions, manifests, and background work explicit
   - preserve nullability and Java interop annotations for public APIs
6. Validate narrowly:
   - compile or assemble the affected module
   - run targeted unit tests
   - run lint for affected variants when UI/resources/platform APIs changed
   - hand off emulator/device checks to the Android testing plugin when needed

## Command Selection

Choose commands from the repo's Gradle tasks:

```bash
./gradlew :app:assembleDebug
./gradlew :app:testDebugUnitTest
./gradlew :app:lintDebug
```

Use narrower module or variant tasks when the project defines them.

## Output Shape

Return:

1. `Implementation surface`: module, source set, packages, UI files, resources, manifest, or tests.
2. `UI path`: Compose, XML/AppCompat, interop, or no UI.
3. `State and lifecycle`: state owner, coroutine scope, lifecycle owner, persistence or background-work impact.
4. `Validation path`: commands run or skipped with concrete reasons.
5. `Handoffs`: Java interop, Gradle/AGP, testing/lint, release readiness, or emulator/device validation.

## Guardrails

- Do not migrate Java to Kotlin without user intent.
- Do not mix Compose and XML patterns casually.
- Do not introduce a new dependency injection, navigation, persistence, or architecture framework without an explicit decision.
- Do not hardcode user-facing text that belongs in resources unless the repo already does so.
- Do not ignore accessibility labels, content descriptions, focus behavior, or dynamic text when changing UI.
- Do not start emulator or device automation from this skill.
