---
name: choose-project-shape
description: Choose the right .NET project shape before implementation, including F# versus C# language choice, solution layout, validation commands, package boundaries, and documentation updates.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with .NET SDK, F#, C#, and the dotnet CLI on macOS or other supported .NET development environments.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: dotnet-planning
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(dotnet:*)
---

# Choose .NET Project Shape

## Purpose

Pick the smallest correct .NET project shape before code changes begin.

The practical decision is what kind of project the user needs, whether F# or C# is the better fit, how many projects belong in the solution, which validation commands should prove the work, and where package or application boundaries should sit.

## When To Use

- Use this skill when the user wants a new .NET project but has not chosen app, library, test, package, or service shape.
- Use this skill before scaffolding a .NET solution.
- Use this skill when the repository already has .NET files and the next change could cross project or package boundaries.
- Use this skill when the user asks whether F# or C# is the right language for the work.

## Source Check

Use repo-local .NET files, checked-out dependency sources, Dash MCP or Dash HTTP for installed .NET docsets, and then official Microsoft documentation when Dash/local coverage is missing or stale. Check one of those source-specific paths before making claims about SDK, CLI, language, or project behavior:

- [.NET CLI documentation](https://learn.microsoft.com/dotnet/core/tools/)
- [F# documentation](https://learn.microsoft.com/dotnet/fsharp/)
- [C# documentation](https://learn.microsoft.com/dotnet/csharp/)
- [`global.json` documentation](https://learn.microsoft.com/dotnet/core/tools/global-json)
- [`dotnet new` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-new)
- [`dotnet test` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-test)

Translate any documentation rule into the concrete repository decision it changes.

## Classification Workflow

1. Inspect the repository shape:
   - `.sln` or `.slnx`
   - `global.json`
   - `Directory.Build.props`
   - `Directory.Packages.props`
   - `.fsproj`
   - `.csproj`
   - test projects
   - package metadata
   - existing CI commands
2. Identify the user-visible job:
   - command-line app
   - reusable library
   - NuGet package
   - test project
   - ASP.NET Core service
   - worker service
   - multi-project solution
   - mixed F# and C# solution
   - package maintenance or upgrade pass
3. Choose language intentionally:
   - Ask for language preference when the user has not chosen.
   - Prefer F# when the user asks for a neutral default and no external constraint points elsewhere.
   - Prefer C# when the repository is already C#-dominant and the requested change belongs inside that existing surface.
   - Use mixed F# and C# only when the boundary is useful and explicit.
4. Choose the project layout:
   - one project for a small app or library
   - app plus test project for normal implementation
   - library plus app plus tests when the reusable API and executable are separate
   - solution-level props only when shared settings reduce real duplication
5. Choose validation:
   - `dotnet restore` when dependency or SDK resolution is part of the task
   - `dotnet build` for compile and analyzer checks
   - `dotnet test` for behavior
   - `dotnet pack` for package surfaces

## Recommendations

### Console App

Use a single app project plus a test project when behavior is non-trivial.

For F#, prefer small modules, explicit domain types, and pure transformations where practical. For C#, prefer nullable-aware models, clear service boundaries, and async APIs only where work is truly asynchronous.

Handoff:

- `dotnet:bootstrap-solution` for new project creation
- `dotnet:build-fsharp-project` for F# implementation
- `dotnet:build-csharp-project` for C# implementation
- `dotnet:testing-workflow` for tests

### Library Package

Use a library project plus a test project. Add package metadata only when the library is intended to be packed or published.

For F#, shape the public API around clear functions and domain types. For C#, shape the public API around nullable-aware types, interfaces only where they have real callers, and explicit async contracts.

Handoff:

- `dotnet:package-workflow` when package validation or NuGet metadata matters
- `dotnet:testing-workflow` for test execution and failure triage

### ASP.NET Core Service

Use ASP.NET Core guidance only after the core solution, language, and test shape is clear. Keep the first decision focused on project ownership, configuration, tests, and whether the service belongs in an existing solution.

Handoff:

- `dotnet:aspnet-core-service-workflow` for service-specific guidance
- `dotnet:bootstrap-solution` for scaffold guidance

### Mixed F# And C# Solution

Use mixed language projects only when the boundary is useful enough to explain.

Good reasons include an F# domain/modeling library consumed by a C# host, or a C# app surface that needs to stay close to an existing ecosystem while F# owns the domain transformations.

Avoid mixed solutions when the only reason is uncertainty. Ask for the language decision instead.

## Output Shape

Return:

1. `Chosen shape`: console app, library package, test project, ASP.NET Core service, worker service, multi-project solution, mixed F#/C# solution, or maintenance pass.
2. `Language decision`: F#, C#, mixed, or user decision needed.
3. `Project layout`: projects, references, and package boundaries.
4. `Validation path`: exact restore, build, test, or pack commands.
5. `Documentation updates`: README, roadmap, package notes, or repo-local guidance.
6. `Next skill`: the next .NET skill to use.

## Guardrails

- Do not silently choose C# when the user has not named a language.
- Do not describe F# as secondary or niche.
- Do not add shared props, helper projects, or package boundaries without naming the duplication or workflow problem they remove.
- Do not publish packages by default.
- Do not commit machine-local SDK, package, or project references.
