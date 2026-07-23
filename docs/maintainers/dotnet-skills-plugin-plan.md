# .NET Skills Plugin Plan

This plan records the first durable shape for a Socket-hosted `.NET` skills plugin.

The plugin's job is to help agents build, test, package, and maintain `.NET` projects while treating F# and C# as equal first-party language choices. F# should stay visibly first-class, so the plugin should avoid silently centering C# in examples, scaffold defaults, skill names, or decision language.

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

The root Socket marketplace now lists `dotnet-skills` as an installable child plugin because the first real skills have landed. If the plugin ever loses its exported skill content, switch the marketplace entry back to `NOT_AVAILABLE` in the same pass.

## F# And C# Parity

F# and C# must be treated as equal first-party `.NET` languages.

That means:

- do not describe F# as secondary, niche, or merely compatible with `.NET`
- do not silently choose C# when the user has not named a language
- ask for language preference before scaffolding when the user's request is ambiguous
- present F# and C# as peer options in project-shape and bootstrap guidance
- include F# in plugin keywords, skill descriptions, examples, and testing guidance
- prefer F# examples first when no broader user-facing default is required
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

### `dotnet:aspnet-core-service-workflow`

Guide agents through ASP.NET Core service work after the core `.NET` project shape is settled.

This skill should cover:

- host project ownership
- F# service, C# service, and mixed C# host plus F# domain-library shapes
- endpoint behavior
- configuration and secret boundaries
- dependency injection only where it solves a real dependency boundary
- domain tests versus endpoint or integration tests
- `dotnet build` and `dotnet test` validation

It should not make ASP.NET Core the default `.NET` project shape when a library, CLI, or package would fit better.

### `dotnet:fsharp-csharp-interop`

Guide agents through mixed F# and C# solution boundaries.

This skill should cover:

- when mixed language projects are useful enough to justify the boundary
- project-reference direction
- F# domain libraries consumed by C# hosts
- C# infrastructure projects consumed by F# apps or libraries
- public API shape for options, records, discriminated unions, nullability, and async/task interop
- tests from the consuming side when a boundary is public or fragile

It should avoid flattening F# domain modeling into C#-shaped classes just for convenience.

### `dotnet:ci-workflow`

Guide agents through .NET CI setup and maintenance.

This skill should cover:

- SDK setup
- `global.json` versus workflow-pinned SDKs
- restore, build, test, format, and pack checks
- F# and C# path filters
- OS and SDK matrix decisions
- keeping local and CI commands aligned

It should not publish packages unless the user explicitly asks for release automation.

### `dotnet:upgrade-workflow`

Guide agents through .NET SDK, target framework, package, and language-version upgrades.

This skill should cover:

- current SDK and target framework inventory
- `global.json`
- package version sources
- official breaking-change notes
- F# compiler or language-version behavior
- C# nullable and analyzer behavior
- staged restore, build, test, and pack validation
- migration notes for contributors or package consumers

### `dotnet:tooling-style-workflow`

Guide agents through .NET formatting and analyzer alignment.

This skill should cover:

- `.editorconfig`
- `dotnet format`
- analyzers
- warnings-as-errors
- local .NET tools
- CI style checks
- which tooling actually applies to F# sources versus C# sources

It should keep formatting-only sweeps separate from behavior changes when practical.

## First Implementation Slice

The first slice should be intentionally small but installable:

- [x] Update `plugins/dotnet-skills/AGENTS.md` with the F#/C# parity policy and `.NET` validation expectations.
- [x] Update `plugins/dotnet-skills/.codex-plugin/plugin.json` so plugin metadata includes F# and avoids C#-only wording.
- [x] Add `dotnet:choose-project-shape`.
- [x] Add `dotnet:bootstrap-solution`.
- [x] Add `dotnet:build-fsharp-project`.
- [x] Add `dotnet:build-csharp-project`.
- [x] Add `dotnet:testing-workflow`.
- [x] Decide not to add per-skill `agents/openai.yaml` metadata in the first slice because this child plugin follows the existing SwiftASB skills shape.
- [x] Switch the root marketplace entry for `dotnet-skills` to installable only after real skill content exists.
- [x] Update `README.md` and `ROADMAP.md` so Socket documents the new child plugin surface.
- [x] Run `uv run scripts/validate_socket_metadata.py`.
- [x] Run any child-plugin validation added by the new plugin; no child-local validator was added in the first slice.

## Second Implementation Slice

The second slice broadens the plugin from core project/test guidance into package, service, interop, CI, upgrade, and tooling guidance:

