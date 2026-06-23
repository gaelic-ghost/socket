---
name: bootstrap-vapor-service
description: Bootstrap new Vapor server-side Swift services with the official Vapor CLI, Vapor Environment, Fluent ORM, PostgreSQL, Docker Compose local dependencies, generated AGENTS guidance, and SwiftPM validation. Use when creating a fresh Vapor service from scratch or maintaining this skill's bootstrap defaults.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Vapor, Vapor Toolbox, SwiftPM, Fluent, PostgreSQL, and Docker-backed local development on macOS or Linux.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-bootstrap
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(brew:*) Bash(swift:*) Bash(vapor:*) Bash(docker:*) Bash(curl:*)
---

# Bootstrap Vapor Service

## Purpose

Create a new Vapor service repository from nothing to a consistent, database-backed local baseline.

The practical decision is not whether Vapor should use the CLI, Fluent, PostgreSQL, or its built-in `Environment` system. The default is already chosen: start with the official Vapor CLI, use Vapor's `Environment` API for runtime environment and process settings, choose Fluent ORM with PostgreSQL, and provide a Docker Compose Postgres service for local development.

## When To Use

- Use this skill when the user wants to start, begin, create, scaffold, or bootstrap a new Vapor service.
- Use this skill when a new Vapor service should receive durable repo-local `AGENTS.md` guidance.
- Use this skill when the user asks for the standard Vapor service baseline, including Fluent ORM, PostgreSQL, and local container support.
- Use this skill when maintaining the bootstrap defaults for future Vapor services.
- Do not use this skill for ordinary routes, controllers, middleware, commands, migrations, or tests in an existing Vapor service. Use `vapor-server-workflow`.
- Do not use this skill for existing persistence changes that are not part of initial bootstrap. Use `persistence-workflow`.
- Do not use this skill for generic Docker image production work. Use `docker-workflow`.
- Do not substitute a manual SwiftPM scaffold, a non-Fluent database layer, SQLite, or non-container local database setup unless the user explicitly approves that exception for the project.

## Source Check

Use official Vapor documentation first:

