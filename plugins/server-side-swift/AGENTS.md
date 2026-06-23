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
- For Codex GUI worktree-first server-side Swift repos, keep local environment files portable and repo-owned. Start from `templates/codex-local-environments/`, keep paths repo-relative, and adjust executable names instead of committing machine-local paths.
- Use repo-local files, checked-out dependency sources, and Dash MCP or Dash HTTP for installed Swift package DocC before reaching for web docs. For Vapor and Hummingbird work, prefer local project and Dash docsets when present, then use official framework docs, GitHub releases, or tagged source when Dash/local coverage is missing, stale, or a public latest-release citation is needed.
- Use `bootstrap-hummingbird-service` for fresh Hummingbird services. Fresh Hummingbird services must start with the official `hb` CLI, use Hummingbird's built-in or generated configuration support, default to Fluent ORM with PostgreSQL, and include Docker Compose local PostgreSQL support unless Gale explicitly approves a project-specific exception.
- Use `bootstrap-vapor-service` for fresh Vapor services. Fresh Vapor services must start with the official Vapor CLI, use Vapor's built-in `Environment` system, default to Fluent ORM with PostgreSQL, and include Docker Compose local PostgreSQL support unless Gale explicitly approves a project-specific exception.
- Treat the Hummingbird template repository as fallback, source inspection, or explicit-template guidance rather than the first default.
- Treat Vapor 4 as the stable default while Vapor 5 is alpha. Vapor 5 is the planned future default once it has a stable release, stable docs, and a migration path that fits the target project; until then, use Vapor 5 only for explicit alpha evaluation, existing alpha-track repos, or migration-readiness audits grounded in current Vapor release notes and source tags.
- For Docker work, use current official Docker documentation and Swift Docker image sources before proposing Dockerfile, Compose, BuildKit, image, registry, or runtime changes.
- For Apple Containerization work, use the official `apple/containerization` and `apple/container` documentation for the relevant branch or release before proposing `container` CLI commands, Containerization Swift API use, host requirements, kernel setup, Rosetta behavior, image, registry, or runtime changes.
- Treat the Vapor Toolbox as project-creation and convenience tooling, not as a replacement for SwiftPM. Prefer `swift build`, `swift test`, `swift run`, and `swift run App serve` after a project exists unless current Vapor documentation says otherwise for the specific task.
- Keep server-side Swift examples portable across macOS and Linux unless the target repository documents an Apple-only service environment.
- Keep dependencies fetchable from GitHub, package registries, package-manager URLs, or other real remote repositories. Do not commit machine-local package paths.
- Do not add bundled services, local daemons, deployment scripts, template feeds, or MCP servers unless a later plan explicitly calls for that scope.
- Use the `server-swift-steward` custom-agent role only for explicit-trigger subagent workflows: broad read-heavy server-side Swift repo-maintenance scans, docs drift checks, and review-packet planning with proposed patch sets. Keep final edits, validation, commits, pushes, releases, migrations, and service execution in the main thread unless Gale explicitly approves a narrower write scope.
