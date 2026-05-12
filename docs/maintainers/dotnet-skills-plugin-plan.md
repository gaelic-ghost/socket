# Dotnet Skills Plugin Plan

This plan records the first durable shape for a Socket-hosted `.NET` skills plugin.

The plugin's job is to help agents build, test, package, and maintain `.NET` projects while treating F# and C# as equal first-party language choices. Gale personally prefers F#, so the plugin should avoid silently centering C# in examples, scaffold defaults, skill names, or decision language.

## Intent

The `dotnet-skills` plugin should help agents do five things:

- choose a `.NET` project shape before scaffolding or implementation starts
- bootstrap reproducible `.NET` solutions, projects, tests, and package surfaces
- write idiomatic F# and C# without translating one language's habits into the other
- run and explain `.NET` build, test, package, and diagnostics workflows
- keep `.NET` guidance grounded in official Microsoft documentation and fetchable package sources

This is a companion guidance plugin, not a runtime plugin. The first version should not bundle an MCP server, custom package manager, private template feed, or local machine-specific SDK state.

## Packaging Direction

Package the guidance as an independent child plugin under:

```text
plugins/dotnet-skills/
```

The child plugin should own its Codex-facing guidance surface:

- `.codex-plugin/plugin.json`
- `skills/`
- plugin metadata, skill metadata, `AGENTS.md`, or maintainer notes that explain the plugin's role
- any validation scripts needed for the plugin's own authored guidance

The root Socket marketplace already lists `dotnet-skills` as a placeholder plugin. Keep it unavailable for install until the child plugin ships real content. When the first skills land, switch the marketplace entry from `NOT_AVAILABLE` to `AVAILABLE` in the same pass as the skill content, root docs, and validation updates.

## F# And C# Parity

F# and C# must be treated as equal first-party `.NET` languages.

That means:

- do not describe F# as secondary, niche, or merely compatible with `.NET`
- do not silently choose C# when the user has not named a language
- ask for language preference before scaffolding when the user's request is ambiguous
- present F# and C# as peer options in project-shape and bootstrap guidance
- include F# in plugin keywords, skill descriptions, examples, and testing guidance
- prefer F# examples first when the user is Gale or when no broader user-facing default is required
- include both `.fsproj` and `.csproj` examples when the guidance is language-neutral but project-file details matter
- call out F# compile-order behavior, module organization, records, discriminated unions, options, async/task interop, and testing style explicitly instead of treating F# as C# with different syntax
- call out C# nullable reference types, records/classes, analyzers, async/task behavior, and idiomatic project layout explicitly instead of treating C# as the universal `.NET` baseline

The plugin identity can stay `dotnet-skills` because `.NET` is the platform surface. The authored guidance should consistently say `.NET, F#, and C#` where language parity matters.

## Documentation Sources

Use official Microsoft documentation first for `.NET` behavior:

