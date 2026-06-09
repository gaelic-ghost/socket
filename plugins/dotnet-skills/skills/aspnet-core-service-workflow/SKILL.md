---
name: aspnet-core-service-workflow
description: Plan, build, and validate ASP.NET Core service surfaces for F#, C#, or mixed .NET solutions using explicit project ownership, configuration, endpoints, tests, and dotnet CLI validation.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with ASP.NET Core services on the .NET SDK.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: dotnet-aspnet-core
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(dotnet:*)
---

# ASP.NET Core Service Workflow

## Purpose

Build or modify an ASP.NET Core service with clear ownership, configuration, endpoints, tests, and validation.

The practical decision is what the service exposes, which project owns the HTTP host, where domain logic lives, how configuration reaches the app, and how tests prove behavior without turning the whole service into a fragile integration fixture.

## When To Use

- Use this skill when adding or changing an ASP.NET Core API or service.
- Use this skill when deciding whether a .NET project should be a web service or a library consumed by one.
- Use this skill when adding endpoints, middleware, configuration, dependency injection, or service tests.
- Use this skill after `dotnet:choose-project-shape` has identified an ASP.NET Core service shape.

## Source Check

Use official Microsoft documentation first:

- [ASP.NET Core documentation](https://learn.microsoft.com/aspnet/core/)
- [Minimal APIs documentation](https://learn.microsoft.com/aspnet/core/fundamentals/minimal-apis)
- [ASP.NET Core configuration](https://learn.microsoft.com/aspnet/core/fundamentals/configuration/)
- [ASP.NET Core dependency injection](https://learn.microsoft.com/aspnet/core/fundamentals/dependency-injection)
- [ASP.NET Core integration tests](https://learn.microsoft.com/aspnet/core/test/integration-tests)

## Planning Workflow

1. Inspect project shape:
   - web project
   - domain library
   - test project
   - config files
   - existing endpoints
   - existing hosting style
2. Identify the service job:
   - HTTP API
   - local service
   - webhook receiver
   - background worker plus HTTP health surface
   - internal admin tool
3. Choose language and boundary:
   - F# service
   - C# service
   - C# host with F# domain library
   - F# host with C# infrastructure library
4. Keep domain logic outside endpoint handlers when it has real behavior.
5. Keep configuration explicit and environment-safe.
6. Add tests at the smallest useful level.
7. Validate with `dotnet build` and `dotnet test`.

## F# Service Notes

For F# services:

- keep endpoint functions small
- model request and response data clearly
- keep domain transformations in modules that can be tested without the HTTP host
- be explicit at task/async boundaries
- preserve `.fsproj` file ordering

## C# Service Notes

For C# services:

- keep nullable request/response contracts clear
- avoid overbuilding service classes for one endpoint
- use dependency injection for real external dependencies, not as decoration
- keep middleware and endpoint registration readable
- respect analyzers and warnings-as-errors

## Configuration And Secrets

Do not commit secrets.

For local development, follow repo conventions first. If none exist, recommend committed safe defaults and ignored local overrides rather than hard-coded secrets. Explain which settings are required for the app to start and which settings are optional.

## Testing

Choose the smallest test that proves the behavior:

- pure domain test for business rules
- endpoint-level test for routing, validation, or response shape
- integration test for host/config/middleware behavior

Do not run live external services as ordinary unit tests unless the repo already has an isolated test harness for that purpose.

## Output Shape

Return:

1. `Service shape`: host project, domain project, and test project.
2. `Language boundary`: F#, C#, or mixed.
3. `Endpoint behavior`: routes, inputs, outputs, and errors.
4. `Configuration`: required settings and local override behavior.
5. `Tests`: level and command.
6. `Validation`: exact `dotnet` commands and results.

## Guardrails

- Do not add a new service layer without naming the real duplication or testability issue it removes.
- Do not put significant business rules directly inside endpoint registration.
- Do not commit secrets or machine-local configuration.
- Do not make ASP.NET Core the default .NET app shape when a library or CLI would fit better.
- Do not ignore F# compile ordering or C# nullable/analyzer settings.
