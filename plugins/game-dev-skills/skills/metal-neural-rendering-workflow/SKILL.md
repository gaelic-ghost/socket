---
name: metal-neural-rendering-workflow
description: Plan and implement experimental Metal neural-rendering paths with MetalFX, Metal 4 machine-learning passes, Metal tensors, and Metal Performance Primitives. Use when Codex works on learned tone mapping, neural denoising, neural materials, inline tensor operations, MTL4MachineLearningCommandEncoder, or model inference scheduled beside rendering; preserve a conventional rendering fallback.
---

# Metal Neural Rendering Workflow

## Scope

Own a small, measurable learned rendering pass and its rendering integration. This skill is experimental and beta-sensitive where it depends on Metal 4.1-era API or hardware; it does not authorize replacing an established renderer with an unproven ML subsystem.

Read [integration-levels.md](references/integration-levels.md) before selecting a technology. Verify the exact SDK header, Metal feature-set support, and device availability before code changes.

## Choose The Smallest Integration

1. Use **MetalFX** when a supported scaler, frame interpolator, or denoiser already solves the visual problem.
2. Use an **ML command encoder** when a pre-trained model must run as a scheduled Metal 4 pass beside existing render/compute work.
3. Use **inline tensor operations** only for a compact shader-local operation whose data layout, precision, and GPU-family gate are explicit.
4. Use **Metal Performance Primitives or MPSGraph** when a maintained primitive or graph fits better than custom shader math.
5. Stop and ask for a design decision when the request requires training, model conversion, artifact distribution, or a persistent model-update system; those are separate product and architecture scopes.

## Workflow

1. State the visual defect, baseline technique, target metric, fallback, and representative scenes before choosing ML.
2. Define model inputs/outputs, colorspace, precision, tensor layout, resource ownership, and synchronization with adjacent passes.
3. Gate by OS, Metal version, GPU family, and hardware. Keep a conventional renderer path for unsupported devices.
4. Validate numerical correctness against a deterministic reference before visual-quality tuning.
5. Compare quality, frame time, memory, power/thermal behavior, and temporal stability against the baseline on target hardware.
6. Keep model provenance, version, preprocessing, and fixed test inputs explicit so results remain reproducible.

## Guardrails

- Do not claim neural acceleration on a device without feature-table and runtime evidence.
- Do not read back tensors merely for convenience on a per-frame path; make any CPU/GPU boundary explicit and measured.
- Do not conflate a Metal 4 ML pass with Core ML, a generic model-serving stack, or a training workflow.

## Handoffs

- `metalfx-game-rendering-workflow` when an off-the-shelf MetalFX effect fits.
- `metal-game-rendering-workflow` for the surrounding render graph and presentation contract.
- `xcode-game-profiling-workflow` for performance evidence.
- `coreml-skills` or `mlx-skills` only when those dedicated plugins ship and the work is model packaging, conversion, or broader on-device ML rather than renderer integration.

## Output

Return the chosen integration level, feature gate and fallback, tensor/model contract, correctness fixture, measured comparison plan, and any broader architecture decision required.
