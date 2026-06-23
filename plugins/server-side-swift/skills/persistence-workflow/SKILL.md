---
name: persistence-workflow
description: Plan, build, test, and diagnose server-side Swift persistence, database, ORM, model, migration, query, transaction, and repository work for Vapor, Hummingbird, Fluent, and SwiftPM services.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with server-side Swift persistence in SwiftPM projects on macOS or Linux.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-persistence
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(curl:*)
---

# Server Persistence Workflow

## Purpose

Plan, build, modify, test, or diagnose database-backed behavior in a server-side Swift service.

The practical decision is which persistence tool owns the data access, how models map to stored records, how schema changes are migrated, where query logic lives, how configuration reaches the database client, and which command proves the service can safely read or write data.

## When To Use

- Use this skill when adding or changing Fluent models, migrations, relations, queries, transactions, or database configuration.
- Use this skill when a Vapor service needs database behavior that goes beyond route setup.
- Use this skill when a Hummingbird service needs database access, repository boundaries, migration handoffs, or driver selection.
- Use `bootstrap-vapor-service` or `bootstrap-hummingbird-service` instead when the database choice is part of fresh service creation.
- Use this skill when comparing Fluent, direct SQL, a package-specific database client, or a small repository/query helper for a Swift service.
- Use this skill when diagnosing failed migrations, missing schema, broken relations, connection-pool problems, query errors, transaction behavior, or database-backed tests.
- Do not use this skill for route, middleware, request-context, server startup, or deployment-only work unless persistence is the reason for the change.
- Do not use this skill for Apple-platform client storage such as SwiftData, Core Data, Keychain, UserDefaults, or app-side sync. Hand that work to an Apple-platform workflow.

## Source Check

Use repo-local Swift files, checked-out dependency sources, Dash MCP or Dash HTTP for installed Swift package DocC first. Check official framework and package docs, GitHub releases, or tagged source when Dash/local coverage is missing, stale, or a public latest-release citation is needed before claiming package names, APIs, migration commands, driver support, or CLI behavior.

Primary sources:

