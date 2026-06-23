---
name: fsharp-csharp-interop
description: Design and maintain explicit F# and C# boundaries in mixed .NET solutions, including project references, public API shape, async/task interop, nullability, options, records, and package-facing contracts.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with mixed F# and C# .NET solutions.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: dotnet-interop
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(dotnet:*)
---

# F# And C# Interop

## Purpose

Keep mixed F# and C# solutions intentional.

The practical job is to decide which language owns which responsibility, make the project-reference direction explicit, and shape public APIs so each language can call the other without awkward translation code leaking everywhere.

## When To Use

- Use this skill when a solution contains both `.fsproj` and `.csproj` projects.
- Use this skill when adding an F# library to a C# app or service.
- Use this skill when adding a C# host or infrastructure project around F# domain code.
- Use this skill when public package APIs need to work well from both F# and C#.

## Source Check

Use repo-local .NET files, checked-out dependency sources, Dash MCP or Dash HTTP for installed .NET docsets, and then official Microsoft documentation when Dash/local coverage is missing or stale:

- [F# documentation](https://learn.microsoft.com/dotnet/fsharp/)
- [C# documentation](https://learn.microsoft.com/dotnet/csharp/)
- [.NET CLI documentation](https://learn.microsoft.com/dotnet/core/tools/)
- [`dotnet add reference` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-add-reference)

## Boundary Workflow

1. Inspect project graph:
   ```bash
   rg --files -g '*.fsproj' -g '*.csproj' -g '*.sln' -g '*.slnx'
   ```
2. Identify the language-owned responsibilities:
   - F# domain library
   - C# host app
   - C# ASP.NET Core service
   - F# CLI
   - shared abstractions
   - tests
3. Choose dependency direction.
4. Shape the API at the boundary.
5. Add tests from the consuming side when the boundary is public or fragile.
6. Run solution-level build and tests.

## Good Mixed Shapes

Common durable shapes:

- F# domain library consumed by a C# app or ASP.NET Core host
- F# transformation package consumed by C# tools
- C# infrastructure adapter consumed by an F# application
- shared test projects that verify public package behavior from both languages

Avoid mixed language solutions when the only reason is indecision. Ask for a language choice instead.

## API Boundary Notes

When C# consumes F#:

- be careful with options, tuples, curried functions, and discriminated unions
- expose C#-friendly functions or classes only at the boundary that needs them
- keep the idiomatic F# API intact when F# callers still matter

When F# consumes C#:

- handle nullability explicitly
- wrap exception-heavy APIs into clearer result shapes when useful
- keep async/task conversion visible at the edge

## Project References

Use `dotnet add reference` or direct project-file edits that match the repo style.

After reference changes, run:

```bash
dotnet build
dotnet test
```

Use package references instead of project references only when the dependency is intentionally versioned and released independently.

## Output Shape

Return:

1. `Boundary`: which language owns which project.
2. `Dependency direction`: project references and rationale.
3. `API shape`: F#-native, C#-friendly, or dual surface.
4. `Interop risks`: nullability, options, unions, async/task, file ordering.
5. `Validation`: exact build and test commands.

## Guardrails

- Do not add mixed language projects without naming the concrete benefit.
- Do not flatten F# domain modeling into C#-shaped classes just for convenience.
- Do not expose awkward F# internals to C# consumers when a small boundary API would be clearer.
- Do not hide nullability or task conversion problems.
- Do not change dependency direction casually in an existing solution.
