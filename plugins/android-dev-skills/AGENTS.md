# AGENTS.md

This file is the Android Dev Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `android-dev-skills` is a monorepo-owned Socket child source for Android, Kotlin, and Java Codex skills, and should remain Socket-owned for the foreseeable future.
- Root [`skills/`](./skills/) is the authored workflow surface.
- The repo root is the Codex plugin root through [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).

## Local Rules

- Prefer Kotlin-first Android guidance while preserving Java interoperability and Java-only project support when the repo being maintained requires it.
- Make Kotlin Android guidance deep enough for common Compose and XML UI implementation tasks, including state, resources, accessibility labels, themes, lists, forms, navigation touchpoints, and focused validation.
- Keep Android build and test guidance grounded in repo-local Gradle configuration, Android Gradle Plugin versions, checked-out dependency sources, relevant Dash.app docsets when installed, and official Android documentation.
- Treat official Android Developers, Android Gradle Plugin, Jetpack Compose, AndroidX, Play delivery, Kotlin, Java, and Gradle documentation as authoritative when Dash coverage is missing, stale, or only adjacent.
- Include release automation routing in release-readiness guidance when a repository already owns Gradle, CI, Fastlane, Play Developer Publishing API, or similar publish machinery, but do not start publish workflows by default.
- When this repository changes the root Socket marketplace or root docs, update those root surfaces in the same pass.
