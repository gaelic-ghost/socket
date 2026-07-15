---
name: game-porting-toolkit-workflow
description: Select and operate Apple Game Porting Toolkit 3 or 4 for bringing an existing Windows game or engine to Apple platforms. Use when Codex encounters a Windows executable, Direct3D, Vulkan, DXIL, Metal Shader Converter, GPTK evaluation, a porting milestone, or the upstream game-porting-skills plugin; route native Metal renderer work to metal-game-rendering-workflow.
---

# Game Porting Toolkit Workflow

## Scope

Choose the correct GPTK lane, preserve evidence, and load Apple’s maintained GPTK 4 skills when they own the work. This is an integration skill, not a fork of Apple’s porting corpus.

Read [version-routing.md](references/version-routing.md) before choosing a toolkit or installing anything. Check the actual local Xcode, macOS, and toolkit versions; never infer them from an app bundle path.

## Choose The Lane

1. Use **GPTK 3** when the immediate job is stable evaluation of an unmodified Windows binary, baseline compatibility/performance evidence, or DXIL conversion with Metal Shader Converter on the current released toolchain.
2. Use **GPTK 4** when the job is source-level porting to Metal 4, macOS 27/Xcode 27 beta tools are intentionally in scope, or agent-driven capture/debugging is valuable.
3. For GPTK 4, install or load Apple’s `game-porting-skills` plugin from `apple/game-porting-toolkit`. Do not copy its expert skills, milestone format, or `.porting/` artifacts into Socket.
4. Stop and request a decision when a project requires a beta toolchain but its shipping target must remain on stable tooling.

## Evidence-First Porting

1. Inventory source API, build system, shaders, windowing, input, audio, assets, and existing platform layers.
2. Separate evaluation evidence from a native port commitment. A translated executable is a diagnostic baseline, not a shipped port.
3. For a GPTK 4 source port, let the upstream workflow own discovery, goal milestones, validation, and handoff artifacts.
4. Keep Socket-owned handoffs narrow: `game-controller-input-workflow`, `core-haptics-game-feedback-workflow`, `gamekit-game-center-workflow` when available, and native renderer or asset-streaming work.
5. Record toolkit version, OS/Xcode version, target hardware, launch configuration, trace or validation artifacts, and unresolved API or feature gaps. For D3D12, use the minimum checklist in `references/version-routing.md`: launch, graphics, input, audio, save, and network behavior; D3D12 feature use; shader-conversion failures; and one repeatable performance capture.

## Boundaries

- Do not use GPTK to claim that a Windows game is compatible, performant, or releasable without actual evaluation evidence.
- Do not use the GPTK evaluation environment as a substitute for porting source code.
- Treat Apple’s upstream GPTK 4 skill plugin as an optional Git-backed dependency. Do not add it to Socket’s marketplace or make Socket releases depend on its install state.

## Output

Return the chosen GPTK version, why it fits, prerequisites, the upstream skill/plugin action if needed, Socket handoffs, evidence required, and the next bounded porting step.
