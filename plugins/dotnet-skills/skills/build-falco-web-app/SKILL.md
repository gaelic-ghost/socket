---
name: build-falco-web-app
description: Build or modify a Falco web application in idiomatic F#, using functional routing, request and response helpers, explicit ASP.NET Core integration, security boundaries, and focused tests.
---

# Build Falco Web App

Use Falco for its lightweight functional HTTP surface while leaving business
behavior as ordinary, testable F# code.

## Source Check

Read existing routes, the web host, project references, tests, and configuration
before editing. Consult [Falco's source and documentation](https://github.com/falcoframework/Falco)
and [ASP.NET Core documentation](https://learn.microsoft.com/aspnet/core/) for
current package behavior.

## Workflow

1. Confirm Falco is the selected framework; otherwise start with
   `dotnet:choose-fsharp-web-framework`.
2. Define route handlers around one request job. Parse input, call a domain
   function, then write one explicit response shape.
3. Keep routing declarative and readable. Split route groups by feature instead
   of building one mutable registration surface.
4. Use the existing ASP.NET Core host for configuration, dependency registration,
   authentication, authorization, logging, and rate or upload limits. Do not hide
   those platform concerns in unrelated response helpers.
5. Treat HTML/view code as presentation. Keep it separate from request parsing,
   authorization, and persistence behavior.
6. Test domain modules without a host, then add endpoint or integration coverage
   for routes, input validation, auth decisions, and response contracts.

## Validation

Run the repository's targeted commands. If it has none, use:

```zsh
dotnet build <web-project.fsproj>
dotnet test <test-project.fsproj>
```

## Boundaries

- Preserve F# compile order and explicit task or async boundaries.
- Do not translate C# controller or service patterns mechanically into Falco.
- For Azure resources, hosting, monitoring, identity, or deployment, use the
  official Azure Skills handoff rather than inventing provider commands here.
