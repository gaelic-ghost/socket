# AGENTS.md

This file is the Web Dev Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `web-dev-skills` hosts focused web and Expo-adjacent Codex skills.
- Keep the repo intentionally minimal around real shipped workflows.
- [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) is the required plugin root today.

## Local Rules

- Do not recreate nested repo-local marketplace wiring or bundled copies of other plugin repos here.
- Prefer adding actual skill content before expanding docs or workflow complexity.
- Use repo-local files, checked-out dependency sources, and Dash MCP or Dash HTTP for installed TypeScript, JavaScript, Node.js, React, CSS, HTML, Expo, and related web docsets before reaching for web docs. Use official project documentation when Dash/local coverage is missing, stale, or a public latest-release citation is needed.

## Expo And React Native Native Boundaries

- Treat Expo SDK 56+ inline modules and `expo-type-information` as experimental surfaces that require current official Expo documentation before claims or edits.
- Keep Expo inline native modules narrow and app-specific. Prefer standalone Expo modules, config plugins, existing packages, or direct native project edits when those shapes better match reuse, generated-project customization, or bare native ownership.
- Inspect the live Expo app before changing app config, generated native projects, generated TypeScript interfaces, Swift, Kotlin, or package dependencies.
- Do not run package installs, `npx expo prebuild --clean`, native builds, EAS builds, or generated-project rewrites until the likely side effects are identified and the user has authorized that level of change.
- Route Swift API design, Apple framework behavior, Xcode validation, simulators, signing, capabilities, entitlements, App Store behavior, and Apple platform availability claims through Apple Dev Skills instead of copying Apple-platform playbooks here.
- Validate Expo, TypeScript, Xcode, Gradle, SwiftPM, and package-manager commands serially. Never run build or test tools concurrently.
