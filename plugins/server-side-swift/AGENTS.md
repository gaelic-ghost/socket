# AGENTS.md

This file is the Server-Side Swift child-plugin override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `server-side-swift` is a monorepo-owned Socket child and the canonical source of truth for shipped server-side Swift workflow skills in this repository.
- Root [`skills/`](./skills/) is the authored workflow surface.
- The repo root is the Codex plugin root through [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).
- Treat `apple-dev-skills` as the Apple-platform specialist layer and `server-side-swift` as the server-side Swift layer. Do not put Vapor, SwiftNIO service-hosting, Linux deployment, database, or HTTP server guidance into Apple Dev Skills unless the task is specifically about Apple-platform integration.

## Local Rules

- Match the `socket` shared semantic version exactly; use the Socket root release workflow for version inventory and bumps.
- Prefer Swift Package Manager as the source of truth for server-side Swift package structure, dependencies, builds, tests, and run commands.
- Use official framework documentation first for server-side Swift libraries and tools. For Vapor work, use the official Vapor docs before proposing CLI usage, app structure, migrations, deployment, or runtime changes. For Hummingbird work, use the official Hummingbird docs before proposing app setup, routes, middleware, request contexts, testing, service lifecycle, deployment, or runtime changes.
- Treat the Vapor Toolbox as project-creation and convenience tooling, not as a replacement for SwiftPM. Prefer `swift build`, `swift test`, `swift run`, and `swift run App serve` after a project exists unless current Vapor documentation says otherwise for the specific task.
- Keep server-side Swift examples portable across macOS and Linux unless the target repository documents an Apple-only service environment.
- Keep dependencies fetchable from GitHub, package registries, package-manager URLs, or other real remote repositories. Do not commit machine-local package paths.
- Do not add bundled services, local daemons, deployment scripts, template feeds, or MCP servers unless a later plan explicitly calls for that scope.
