---
name: build-fsharp-project
description: Build or modify idiomatic F# .NET projects using explicit modules, domain types, functional data flow, file ordering, async/task interop, tests, and repo-local validation.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with F# projects on the .NET SDK.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: dotnet-fsharp
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(dotnet:*)
---

# Build F# Project

## Purpose

Implement or modify an F# .NET project in F#'s own shape.

The practical goal is readable domain modeling, explicit data flow, good module boundaries, correct file ordering, useful tests, and validation through the repository's .NET commands.

## When To Use

- Use this skill when the chosen language is F#.
- Use this skill when an existing `.fsproj` needs new source, tests, or package-facing API.
- Use this skill when a mixed solution needs an F# library or domain project.
- Use this skill when code looks like translated C# and should be made idiomatic F#.

## Source Check

Use official Microsoft documentation first:

- [F# documentation](https://learn.microsoft.com/dotnet/fsharp/)
- [F# language reference](https://learn.microsoft.com/dotnet/fsharp/language-reference/)
- [.NET CLI documentation](https://learn.microsoft.com/dotnet/core/tools/)
- [`dotnet test` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-test)

Inspect the repository before editing:

```bash
rg --files -g '*.fs' -g '*.fsproj' -g '*.sln' -g '*.slnx' -g 'global.json'
```

## Implementation Workflow

1. Read the existing `.fsproj` and source ordering.
2. Identify the domain values and transformations.
3. Prefer small modules with explicit inputs and outputs.
4. Use records for named product data.
5. Use discriminated unions for closed sets of alternatives.
6. Use options and results for expected absence or recoverable failure.
7. Keep side effects at the edge of the workflow.
8. Add or update tests around the behavior changed.
9. Run the narrowest useful validation command.

## File Ordering

F# compiles files in project order.

Before adding a new file:

- decide which later files depend on it
- place shared domain types before modules that use them
- place entry points after the implementation they call
- update `.fsproj` deliberately

Do not assume globbed source discovery unless the project already proves it.

## API Shape

For library APIs:

- expose a small set of clear modules and functions
- keep constructors and helpers close to the types they create
- avoid leaking implementation-only records or unions into public API
- provide C#-friendly APIs only when there is a real C# consumer

For apps:

- keep parsing, IO, environment reads, and process exits at the edge
- keep core transformations testable without shelling out
- return values that describe what happened before printing or logging them

## Async And Task Interop

Use the existing project style first.

When calling modern .NET APIs from F#, be explicit about whether a function returns `Async<'T>`, `Task<'T>`, or a plain value. Avoid hiding task conversion in unrelated helpers. Explain the boundary when a public API exposes tasks for C# consumers.

## Testing

Use the repository's existing test framework and command if present.

When no convention exists yet, keep guidance centered on `dotnet test` and make any framework choice explicit before scaffolding. Do not declare a universal F# test framework default in this first slice.

## Output Shape

Return:

1. `F# change`: what module, type, function, or project behavior changed.
2. `Data flow`: inputs, transformations, side effects, and outputs.
3. `Project ordering`: any `.fsproj` ordering changes.
4. `Tests`: what behavior is covered.
5. `Validation`: exact `dotnet` commands and result.

## Guardrails

- Do not translate C# examples line-by-line into F#.
- Do not hide mutation or IO inside broad helpers when a pure transformation would be clearer.
- Do not add compatibility APIs for C# unless a C# caller exists or the user asks for one.
- Do not ignore `.fsproj` file ordering.
- Do not skip tests for behavior changes when the repo has a test surface.
