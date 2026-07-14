# Reverse Engineering Skills Plugin Plan

This plan records the durable shape and expansion sequence for a Socket-hosted reverse engineering skills plugin.

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

## Architecture Direction

Build the plugin from small, composable workflow skills rather than one broad reverse-engineering playbook.

The durable structure has three layers:

1. Shared analysis skills own artifact preservation, evidence quality, tool selection, version comparison, and decompiler-output review.
2. Domain skills own facts and procedures for a binary format, runtime, platform-security boundary, or artifact family.
3. Tool-adapter skills own the controls, project state, imports, exports, and tool-specific failure modes for Cutter, Rizin, Malimite, Ghidra, Hopper, and later tools.

This removes a concrete limitation in the first plan: a single `apple-binary-workflow` would have to mix Mach-O structure, Swift and Objective-C recovery, crash correlation, code signing, dyld caches, Apple Silicon instructions, dynamic analysis, and firmware research. Those jobs change at different rates and need different evidence. The smaller skills let an agent compose only the relevant pieces and let beta-sensitive guidance change without destabilizing durable binary-format guidance.

The simpler extension path was to lengthen `apple-binary-workflow` and add tool sections to it. Do not use that path. It would create one multi-responsibility entry point with ambiguous triggers and repeated Cutter, Malimite, and evidence-handling instructions.

