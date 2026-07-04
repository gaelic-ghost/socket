---
name: upgrade-workflow
description: Plan and validate .NET SDK, target framework, package, and language-version upgrades for F#, C#, and mixed solutions with compatibility checks and staged validation.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients upgrading .NET SDK projects in F#, C#, and mixed-language solutions.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: dotnet-upgrade
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(dotnet:*)
---

# .NET Upgrade Workflow

## Purpose

Upgrade .NET projects without losing track of compatibility, validation, or language-specific behavior.

The practical job is to inventory SDK and target framework state, choose the upgrade boundary, apply the smallest coherent change, run staged validation, and document migration notes when users or package consumers need them.

## When To Use

- Use this skill when changing `TargetFramework` or `TargetFrameworks`.
- Use this skill when changing `global.json`.
- Use this skill when upgrading package versions across a .NET solution.
- Use this skill when moving between .NET major versions.
- Use this skill when F# or C# language behavior may change with the SDK or target framework.

## Source Check

Use repo-local files, checked-out dependency sources, Dash MCP or Dash HTTP for installed docsets, and then official project documentation when Dash/local coverage is missing or stale:

- [.NET breaking changes reference](https://learn.microsoft.com/dotnet/core/compatibility/breaking-changes)
- [Breaking changes may occur when porting code](https://learn.microsoft.com/dotnet/core/porting/breaking-changes)
- [`global.json` documentation](https://learn.microsoft.com/dotnet/core/tools/global-json)
- [`dotnet sdk check` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-sdk-check)
- [.NET CLI documentation](https://learn.microsoft.com/dotnet/core/tools/)

## Upgrade Workflow

1. Inventory current state:
   ```bash
   rg -n "TargetFramework|TargetFrameworks|LangVersion|PackageReference|PackageVersion|Sdk=" .
   rg --files -g 'global.json' -g 'Directory.Build.props' -g 'Directory.Packages.props' -g '*.fsproj' -g '*.csproj' -g '*.sln' -g '*.slnx'
   ```
2. Check installed SDKs when local validation is required:
   ```bash
   dotnet --list-sdks
   dotnet sdk check
   ```
3. Decide upgrade boundary:
   - SDK only
   - target framework only
   - package versions only
   - SDK plus target framework
   - package plus framework compatibility pass
4. Read breaking-change notes for the source and target versions.
5. Apply one coherent upgrade slice.
6. Run staged validation:
   - `dotnet restore`
   - `dotnet build`
   - `dotnet test`
   - `dotnet pack` when package surfaces exist
7. Update docs or release notes when public behavior, package requirements, or contributor setup changes.

## F# Upgrade Notes

For F#:

- check compiler or language-version behavior before changing project defaults
- inspect `.fsproj` ordering after automated edits
- watch for APIs that become more awkward across async/task boundaries
- run tests that cover discriminated union, option, and record serialization when those are public contracts

## C# Upgrade Notes

For C#:

- check nullable and analyzer behavior after SDK changes
- avoid broad warning suppression after analyzer updates
- decide whether new language features belong in the repo style before using them
- check source generators or analyzers when present

## Output Shape

Return:

1. `Upgrade boundary`: SDK, target framework, packages, or combination.
2. `Before`: current SDK, TFM, package, and language state.
3. `After`: target SDK, TFM, package, and language state.
4. `Compatibility notes`: breaking changes or migration concerns checked.
5. `Validation`: exact commands and results.
6. `Docs`: README, contributing, release notes, or package guidance updated.

## Guardrails

- Do not upgrade multiple unrelated surfaces in one commit without a clear reason.
- Do not ignore official breaking-change notes for major upgrades.
- Do not commit machine-local SDK paths or private package feeds.
- Do not suppress new analyzer warnings without explaining the rule and reason.
- Do not call an upgrade complete until build and tests have run or the blocker is explicit.
