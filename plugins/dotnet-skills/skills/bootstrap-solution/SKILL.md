---
name: bootstrap-solution
description: Bootstrap or guide a reproducible .NET solution with explicit F# or C# language choice, SDK selection, project layout, test project setup, and initial validation commands.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with .NET SDK, F#, C#, and the dotnet CLI on macOS or other supported .NET development environments.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: dotnet-bootstrap
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(dotnet:*)
---

# Bootstrap .NET Solution

## Purpose

Create or guide a reproducible .NET solution scaffold without making C# the silent default.

The user should leave with a clear project layout, explicit F# or C# choice, predictable SDK behavior, and validation commands that prove the scaffold works.

## When To Use

- Use this skill when creating a new .NET solution or project.
- Use this skill when adding a test project to an existing .NET repository.
- Use this skill when a repo needs `global.json`, solution-level layout, or explicit validation commands.
- Use this skill after `dotnet:choose-project-shape` when the project shape is settled.

## Source Check

Use repo-local .NET files, checked-out dependency sources, Dash MCP or Dash HTTP for installed .NET docsets, and then official Microsoft documentation when Dash/local coverage is missing or stale:

- [.NET CLI documentation](https://learn.microsoft.com/dotnet/core/tools/)
- [`dotnet new` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-new)
- [`global.json` documentation](https://learn.microsoft.com/dotnet/core/tools/global-json)
- [`dotnet build` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-build)
- [`dotnet test` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-test)

Check the local SDK only when implementation actually needs it:

```bash
dotnet --info
dotnet --list-sdks
```

## Required Inputs

- target path
- project or solution name
- project shape
- language: F#, C#, or mixed
- test project expectation
- test framework expectation; default to xUnit for new scaffolds unless the repo or user chooses another framework
- SDK pinning expectation
- git initialization or commit expectation

If the user has not selected F# or C#, ask before scaffolding.

## Guidance Workflow

1. Inspect the target:
   - existing files
   - git state
   - `.sln` or `.slnx`
   - `global.json`
   - `Directory.Build.props`
   - `.fsproj` or `.csproj`
2. Confirm the project shape and language.
3. Choose SDK behavior:
   - use existing `global.json` when present
   - add `global.json` when reproducibility matters and the user accepts the SDK pin
   - avoid inventing a machine-local SDK path
4. Create projects with the `dotnet` CLI.
5. Add project references.
6. Add tests when the project has behavior worth preserving. Use the existing repo test framework if one exists; otherwise default new scaffolds to xUnit.
7. Run validation.
8. Report the generated paths and exact commands.

## Command Recipes

These recipes use xUnit intentionally. It is the recommended default for new scaffolds in this plugin because it is a common .NET CLI test template and Microsoft documents `dotnet test` workflows with xUnit examples. Preserve existing repo test-framework choices when adding to an established repository.

F# console app with tests:

```bash
dotnet new sln --name MyTool
dotnet new console --language "F#" --name MyTool --output src/MyTool
dotnet new xunit --language "F#" --name MyTool.Tests --output tests/MyTool.Tests
dotnet sln add src/MyTool/MyTool.fsproj
dotnet sln add tests/MyTool.Tests/MyTool.Tests.fsproj
dotnet add tests/MyTool.Tests/MyTool.Tests.fsproj reference src/MyTool/MyTool.fsproj
dotnet test
```

C# console app with tests:

```bash
dotnet new sln --name MyTool
dotnet new console --language "C#" --name MyTool --output src/MyTool
dotnet new xunit --language "C#" --name MyTool.Tests --output tests/MyTool.Tests
dotnet sln add src/MyTool/MyTool.csproj
dotnet sln add tests/MyTool.Tests/MyTool.Tests.csproj
dotnet add tests/MyTool.Tests/MyTool.Tests.csproj reference src/MyTool/MyTool.csproj
dotnet test
```

Library package shape:

```bash
dotnet new sln --name MyLibrary
dotnet new classlib --language "F#" --name MyLibrary --output src/MyLibrary
dotnet new xunit --language "F#" --name MyLibrary.Tests --output tests/MyLibrary.Tests
dotnet sln add src/MyLibrary/MyLibrary.fsproj
dotnet sln add tests/MyLibrary.Tests/MyLibrary.Tests.fsproj
dotnet add tests/MyLibrary.Tests/MyLibrary.Tests.fsproj reference src/MyLibrary/MyLibrary.fsproj
dotnet test
```

Use C# by changing `--language "F#"` to `--language "C#"` and project extensions from `.fsproj` to `.csproj`.

## F# Specific Checks

- Confirm file order in `.fsproj` after adding files.
- Prefer explicit modules and domain types over class-shaped code unless interop calls for classes.
- Keep examples idiomatic instead of direct translations from C#.

## C# Specific Checks

- Enable or preserve nullable reference type behavior when the repo already uses it.
- Respect existing analyzer and warnings-as-errors settings.
- Keep examples idiomatic instead of pretending C# is the only .NET shape.

## Output Shape

Return:

1. `Created or planned layout`: solution, source projects, test projects.
2. `Language`: F#, C#, or mixed.
3. `SDK behavior`: existing SDK, pinned SDK, or not pinned.
4. `Commands`: exact commands run or recommended.
5. `Validation`: restore, build, test, or pack results.
6. `Next skill`: implementation or testing handoff.

## Guardrails

- Do not scaffold into a non-empty directory without checking the user's intent.
- Do not silently choose C#.
- Do not add a scaffolding script for this first slice; this skill is guidance-only.
- Do not replace an existing test framework with xUnit unless the user explicitly asks for that migration.
- Do not publish packages.
- Do not commit generated files unless the user asks for a commit or the active repo workflow calls for one.
