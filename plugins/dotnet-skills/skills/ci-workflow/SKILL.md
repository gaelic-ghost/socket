---
name: ci-workflow
description: Design and maintain .NET CI workflows for F#, C#, and mixed solutions with SDK setup, restore, build, test, format checks, package checks, caching, and matrix decisions.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with .NET projects and GitHub Actions or equivalent CI systems.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: dotnet-ci
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(dotnet:*)
---

# .NET CI Workflow

## Purpose

Make .NET CI prove the same behavior maintainers care about locally.

The practical job is to choose SDK setup, restore/build/test commands, optional format/package checks, path filters, and matrix scope without making CI broader or noisier than the project needs.

## When To Use

- Use this skill when adding or changing CI for a .NET repository.
- Use this skill when local validation and CI disagree.
- Use this skill when adding F# or C# projects to an existing CI workflow.
- Use this skill before package or release workflows depend on CI results.

## Source Check

Use repo-local files, checked-out dependency sources, Dash MCP or Dash HTTP for installed docsets, and then official project documentation when Dash/local coverage is missing or stale:

- [GitHub Actions and .NET](https://learn.microsoft.com/dotnet/devops/github-actions-overview)
- [Create a .NET test validation GitHub workflow](https://learn.microsoft.com/dotnet/devops/dotnet-test-github-action)
- [`actions/setup-dotnet`](https://github.com/actions/setup-dotnet)
- [`dotnet restore` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-restore)
- [`dotnet build` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-build)
- [`dotnet test` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-test)

## CI Planning Workflow

1. Inspect local validation commands.
2. Inspect existing workflow files:
   ```bash
   rg --files .github/workflows -g '*.yml' -g '*.yaml'
   ```
3. Check SDK source:
   - `global.json`
   - workflow `dotnet-version`
   - repository docs
4. Decide job scope:
   - restore
   - build
   - test
   - format check
   - pack check
5. Decide matrix scope:
   - one OS for library CI unless cross-platform behavior matters
   - multiple OSes for filesystem, process, path, native dependency, or user-facing CLI differences
6. Keep local and CI commands aligned.

## Baseline Command Order

Prefer a simple shape:

```bash
dotnet restore
dotnet build --configuration Release --no-restore
dotnet test --configuration Release --no-build
```

Add package validation only for package surfaces:

```bash
dotnet pack --configuration Release --no-build
```

Add formatting verification only when the repo has `.editorconfig` and expects it:

```bash
dotnet format --verify-no-changes
```

## F# And C# Notes

For F#:

- make sure CI builds the projects that prove `.fsproj` ordering
- do not path-filter only `**.cs` when F# files exist

For C#:

- keep nullable/analyzer failures visible
- respect warnings-as-errors behavior already used by the repo

For mixed solutions:

- include `**.fs`, `**.fsproj`, `**.cs`, and `**.csproj` in path filters when filters are used
- run solution-level validation when project references cross language boundaries

## Output Shape

Return:

1. `CI scope`: restore, build, test, format, pack.
2. `SDK source`: `global.json`, workflow version, or repo docs.
3. `Matrix`: OS and SDK versions.
4. `Commands`: local and CI command match.
5. `Path filters`: F#, C#, project, props, and workflow files.
6. `Residual risk`: what CI intentionally does not cover.

## Guardrails

- Do not make CI publish packages unless the user asks for a release workflow.
- Do not filter out F# paths in a plugin that promises F# parity.
- Do not add large OS matrices without naming the cross-platform behavior they protect.
- Do not hide build warnings if the repo treats warnings as errors locally.
- Do not make CI commands differ from documented local validation without explaining why.
