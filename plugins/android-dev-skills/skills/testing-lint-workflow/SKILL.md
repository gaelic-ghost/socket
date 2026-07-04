---
name: testing-lint-workflow
description: Plan, run, filter, and triage Android tests and lint, including local unit tests, instrumentation and Compose UI test handoffs, Gradle variant tasks, lint configuration, lint baselines, failure explanations, emulator-aware validation routing, and readable next checks.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Android Gradle projects.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: android-testing
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(./gradlew:*) Bash(gradle:*) Bash(adb:*)
---

# Android Testing And Lint Workflow

## Purpose

Run the narrowest useful Android tests and lint checks, explain failures clearly, and route emulator/device validation to the Android testing plugin.

The practical decision is which module, source set, variant, and task prove the work without turning every change into a full device run.

## Source Check

Use repo-local Gradle files, test files, lint config, checked-out dependency sources, and Dash.app docsets opportunistically for exact Gradle or Java questions. Use official documentation as authority for Android-specific testing and lint behavior:

- [Test apps on Android](https://developer.android.com/training/testing)
- [Android build documentation](https://developer.android.com/build)
- [Android lint documentation](https://developer.android.com/studio/write/lint)
- [Jetpack Compose testing documentation](https://developer.android.com/develop/ui/compose/testing)
- [Gradle User Manual](https://docs.gradle.org/current/userguide/userguide.html)

Translate documentation into concrete test source sets, Gradle tasks, variants, and failure modes.

## Inspection Workflow

1. Identify test layout:
   - `src/test`
   - `src/androidTest`
   - Compose UI test files
   - fixture, fake, mock, and dependency-injection test support
2. Identify lint setup:
   - `lint.xml`
   - lint baselines
   - Gradle lint options
   - CI lint commands
3. Identify affected variants:
   - debug versus release
   - product flavors
   - application versus library modules
4. Identify validation level:
   - local unit tests for JVM-only behavior
   - instrumentation tests for Android runtime behavior
   - Compose UI tests for UI semantics and interactions
   - lint for resources, APIs, permissions, lifecycle, accessibility, and manifest issues
   - emulator/device validation handoff when runtime proof is required

## Command Selection

Start narrow, then widen:

```bash
./gradlew :app:testDebugUnitTest
./gradlew :app:lintDebug
./gradlew :app:connectedDebugAndroidTest
```

Use connected or managed-device tasks only when the user requested device validation or the change cannot be proved locally. If emulator operation is needed, hand off to the Android testing plugin instead of duplicating device-control steps here.

Run one Gradle command at a time.

## Failure Triage

Classify failures by first concrete break:

- Gradle setup or dependency resolution
- compile, KSP, KAPT, or generated-source failure
- local unit test failure
- instrumentation setup failure
- instrumentation assertion failure
- Compose UI semantics, synchronization, or interaction failure
- lint configuration or baseline failure
- lint finding from changed code
- emulator/device availability issue

Report the command, module, variant, source set, first meaningful error, likely cause, and smallest next check.

## Lint Policy

- Preserve existing baseline policy.
- Do not update a baseline just to hide a new issue.
- Treat accessibility, permissions, exported components, manifest, resource, and API-level findings as user-facing risk until understood.
- Keep suppressions local and justified when the repo already allows suppressions.

## Output Shape

Return:

1. `Test scope`: module, source set, variant, unit, instrumentation, Compose UI, or lint.
2. `Commands`: exact commands run or recommended.
3. `Result`: pass, fail, or skipped with concrete reason.
4. `Failure mode`: setup, compile, unit, instrumentation, Compose UI, lint config, lint finding, or emulator/device issue.
5. `Next check`: smallest code, test, lint, Gradle, or Android testing plugin handoff.

## Guardrails

- Do not run broad device tests first when unit tests or lint prove the change.
- Do not start emulator or device automation directly from this skill.
- Do not rewrite or remove lint baselines without explaining the policy impact.
- Do not weaken tests to match broken behavior.
- Do not run Gradle commands concurrently.
