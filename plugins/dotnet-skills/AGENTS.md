# AGENTS.md

This file is the .NET Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `dotnet-skills` is a monorepo-owned Socket child and the canonical source of truth for shipped .NET workflow skills.
- Root [`skills/`](./skills/) is the authored workflow surface.
- The repo root is the Codex plugin root through [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).
- Treat `productivity-skills` as the default baseline maintainer layer for general repo-doc and maintenance work; use this repo when .NET, F#, C#, SDK, CLI, project, package, or test behavior should materially change the workflow.

## Local Rules

- Match the `socket` shared semantic version exactly; use the Socket root release workflow for version inventory and bumps.
- Treat F# and C# as equal first-party .NET language choices.
- Do not describe F# as secondary, niche, or merely compatible with .NET.
- Do not silently choose C# when the user has not named a language.
- Ask for language preference before scaffolding when the user's request is ambiguous.
- Prefer F# examples first when working for Gale or when no broader public default is required.
- Keep .NET examples grounded in the `dotnet` CLI unless a repository already documents a different tool path.
- Use official Microsoft documentation first for .NET SDK, CLI, F#, C#, ASP.NET Core, testing, package, and project behavior.
- Keep package dependencies fetchable from NuGet, GitHub, package registries, or other real remote repositories; do not commit machine-local SDK, package, or project references.
- For validation guidance, prefer the narrowest relevant `dotnet restore`, `dotnet build`, `dotnet test`, or `dotnet pack` command for the project shape.
- Do not add extra packaging layers, repo-local install machinery, broad maintainer automation, custom template feeds, or bundled MCP servers unless a later plan explicitly calls for that scope.
