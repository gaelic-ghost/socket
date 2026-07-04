---
name: vapor-server-workflow
description: Plan, build, run, test, and diagnose existing Vapor server-side Swift services using current Vapor documentation, SwiftPM-first commands, routing, middleware, Fluent migrations, Vapor 5 alpha adoption posture, environment configuration, and deployment handoffs. Hand fresh service creation to bootstrap-vapor-service.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Vapor, SwiftPM, and server-side Swift projects on macOS or Linux.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-vapor
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(brew:*) Bash(swift:*) Bash(vapor:*) Bash(curl:*)
---

# Vapor Server Workflow

## Purpose

Build, modify, run, or diagnose a Vapor service without confusing Vapor-specific server behavior with generic Swift package work or Apple-platform Xcode work.

The practical decision is what the HTTP service exposes, which target owns the Vapor app, where domain logic lives, how configuration reaches the service, how migrations are run, and which command proves the app starts or behaves correctly.

## When To Use

- Use `bootstrap-vapor-service` when creating a new Vapor service with the Vapor Toolbox.
- Use this skill when evaluating or migrating toward Vapor 5 alpha, but keep alpha work explicitly experimental until Vapor publishes a stable Vapor 5 release and migration path.
- Use this skill when modifying Vapor routes, route groups, controllers, middleware, app configuration, commands, migrations, or local server behavior.
- Use this skill when diagnosing `vapor new`, `swift build`, `swift test`, `swift run`, `swift run App serve`, migration, or local HTTP failures in a Vapor project.
- Use this skill when deciding whether an existing Swift package should become a Vapor service or stay a library consumed by one.
- Do not use this skill for generic Swift package work that has no Vapor-specific behavior. Hand that work to a SwiftPM package workflow when available.
- Do not use this skill for Apple-platform app, simulator, preview, or Xcode project membership work.
- Do not use this skill for non-Vapor server-side Swift frameworks unless the task is a comparison or migration involving Vapor.

## Source Check

Use repo-local Swift files, checked-out dependency sources, Dash MCP or Dash HTTP for installed Vapor DocC first, then official Vapor documentation when Dash/local coverage is missing or stale:

