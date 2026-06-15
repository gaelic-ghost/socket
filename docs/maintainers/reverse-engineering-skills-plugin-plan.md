# Reverse Engineering Skills Plugin Plan

This plan records the first durable shape for a Socket-hosted reverse engineering skills plugin.

The plugin's job is to help agents inspect compiled artifacts, decompile or disassemble outputs when useful, compare symbols and metadata, organize findings, and keep reverse-engineering notes reproducible enough that another pass can follow the same evidence trail.

## Intent

The `reverse-engineering-skills` plugin should help agents do five things:

- triage an unknown artifact and identify useful next inspection paths
- inspect .NET assemblies, Unity managed assemblies, Unity IL2CPP outputs, Apple binaries, symbols, crash logs, and generated metadata
- choose decompilation, disassembly, metadata extraction, or symbol inspection based on the artifact shape
- keep original inputs stable while working from copied artifacts and clearly named analysis output
- write evidence-backed notes that distinguish observed facts, tool output, inferred behavior, and open questions

This is a companion guidance plugin, not a runtime plugin. The first version should not bundle a decompiler, disassembler, debugger, emulator, private tool feed, sample binary corpus, MCP server, or machine-local tool state.

The skill surface should stay technical. It should not decide whether a reverse-engineering task is legitimate, authorized, or acceptable; that scope belongs to the user, project, client, or repository context outside the plugin.

## Packaging Direction

Package the guidance as an independent child plugin under:

```text
plugins/reverse-engineering-skills/
```

The child plugin owns its Codex-facing guidance surface:

- `.codex-plugin/plugin.json`
- `skills/`
- plugin metadata, skill metadata, `AGENTS.md`, and maintainer notes that explain the plugin's role
- any validation scripts needed for the plugin's own authored guidance

The root Socket marketplace lists `reverse-engineering-skills` as installable now that the first real skill content exists. If the plugin ever loses its exported skill content, switch the marketplace entry back to `NOT_AVAILABLE` in the same pass.

## Boundaries With Existing Plugins

`reverse-engineering-skills` should own compiled-artifact analysis. It should not replace existing development workflow plugins.

- Use `dotnet-skills` for normal .NET project creation, build, test, package, diagnostics, ASP.NET Core, and F#/C# implementation work.
- Use `apple-dev-skills` for normal Swift, Objective-C, Xcode, SwiftPM, app, simulator, signing, formatting, DocC, and Apple-platform validation work.
- Use `game-dev-skills`, if it is later added, for building, testing, packaging, profiling, and maintaining game projects.
- Use `reverse-engineering-skills` when the central input is a binary, assembly, bundle, archive, symbol file, metadata file, crash log, or decompiler/disassembler output.

Unity belongs here when the task is about compiled Unity artifacts, managed assemblies, IL2CPP output, metadata, asset/package inspection, or reconstructing behavior from build outputs. Unity project authoring belongs in a future game development plugin.

## Documentation And Tool Sources

Use official or canonical project sources first when a skill names a tool or format:

