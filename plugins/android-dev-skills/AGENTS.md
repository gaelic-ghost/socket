# AGENTS.md

This file is the Android Dev Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `android-dev-skills` is a monorepo-owned placeholder source for future Android, Kotlin, and Java Codex skills.
- Keep the repo intentionally minimal until the first real skill lands.
- [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) is the required plugin root today.

## Local Rules

- Do not present this repository as already shipping Android workflows before real skills exist.
- Prefer Kotlin-first Android guidance while preserving Java interoperability and Java-only project support when the repo being maintained requires it.
- Keep Android build and test guidance grounded in repo-local Gradle configuration, Android Gradle Plugin versions, and official Android documentation.
- When this repository changes the root Socket marketplace or root docs, update those root surfaces in the same pass.