- [Vapor installation](https://docs.vapor.codes/install/macos/)
- [Vapor Hello, world](https://docs.vapor.codes/getting-started/hello-world/)
- [Vapor server configuration](https://docs.vapor.codes/advanced/server/)
- [Vapor commands](https://docs.vapor.codes/advanced/commands/)
- [Vapor environment](https://docs.vapor.codes/basics/environment/)
- [Vapor Fluent migrations](https://docs.vapor.codes/fluent/migration/)
- [Vapor Fly deployment](https://docs.vapor.codes/deploy/fly/)
- [Vapor GitHub organization](https://github.com/vapor)
- [Vapor repository](https://github.com/vapor/vapor)
- [Vapor 5 Alpha 1 release](https://github.com/vapor/vapor/releases/tag/5.0.0-alpha.1)
- [Vapor 5 alpha source tag](https://github.com/vapor/vapor/tree/5.0.0-alpha.1)
- [Vapor Community GitHub organization](https://github.com/vapor-community)

Use Swift.org or Swift Package Manager documentation for Swift toolchain and package behavior when Vapor docs do not own the rule being used.

For Vapor 5, treat GitHub releases and tagged source as the authoritative alpha surface until official Vapor 5 documentation and migration guides exist. Check current release notes before recommending alpha APIs, package products, macros, server internals, platform requirements, or migration steps.

## Planning Workflow

1. Inspect project shape:
   - `Package.swift`
   - executable target name, usually `App`
   - `Sources/App/configure.swift`
   - `Sources/App/routes.swift`
   - controllers, models, migrations, middleware, and tests
   - Docker, deployment, or environment files when present
2. Identify the service job:
   - JSON API
   - website or Leaf-rendered app
   - webhook receiver
   - internal service
   - background command plus HTTP health surface
3. Confirm the documented command path before running or recommending commands.
4. Keep SwiftPM as the default execution surface after creation:
   - hand fresh service creation to `bootstrap-vapor-service`
   - build with `swift build`
   - test with `swift test`
   - run locally with `swift run` or `swift run App serve`
   - inspect Vapor app commands with `swift run App --help`
   - inspect serve options with `swift run App serve --help`
5. Keep domain logic outside route handlers when it has meaningful behavior.
6. Keep configuration explicit and environment-safe.
7. Add tests at the smallest level that proves behavior.
8. Validate with the narrowest useful SwiftPM, Vapor app, or HTTP check.

## Vapor Ecosystem Package Preference

When a Vapor service needs framework-adjacent behavior, prefer maintained packages from the official `vapor` GitHub organization when they fit the need and match the project's Vapor major version.

Check official Vapor packages first for:

- ORM, migrations, and database drivers: Fluent, Fluent drivers, FluentKit, SQLKit, Postgres, MySQL, SQLite, and MongoDB packages
- authentication and tokens: Authentication, JWT, and JWTKit
- background jobs: Queues and official queue drivers
- cache or ephemeral state: Redis or the repository's existing cache choice
- templating and HTML: Leaf and LeafKit
- OpenAPI-backed servers: OpenAPIVapor
- WebSocket, multipart, routing, console, APNS, templates, and Vapor Toolbox support

Check `vapor-community` next when official Vapor packages do not cover the need and the community package is maintained, current, and a better fit than a generic third-party package. Common examples include HTML rendering, OAuth or identity flows, Stripe, SendGrid, Mailgun, Wallet, CSRF, SQLKit extras, Valkey support, Lambda runtime support, and service-specific providers.

Before recommending or adding any package:

- verify current documentation or source, repository maintenance status, and package version compatibility
- inspect the existing `Package.swift` dependency style, exact-version policy, and target ownership
- choose the narrowest package that fits the service behavior instead of adding a broad framework around one feature
- explain why the aligned Vapor or Vapor Community package fits better than a generic Swift package or custom code
- avoid archived packages, stale Vapor-major-version packages, or packages that force unrelated architecture changes

## Project Creation Handoff

Fresh Vapor services belong to `bootstrap-vapor-service`. That bootstrap path starts with the official Vapor CLI, uses Vapor's built-in `Environment` system, defaults to Fluent ORM with PostgreSQL, creates a Docker Compose PostgreSQL dependency surface, and installs repo-local `AGENTS.md` guidance for the generated service.

Use this default creation path only as part of the bootstrap workflow:

```bash
brew install vapor
vapor new MyService
cd MyService
```

Use `vapor new MyService -n` only when the user wants the non-interactive bare template and the documented options fit the task. Otherwise, preserve the interactive template questions because they choose real project features such as Fluent, database support, or Leaf. For Gale's default Vapor bootstrap, answer the interactive prompts to include Fluent and choose PostgreSQL unless Gale explicitly approves a project-specific exception.

## Vapor 5 Alpha Adoption

Vapor 4 remains the normal stable default for new production services, existing app maintenance, package recommendations, Fluent migrations, and docs-backed examples while Vapor 5 is alpha.

Vapor 5 is the planned future default once Vapor publishes a stable Vapor 5 release, stable docs, and a migration path that fits the target project. Until then, use Vapor 5 only when the user explicitly asks to evaluate alpha behavior, the repository is already intentionally tracking Vapor 5, or the task is a migration-readiness audit.

When evaluating Vapor 5 alpha:

- say that the current official release is a prerelease alpha, not stable Vapor behavior
- read the current Vapor 5 release notes and tagged source before making API claims
- prefer a branch, experiment package, or small spike over replacing a working Vapor 4 service in place
- pin exact prerelease versions or source revisions used for the experiment
- inventory Vapor 4 dependencies such as Fluent, Leaf, Queues, Auth, JWT, OpenAPIVapor, Vapor Community packages, middleware, and custom commands before assuming they have Vapor 5 equivalents
- look for source-level changes around structured concurrency, type-safe routing, macros, server internals, testing, platform requirements, and package products
- keep production runbooks, deployment docs, and migration commands on Vapor 4 unless the repo has already chosen a Vapor 5 alpha track

Do not present Vapor 5 alpha examples as stable documentation. If a Vapor 5 API is only visible in source or release notes, say that plainly and include the exact tag or release used.

## Codex GUI Local Environment

When a Vapor repo should be easy to use from Codex GUI Worktree mode, start from `templates/codex-local-environments/vapor.toml`. Keep the copied file under `.codex/environments/`, keep paths repo-relative, and adjust the executable name only when the app target is not `App`.

## App Structure

For typical Vapor 4 projects:

- `configure.swift` owns app-wide setup such as middleware, databases, migrations, commands, encoders, and services.
- `routes.swift` owns route registration and should stay readable.
- Controllers are useful when a route group has enough behavior to deserve a named owner.
- Models and migrations should stay paired closely enough that schema changes are easy to audit.
- Domain transformations that can be tested without a running HTTP server should live outside route closures.

Do not introduce a service, repository, coordinator, or manager unless it removes a concrete duplication, testability problem, or dependency boundary issue in the current service.

## Configuration And Secrets

Do not commit secrets.

Use Vapor's built-in `Environment` system for runtime environment and process settings. Use environment variables for deployment-sensitive values. For local development, follow existing repo conventions first. If none exist, recommend committed safe defaults and ignored local overrides rather than hard-coded credentials.

When diagnosing configuration, state which variable is missing, where Vapor reads it, which command was running, and what local or deployment setup likely needs correction.

## Routes, Middleware, And Errors

When adding or changing routes:

- name the route method and path
- describe request body, query, path parameters, response body, and status codes
- keep validation errors explicit and user-readable
- avoid blocking work on the event loop
- use async APIs where the project already uses async handlers
- prefer typed request and response models over ad hoc dictionaries

When adding middleware:

- identify whether it is global, grouped, or route-specific
- explain the request or response behavior it changes
- include a small test or manual check that proves the middleware is active

## Fluent Migrations

When a Vapor project uses Fluent:

- define schema changes as migrations
- register migrations in app configuration
- run migrations with `swift run App migrate`
- revert only when the user understands data-loss risk and the migration supports it
- use `swift run App migrate --revert` as the documented command form when a revert is intentionally needed

Do not edit a database manually as a substitute for a migration unless the task is explicitly an emergency data repair and the user accepts that risk.

## Testing

Choose the smallest test that proves the behavior:

- pure Swift test for domain logic
- handler or controller test for request and response behavior
- migration test when schema setup is the risk
- local HTTP check only when runtime routing, middleware, or server binding matters

Prefer `swift test` for normal validation. Use `curl` against a locally running server only when the user asked for runtime validation or the change cannot be proven through tests alone.

## Deployment Handoffs

Keep deployment guidance grounded in the repository's existing target first.

When no target exists, distinguish:

- local development run
- Docker image or Compose workflow
- Fly.io deployment
- Linux process manager or system service
- hosted platform deployment
- database migration timing

Do not add Docker, CI, process-manager, or cloud deployment files as part of a route or local development change unless the user asked for deployment scope.

Use `fly-io-deployment-workflow` when the task involves `fly.toml`, `fly launch`, `fly deploy`, Fly secrets, Fly Postgres attachment, Fly health checks, Fly process groups, or production port binding for a Vapor service. Keep Vapor route, command, environment, server binding, and Fluent migration behavior here; hand Fly-specific config and deploy validation to the Fly workflow.

## Output Shape

Return:

1. `Service shape`: package root, executable target, app configuration, route owners, and test surface.
2. `Vapor docs used`: specific official docs relied on for CLI, app, migration, or runtime behavior.
3. `Command path`: exact commands run or recommended.
4. `Behavior`: routes, inputs, outputs, errors, middleware, migrations, or configuration changes.
5. `Validation`: build, test, serve, migrate, or HTTP check results.
6. `Handoffs`: SwiftPM, testing, Apple-platform, deployment, or database follow-up when the task crosses this skill's boundary.

## Guardrails

- Do not treat Xcode as required for Vapor service work unless the repository already uses Xcode-specific workflow.
- Do not let route closures accumulate unrelated business rules.
- Do not commit secrets, machine-local paths, or deployment credentials.
- Do not run migration reverts or destructive database commands without explicit user approval.
- Do not claim Vapor CLI behavior from memory when current official docs can be checked.
- Do not use obsolete Vapor Toolbox command habits when SwiftPM is the documented path for the task.
- Do not bootstrap fresh Vapor services manually; use `bootstrap-vapor-service` unless Gale explicitly approves an exception.