- [Vapor Fluent docs](https://docs.vapor.codes/fluent/overview/)
- [Vapor migrations docs](https://docs.vapor.codes/fluent/migration/)
- [Vapor Fluent GitHub repository](https://github.com/vapor/fluent)
- [Vapor GitHub organization](https://github.com/vapor)
- [Hummingbird docs](https://docs.hummingbird.codes/)
- [Hummingbird persistent data docs](https://docs.hummingbird.codes/2.0/documentation/hummingbird/persistentdata/)
- [Hummingbird GitHub repository](https://github.com/hummingbird-project/hummingbird)
- [Hummingbird Fluent package](https://github.com/hummingbird-project/hummingbird-fluent)
- [Hummingbird GitHub organization](https://github.com/hummingbird-project)
- [Swift.org database and persistence package catalog](https://www.swift.org/packages/database.html)

For Dash.app:

- Check the local Dash docsets before relying on them.
- If a needed docset is missing, use official hosted docs and GitHub source first.
- For docset availability or creation, use [Dash docset generation guidance](https://kapeli.com/docsets) and [Dash user-contributed docsets](https://github.com/Kapeli/Dash-User-Contributions). Do not claim a Vapor, Hummingbird, or Fluent Dash docset exists until the local Dash installation or the docset source has been checked.

Use Swift Package Manager and Swift.org documentation for package, target, dependency, and toolchain behavior when the framework docs do not own the rule being used.

## Planning Workflow

1. Inspect project shape:
   - `Package.swift`
   - executable target and library targets
   - route, controller, handler, or router owners
   - existing model, migration, repository, query, and database-support files
   - configuration, environment, Docker, Compose, or test database setup
   - tests that create, migrate, seed, or reset storage
2. Identify the persistence job:
   - CRUD storage
   - relational data model
   - migration or schema evolution
   - direct SQL query
   - transaction boundary
   - background job persistence
   - read model or reporting query
   - test fixture or ephemeral database setup
3. Choose the narrowest fitting data-access path:
   - fresh Vapor and Hummingbird services default to Fluent ORM with PostgreSQL through their bootstrap skills
   - official Vapor Fluent and Vapor database drivers first for Vapor projects already using Fluent models, migrations, and `req.db`
   - Hummingbird-specific persistence packages first for Hummingbird services before direct drivers or generic database clients
   - a documented direct database client when the service needs SQL-specific behavior or does not use Fluent
   - a small repository or query helper when route handlers are accumulating duplicated database code
   - existing repo conventions when a project already has a tested persistence boundary
4. Keep schema changes explicit and reversible only when a safe revert really exists.
5. Keep database credentials out of source control.
6. Add or update tests at the smallest level that proves the data behavior.
7. Validate with the narrowest useful SwiftPM, migration, database, or HTTP check.

## Vapor And Fluent

For Vapor projects that use Fluent:

- check the official Vapor Fluent docs, Fluent package, and Vapor-maintained database drivers before adding community or generic persistence packages
- keep models, migrations, and database configuration aligned with current Vapor Fluent docs
- register database drivers and migrations in app configuration
- run migrations with the documented app command, usually `swift run App migrate`
- use `swift run App migrate --revert` only when the user accepts the data-loss and rollback risk
- keep model types focused on stored fields and relations
- avoid putting unrelated business rules in route closures or model types
- use transactions when multiple writes must succeed or fail together
- keep request/response DTOs separate from database models when API shape and stored shape differ

When the work is mostly route, middleware, command, environment, or Vapor app structure, compose with `vapor-server-workflow`.

## Hummingbird Services

For Hummingbird projects:

- do not assume Fluent or any ORM is already part of an existing service
- for fresh services, route to `bootstrap-hummingbird-service`, where Fluent ORM with PostgreSQL is Gale's strong default
- inspect how the `Application`, router, service lifecycle, and dependencies are currently constructed
- check Hummingbird's persistent-data docs and Hummingbird-specific packages such as HummingbirdPostgres, HummingbirdFluent, PostgresMigrations, and Valkey or Redis integrations before choosing PostgresNIO, a direct driver, or a generic database package
- choose a database client or repository shape that fits the existing Hummingbird service instead of copying Vapor app structure
- keep database clients, pools, or repositories created at app startup and passed into the handlers or context path already used by the project
- keep request context values per-request; do not turn request context into a generic dependency container
- keep typed request and response models at the HTTP boundary and persistence models at the storage boundary when they diverge

When the work is mostly routing, middleware, request context, testing helpers, or Hummingbird app structure, compose with `hummingbird-server-workflow`.

## Query And Migration Design

When changing stored data behavior:

- name the table, collection, schema, model, or aggregate being changed
- describe the old shape, new shape, and migration path
- state whether existing data must be backfilled, transformed, preserved, or dropped
- keep operator-facing migration errors descriptive and tied to the schema or connection being changed
- keep query helpers explicit about inputs, filters, ordering, paging, and returned shape
- avoid stringly typed fallback paths when the project has typed model or query support
- avoid hidden writes in read-looking helpers

Use direct SQL only when it is simpler, more transparent, or required for the query. If direct SQL is introduced, keep it isolated, parameterized, tested, and named by the use case it serves.

## Testing

Choose the smallest test that proves the persistence behavior:

- pure Swift test for mapping or validation logic
- migration test for schema creation and upgrade behavior
- repository or query test for database reads and writes
- handler/controller test when the HTTP surface and database behavior must be proven together
- local HTTP check only when runtime wiring, configuration, or connection behavior cannot be proven through tests alone

Prefer `swift test` for normal validation. If the project uses a real database in tests, identify how the database is created, migrated, seeded, isolated, and cleaned up before adding new tests.

## Output Shape

Return:

1. `Persistence shape`: database tool, model owners, migration owners, query/repository owners, and configuration source.
2. `Docs used`: official docs, GitHub sources, or checked Dash docsets relied on for API, migration, or package behavior.
3. `Command path`: exact build, test, migrate, run, or diagnostic commands run or recommended.
4. `Data behavior`: schema changes, models, relations, queries, transactions, errors, or configuration changes.
5. `Validation`: SwiftPM, migration, test database, or HTTP check results.
6. `Handoffs`: Vapor, Hummingbird, SwiftPM, Apple-platform client, deployment, or observability follow-up when the task crosses this skill's boundary.

## Guardrails

- Do not commit secrets, credentials, connection strings, local database files, or machine-local dependency paths.
- Do not run destructive migrations, reverts, truncates, drops, or data repairs without explicit user approval.
- Do not claim a database driver, Dash docset, package API, or migration command from memory when current docs or local project files can be checked.
- Do not introduce a repository, service, manager, or helper unless it removes concrete duplication, clarifies a real dependency boundary, or makes tests meaningfully simpler.
- Do not move client-side Apple persistence guidance into this skill.
- Do not ask Gale to re-decide direct Postgres versus Fluent for fresh services; Fluent ORM with PostgreSQL is the consistency default unless Gale explicitly asks for a different persistence model.
