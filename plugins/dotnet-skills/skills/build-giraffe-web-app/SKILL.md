---
name: build-giraffe-web-app
description: Build or modify a Giraffe web application in idiomatic F#, using composable HttpHandler functions, explicit ASP.NET Core integration, configuration, authentication, and focused endpoint tests.
---

# Build Giraffe Web App

Use Giraffe's functional handler composition as the HTTP boundary, not as a
reason to place business rules in route declarations.

## Source Check

Inspect the existing host, package lock or project references, handlers, tests,
and configuration first. Use the [Giraffe documentation](https://giraffe.wiki/)
and [ASP.NET Core documentation](https://learn.microsoft.com/aspnet/core/) when
repository evidence is insufficient.

## Workflow

1. Confirm that Giraffe is already selected; otherwise use
   `dotnet:choose-fsharp-web-framework` first.
2. Keep request parsing, authentication context, and response writing in narrow
   `HttpHandler` functions. Compose reusable HTTP concerns with `>=>` only when
   they have one clear request-pipeline responsibility.
3. Put domain transformations and external-dependency contracts in separately
   testable F# modules. Pass dependencies explicitly or resolve genuine host
   dependencies at a clear ASP.NET Core boundary.
4. Preserve ASP.NET Core ordering: routing, authentication, authorization,
   static files, exception handling, and Giraffe middleware must remain aligned
   with the application's existing host contract.
5. Make response errors specific: route, failed input or dependency, and the
   safe client-facing outcome. Do not leak secrets or internal exception details.
6. Test pure domain behavior first, then handler or host behavior for route,
   authorization, binding, status, and response regressions.

## Validation

Use the narrowest project commands available, normally:

```zsh
dotnet build <web-project.fsproj>
dotnet test <test-project.fsproj>
```

Do not run a live deployment or add a replacement middleware stack merely to
exercise one handler.

## Boundaries

- Keep `.fsproj` file order valid as modules are added.
- Use ordinary ASP.NET Core middleware and services when that is the existing
  integration surface; do not reimplement them as Giraffe helpers.
- Route Azure hosting, identity, resource configuration, and deployment work to
  the official Azure Skills plugin through `cloud-deployment-routing-workflow`.