- [Vapor installation](https://docs.vapor.codes/install/macos/)
- [Vapor Hello, world](https://docs.vapor.codes/getting-started/hello-world/)
- [Vapor Environment](https://docs.vapor.codes/basics/environment/)
- [Vapor Fluent overview](https://docs.vapor.codes/fluent/overview/)
- [Vapor Fluent migrations](https://docs.vapor.codes/fluent/migration/)
- [Vapor Docker deploys](https://docs.vapor.codes/deploy/docker/)
- [Vapor GitHub organization](https://github.com/vapor)

Use SwiftPM and Swift.org documentation for package, toolchain, and Linux behavior when Vapor docs do not own the rule being used.

## Single-Path Workflow

1. Collect the required inputs:
   - `name`
   - `destination`
   - optional `database_name`
   - optional `database_user`
   - optional `database_password`
   - optional `skip_validation`
2. Verify prerequisites:
   - `swift`
   - `git`
   - `vapor`
   - Docker-compatible runtime only when Compose validation is requested
3. Create the service with the official CLI:
   ```bash
   vapor new <name>
   ```
4. Answer the CLI prompts using the standard default:
   - include Fluent
   - choose PostgreSQL as the database driver
   - keep Vapor 4 as the stable default unless the user explicitly asks for Vapor 5 alpha evaluation
5. Preserve Vapor's generated application structure:
   - `Sources/App/configure.swift`
   - `Sources/App/routes.swift`
   - generated model, migration, and test shape when present
6. Use Vapor `Environment` for runtime behavior:
   - keep environment-specific branching on `app.environment`
   - use `Environment.get` or `Environment.process` for process settings
   - keep committed `.env` content as a safe template only
   - keep `.env.*` overrides ignored when they may contain local or secret values
7. Add or verify local database container support:
   - create or preserve `compose.yaml` with a `postgres` service
   - use safe development-only defaults
   - use a named volume for database storage
   - align host, port, database, user, and password with Vapor's local `.env` template
8. Install generated repo guidance:
   - copy `assets/AGENTS.md` into the new repository root
   - update placeholders for project name, database name, and validation commands
   - keep the generated guidance local to the new service because this plugin's own `AGENTS.md` is not visible inside ordinary service repositories
9. Install Codex GUI local environment guidance when desired:
   - copy `templates/codex-local-environments/vapor.toml` into `.codex/environments/vapor.toml`
   - adjust the executable name only when the app target is not `App`
10. Validate the scaffold:
   - `swift build`
   - `swift test`
   - `docker compose config`
   - optional `docker compose up -d postgres`
   - optional `swift run App migrate` after confirming the generated database config and migration list
   - optional `swift run App serve` only when runtime startup validation is requested
11. Return the created path, exact commands, environment source, database defaults, validation results, and next handoff.

## Defaults

- service framework: Vapor
- creation command: `vapor new <name>`
- Vapor version posture: Vapor 4 stable default; Vapor 5 alpha only by explicit request
- persistence: Fluent ORM
- database: PostgreSQL
- local dependency runtime: Docker Compose Postgres service
- generated guidance: root `AGENTS.md`
- app configuration: Vapor `Environment`
- development database defaults:
  - host: `localhost`
  - port: `5432`
  - database: normalized service name
  - username: normalized service name
  - password: `development-password`
- validation runs unless `skip_validation` is requested

## Outputs

- `status`
  - `success`: service scaffold, repo guidance, and requested validation completed
  - `blocked`: prerequisites, target-directory constraints, or unsupported CLI choices prevented the run
  - `failed`: the scaffold started but generation, dependency wiring, or validation failed
- `path_type`
  - `primary`: official Vapor CLI bootstrap path
  - `fallback`: non-mutating guidance only because the CLI path could not safely run
- `output`
  - resolved service path
  - Vapor app target name
  - Vapor `Environment` and dotenv source
  - Fluent and PostgreSQL dependencies added or confirmed
  - `compose.yaml` shape
  - generated `AGENTS.md` installed
  - validation result
  - one concise next handoff

## Guardrails

- Strong default: use `vapor new`, Vapor `Environment`, Fluent ORM, PostgreSQL, and Docker Compose for every fresh Vapor service unless the user explicitly approves a project-specific exception.
- Do not hand-roll a new SwiftPM project as the default Vapor bootstrap path.
- Do not bypass Vapor `Environment` with a second settings framework for standard runtime configuration.
- Do not choose SQLite, MySQL, direct SQL, or non-Fluent persistence as the default bootstrap path.
- Do not commit secrets, real database passwords, `.env.*` files with sensitive values, machine-local paths, or private dependency URLs.
- Do not run destructive migrations, database drops, volume deletion, or migration reverts without explicit user approval.
- Do not claim Vapor CLI behavior, generated file layouts, Fluent driver names, or migration commands from memory; check current Vapor docs, `vapor --help`, or generated scaffold files.
- Do not add production Docker image files unless the user asks for containerized deployment or the target repo already treats a production image as part of its baseline.

## Fallbacks And Handoffs

- If `vapor` is missing and Homebrew is acceptable, install with:
  ```bash
  brew install vapor
  ```
- If `vapor` is unavailable and cannot be installed, stop with a non-mutating fallback plan. Do not silently switch to a manual SwiftPM scaffold.
- After successful bootstrap, use `vapor-server-workflow` for routes, controllers, middleware, commands, app configuration, and Vapor tests.
- Use `persistence-workflow` for models, migrations, query design, transactions, and database-backed tests after the initial baseline exists.
- Use `docker-workflow` for production Dockerfiles, multi-stage images, image validation, registries, or container deployment.
- Use `fly-io-deployment-workflow` for Fly.io apps, Fly Postgres, secrets, health checks, and deploy validation.

## References

- `assets/AGENTS.md`
