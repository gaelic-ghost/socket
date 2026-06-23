# AGENTS.md

Use this file for durable repo-local guidance before changing this Vapor service.

## Service Defaults

- This repository is a Vapor server-side Swift service created with the official Vapor CLI.
- Keep Swift Package Manager as the source of truth for package structure, dependencies, builds, tests, and run commands.
- Use Vapor's built-in `Environment` system for runtime environment and process settings. Do not add a parallel bespoke settings loader unless Gale explicitly approves that design for this service.
- Default persistence is Fluent ORM with PostgreSQL. Do not replace it with direct SQL, SQLite, MySQL, or non-Fluent persistence unless Gale explicitly approves the project-specific exception.
- Keep local PostgreSQL development support in Docker Compose. Real secrets belong in ignored local overrides or deployment secret stores, not committed files.

## Expected Surfaces

- `Package.swift` owns Vapor, Fluent, FluentPostgresDriver, and test dependencies.
- `Sources/App/configure.swift` owns app-wide setup such as middleware, databases, migrations, commands, encoders, and services.
- `Sources/App/routes.swift` owns route registration and should stay readable.
- Models and migrations stay paired and easy to audit.
- `compose.yaml` owns the local PostgreSQL container and named volume.
- `.codex/environments/vapor.toml`, when present, uses the actual app executable target name.

## Commands

Use the repo's documented commands first. If no narrower command exists, prefer:

```bash
swift build
swift test
docker compose config
docker compose up -d postgres
swift run App migrate
swift run App serve
```

## Configuration And Secrets

- Use `app.environment` for environment-specific app setup.
- Use `Environment.get` or `Environment.process` for process settings.
- Keep committed `.env` content safe and template-like.
- Ignore `.env.*` files that may contain machine-local or secret values.
- Do not commit real database passwords, tokens, private keys, `.env.*` files with secrets, or machine-local dependency paths.
- Error and log messages must name the missing setting, the config source being read, and the likely local or deployment fix.

## Persistence

- Use Fluent models, migrations, and query APIs for normal database-backed behavior.
- Register migrations explicitly in app configuration.
- Run migrations through `swift run App migrate` unless this repository documents a narrower command.
- Keep request/response DTOs separate from database models when the API shape and stored shape differ.
- Do not run destructive migrations, database drops, volume deletion, or migration reverts without explicit approval.

## Docker Compose

- Compose is the local dependency surface, not automatically the production deployment model.
- Keep the PostgreSQL service name, database name, user, password, port, and volume names obvious.
- Do not bake secrets into images, build args, committed Compose files, or logs.

## Handoffs

- Use `server-side-swift:vapor-server-workflow` for routes, controllers, middleware, commands, app configuration, and Vapor tests.
- Use `server-side-swift:persistence-workflow` for models, migrations, query design, transactions, and database-backed tests.
- Use `server-side-swift:docker-workflow` for production Dockerfiles, image builds, registries, and container runtime validation.
