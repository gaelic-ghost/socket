---
name: build-csharp-project
description: Build or modify idiomatic C# .NET projects using nullable-aware APIs, records/classes, async/task behavior, analyzer conventions, tests, and repo-local validation.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with C# projects on the .NET SDK.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: dotnet-csharp
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(dotnet:*)
---

# Build C# Project

## Purpose

Implement or modify a C# .NET project in C#'s own shape while keeping F# as an equal peer elsewhere in the plugin.

The practical goal is clear nullable-aware APIs, focused types, useful async boundaries, tests that cover changed behavior, and validation through the repository's .NET commands.

## When To Use

- Use this skill when the chosen language is C#.
- Use this skill when an existing `.csproj` needs new source, tests, or package-facing API.
- Use this skill when a mixed solution has a C# host, app, API, or interop surface.
- Use this skill when the user asks for C# implementation specifically.

## Source Check

Use official Microsoft documentation first:

- [C# documentation](https://learn.microsoft.com/dotnet/csharp/)
- [C# language reference](https://learn.microsoft.com/dotnet/csharp/language-reference/)
- [.NET CLI documentation](https://learn.microsoft.com/dotnet/core/tools/)
- [`dotnet test` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-test)

Inspect the repository before editing:

```bash
rg --files -g '*.cs' -g '*.csproj' -g '*.sln' -g '*.slnx' -g 'global.json' -g '.editorconfig'
```

## Implementation Workflow

1. Read the existing project file and analyzer/style settings.
2. Check nullable reference type behavior.
3. Identify the public API or app behavior being changed.
4. Use records for value-like data when that matches the domain.
5. Use classes for identity, behavior, mutable state, or framework integration.
6. Use interfaces only when there is a real alternate implementation, test boundary, or public contract.
7. Keep async APIs async only when they perform asynchronous work or match an existing contract.
8. Add or update tests around the behavior changed.
9. Run the narrowest useful validation command.

## Nullable And Analyzer Behavior

Respect existing repo configuration first.

When nullable reference types are enabled:

- avoid `!` unless the invariant is real and local
- prefer explicit null handling at boundaries
- keep public method contracts clear

When analyzers or warnings-as-errors are configured:

- fix warnings instead of suppressing them by default
- add suppressions only with a concrete reason
- avoid adding new style rules inside a feature change unless the user asked for tooling work

## API Shape

For library APIs:

- keep public types small and purposeful
- prefer immutable inputs and outputs unless mutation is part of the model
- keep exceptions for exceptional failure and use result-like values only when the repo already has that convention

For apps:

- keep process, environment, filesystem, and network effects explicit
- keep business rules testable without shelling out
- write human-friendly errors that name what failed and likely cause

## Testing

Use the repository's existing test framework and command if present.

When no convention exists yet, keep guidance centered on `dotnet test` and make any framework choice explicit before scaffolding. Do not declare a universal C# test framework default in this first slice.

## Output Shape

Return:

1. `C# change`: what type, method, project, or behavior changed.
2. `Contracts`: nullable, async, public API, or analyzer choices.
3. `Tests`: what behavior is covered.
4. `Validation`: exact `dotnet` commands and result.
5. `F# boundary`: if relevant, how this C# code interacts with F# projects.

## Guardrails

- Do not treat C# as the automatic .NET default in user-facing explanations.
- Do not add interfaces, services, factories, or managers without naming the concrete caller or pain they address.
- Do not disable nullable or analyzers to make a change pass.
- Do not skip tests for behavior changes when the repo has a test surface.
- Do not rewrite a mixed F#/C# boundary without explaining the practical effect.
