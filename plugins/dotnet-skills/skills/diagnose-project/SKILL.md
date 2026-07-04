---
name: diagnose-project
description: Diagnose .NET SDK, restore, build, test, package, target framework, F# compile-order, C# analyzer, and project-reference failures with concrete next checks.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients diagnosing .NET SDK projects in F#, C#, and mixed-language solutions.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: dotnet-diagnostics
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(dotnet:*)
---

# Diagnose .NET Project

## Purpose

Find the first meaningful cause of a .NET failure and explain it in human terms.

The useful answer is not "build failed." It is what command failed, which project failed, which phase failed, why it most likely failed, and the smallest next check or fix.

## When To Use

- Use this skill when `dotnet restore`, `dotnet build`, `dotnet test`, or `dotnet pack` fails.
- Use this skill when SDK selection, target framework, package restore, or project references are unclear.
- Use this skill when F# compile order or C# analyzer/nullability failures need explanation.
- Use this skill before widening into refactors after a vague .NET error.

## Source Check

Use repo-local .NET files, checked-out dependency sources, Dash MCP or Dash HTTP for installed .NET docsets, and then official Microsoft documentation when Dash/local coverage is missing or stale:

- [.NET CLI documentation](https://learn.microsoft.com/dotnet/core/tools/)
- [`dotnet restore` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-restore)
- [`dotnet build` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-build)
- [`dotnet test` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-test)
- [`dotnet pack` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-pack)
- [`global.json` documentation](https://learn.microsoft.com/dotnet/core/tools/global-json)

## Diagnostic Workflow

1. Capture repository shape:
   ```bash
   rg --files -g '*.sln' -g '*.slnx' -g '*.fsproj' -g '*.csproj' -g 'global.json' -g 'Directory.Build.props' -g 'Directory.Packages.props' -g 'NuGet.config'
   ```
2. Check SDK context only when relevant:
   ```bash
   dotnet --info
   dotnet --list-sdks
   ```
3. Re-run the narrowest failing command.
4. Classify the failure phase:
   - SDK selection
   - restore
   - build
   - test discovery
   - test execution
   - pack
   - publish or release
5. Identify the first meaningful error.
6. Explain likely cause and next check.

## Common Failure Classes

### SDK Selection

Look for `global.json`, installed SDK versions, target framework, and CI SDK setup.

Report when a repo asks for an SDK that is not installed or when local and CI SDK versions likely differ.

### Restore

Look for package source, authentication, locked mode, central package management, and `NuGet.config`.

Do not turn an authenticated feed problem into a generic network diagnosis. Name the package source or credential surface when visible.

### Build

Look for target framework mismatch, project references, analyzer failures, nullable failures, generated code, and compile order.

For F#, inspect `.fsproj` file ordering when names are unresolved. For C#, inspect nullable and analyzer settings before suppressing warnings.

### Test

Separate test discovery from test execution.

Discovery failures usually point at framework adapters, target frameworks, build output, or project type. Execution failures usually point at behavior, environment, timing, or fixture setup.

### Pack

Look for missing metadata, invalid project type, failed Release build, project references, and artifact output path.

Remember that package publication is separate from package creation.

## Output Shape

Return:

1. `Command`: exact failing command.
2. `Phase`: SDK, restore, build, discovery, execution, pack, or release.
3. `Project`: solution or project path involved.
4. `First meaningful error`: short quoted or paraphrased error.
5. `Likely cause`: concrete explanation.
6. `Next check`: one or two smallest useful commands or edits.

## Guardrails

- Do not bury the first meaningful error under a long transcript.
- Do not rerun broad commands repeatedly before narrowing the phase.
- Do not delete build artifacts, caches, or lockfiles without explaining why and getting approval when destructive.
- Do not suppress warnings to make a build pass unless the suppression is intentional and documented.
- Do not assume C# project behavior explains an F# compile-order failure.
