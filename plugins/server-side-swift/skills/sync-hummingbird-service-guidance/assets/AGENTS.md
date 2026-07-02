# AGENTS.md

Use this file for durable repo-local guidance before changing this Hummingbird service.

## Service Defaults

- This repository is an existing Hummingbird server-side Swift service. Preserve its current Server, Lambda, or dual-adapter shape unless Gale explicitly asks for a migration.
- Fresh Hummingbird services start with the official `hb` CLI through `server-side-swift:bootstrap-hummingbird-service`; do not copy a fresh template over this existing repository without explicit approval.
- Keep Swift Package Manager as the source of truth for package structure, dependencies, builds, tests, and run commands.
- Use Hummingbird's generated `swift-configuration` support when it fits the repo. Do not add a parallel bespoke settings loader unless Gale explicitly approves that design.
- For `hb`-generated Lambda apps, keep `hummingbird-lambda` as the Lambda adapter. When OpenAPI is selected, keep `OpenAPIHummingbird` as the transport that registers generated handlers on the Hummingbird router.
- Treat `swift-openapi-lambda` as a separate valid OpenAPI Lambda transport, not as the default transport for current Hummingbird templates.

## Expected Surfaces

- `Package.swift` owns Hummingbird, generated transport, persistence, testing, and plugin dependencies.
- The executable target owns application startup, configuration, and Server or Lambda adapter setup.
- Route registration stays readable and delegates meaningful domain behavior out of route closures.
- Generated `APIProtocol` implementations should stay transport-neutral when the repo may support both long-running server and Lambda deployments.
- `.codex/environments/hummingbird.toml`, when present, uses the actual executable target name.

## Commands

Use the repo's documented commands first. If no narrower command exists, prefer:

```bash
swift build
swift test
docker compose config
swift run <EXECUTABLE_NAME>
```

Use `hb watch` only for local rebuild-and-run development in long-running Server apps. Do not use `hb watch` as a Lambda deployment validation command.

## Configuration And Secrets

- Keep host, port, log level, database URL, migration behavior, and testing toggles in the Hummingbird configuration path.
- Preserve the generated configuration-provider model unless the repo intentionally documents a replacement.
- Committed development defaults must be fake, local-only, and safe.
- Do not commit real database passwords, tokens, private keys, `.env.*` files with secrets, or machine-local dependency paths.
- Error and log messages must name the missing setting, the config source being read, and the likely local or deployment fix.

## Handoffs

- Use `server-side-swift:sync-hummingbird-service-guidance` when this file or the repo's Hummingbird guidance needs to be refreshed.
- Use `server-side-swift:hummingbird-server-workflow` for routes, middleware, request contexts, service lifecycle, and Hummingbird tests.
- Use `server-side-swift:openapi-rpc-workflow` for OpenAPI documents, generated stubs, transport registration, and RPC-fit decisions.
- Use `server-side-swift:persistence-workflow` for models, migrations, query design, transactions, and database-backed tests.
- Use `server-side-swift:docker-workflow` for production Dockerfiles, image builds, registries, and container runtime validation.