- [.NET documentation](https://learn.microsoft.com/dotnet/)
- [.NET CLI documentation](https://learn.microsoft.com/dotnet/core/tools/)
- [F# documentation](https://learn.microsoft.com/dotnet/fsharp/)
- [C# documentation](https://learn.microsoft.com/dotnet/csharp/)
- [`global.json` documentation](https://learn.microsoft.com/dotnet/core/tools/global-json)
- [`dotnet test` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-test)
- [`dotnet pack` documentation](https://learn.microsoft.com/dotnet/core/tools/dotnet-pack)
- [ASP.NET Core documentation](https://learn.microsoft.com/aspnet/core/)

When a skill relies on documentation, translate the relevant rule into practical workflow guidance. Do not drop citations into a skill as a substitute for explaining the effect on scaffolding, validation, project layout, or user-facing behavior.

## Proposed Skill Inventory

### `dotnet:choose-project-shape`

Help an agent decide how `.NET` should fit into a user's project before implementation starts.

This skill should classify the requested work:

- console app
- library package
- test project
- CLI tool
- ASP.NET Core service
- worker service
- multi-project solution
- mixed F# and C# solution
- package maintenance or upgrade pass

The output should recommend language choice, project templates, solution layout, validation commands, package boundaries, and documentation updates. It should ask about F# versus C# when the user has not decided.

### `dotnet:bootstrap-solution`

Create or guide a reproducible `.NET` solution scaffold.

This skill should cover:

- SDK selection and `global.json` when reproducibility matters
- solution and project naming
- F# and C# project creation with the `dotnet` CLI
- library, app, and test project layout
- project references
- `.editorconfig`
- package restore
- initial build and test validation
- optional initial commit when the user asks for it

The scaffold path should require an explicit language choice or an interactive decision before creating source files.

### `dotnet:build-fsharp-project`

Guide agents through idiomatic F# project implementation.

This skill should emphasize:

- modules, namespaces, records, discriminated unions, options, and results
- functional data flow and explicit inputs and outputs
- file ordering in `.fsproj`
- async/task interop for modern `.NET` APIs
- public API shape for libraries
- test project layout and assertion style
- interop boundaries when a solution also contains C#

This is a language-specific skill, not a translation layer from C# examples.

### `dotnet:build-csharp-project`

Guide agents through idiomatic C# project implementation.

This skill should emphasize:

- nullable reference types
- records, classes, interfaces, and primary constructors where appropriate
- async/task behavior
- analyzers and warnings-as-errors when a repo already uses them
- public API shape for libraries
- test project layout and assertion style
- interop boundaries when a solution also contains F#

This is a language-specific skill, not the default `.NET` skill.

### `dotnet:testing-workflow`

Run, debug, filter, and explain `.NET` tests.

This skill should cover:

- `dotnet test`
- targeted test filters
- solution-level versus project-level testing
- test output and logger choices
- failing restore, build, and test phases
- F# test project expectations
- C# test project expectations
- when to add focused tests versus broader integration checks

### `dotnet:package-workflow`

Build and validate `.NET` package surfaces.

This skill should cover:

- package metadata in project files
- `dotnet pack`
- local package smoke checks
- semantic versioning
- NuGet package-source expectations
- release notes and upgrade guidance
- F# and C# library package examples

It should not publish packages by default. Publishing is a release activity and should require an explicit user request or repo-local release workflow.

### `dotnet:diagnose-project`

Help agents debug `.NET` restore, build, test, package, SDK, and project-reference failures.

This skill should cover:

- missing or mismatched SDKs
- target framework drift
- package restore failures
- broken project references
- F# compile-order failures
- C# nullable or analyzer failures
- test discovery problems
- package metadata failures
- ambiguous or vague error messages that need human-friendly explanation

Diagnostics should report what broke, where it broke, the likely cause, and the smallest useful next check.

## First Implementation Slice

The first slice should be intentionally small but installable:

- [ ] Update `plugins/dotnet-skills/AGENTS.md` with the F#/C# parity policy and `.NET` validation expectations.
- [ ] Update `plugins/dotnet-skills/.codex-plugin/plugin.json` so plugin metadata includes F# and avoids C#-only wording.
- [ ] Add `dotnet:choose-project-shape`.
- [ ] Add `dotnet:bootstrap-solution`.
- [ ] Add `dotnet:build-fsharp-project`.
- [ ] Add `dotnet:build-csharp-project`.
- [ ] Add `dotnet:testing-workflow`.
- [ ] Wire skill metadata consistently across `SKILL.md` and `agents/openai.yaml` if the child plugin uses per-skill agent metadata.
- [ ] Switch the root marketplace entry for `dotnet-skills` to installable only after real skill content exists.
- [ ] Update `README.md` and `ROADMAP.md` so Socket documents the new child plugin surface.
- [ ] Run `uv run scripts/validate_socket_metadata.py`.
- [ ] Run any child-plugin validation added by the new plugin.

## Later Slices

After the first slice proves useful, add:

- [ ] `dotnet:package-workflow`.
- [ ] `dotnet:diagnose-project`.
- [ ] `dotnet:aspnet-core-service-workflow`.
- [ ] `dotnet:fsharp-csharp-interop`.
- [ ] `dotnet:ci-workflow`.
- [ ] `dotnet:upgrade-workflow`.
- [ ] `dotnet:tooling-style-workflow`.
- [ ] install testing with a temporary `CODEX_HOME`.

## Deferred Scope

These are useful but should not block the first installable plugin:

- Blazor app workflows
- .NET Aspire workflows
- .NET MAUI workflows
- advanced performance profiling
- C# source generators
- NuGet publishing automation
- custom project template generation
- bundled MCP servers or app connectors

## Open Decisions Before Implementation

### Skill Names

Decide whether skill names should use short names such as `build-fsharp-project` or longer names such as `build-dotnet-fsharp-project`.

Short names read better inside the `dotnet-skills` plugin namespace. Longer names are more self-describing when copied outside plugin context.

### Scaffolding Depth

Decide whether `dotnet:bootstrap-solution` should be pure guidance or ship a small script.

Pure guidance is easier to keep correct early. A script becomes useful if Gale wants repeatable solution scaffolds with F# and C# parity baked into command generation, but it also creates a validation and maintenance surface immediately.

### Default Test Frameworks

Decide the default testing guidance for F# and C#.

The first version can avoid declaring a universal test-framework default by reading existing repo choices first and using `dotnet test` as the stable command surface. If the plugin eventually scaffolds tests, it should choose explicit defaults and explain why.

### Formatting And Analyzer Policy

Decide how opinionated the plugin should be about `dotnet format`, analyzers, `.editorconfig`, warnings-as-errors, and language-specific style.

The first version should probably respect existing repo configuration and add conservative `.editorconfig` guidance for new scaffolds. A later `tooling-style-workflow` can make the policy more complete.

### ASP.NET Core Timing

Decide whether ASP.NET Core service guidance belongs in the first release or the second slice.

The current recommendation is second slice. Core `.NET` solution, language, and test guidance should land first so web-service guidance can reuse stable project and validation rules.

### Versioning And Marketplace Timing

Decide whether the first implementation should ship as a Socket minor release.

Because this turns a placeholder plugin into an installable plugin with real user-facing capability, a minor release is the likely SemVer shape once implementation lands.

## Definition Of Done

The plugin is ready for first release when:

- [ ] Socket exposes `dotnet-skills` as an installable child plugin.
- [ ] The plugin metadata names both F# and C#.
- [ ] The skills consistently treat F# and C# as equal first-party `.NET` choices.
- [ ] Ambiguous scaffolding guidance asks for language preference instead of silently choosing C#.
- [ ] The first skill set covers project choice, solution bootstrap, F# implementation, C# implementation, and testing workflow.
- [ ] The guidance uses official Microsoft documentation as the source of truth for `.NET` SDK, CLI, language, test, and package behavior.
- [ ] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.
