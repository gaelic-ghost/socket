---
name: package-workflow
description: Validate .NET package surfaces for F# and C# libraries with project metadata, dotnet pack, local package smoke checks, semantic versioning, and release-boundary guidance.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with NuGet package-oriented .NET SDK projects in F#, C#, or mixed-language solutions.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: dotnet-packaging
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(dotnet:*)
---

# .NET Package Workflow

## Purpose

Validate a .NET library package before release or publication.

The practical job is to make package metadata explicit, build and test the library, run `dotnet pack`, inspect the generated package, and keep publishing as an explicit release step rather than an accidental side effect.

## When To Use

- Use this skill when a .NET library is intended to become a NuGet package.
- Use this skill when package metadata, versioning, or release notes are changed.
- Use this skill when adding package validation to F#, C#, or mixed solutions.
- Use this skill before package publication, but do not publish unless the user asks for that release step.

## Source Check

Use official Microsoft documentation first:

- [`dotnet pack` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-pack)
- [`dotnet build` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-build)
- [`dotnet restore` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-restore)
- [NuGet package creation guidance](https://learn.microsoft.com/nuget/create-packages/creating-a-package-dotnet-cli)
- [NuGet package versioning](https://learn.microsoft.com/nuget/concepts/package-versioning)

Translate documentation into the specific package, project file, and release decision in front of you.

## Inspection Workflow

1. Identify package-bearing projects:
   - `.fsproj`
   - `.csproj`
   - `Directory.Build.props`
   - `Directory.Packages.props`
   - package metadata fields
2. Confirm the intended package boundary:
   - one package per public library project
   - no accidental app project packages
   - no hidden machine-local references
3. Check metadata:
   - `PackageId`
   - `Version` or repository-owned version source
   - `Authors`
   - `Description`
   - `PackageTags`
   - `RepositoryUrl`
   - `PackageLicenseExpression` or license file policy
   - README and release notes if the repo ships them
4. Run validation:
   - `dotnet restore`
   - `dotnet build --configuration Release`
   - `dotnet test`
   - `dotnet pack --configuration Release --no-build`
5. Inspect generated package output.

## F# Package Notes

For F# packages:

- check `.fsproj` compile order before packaging
- keep public modules and types intentional
- avoid exposing implementation-only records or unions as accidental public API
- add C#-friendly API shapes only when there is a real C# consumer or package promise

## C# Package Notes

For C# packages:

- keep nullable reference type behavior explicit
- respect analyzer and warnings-as-errors settings
- avoid publishing broad interfaces or service types that only exist for test setup
- document public async contracts clearly

## Local Smoke Checks

When package behavior matters, create a temporary consumer outside the package source tree or in an ignored scratch path.

The smoke check should prove:

- the package can be restored from a local output directory
- the public API can be referenced by a fresh project
- F# and C# consumers work when the package promises both

Do not commit scratch consumers unless the repo intentionally keeps package integration tests.

## Output Shape

Return:

1. `Package boundary`: which project or projects produce packages.
2. `Metadata`: fields changed or verified.
3. `Validation`: exact restore, build, test, and pack commands.
4. `Artifacts`: package output paths.
5. `Consumer check`: skipped, passed, failed, or not applicable.
6. `Release boundary`: whether publication is still pending and what explicit release step would be needed.

## Guardrails

- Do not publish packages unless the user explicitly asks or the repo-local release workflow requires it.
- Do not pack app projects accidentally.
- Do not commit package metadata that points at machine-local paths.
- Do not use `--no-build` unless a successful Release build already ran in the same validation flow.
- Do not treat package creation as proof that public API design is good; inspect the API boundary too.
