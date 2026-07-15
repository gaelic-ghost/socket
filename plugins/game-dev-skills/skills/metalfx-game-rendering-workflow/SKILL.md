---
name: metalfx-game-rendering-workflow
description: Guide native Apple-game MetalFX integration for spatial or temporal upscaling, frame interpolation, and temporal denoising. Use when Codex works with MetalFX descriptors, jitter, motion vectors, depth, exposure, history, dynamic resolution, present threads, or MetalFX performance validation; use Game Porting Toolkit guidance for a D3D or Vulkan port.
---

# MetalFX Game Rendering Workflow

## Scope

Own the renderer-side contract that makes a MetalFX effect correct. MetalFX is not a generic FPS toggle: each effect has required inputs, lifecycle state, feature gates, and a presentation path.

Read [effect-selection.md](references/effect-selection.md) before choosing an effect. Confirm the effect’s documented availability from local Xcode or Dash API references before coding.

## Workflow

1. Establish the target device and OS matrix, target display cadence, baseline quality, and GPU-bound evidence. Do not add MetalFX to mask a CPU or asset-streaming bottleneck.
2. Choose one job: spatial scaling for a simpler resolution conversion, temporal scaling for reconstruction from history and motion, interpolation for generated display frames, or denoised temporal scaling for noisy rendered input.
3. Define the input contract explicitly: render/output size, color format, depth, motion-vector convention and units, jitter sequence, exposure, reset conditions, and history ownership.
4. Keep dynamic-resolution changes synchronized with the effect descriptor and resource allocation. Reset temporal history after camera cuts, resolution changes, content discontinuities, or other invalidating events.
5. Keep frame interpolation presentation isolated on its documented dedicated presentation path; do not let simulation or UI state advance merely because a generated frame is displayed.
6. Validate image quality before performance: inspect disocclusion, HUD/UI separation, motion-vector sign and scale, ghosting, shimmer, latency, and frame pacing on suitable hardware.

## Guardrails

- Preserve a non-MetalFX presentation path when the deployment matrix requires it.
- Do not claim a path is zero-latency, artifact-free, or supported from a simulator-only run.
- Treat MetalFX 4.1-era APIs as beta-sensitive until their shipping SDK availability is verified.

## Handoffs

- `metal-game-rendering-workflow` for the renderer, frame contract, queues, or command encoders.
- `xcode-game-profiling-workflow` for performance evidence.
- `metal-neural-rendering-workflow` when the work moves beyond MetalFX into custom ML, tensors, or neural rendering.
- `game-porting-toolkit-workflow` for a translated or source port.

## Output

Return the selected effect, availability and fallback, exact input/history contract, presentation ownership, visual-validation plan, and measured performance question.
