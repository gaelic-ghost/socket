---
name: metal-asset-streaming-workflow
description: Guide Metal game asset residency and streaming for textures, meshes, mipmaps, heaps, residency sets, sparse resources, and fast resource loading. Use when Codex investigates GPU memory pressure, streaming hitches, resource lifetime, texture or mesh upload, sparse texture mapping, or asset budgets in a Metal renderer; do not use for generic asset-catalog or SceneKit resource work.
---

# Metal Asset Streaming Workflow

## Scope

Own the GPU-facing asset path: package or source asset, CPU staging, upload, residency, eviction, and use in a frame. Do not hide all asset ownership in a generic cache; name the asset manager and the renderer boundary that consumes it.

Read [streaming-model.md](references/streaming-model.md) before introducing a heap, residency set, sparse resource, or fast-resource-loading path.

## Workflow

1. Measure the actual symptom: first-use hitch, sustained stutter, missing detail, out-of-memory termination, or GPU resource-pressure growth.
2. Inventory asset classes, size ranges, mip/LOD behavior, residency lifetime, upload path, and current CPU/GPU ownership.
3. Choose the simplest durable path:
   - ordinary texture or buffer loading for bounded content;
   - explicit heaps or residency sets when allocation and lifetime grouping are the problem;
   - fast resource loading when packaged asset loading is proven to dominate;
   - sparse resources only when content size or streaming granularity justifies their mapping complexity.
4. Define budget and eviction policy before loading more data: per-class budget, minimum viable mip/LOD, prefetch trigger, eviction trigger, fallback content, and telemetry.
5. Synchronize upload, mapping, and use. A resource must not become visible to a render pass until its data and mapping work have completed.
6. Validate memory and frame pacing on target hardware with representative content and movement, not a synthetic empty scene.

## Guardrails

- Do not equate unified memory with unlimited GPU memory or omit budgeting on Apple silicon.
- Do not call a resource zero-copy without demonstrating compatible storage, format, synchronization, and absence of conversion/readback.
- Keep sparse residency and asset LOD decisions data-driven; do not infer success from allocated bytes alone.

## Handoffs

- `metal-game-rendering-workflow` for command encoding, renderer lifetime, and resource consumers.
- `xcode-game-profiling-workflow` for memory pressure, VM behavior, GPU timeline, or hitch evidence.
- `game-porting-toolkit-workflow` for a source port that needs GPTK’s asset and resource translation guidance.

## Output

Return the measured symptom, selected loading/residency path, budget and fallback policy, synchronization boundary, validation evidence, and unproven hardware assumptions.
