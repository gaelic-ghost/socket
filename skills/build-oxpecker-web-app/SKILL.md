---
name: build-oxpecker-web-app
description: Build or modify an Oxpecker web application in idiomatic F#, using endpoint routing, functional EndpointHandler and EndpointMiddleware composition, ASP.NET Core metadata, and focused endpoint tests.
---

# Build Oxpecker Web App

Use Oxpecker's endpoint-routing model deliberately. Its F# DSL sits on ASP.NET
Core Endpoint Routing, so native endpoint metadata and middleware behavior remain
part of the application contract.

## Source Check

Inspect the existing host, endpoints, middleware, project references, tests, and
configuration. Use the [Oxpecker documentation](https://lanayx.github.io/Oxpecker/src/Oxpecker/)
and [ASP.NET Core routing documentation](https://learn.microsoft.com/aspnet/core/fundamentals/routing)
when local evidence does not answer the question.

## Workflow

1. Confirm Oxpecker is selected through `dotnet:choose-fsharp-web-framework`.
2. Model one endpoint as an `EndpointHandler`: validate or bind input, invoke a
   focused domain operation, and produce the response.
3. Use `EndpointMiddleware` for a reusable pipeline concern with an explicit
   before/after or short-circuit behavior. Do not use it as a generic service
   locator or business-rule container.
4. Keep route patterns, HTTP methods, authorization requirements, tags, and
   other endpoint metadata co-located enough to review as one API contract.
5. Continue using ASP.NET Core for host configuration, authentication,
   authorization, logging, and cross-cutting middleware. Preserve its pipeline
   ordering when introducing Oxpecker endpoints.
6. Test domain behavior independently and endpoint behavior for routing, binding,
   status, metadata, authorization, and serialized response contracts.

## Validation

Use the smallest project-level validation available, normally:

```zsh
dotnet build <web-project.fsproj>
dotnet test <test-project.fsproj>
```

## Boundaries

- Keep `.fsproj` file ordering explicit and preserve `Task` boundaries at the
  `HttpContext` edge.
- Do not assume Giraffe handlers or middleware map mechanically to Oxpecker;
  migrate only with an explicit route and test-contract review.
- Use the official Azure Skills plugin for Azure architecture, provisioning,
  diagnostics, and deployment decisions.