- [x] `dotnet:package-workflow`.
- [x] `dotnet:diagnose-project`.
- [x] `dotnet:aspnet-core-service-workflow`.
- [x] `dotnet:fsharp-csharp-interop`.
- [x] `dotnet:ci-workflow`.
- [x] `dotnet:upgrade-workflow`.
- [x] `dotnet:tooling-style-workflow`.
- [ ] install testing with a temporary `CODEX_HOME`.

## Third Implementation Slice: F# Web Frameworks

This slice makes the existing ASP.NET Core service workflow actionable for the
F# frameworks that have distinct handler and routing contracts. It is a durable
building-block change: it removes the current ambiguity between generic ASP.NET
Core guidance and framework-specific F# code, while keeping cloud operations in
Microsoft's official Azure Skills plugin.

- [x] `dotnet:choose-fsharp-web-framework` selects Minimal APIs, Giraffe,
  Falco, Oxpecker, or Saturn from the application's actual HTTP and ownership
  needs.
- [x] `dotnet:build-giraffe-web-app` covers composable `HttpHandler` work.
- [x] `dotnet:build-falco-web-app` covers functional routes, response helpers,
  and ASP.NET Core integration.
- [x] `dotnet:build-oxpecker-web-app` covers endpoint routing,
  `EndpointHandler`, and `EndpointMiddleware` contracts.
- [x] Keep Saturn, SAFE Stack, Fable, Bolero, and WebSharper as explicit
  selection or handoff boundaries until a concrete project requires deeper
  framework-specific workflows.
- [x] Export the new portable instructions through the Hermes tap; do not claim
  that the Codex plugin manifest itself is a Hermes plugin.
- [x] Route Azure infrastructure, diagnostics, and deployment work to the
  official Microsoft Azure Skills plugin rather than adding an Azure MCP server
  or duplicated IaC workflow to `dotnet-skills`.

## Deferred Scope

After the first two slices prove useful, consider deeper specialized workflows. These are useful but should not block the current installable plugin:

- Blazor app workflows
- .NET Aspire workflows
- .NET MAUI workflows
- advanced performance profiling
- C# source generators
- NuGet publishing automation
- custom project template generation
- bundled MCP servers or app connectors

The F# web-framework slice intentionally does not add a new runtime plugin,
framework template feed, browser-client framework implementation, or Azure
adapter. Those would broaden the architecture beyond the shared guidance need.

## Open Decisions Before Implementation

### Skill Names

Decision for the first slice: use short names such as `build-fsharp-project` because the plugin namespace already supplies the `.NET` context.

Longer names can be reconsidered only if skills are later copied outside the `dotnet-skills` plugin context.

### Scaffolding Depth

Decision for the first slice: keep `dotnet:bootstrap-solution` as pure guidance.

A script becomes useful if repeatable solution scaffolds with F# and C# parity need to be baked into command generation, but it also creates a validation and maintenance surface. Defer that until the guidance shape proves itself.

### Default Test Frameworks

Updated decision: recommend xUnit as the default scaffold template for new F# and C# test projects.

Read existing repo choices first and preserve them in existing projects. For new scaffolds without a repo-local test framework, use `dotnet new xunit` because it is the common .NET CLI template path documented by Microsoft, then use `dotnet test` as the stable command surface.

### Formatting And Analyzer Policy

Decision for the first slice: respect existing repo configuration and keep new-project style guidance conservative.

A later `tooling-style-workflow` can make `dotnet format`, analyzers, `.editorconfig`, warnings-as-errors, and language-specific style more complete.

### ASP.NET Core Timing

Decision for the first slice: defer ASP.NET Core service guidance to the second slice.

Core `.NET` solution, language, and test guidance should land first so web-service guidance can reuse stable project and validation rules.

### Versioning And Marketplace Timing

Decision for the first implementation: treat this as a likely Socket minor release candidate.

Because this turns a placeholder plugin into an installable plugin with real user-facing capability, a minor release is the likely SemVer shape for publication.

## Definition Of Done

The plugin is ready for first release when:

- [x] Socket exposes `dotnet-skills` as an installable child plugin.
- [x] The plugin metadata names both F# and C#.
- [x] The skills consistently treat F# and C# as equal first-party `.NET` choices.
- [x] Ambiguous scaffolding guidance asks for language preference instead of silently choosing C#.
- [x] The first skill set covers project choice, solution bootstrap, F# implementation, C# implementation, and testing workflow.
- [x] The guidance uses official Microsoft documentation as the source of truth for `.NET` SDK, CLI, language, test, and package behavior.
- [x] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.
