---
name: release-readiness-workflow
description: Check Android release readiness without publishing by default, including versionCode and versionName, signing and keystore boundaries, release build types, R8/ProGuard, mapping outputs, app bundles, APKs, Play delivery handoffs, privacy, permissions, changelogs, and repository-owned release automation routing through Gradle, CI, Fastlane, or Play Developer Publishing API clients.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Android release-preparation surfaces.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: android-release
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(./gradlew:*) Bash(gradle:*) Bash(gh:*)
---

# Android Release Readiness Workflow

## Purpose

Check whether an Android app or library is ready for release without starting a publish workflow by default.

The practical decision is which version, signing, packaging, policy, changelog, and automation surfaces must be verified before a human or repo-owned release system publishes artifacts.

## Source Check

Use repo-local Gradle files, release docs, CI workflows, Fastlane files, checked-out automation sources, and Dash.app docsets opportunistically for exact Gradle or Java questions. Use official documentation as authority for Android-specific release, signing, privacy, permissions, and Play behavior:

- [Prepare and roll out a release](https://developer.android.com/studio/publish)
- [Android App Bundles](https://developer.android.com/guide/app-bundle)
- [Sign your app](https://developer.android.com/studio/publish/app-signing)
- [Shrink, obfuscate, and optimize your app](https://developer.android.com/build/shrink-code)
- [Play Developer API](https://developers.google.com/android-publisher)
- [Fastlane supply documentation](https://docs.fastlane.tools/actions/supply/)

Translate documentation into concrete release files, commands, artifacts, and gates.

## Inspection Workflow

1. Identify release ownership:
   - app module
   - release build type
   - product flavors
   - version code and version name
   - changelog or release notes
   - CI release workflow
   - Fastlane, Gradle Play Publisher, Play Developer Publishing API client, or custom scripts
2. Inspect signing boundaries:
   - signing config names
   - keystore references
   - environment variable names
   - secret-handling docs
   - local placeholder configs
3. Inspect packaging:
   - app bundle tasks
   - APK tasks
   - R8/ProGuard files
   - mapping output expectations
   - native debug symbols if present
4. Inspect policy-sensitive surfaces:
   - permissions
   - exported components
   - privacy disclosures
   - target SDK requirements
   - Play delivery tracks and rollout docs
5. Route automation:
   - identify the repo-owned release command or CI job
   - explain required credentials or approvals
   - stop before publish unless the user explicitly requested the publish action

## Command Selection

Prefer dry, local, or artifact-building checks first:

```bash
./gradlew :app:lintRelease
./gradlew :app:assembleRelease
./gradlew :app:bundleRelease
```

Use repository-documented release commands when they exist. Treat commands that upload, promote, submit for review, or publish as explicit approval-gated actions.

## Automation Routing

When a repository already owns release automation, report:

- automation owner: Gradle, CI, Fastlane, Play Developer Publishing API client, or custom script
- trigger: local command, CI workflow dispatch, tag, branch, or manual approval
- credentials: environment variable names or secret names, without printing secret values
- artifacts: AAB, APK, mapping file, native symbols, changelog, or release notes
- publish boundary: the exact command or click that would upload, promote, or release

## Output Shape

Return:

1. `Release surface`: app or library module, variant, flavor, and artifact type.
2. `Versioning`: version code, version name, changelog, and policy status.
3. `Signing`: signing config, secret boundary, and local-safe checks.
4. `Packaging`: AAB, APK, R8/ProGuard, mapping, and symbol outputs.
5. `Automation route`: Gradle, CI, Fastlane, Play API, custom script, or none found.
6. `Validation path`: commands run or recommended.
7. `Publish boundary`: what was deliberately not run without explicit approval.

## Guardrails

- Do not publish, upload, promote, submit for review, or change Play tracks by default.
- Do not print keystore passwords, service account keys, tokens, or signing secrets.
- Do not invent release automation when the repo has no release owner.
- Do not bump version code, version name, target SDK, or signing config without explaining the release impact.
- Do not remove R8/ProGuard rules or mapping outputs casually.
