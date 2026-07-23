---
name: choose-fsharp-web-framework
description: Choose an F# web application framework before implementation, comparing ASP.NET Core Minimal APIs, Giraffe, Falco, Oxpecker, and Saturn by application shape, composition model, dependencies, testing, and deployment boundaries.
---

# Choose F# Web Framework

Choose the web surface before scaffolding. Keep the application's F# domain model,
HTTP host, persistence, and deployment decision explicit instead of treating a
framework DSL as the whole architecture.

## Source Check

Inspect the repository and its locked packages first. When a current framework
behavior matters, use its official documentation before generating code:

- [ASP.NET Core Minimal APIs](https://learn.microsoft.com/aspnet/core/fundamentals/minimal-apis)
- [Giraffe](https://giraffe.wiki/)
- [Falco](https://github.com/falcoframework/Falco)
- [Oxpecker](https://lanayx.github.io/Oxpecker/src/Oxpecker/)
- [Saturn](https://saturnframework.org/)

## Selection

| Need | Default fit | Why |
| --- | --- | --- |
| Small service using standard ASP.NET endpoint conventions | Minimal APIs | Least extra framework surface; keep idiomatic F# modules around the host. |
| Composable middleware-style functional handlers | Giraffe | `HttpHandler` composition over the ASP.NET Core pipeline. |
| Lightweight functional API or full-stack server toolkit | Falco | Direct routing and response helpers with ordinary ASP.NET Core integration. |
| Endpoint-routing / Minimal-API-shaped F# DSL | Oxpecker | F# endpoint handlers and middleware on ASP.NET Core Endpoint Routing. |
| Established convention-heavy F# MVC application | Saturn | Use only when its MVC/scaffolding shape is desired by the project. |

Do not select from popularity alone. Check existing package choices, team
experience, endpoint style, HTML/view needs, authentication, hosting, and how
much framework-specific API the project is willing to own.

## Workflow

1. Classify the application: API, HTML server app, webhook, internal tool,
   background worker with health endpoints, or full-stack application.
2. Inspect its existing ASP.NET Core host, package versions, test harness,
   configuration, and deployment files.
3. State the chosen framework and why the alternatives do not fit this project.
4. Keep domain operations in F# modules independent of HTTP handlers.
5. Use the matching framework skill for Giraffe, Falco, or Oxpecker. For Minimal
   APIs use `dotnet:aspnet-core-service-workflow`; for Saturn, inspect its local
   conventions and official documentation before making framework-specific edits.
6. Select the smallest useful test level and run `dotnet build` plus the relevant
   `dotnet test` command.

## Boundaries

- SAFE Stack, Fable, Bolero, WebSharper, and browser-client architecture are
  separate decisions; do not imply that a server framework selects a client.
- Keep F# compile order deliberate in `.fsproj` files.
- Do not introduce a repository, service, or view-model layer merely to mirror a
  framework's API. Name the concrete external dependency or reuse boundary first.
- For Azure architecture, provisioning, diagnostics, or deployment, hand off to
  the official Microsoft Azure Skills plugin through the cloud deployment routing
  workflow; do not duplicate its MCP or infrastructure guidance here.

## Output

Return the application shape, selected framework, rejected alternatives, host and
domain ownership, test approach, Azure handoff if applicable, and exact validation
commands.
