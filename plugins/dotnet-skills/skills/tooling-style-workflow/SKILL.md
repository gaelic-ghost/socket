---
name: tooling-style-workflow
description: Align .NET formatting, analyzers, .editorconfig, warnings-as-errors, local tools, and validation commands for F#, C#, and mixed solutions without overriding repo-local conventions.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients maintaining .NET style and tooling workflows for F#, C#, and mixed-language solutions.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: dotnet-tooling
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(dotnet:*)
---

# .NET Tooling And Style Workflow

## Purpose

Keep .NET formatting and analyzer behavior explicit.

The practical job is to respect existing repo conventions, use `.editorconfig` and `dotnet format` where they fit, keep analyzers and warnings understandable, and make local validation match CI.

## When To Use

- Use this skill when adding or changing `.editorconfig`, analyzers, or warnings-as-errors.
- Use this skill when `dotnet format` is part of local or CI validation.
- Use this skill when style drift causes noisy diffs.
- Use this skill when F# and C# projects need one documented validation story.

## Source Check

Use repo-local files, checked-out dependency sources, Dash MCP or Dash HTTP for installed docsets, and then official project documentation when Dash/local coverage is missing or stale:

- [`dotnet format` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-format)
- [.NET code analysis overview](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/overview)
- [EditorConfig settings for .NET](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/code-style-rule-options)
- [.NET local tools](https://learn.microsoft.com/dotnet/core/tools/local-tools-how-to-use)

## Inspection Workflow

1. Inspect tooling files:
   ```bash
   rg --files -g '.editorconfig' -g 'Directory.Build.props' -g 'Directory.Packages.props' -g 'dotnet-tools.json' -g '*.fsproj' -g '*.csproj'
   ```
2. Read existing repo guidance and CI.
3. Identify what is already enforced:
   - `dotnet format`
   - analyzers
   - warnings-as-errors
   - local tools
   - custom scripts
4. Decide the smallest alignment:
   - document existing commands
   - add missing `.editorconfig`
   - add format verification
   - adjust analyzers
   - add local tool restore
5. Run validation.

## dotnet format Guidance

`dotnet format` formats a project or solution according to `.editorconfig` settings when present.

Use verification mode for CI or pre-commit checks:

```bash
dotnet format --verify-no-changes
```

Use normal mode only when the user asked for formatting or when the change is explicitly a formatting pass:

```bash
dotnet format
```

Keep formatting-only sweeps separate from behavior changes when practical.

## Analyzer Guidance

Respect existing analyzer settings first.

When adding analyzer rules:

- explain what bug class or style drift the rule catches
- start conservative
- avoid turning every suggestion into a blocking error at once
- keep suppressions narrow and documented

For F#, check whether the proposed tooling actually applies to F# sources before promising enforcement.

For C#, nullable reference types and analyzer severity are often part of the public code quality contract. Do not disable them to make a change pass.

## Local Tools

When a repo uses local .NET tools, restore them through:

```bash
dotnet tool restore
```

Do not assume globally installed tools are available in CI or on another contributor's machine.

## Output Shape

Return:

1. `Existing tooling`: `.editorconfig`, analyzers, warnings-as-errors, local tools, CI.
2. `Change`: documentation, formatting, analyzer, local tool, or CI alignment.
3. `Commands`: exact format/build/test/tool commands.
4. `F# coverage`: what applies to F# sources.
5. `C# coverage`: what applies to C# sources.
6. `Residual risk`: anything not enforced automatically.

## Guardrails

- Do not make a broad formatting sweep inside an unrelated behavior change.
- Do not promise F# formatting/analyzer coverage from C#-only tooling.
- Do not depend on globally installed tools when a local tool manifest is appropriate.
- Do not disable analyzers or nullable checks to hide real issues.
- Do not add warnings-as-errors across an existing noisy repo without a cleanup plan.
