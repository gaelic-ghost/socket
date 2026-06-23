# AGENTS.md

This file is the Server-Side JVM child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `server-side-jvm` is a monorepo-owned placeholder source for future server-side JVM, Java, Scala, and Clojure Codex skills.
- Keep the repo intentionally minimal until the first real skill lands.
- [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) is the required plugin root today.

## Local Rules

- Do not present this repository as already shipping server-side JVM workflows before real skills exist.
- Treat Java and Scala as equal first-party JVM languages, and leave room for future Clojure skills without renaming the plugin.
- Prefer functional style where it fits the selected language and framework, especially for Scala and future Clojure guidance, without forcing functional patterns into Java codebases that are deliberately object-oriented.
- Keep JVM build, test, and dependency guidance grounded in repo-local Gradle, Maven, or SBT configuration, checked-out dependency sources, Dash MCP or Dash HTTP when installed Java, Gradle, Maven, or SBT docsets cover the question, and canonical upstream documentation when Dash/local coverage is missing or stale.
- Keep Android app, Android Gradle Plugin, emulator, device, and release guidance in `android-dev-skills`. This plugin should only own Android-adjacent work when the repository is really a server-side JVM service, backend, or shared non-Android JVM library.
- When this repository changes the root Socket marketplace or root docs, update those root surfaces in the same pass.