- [Unity documentation](https://docs.unity3d.com/)
- [Unity IL2CPP documentation](https://docs.unity3d.com/Manual/scripting-backends-il2cpp.html)
- [Microsoft .NET documentation](https://learn.microsoft.com/dotnet/)
- [ILSpy](https://github.com/icsharpcode/ILSpy)
- [Ghidra](https://github.com/NationalSecurityAgency/ghidra)
- [Cutter](https://cutter.re/)
- [Rizin](https://rizin.re/)
- [Malimite](https://github.com/LaurieWired/Malimite)
- [Hopper](https://www.hopperapp.com/)
- [radare2](https://rada.re/n/)
- [LLVM command guide](https://llvm.org/docs/CommandGuide/)
- [Apple developer documentation](https://developer.apple.com/documentation/)
- [Mach-O Runtime Architecture](https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/MachORuntime/)

When a skill relies on tool behavior, translate the relevant behavior into practical workflow guidance. Do not drop citations into a skill as a substitute for explaining what command output means, what artifact it came from, or what uncertainty remains.

## Shipped Skill Inventory

### `reverse-engineering:triage-artifact`

Help an agent classify an unknown artifact before choosing tools or making changes.

This skill should cover:

- file type and container identification
- directory and bundle shape
- hashes or stable identifiers when useful
- platform, architecture, and runtime clues
- debug symbols, stripped symbols, metadata, resources, manifests, and dependency hints
- a short next-step recommendation with the least invasive useful inspection path

### `reverse-engineering:evidence-notes-workflow`

Create durable analysis notes for reverse-engineering sessions.

This skill covers:

- artifact inventory
- tool and command inventory
- copied working files versus original inputs
- observations, inferences, and open questions
- screenshots or snippets when useful
- follow-up validation tasks
- concise handoff summaries for another agent or future session

## Proposed Skill Inventory

The following skills are planned after the common triage and notes surfaces have been used on real artifacts.

### `reverse-engineering:dotnet-decompilation-workflow`

Guide agents through .NET assembly inspection and decompiler-output review.

This skill should cover:

- assembly metadata and target framework checks
- managed DLL and EXE inspection
- IL versus higher-level decompiled language views
- symbol and PDB handling
- dependency mapping
- distinguishing decompiler artifacts from likely source-level intent
- handing ordinary project repair or rebuild work back to `dotnet-skills`

### `reverse-engineering:unity-artifact-workflow`

Guide agents through Unity build and package artifact inspection.

This skill should cover:

- managed assemblies under Unity build outputs
- IL2CPP output shape and metadata artifacts
- Unity player data, resources, and asset/package clues
- platform-specific Unity build layout
- version and scripting-backend identification
- decompiler/disassembler handoffs based on whether the build is managed or IL2CPP
- handing Unity authoring, profiling, and build-pipeline work to a future game development plugin

### `reverse-engineering:apple-binary-workflow`

Guide agents through Apple binary, bundle, framework, symbol, and crash-log inspection.

This skill should cover:

- app, framework, dylib, command-line tool, and package artifact shape
- Mach-O metadata and architecture slices
- Swift and Objective-C symbol clues
- dSYM, crash log, and UUID matching
- exported symbols, strings, linked libraries, entitlements, and Info.plist context
- handing ordinary Swift, Objective-C, Xcode, signing, or package work back to `apple-dev-skills`

### `reverse-engineering:tool-selection-workflow`

Help agents choose between available local inspection tools without treating one tool as the default.

This skill should cover:

- starting from artifact shape and desired output rather than tool preference
- Cutter and Rizin-backed interactive analysis
- Ghidra project setup and decompiler output review
- Malimite for iOS and macOS app or bundle inspection when its Apple-focused workflow fits
- Hopper for Mac-native disassembly, decompiler, Objective-C, Swift, LLDB, and scripted analysis workflows
- recording which tool produced each observation or exported snippet
- comparing tool output when names, types, control flow, or pseudo-code disagree

### `reverse-engineering:decompiler-output-review`

Help agents review generated decompiler or disassembler output without overclaiming.

This skill should cover:

- separating observed tool output from inferred source behavior
- naming common decompiler artifacts and uncertainty markers
- tracking renamed symbols and recovered structure
- building a concise findings log
- comparing multiple tool outputs when they disagree
- avoiding edits to original artifacts unless the user explicitly asks for patching or transformation work

## First Slice

- [x] Create `plugins/reverse-engineering-skills/` with `.codex-plugin/plugin.json` and `AGENTS.md`.
- [x] Add this maintainer plan.
- [x] Wire `reverse-engineering-skills` into the root Socket marketplace as `NOT_AVAILABLE` while it was a placeholder.
- [x] Update README, ROADMAP, and TODO so users understand the placeholder surface.
- [x] Add `reverse-engineering:triage-artifact` as the first skill.
- [x] Add `reverse-engineering:evidence-notes-workflow` before deeper platform-specific skills so all later workflows share the same note discipline.
- [ ] Add `reverse-engineering:tool-selection-workflow` after Gale has tried Cutter, Ghidra, Malimite, and Hopper on representative artifacts.
- [x] Switch the root marketplace entry to installable only after real skill content exists.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py` after each marketplace-facing update.

## Next Skill Candidates

- `reverse-engineering:dotnet-decompilation-workflow`
- `reverse-engineering:unity-artifact-workflow`
- `reverse-engineering:apple-binary-workflow`
- `reverse-engineering:tool-selection-workflow`
- `reverse-engineering:decompiler-output-review`
- `reverse-engineering:symbols-and-crashlogs-workflow`
- `reverse-engineering:asset-and-resource-inventory`

## Exit Criteria

- [x] The Socket marketplace exposes `reverse-engineering-skills` as an installable child plugin after real skill content lands.
- [x] The first skills can help an agent triage artifacts and write reproducible analysis notes before platform-specific decompilation work starts.
- [ ] Unity, .NET, and Apple binary workflows each have a clear owner skill or an explicit reason to stay backlog-only.
- [ ] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.
