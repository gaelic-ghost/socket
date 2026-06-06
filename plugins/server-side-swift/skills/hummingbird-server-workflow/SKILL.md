---
name: hummingbird-server-workflow
description: Plan, build, run, test, and diagnose Hummingbird server-side Swift services using current Hummingbird documentation, SwiftPM-first commands, routing, middleware, request contexts, typed request and response models, service lifecycle, and deployment handoffs.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Hummingbird, SwiftPM, and server-side Swift projects on macOS or Linux.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-hummingbird
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(curl:*)
---

# Hummingbird Server Workflow

## Purpose

Build, modify, run, or diagnose a Hummingbird service without confusing Hummingbird-specific server behavior with generic Swift package work, Vapor app structure, or Apple-platform Xcode work.

The practical decision is what the HTTP service exposes, which executable owns the `Application`, how routes and middleware are composed, what request context carries per-request data, how typed request and response models are encoded, and which command proves the service starts or behaves correctly.

## When To Use

- Use this skill when creating or modifying a Hummingbird service.
- Use this skill when changing Hummingbird routes, route groups, middleware, request contexts, application configuration, persistent request data, file middleware, service lifecycle integration, or local server behavior.
- Use this skill when diagnosing `swift build`, `swift test`, `swift run`, application startup, route matching, middleware, request decoding, response encoding, or local HTTP failures in a Hummingbird project.
- Use this skill when deciding whether an existing Swift package should become a Hummingbird service or stay a library consumed by one.
- Use this skill when comparing Hummingbird to Vapor only long enough to choose the correct framework-specific workflow.
- Do not use this skill for generic Swift package work that has no Hummingbird-specific behavior. Hand that work to a SwiftPM package workflow when available.
- Do not use this skill for Vapor services unless the task is a comparison or migration involving Hummingbird.
- Do not use this skill for Apple-platform app, simulator, preview, or Xcode project membership work.

## Source Check

Use official Hummingbird documentation first:

- [Hummingbird documentation](https://docs.hummingbird.codes/)
- [Hummingbird framework overview](https://docs.hummingbird.codes/2.0/documentation/hummingbird/)
- [Create a Hummingbird application](https://docs.hummingbird.codes/2.0/tutorials/hummingbird/todos-1-template/)
- [Middleware](https://docs.hummingbird.codes/2.0/documentation/hummingbird/middlewareguide/)
- [Request Contexts](https://docs.hummingbird.codes/2.0/documentation/hummingbird/requestcontexts/)
- [Error Handling](https://docs.hummingbird.codes/2.0/documentation/hummingbird/errorhandling/)
- [Hummingbird Testing](https://docs.hummingbird.codes/2.0/documentation/hummingbird/testing/)
- [Hummingbird ecosystem](https://hummingbird.codes/ecosystem/)
- [Hummingbird GitHub organization](https://github.com/hummingbird-project)

Use Swift.org, Swift Package Manager, Swift Service Lifecycle, SwiftNIO, or Swift server package documentation for toolchain, package, lifecycle, event-loop, deployment, or observability behavior when Hummingbird docs do not own the rule being used.

## Planning Workflow

1. Inspect project shape:
   - `Package.swift`
   - executable target name, often `App`
   - application entry point and `Application` construction
   - `Router` creation and route registration
   - middleware registration and route groups
   - custom `RequestContext` types
   - request and response models
   - tests using `HummingbirdTesting`, `swift test`, or local HTTP checks
   - Docker, deployment, service lifecycle, or environment files when present
2. Identify the service job:
   - JSON API
   - static file or website surface
   - webhook receiver
   - internal service
   - background service with HTTP health or control routes
   - OpenAPI-backed server transport
3. Confirm the documented Hummingbird command and API path before running or recommending commands.
4. Keep SwiftPM as the default execution surface:
   - create from the Hummingbird template when the user wants the official template flow
   - build with `swift build`
   - test with `swift test`
   - run locally with the package's documented `swift run` command
   - inspect available executable commands with `swift run <executable> --help` when the package uses `AsyncParsableCommand`
5. Keep domain logic outside route closures when it has meaningful behavior.
6. Keep request and response models typed and small enough to test directly.
7. Keep request context additions deliberate, because they become per-request data that middleware and handlers depend on.
8. Validate with the narrowest useful SwiftPM, Hummingbird testing, or HTTP check.

## Hummingbird Ecosystem Package Preference

When a Hummingbird service needs framework-adjacent behavior, prefer maintained packages from the `hummingbird-project` GitHub organization when they fit the need and match the project's Hummingbird major version.

Check Hummingbird-aligned packages first for:

- authentication: Hummingbird Auth
- persistence and migrations: Hummingbird Fluent, Hummingbird Postgres, Postgres migrations, Valkey or Redis integration, and Swift Jobs drivers
- background jobs and durable work: Swift Jobs and Swift Jobs Workflows
- transport and API surfaces: OpenAPI Hummingbird, WebSocket support, SSE, compression, and Lambda runtime support
- rendering and examples: Swift Mustache, the Hummingbird template, and Hummingbird examples

Use the official Hummingbird ecosystem page for closely aligned packages outside the core organization when the project needs observability, JWT, WebAuthn, APNS, AWS, MQTT, or another Swift server integration that Hummingbird documents as ecosystem-fit.

Before recommending or adding any package:

- verify current documentation or source, repository maintenance status, and package version compatibility
- inspect the existing `Package.swift` dependency style, exact-version policy, and target ownership
- choose the package that fits the current Hummingbird app shape instead of copying Vapor patterns
- explain why the aligned Hummingbird package fits better than a generic Swift package or custom code
- avoid archived packages, stale Hummingbird-major-version packages, or packages that turn request context into a generic dependency container

## Project Creation

Hummingbird documents a template-based creation flow. Use it when the user wants a fresh Hummingbird app and accepts the official template as the starting point:

```bash
git clone https://github.com/hummingbird-project/template
./template/configure.sh MyService
cd MyService
swift run
```

When adding Hummingbird to an existing package, edit `Package.swift` through normal SwiftPM dependency rules and follow current Hummingbird docs for package products. Do not copy a template over an existing service unless the user explicitly asks for replacement.

## Codex GUI Local Environment

When a Hummingbird repo should be easy to use from Codex GUI Worktree mode, start from `templates/codex-local-environments/hummingbird.toml`. Keep the copied file under `.codex/environments/`, keep paths repo-relative, and replace `EXECUTABLE_NAME` with the repo's actual executable target.

## App Structure

For typical Hummingbird 2 projects:

- `Application` brings together the router and application configuration.
- `Router` owns route registration and produces the responder path for requests.
- Route groups are the right place to share path prefixes or scoped middleware.
- Middleware is useful for cross-cutting request and response behavior such as logging, metrics, tracing, CORS, authentication, compression, or static files.
- Request contexts carry per-request data such as logger, decoder, encoder, endpoint path, and project-specific context values.
- Typed request and response models should carry API data instead of route handlers assembling ad hoc dictionaries.

Do not introduce a service, repository, coordinator, or manager unless it removes a concrete duplication, testability problem, or dependency boundary issue in the current service.

## Configuration And Secrets

Do not commit secrets.

Use environment variables or the repository's existing configuration conventions for deployment-sensitive values. When diagnosing configuration, state which value is missing, where the app reads it, which command was running, and what local or deployment setup likely needs correction.

If a template-generated executable exposes hostname, port, or log-level options, preserve that command-line shape unless the user explicitly wants to change how the service is configured.

## Routes, Middleware, Contexts, And Errors

When adding or changing routes:

- name the route method and path
- describe request body, query, path parameters, response body, and status codes
- keep validation errors explicit and user-readable
- avoid blocking work on SwiftNIO event loops
- use async route handlers when the project already uses async Hummingbird APIs
- prefer typed request and response models over ad hoc dictionaries

When adding middleware:

- identify whether it is global, grouped, or route-specific
- add middleware before the routes that should receive it
- explain the request or response behavior it changes
- include a small test or manual check that proves the middleware is active

When adding request context data:

- name who creates the context value
- name which middleware or handler reads it
- keep the stored value scoped to a real per-request need
- avoid using request context as a generic dependency container

When handling errors:

- prefer Hummingbird's documented HTTP error surfaces
- return useful status codes and human-readable messages
- avoid leaking secrets, tokens, connection strings, or internal stack details in responses

## Testing

Choose the smallest test that proves the behavior:

- pure Swift test for domain logic
- Hummingbird testing helper for route, middleware, request, and response behavior
- local HTTP check only when runtime binding, headers, streaming, service lifecycle, or network behavior matters

Prefer `swift test` for normal validation. Use `curl` against a locally running server only when the user asked for runtime validation or the change cannot be proven through tests alone.

## Deployment Handoffs

Keep deployment guidance grounded in the repository's existing target first.

When no target exists, distinguish:

- local development run
- Docker image or Compose workflow
- Apple Containerization workflow
- Linux process manager or system service
- hosted platform deployment
- database migration or background service timing

Do not add Docker, CI, process-manager, cloud deployment, or Apple Containerization files as part of a route or local development change unless the user asked for deployment scope.

## Output Shape

Return:

1. `Service shape`: package root, executable target, application construction, router owners, middleware, context types, and test surface.
2. `Hummingbird docs used`: specific official docs relied on for app setup, routes, middleware, contexts, testing, or runtime behavior.
3. `Command path`: exact commands run or recommended.
4. `Behavior`: routes, inputs, outputs, errors, middleware, contexts, persistence, or configuration changes.
5. `Validation`: build, test, run, or HTTP check results.
6. `Handoffs`: SwiftPM, testing, Vapor, Apple-platform, OpenAPI, observability, deployment, or database follow-up when the task crosses this skill's boundary.

## Guardrails

- Do not treat Xcode as required for Hummingbird service work unless the repository already uses Xcode-specific workflow.
- Do not let route closures accumulate unrelated business rules.
- Do not commit secrets, machine-local paths, or deployment credentials.
- Do not claim Hummingbird API behavior from memory when current official docs can be checked.
- Do not use Hummingbird request context as a catch-all app dependency bag.
- Do not add Docker, Apple Containerization, CI, or cloud deployment files without explicit deployment scope.
