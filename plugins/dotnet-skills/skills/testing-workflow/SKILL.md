---
name: testing-workflow
description: Run, filter, debug, and explain .NET tests for F#, C#, and mixed solutions using dotnet test while respecting repo-local test framework choices.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with .NET SDK test workflows for F#, C#, and mixed-language solutions.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: dotnet-testing
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(dotnet:*)
---

# .NET Testing Workflow

## Purpose

Run and explain .NET tests without assuming one language owns the platform.

The stable command surface is `dotnet test`. The repository's existing test framework, project layout, SDK pin, and CI commands are the source of truth for how broad the check should be. For new scaffolds with no repo-local test framework, recommend xUnit as the default test template.

## When To Use

- Use this skill when the user asks to run, add, debug, or explain .NET tests.
- Use this skill after changing F# or C# behavior.
- Use this skill when `dotnet test` fails and the failure needs triage.
- Use this skill when deciding whether to run project-level or solution-level tests.

## Source Check

Use repo-local .NET files, checked-out dependency sources, Dash MCP or Dash HTTP for installed .NET docsets, and then official Microsoft documentation when Dash/local coverage is missing or stale:

- [`dotnet test` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-test)
- [.NET CLI documentation](https://learn.microsoft.com/dotnet/core/tools/)
- [F# documentation](https://learn.microsoft.com/dotnet/fsharp/)
- [C# documentation](https://learn.microsoft.com/dotnet/csharp/)
- [Unit testing C# with xUnit and `dotnet test`](https://learn.microsoft.com/dotnet/core/testing/unit-testing-csharp-with-xunit)

Inspect the repository before running broad checks:

```bash
rg --files -g '*.sln' -g '*.slnx' -g '*.fsproj' -g '*.csproj' -g 'global.json' -g 'Directory.Build.props'
```

## Test Selection

Choose the narrowest useful test command first:

- changed test project: `dotnet test path/to/Project.Tests.fsproj`
- changed C# test project: `dotnet test path/to/Project.Tests.csproj`
- changed shared library used by many tests: `dotnet test`
- dependency or SDK issue: `dotnet restore` before `dotnet test`
- compile issue without tests: `dotnet build`

Use solution-level `dotnet test` before commit, push, PR, release, or any change that could affect multiple projects.

## Test Framework Choice

Preserve the repository's current test framework in existing projects.

For new scaffolds without a repo-local convention, recommend xUnit:

```bash
dotnet new xunit --language "F#" --name MyLibrary.Tests --output tests/MyLibrary.Tests
dotnet new xunit --language "C#" --name MyLibrary.Tests --output tests/MyLibrary.Tests
```

The recommendation is a scaffold default, not a migration rule. Do not replace MSTest, NUnit, or another established test stack unless the user asks for that migration.

## Failure Triage

Classify failures by phase:

- SDK selection
- restore
- build
- test discovery
- test execution
- logger or result output

Report:

- what command ran
- which project failed
- which phase failed
- the first meaningful error
- the likely cause
- the smallest next check

## F# Test Notes

For F# tests:

- check `.fsproj` file ordering when test helpers or fixtures are added
- keep domain examples idiomatic F# instead of translated C#
- test pure transformations directly when possible
- keep async/task boundaries explicit in test code

## C# Test Notes

For C# tests:

- respect nullable and analyzer behavior in test projects too
- avoid over-broad mocks when a small value-based test would prove the behavior
- keep async tests aligned with the framework's expected async pattern
- avoid suppressing warnings only in tests unless the suppression has a clear reason

## Output Shape

Return:

1. `Command`: exact test command.
2. `Scope`: project, solution, or targeted filter.
3. `Result`: pass, fail, skipped, or blocked.
4. `Failure phase`: SDK, restore, build, discovery, execution, or output.
5. `Next step`: smallest useful fix or broader validation.

## Guardrails

- Do not run multiple build or test toolchains concurrently.
- Do not replace an existing test framework with xUnit unless the user explicitly asks for that migration.
- Do not hide restore or build failures under a generic "tests failed" summary.
- Do not skip tests after behavior changes when a relevant test surface exists.
- Do not broaden to package publishing or release workflow unless the user explicitly asks.
