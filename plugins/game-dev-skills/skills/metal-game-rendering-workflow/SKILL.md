---
name: metal-game-rendering-workflow
description: Guide native Apple game and custom-renderer work with Metal 3 and Metal 4. Use when Codex owns MTKView, CAMetalLayer, drawable presentation, render passes, command encoding, MSL shaders, pipeline states, GPU resources, Metal capability fallback, GPU capture, or renderer validation; do not use for DirectX or Vulkan porting, which belongs to the Game Porting Toolkit workflow.
---

# Metal Game Rendering Workflow

## Scope

Own a native renderer's data flow from frame input through presentation. Keep the renderer, scene, assets, input, and host app in separate owners; do not turn a local rendering repair into a new engine abstraction.

Read [renderer-architecture.md](references/renderer-architecture.md) before changing command or resource lifetime. Use Xcode MCP `DocumentationSearch`, Dash Apple API Reference, or current SDK headers before naming version-sensitive Metal APIs.

## Workflow

1. Inspect the renderer boundary: view or layer, device, queues, frame scheduler, resource owner, shaders, pipeline cache, and presentation owner.
2. Select the smallest API family that meets the target matrix:
   - Keep established Metal 3 code on `MTLCommandQueue` when it already meets the product need.
   - Adopt Metal 4 only behind an explicit OS-availability plus `device.supportsFamily(.metal4)` gate; preserve a Metal 3 path for supported targets that lack it.
   - Do not mix Metal 3 and Metal 4 command models casually. When they coexist, state the event or shared-event synchronization boundary.
3. Define a frame contract before adding passes: input resources, output attachments, ownership until GPU completion, load/store behavior, and ordering dependencies.
4. Keep resource allocation and transient per-frame state distinct from long-lived meshes, textures, shader libraries, and pipeline caches. Label resources and encoders at creation time.
5. Compile or load shaders before the first visible frame when practical. Treat runtime pipeline compilation as a measured, cached exception rather than a default; use a shipped `MTLBinaryArchive` for persistent cold-start pipeline work when the deployment path supports it.
6. Validate first with API and shader validation, then a representative GPU capture. Use the Metal Performance HUD or Instruments only to answer a concrete timing or memory question.

## Architecture Rules

- Make the render loop own drawable acquisition and presentation; scene or simulation code supplies render data rather than presenting drawables.
- Do not retain a drawable beyond its frame or access it after presentation.
- Keep CPU-side resource preparation, GPU encoding, and completion handling as explicit directional phases.
- For an incremental Metal 4 migration, first extract shared render data and pipeline-key construction, retain the Metal 3 backend intact, then move one independent pass or backend at a time. Never mix encoding models without an explicit event and resource-lifetime boundary.
- Use capability checks, not model-name guesses, for GPU families, Metal versions, MetalFX, mesh shaders, ray tracing, sparse resources, or neural paths.
- Use Simulator for fast functional iteration only. Verify final rendering, latency, memory, and performance claims on representative hardware.

## Handoffs

- `metalfx-game-rendering-workflow` for temporal upscaling, interpolation, or denoising.
- `metal-asset-streaming-workflow` for residency, sparse resources, streaming, or asset budgets.
- `metal-neural-rendering-workflow` for a learned rendering pass, tensors, or ML command encoding.
- `game-porting-toolkit-workflow` for a Windows executable, D3D, Vulkan, DXIL, Metal Shader Converter, or an Apple GPTK port.
- `xcode-game-profiling-workflow` when the next unanswered question is frame pacing, CPU/GPU overlap, memory, or thermals.

## Output

Return the renderer owner, chosen Metal family and fallback, frame/resource contract, changed passes or pipelines, evidence gathered, and remaining hardware validation.
