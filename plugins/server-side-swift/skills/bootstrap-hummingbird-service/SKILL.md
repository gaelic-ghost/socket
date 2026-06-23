---
name: bootstrap-hummingbird-service
description: Bootstrap new Hummingbird server-side Swift services with the official hb CLI, Hummingbird configuration support, Fluent ORM, PostgreSQL, CLI-generated Docker files, Docker Compose local dependencies, generated AGENTS guidance, and SwiftPM validation. Use when creating a fresh Hummingbird service from scratch or maintaining this skill's bootstrap defaults.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Hummingbird, hb, SwiftPM, Fluent, PostgreSQL, and Docker-backed local development on macOS or Linux.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-bootstrap
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(brew:*) Bash(swift:*) Bash(hb:*) Bash(docker:*) Bash(curl:*)
---

# Bootstrap Hummingbird Service

## Purpose

Create a new Hummingbird service repository from nothing to a consistent, database-backed local baseline.

The practical decision is not whether Hummingbird should use Fluent, direct Postgres, Docker, or a hand-built SwiftPM scaffold. The default is already chosen: start with the official `hb` CLI, keep Hummingbird's generated application and Docker shape, use Hummingbird configuration support for runtime settings, add Fluent ORM with PostgreSQL, and provide a Docker Compose Postgres service for local development during bootstrap.

## When To Use

- Use this skill when the user wants to start, begin, create, scaffold, or bootstrap a new Hummingbird service.
- Use this skill when a new Hummingbird service should receive durable repo-local `AGENTS.md` guidance.
- Use this skill when the user asks for the standard Hummingbird service baseline, including Fluent ORM, PostgreSQL, and local container support.
- Use this skill when maintaining the bootstrap defaults for future Hummingbird services.
- Do not use this skill for ordinary route, middleware, request-context, or test work in an existing Hummingbird service. Use `hummingbird-server-workflow`.
- Do not use this skill for existing persistence changes that are not part of initial bootstrap. Use `persistence-workflow`.
- Do not use this skill for generic Docker image production work. Use `docker-workflow`.
- Do not substitute a manual SwiftPM scaffold, discard the CLI-generated Docker files, use direct Postgres-only persistence, use SQLite, or use non-container local database setup unless the user explicitly approves that exception for the project.

## Source Check

Use official Hummingbird and package sources before making CLI, configuration, persistence, or package claims:

- [Hummingbird documentation](https://docs.hummingbird.codes/)
- [Hummingbird hb CLI](https://github.com/hummingbird-project/hb)
- [Hummingbird project template](https://github.com/hummingbird-project/hummingbird-project-template)
- [Hummingbird Fluent package](https://github.com/hummingbird-project/hummingbird-fluent)
- [Hummingbird Postgres package](https://github.com/hummingbird-project/hummingbird-postgres)
- [Hummingbird Fluent tutorial](https://github.com/hummingbird-project/hummingbird-docs/tree/main/Hummingbird.docc/Tutorials/FluentUniverse)
- [Hummingbird Postgres tutorial](https://github.com/hummingbird-project/hummingbird-docs/blob/main/Hummingbird.docc/Tutorials/Todos/Todos-4-Postgres.tutorial)
- [Docker Compose file reference](https://docs.docker.com/reference/compose-file/)

Use SwiftPM and Swift.org documentation for package, toolchain, and Linux behavior when Hummingbird docs do not own the rule being used.

## Single-Path Workflow

1. Collect the required inputs:
   - `name`
   - `destination`
   - optional `executable_name`
   - optional `database_name`
   - optional `database_user`
   - optional `database_password`
   - optional `skip_validation`
2. Verify prerequisites:
   - `swift`
   - `git`
   - `hb`
   - Docker-compatible runtime only when Compose validation is requested
3. Create the service with the official CLI:
   ```bash
   hb init <name>
   ```
4. Answer the CLI prompts using the service's intended shape. Preserve Hummingbird's generated application, executable layout, `.dockerignore`, and `Dockerfile` instead of replacing them with a hand-written SwiftPM or Docker scaffold.
5. Add or verify the Hummingbird configuration path:
   - use the configuration support generated or documented by Hummingbird
   - keep host, port, log level, database URL, migration behavior, and testing toggles in one named configuration path
   - do not add a second bespoke settings loader when the generated Hummingbird configuration model already fits
6. Add Fluent ORM with PostgreSQL:
   - add Hummingbird Fluent and the PostgreSQL Fluent driver dependencies
   - keep Fluent setup at application startup
   - register migrations explicitly
   - keep models and migrations under predictable storage-oriented paths
   - use direct Hummingbird Postgres or PostgresNIO only when the user explicitly chooses SQL-first persistence for this project
7. Keep container support in the initial scaffold:
   - preserve and validate the Dockerfile generated by `hb init`
   - create `compose.yaml` with a `postgres` service when the selected `hb` template does not already generate a Compose file
   - if the selected official template generates Compose, preserve and adapt that file instead of replacing it
   - use safe development-only defaults
   - use a named volume for database storage
   - keep real secrets out of committed files
   - align host, port, database, user, and password with the committed safe local configuration
8. Install generated repo guidance:
   - copy `assets/AGENTS.md` into the new repository root
   - update placeholders for project name, executable name, database name, and validation commands
   - keep the generated guidance local to the new service because this plugin's own `AGENTS.md` is not visible inside ordinary service repositories
9. Install Codex GUI local environment guidance when desired:
   - copy `templates/codex-local-environments/hummingbird.toml` into `.codex/environments/hummingbird.toml`
   - replace `EXECUTABLE_NAME` with the actual executable target
10. Validate the scaffold:
   - `swift build`
   - `swift test`
   - `docker compose config`
   - optional `docker build .`
   - optional `docker compose up -d postgres`
   - optional migration command only after the app's migration command is known and safe
   - optional `swift run <executable>` or `hb watch` only when runtime startup validation is requested
11. Return the created path, exact commands, config source, database defaults, validation results, and next handoff.

## Defaults

- service framework: Hummingbird
- creation command: `hb init <name>`
- persistence: Fluent ORM
- database: PostgreSQL
- local dependency runtime: Docker Compose Postgres service
- service image baseline: preserve the CLI-generated Dockerfile
- generated guidance: root `AGENTS.md`
- app configuration: Hummingbird's built-in or generated configuration support
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
  - `primary`: official `hb` CLI bootstrap path
  - `fallback`: non-mutating guidance only because the CLI path could not safely run
- `output`
  - resolved service path
  - executable name
  - Hummingbird configuration source
  - Fluent and PostgreSQL dependencies added or confirmed
  - `compose.yaml` shape
  - generated `AGENTS.md` installed
  - validation result
  - one concise next handoff

## Guardrails

- Strong default: use `hb`, Hummingbird configuration support, Fluent ORM, PostgreSQL, and Docker Compose for every fresh Hummingbird service unless the user explicitly approves a project-specific exception.
- Do not hand-roll a new SwiftPM project as the default Hummingbird bootstrap path.
- Do not remove or postpone Docker files generated by `hb init`; validate and keep them in the initial scaffold.
- Do not use direct Hummingbird Postgres, PostgresNIO, SQLite, or in-memory persistence as the default bootstrap path.
- Do not add a custom configuration framework when Hummingbird's built-in or generated configuration support fits.
- Do not commit secrets, real database passwords, `.env.*` files with sensitive values, machine-local paths, or private dependency URLs.
- Do not run destructive migrations, database drops, volume deletion, or migration reverts without explicit user approval.
- Do not claim CLI options, package names, or generated file layouts from memory; check current Hummingbird docs, `hb --help`, or generated scaffold files.
- Use `docker-workflow` only when changing beyond the CLI-generated Docker baseline, such as adding multi-service production behavior, registry publishing, CI image builds, deployment-runtime tuning, or nonstandard image hardening.

## Fallbacks And Handoffs

- If `hb` is missing and Homebrew is acceptable, install with:
  ```bash
  brew tap hummingbird-project/tap
  brew install hb
  ```
- If `hb` is unavailable and cannot be installed, stop with a non-mutating fallback plan. Do not silently switch to the template repository.
- After successful bootstrap, use `hummingbird-server-workflow` for routes, middleware, request contexts, service lifecycle, and framework tests.
- Use `persistence-workflow` for models, migrations, query design, transactions, and database-backed tests after the initial baseline exists.
- Use `docker-workflow` for production Dockerfiles, multi-stage images, image validation, registries, or container deployment.
- Use `fly-io-deployment-workflow` for Fly.io apps, Fly Postgres, secrets, health checks, and deploy validation.

## References

- `assets/AGENTS.md`