Treat this as a durable building-block change. Tool-specific workflows should remain thin adapters over shared and domain skills rather than parallel reverse-engineering systems.

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
- [Apple developer release feed](https://developer.apple.com/news/releases/)
- [Apple security releases](https://support.apple.com/100100)
- [Apple Platform Security](https://support.apple.com/guide/security/welcome/web)
- [Apple Security Research](https://security.apple.com/)
- [Apple Security Research Device](https://security.apple.com/research-device)
- [Apple open-source distributions](https://github.com/apple-oss-distributions)
- [XNU source](https://github.com/apple-oss-distributions/xnu)
- [dyld source](https://github.com/apple-oss-distributions/dyld)
- [Apple Security sources](https://github.com/apple-oss-distributions/Security)
- [macOS distribution manifests](https://github.com/apple-oss-distributions/distribution-macOS)
- [iOS distribution manifests](https://github.com/apple-oss-distributions/distribution-iOS)
- [Arm ABI specifications](https://github.com/ARM-software/abi-aa)
- [LLVM object inspection](https://llvm.org/docs/CommandGuide/llvm-objdump.html)
- [LLDB tutorial](https://lldb.llvm.org/use/tutorial.html)
- [Mach-O Runtime Architecture](https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/MachORuntime/)

When a skill relies on tool behavior, translate the relevant behavior into practical workflow guidance. Do not drop citations into a skill as a substitute for explaining what command output means, what artifact it came from, or what uncertainty remains.

For Apple-platform work, use this evidence order:

1. exact artifact, device, host, local SDK, and installed-tool evidence
2. current Apple Platform Security, Apple Security Research, security releases, release notes, and developer documentation
3. Apple open-source distributions such as XNU, dyld, Security, and objc4
4. Arm ABI, LLVM, LLDB, DWARF, and other canonical specifications
5. canonical FOSS tool documentation and source
6. community research used as a reproducible hypothesis rather than a confirmed platform claim

Never claim that an Apple open-source tag exactly matches a shipping binary without build, UUID, symbol, or behavior correlation. Never treat generated pseudo-code as recovered original source.

### Stable And Version-Sensitive Guidance

Keep stable foundations in skill references: Mach-O containers and load commands, universal slices, UUID matching, code-signature structure, dyld's role, Objective-C runtime metadata, Swift mangling principles, AArch64 calling conventions, pointer-authentication concepts, artifact preservation, and observation-versus-inference language.

Require live lookup and exact-build notes for current OS, SDK, Xcode, beta, and KDK versions; dyld-cache layouts; private symbols; undocumented interfaces; entitlement availability and enforcement; current hardware scope for mitigations; Xcode and debugger behavior; firmware signing availability; Rosetta support; and beta-only behavior.

Record both marketing version and build number. Also record the device or Mac model, processor family, artifact UUIDs, dyld-cache UUID when relevant, Xcode build, SDK build, KDK build, and tool version. Avoid writing `latest` into durable workflow instructions.

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

The next skills are grouped by responsibility. Names are verb-led where practical so their trigger and primary action remain clear.

### Shared Analysis Skills

#### `reverse-engineering:select-analysis-path`

Choose the smallest useful workflow from the artifact shape and research question. Compare metadata inspection, static analysis, decompilation, disassembly, dynamic analysis, symbol correlation, resource inspection, and version diffing before choosing a tool. Route into domain and tool skills without making Cutter, Malimite, Ghidra, Hopper, or any other tool a universal default.

#### `reverse-engineering:review-decompiler-output`

Review pseudo-code and disassembly while preserving uncertainty. Track tool-generated types, renamed symbols, compiler artifacts, control-flow reconstruction, disagreement between tools, and the observations supporting each source-level inference.

#### `reverse-engineering:preserve-binary-artifacts`

Create a preservation-grade inventory for research, education, FOSS, and historical work. Separate immutable originals, working copies, extracted members, normalized metadata, analysis databases, screenshots, and notes. Record hashes, acquisition source and date, original names, container paths, signatures, certificates, build IDs, UUIDs, architecture, and tool versions. Keep preservation evidence distinct from redistribution or licensing decisions.

#### `reverse-engineering:compare-binary-versions`

Compare exact builds without treating a marketing version as sufficient identity. Match architecture, hardware class, binary UUID, cache UUID, extraction method, and tool version; then record symbol, dependency, size, section-layout, entitlement, and control-flow differences using `first observed`, `last observed`, and `changed between` language.

### Apple Domain Skills

#### `reverse-engineering:inspect-apple-artifact`

Continue generic triage for `.app`, `.appex`, `.framework`, `.dylib`, static archives, XCFrameworks, IPA files, IPSW or restore images, kernel collections, dyld shared caches, dSYMs, crash reports, and `.ips` logs. Inspect bundle metadata before the executable, select universal slices deliberately, and record Mach-O UUIDs, deployment and SDK clues, encryption metadata, signing state, imports, exports, rpaths, segments, sections, chained fixups, function starts, unwind data, and address-space conventions.

#### `reverse-engineering:recover-apple-runtime-metadata`

Recover Objective-C classes, categories, protocols, selectors, methods, properties, and ivars plus Swift mangled names, metadata, conformances, witness tables, async state machines, closure thunks, and generic specialization clues. Keep runtime metadata, decompiler guesses, analyst renames, and inferred source declarations distinct.

#### `reverse-engineering:correlate-apple-symbols-and-crashes`

Match binaries, dSYMs, crash reports, and analysis databases by UUID and architecture. Preserve ASLR slide, image load address, OS build, device model, and symbol source. Cover `dwarfdump`, `atos`, Xcode symbolication, Swift demangling, Objective-C names, and partially symbolicated reports, then hand ordinary Xcode debugging back to `apple-dev-skills`.

#### `reverse-engineering:audit-apple-signing-and-containment`

Inspect code directories, CDHashes, signing authorities, Team ID, designated requirements, provisioning profiles, entitlements, hardened runtime, library validation, notarization, App Sandbox, SIP, Data Vaults, and platform-binary status. Inspect the original before any re-signing and record changed signatures or entitlements as a new behavioral artifact. Distinguish declared entitlements from access observed at runtime.

#### `reverse-engineering:inspect-dyld-shared-cache`

Identify caches by platform, architecture, UUID, and OS build. Cover subcaches, mappings, images, slide information, local symbols, chained fixups, extraction or export, cache-native address traceability, and cross-build comparison. Use Apple dyld source as a format reference without assuming it exactly matches every shipping cache.

#### `reverse-engineering:analyze-apple-silicon-arm64e`

Cover AArch64 calling conventions, registers, stack frames, SIMD, compiler idioms, `arm64` versus `arm64e`, pointer authentication, tagged pointers, top-byte handling, tool display pitfalls, Rosetta boundaries, and hardware-scoped mitigations. Keep SPTM, PPL, memory tagging, and Memory Integrity Enforcement claims tied to documented hardware and exact builds instead of generalizing across all Apple Silicon.

#### `reverse-engineering:perform-apple-dynamic-analysis`

Plan and record LLDB, Instruments, logging, Simulator, physical-device, and macOS-VM analysis. Capture launch versus attach, image lists, memory maps, registers, exceptions, Developer Mode, signing state, `get-task-allow`, SIP or security policy, Rosetta use, device model, and OS build. Never use a Simulator or VM result as proof of physical-device secure boot, PAC, Secure Enclave, or memory-integrity behavior.

#### `reverse-engineering:research-apple-kernel-boot-and-firmware`

Keep kernel, boot, and firmware research separate from app-binary analysis. Cover XNU source correlation, kernel collections, exact-build KDK matching, panic logs, device trees, boot-chain and LocalPolicy context, SSV and AuxKC state, IPSW manifests, board identity, component hashes, personalization, and firmware inventories. Separate Mac restore artifacts from iPhone and iPad firmware workflows and avoid treating public source as an exact shipping implementation without correlation.

#### `reverse-engineering:report-apple-security-research`

Produce reproducible research reports with affected hardware and build, expected and observed behavior, minimal test case, timestamps, hashes, crash or sysdiagnose context, impact evidence, and open questions. Revalidate beta findings on the newest available build, follow current Apple Security Research and bounty guidance when that program is in scope, and keep disclosure workflow separate from technical artifact analysis.

### Tool Adapter Skills

#### `reverse-engineering:use-cutter-and-rizin`

Use Cutter as an interactive GUI around Rizin for navigation, graphs, cross-references, annotations, types, renames, and comparison between disassembly and available decompiler output. Use Rizin CLI for repeatable triage, exact command provenance, scripted queries, batch analysis, and structured exports. Teach the GUI-to-CLI handoff instead of reproducing every Cutter click.

Start with capability discovery: record Cutter and Rizin versions separately, installed analysis and decompiler plugins, supported architecture, debugger availability, selected image and slice, loader choice, base address, and analysis settings. Do not assume a particular decompiler or `rzpipe` binding is installed. Cover file and shellcode imports, bounded initial analysis, functions, strings, imports, exports, sections, references, graphs, types, flags, comments, bookmarks, project databases, integrated Rizin commands, exports, scripting, patch-state separation, and static-versus-debugger boundaries.

For Mach-O work, analyze universal slices separately and do not present one `arm64` view as covering `x86_64` or `arm64e`. Flag App Store encryption, stripped symbols, optimized Swift, Objective-C runtime recovery, pointer authentication, chained fixups, dyld shared-cache images, and hardened or device-only debugging as explicit handoffs or uncertainty sources. Cutter and Rizin should complement `file`, `lipo`, `otool`, `nm`, `dwarfdump`, `codesign`, `dyld_info`, and Apple-specific workflows rather than replacing them.

Preserve an original-name to proposed-name table with evidence and confidence. Record project state, screenshots, exports, and CLI output separately from original inputs, and retain disagreements between Cutter, Rizin, another decompiler, and runtime evidence. Support Computer Use for the Cutter GUI when the app integration is available, but retain manual-GUI and CLI paths.

#### `reverse-engineering:use-malimite`

Use Malimite for Apple-focused IPA and copied ZIP or application-bundle exploration when its Ghidra-backed Swift, Objective-C, and resource workflow fits the artifact. Treat it as a package triage and navigation front end around Ghidra, not a general Apple decompiler or standalone Mach-O solution. Cover Java and Ghidra prerequisite verification, executable discovery through bundle metadata, encryption and universal-slice preflight, resource decoding, known-library filtering, reconstructed class views, strings and cross-references, adjacent project and SQLite state, and handoff into shared Mach-O, runtime-metadata, decompiler-review, and evidence skills.

The workflow must route unsupported or unreliable shapes explicitly: use another static-analysis tool for bare Mach-O input, try a copied ZIP wrapper when direct `.app` selection fails, and stop before analysis when the executable is encrypted or the selected universal format is unsupported. Record exact Malimite, Java, and Ghidra versions because compatibility is not pinned. Preserve the project directory and database as generated evidence because bulk source export is not a supported assumption.

Treat Swift reconstruction as heuristic and Ghidra pseudo-code as generated C-like output. Treat built-in LLM translation, summary, or vulnerability actions as generated interpretations whose model, destination, source method, and settings must be recorded when available. Prefer a local model or omit LLM processing when decompiled material should not leave the host. Do not rely on Malimite's stored API-key protection for sensitive long-lived credentials.

When processing an untrusted artifact, use an isolated working area and inspect Malimite's local listener exposure. The current source opens an unauthenticated analysis socket without an explicit loopback bind; the skill should recommend offline or firewall-isolated use until a tested release proves a narrower listener. Avoid installation guidance that mutates a Ghidra install or requests elevated privileges without explaining the exact file operation and obtaining the required approval.

#### `reverse-engineering:use-ghidra`

Own project creation, import and language selection, analyzers, data types, symbol and function renaming, decompiler views, scripts, exports, project archives, processor modules, and comparison with other tools. Keep Ghidra-backed behavior inside Malimite attributed to Malimite unless the workflow opens or operates a Ghidra project directly.

#### `reverse-engineering:use-hopper`

Own Hopper document setup, loaders, disassembly, decompiler views, Objective-C and Swift presentation, procedures and types, LLDB integration, scripting, patch state, and exported evidence. Route general Apple binary facts back to the Apple domain skills.

### Existing Non-Apple Domain Candidates

#### `reverse-engineering:inspect-dotnet-assemblies`

Cover assembly metadata, target frameworks, IL versus higher-level decompilation, PDBs, dependencies, and decompiler artifacts, then hand source repair and rebuilding to `dotnet-skills`.

#### `reverse-engineering:inspect-unity-artifacts`

Cover managed Unity assemblies, IL2CPP layout and metadata, player data, resources, asset clues, platform layout, version and scripting-backend identification, and the handoff between managed decompilation and native disassembly. Hand Unity authoring, profiling, and builds to `game-dev-skills`.

## Delivery Sequence

### Phase 0: Shipped Foundation

- [x] Create the child plugin, marketplace entry, maintainer plan, and metadata.
- [x] Ship `reverse-engineering:triage-artifact`.
- [x] Ship `reverse-engineering:evidence-notes-workflow`.

### Phase 1: Shared Foundation Expansion

- [ ] Add `select-analysis-path`.
- [ ] Add `review-decompiler-output`.
- [ ] Add `preserve-binary-artifacts`.
- [ ] Add `compare-binary-versions`.
- [ ] Define reusable artifact, environment, tool-context, symbol-map, and version-diff note shapes as references rather than duplicating templates across skills.

### Phase 2: Apple Static Analysis Foundation

- [ ] Add `inspect-apple-artifact` first because all later Apple workflows depend on stable artifact identity and address mapping.
- [ ] Add `recover-apple-runtime-metadata`.
- [ ] Add `correlate-apple-symbols-and-crashes`.
- [ ] Add `audit-apple-signing-and-containment`.
- [ ] Add `analyze-apple-silicon-arm64e`.

### Phase 3: Tool Workflows And Hands-On Calibration

- [ ] Add `use-cutter-and-rizin` after testing a Mach-O and one non-Apple artifact through both the GUI and CLI paths.
- [ ] Add `use-malimite` after testing an IPA or application bundle and recording its actual install, import, resource, Swift, Objective-C, export, and failure surfaces.
- [ ] Add `use-ghidra` and `use-hopper` after representative project comparisons.
- [ ] Add `inspect-dyld-shared-cache` and `perform-apple-dynamic-analysis` after the shared address and environment manifests are proven in the static workflows.

### Phase 4: Advanced Apple And Cross-Platform Domains

- [ ] Add `research-apple-kernel-boot-and-firmware` only with exact-build KDK, kernel, restore, and source-correlation rules in place.
- [ ] Add `report-apple-security-research` with live Apple program-source checks.
- [ ] Add .NET and Unity workflows without delaying the Apple-focused sequence.

## Skill Authoring And Validation

For every new skill:

- keep `SKILL.md` procedural and concise; put format details, source maps, version-sensitive notes, and larger examples in directly linked `references/`
- give frontmatter descriptions concrete artifact, tool, and task triggers
- generate or refresh matching `agents/openai.yaml` metadata
- avoid bundling decompilers, sample binaries, private SDK material, machine-local paths, tool databases, or extracted proprietary artifacts
- validate the skill folder with the skill-authoring validator and validate the Socket marketplace with `uv run scripts/validate_socket_metadata.py`
- forward-test with small, redistributable or locally generated artifacts that exercise success, uncertainty, disagreement between tools, and unsupported-version failure paths
- smoke-test GUI adapter steps through the available app integration when practical and retain a CLI or manual-GUI path
- date and link any beta-sensitive claim, and require live confirmation before relying on it in a later analysis session
- update `ROADMAP.md`, root plugin inventory text, and architecture metadata when the shipped skill inventory changes

The first Cutter calibration on this planning branch found Cutter `2.5.0-HEAD-a6f6ad7` with an accessibility-visible welcome and open-file workflow. Standalone Rizin commands were not on `PATH`. Treat this only as a dated workstation observation, not an install requirement or a capability claim for other Cutter builds. Recheck the [Cutter site and documentation](https://cutter.re/), [Cutter source](https://github.com/rizinorg/cutter), [Rizin handbook](https://book.rizin.re/), [Rizin source](https://github.com/rizinorg/rizin), and [rz-ghidra integration](https://github.com/rizinorg/rz-ghidra) before implementing the adapter.

The July 14, 2026 Malimite research pass confirmed the spelling `Malimite` and found release `1.2` as the newest canonical GitHub release. The source and open issues show important workflow limits: bare Mach-O support remains open, direct `.app` selection can require a copied ZIP workaround, bulk decompiled-source export is not established, Ghidra compatibility is version-sensitive, and the code has no verified iOS 26, macOS 26, `arm64e`, PAC, or current-beta-specific path. Recheck the [canonical repository](https://github.com/LaurieWired/Malimite), [releases](https://github.com/LaurieWired/Malimite/releases), [supported-format documentation](https://lauriewired-malimite.mintlify.app/reference/supported-formats), and live issues before authoring or using the skill.

## Exit Criteria

- [x] The Socket marketplace exposes `reverse-engineering-skills` as an installable child plugin after real skill content lands.
- [x] The first skills can help an agent triage artifacts and write reproducible analysis notes before platform-specific decompilation work starts.
- [ ] Shared routing, review, preservation, and version-comparison skills compose with domain and tool skills without duplicated evidence rules.
- [ ] Cutter/Rizin, Malimite, Ghidra, and Hopper each have a tested adapter workflow or a documented reason to remain backlog-only.
- [ ] Stable Apple app-binary, runtime, symbol, signing, and Apple Silicon workflows are usable without depending on beta-only facts.
- [ ] Beta, dyld-cache, dynamic-analysis, kernel, boot, and firmware workflows require exact-build context and live source checks.
- [ ] Unity and .NET workflows each have a clear owner skill or an explicit reason to stay backlog-only.
- [x] Root Socket docs, marketplace wiring, and validation agree on the current install surface.
