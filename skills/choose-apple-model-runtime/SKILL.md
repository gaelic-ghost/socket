---
name: choose-apple-model-runtime
description: Compare and select Core AI, Core ML, MLX, MLX Swift, MLX LM, ExecuTorch Apple delegates, or Foundation Models. Use when an Apple model workflow needs a runtime choice and implementation handoff.
---

# Choose Apple Model Runtime

## Route By Artifact And Constraint

| Need | Start with |
| --- | --- |
| Host a downloaded model locally for an API client, agent framework, or dev tool | LM Studio local server; choose native `/api/v1` model-management APIs or OpenAI-compatible `/v1` inference APIs deliberately |
| Author `.aimodel` packages with editable Python primitives and Swift runtime utilities | Choose Core AI, then hand off to the `coreai-models` `working-with-coreai` and `model-authoring` skills |
| Lower `torch.export.ExportedProgram` into Core AI IR | `coreai-torch` |
| Quantize, palettize, or prune Core AI models | Choose Core AI, then hand off to Apple's `model-compression-exploration` skill and `coreai-optimization` |
| Convert and deploy established Core ML model packages | `coremltools` plus Core ML |
| Train or run tensor programs natively on Apple silicon | MLX |
| Integrate MLX models in Swift | MLX Swift |
| Fine-tune or serve supported language models with MLX | MLX LM |
| Use one ExecuTorch `.pte` pipeline with Apple acceleration | Compare the ExecuTorch Core ML backend and experimental MLX delegate |
| Use Apple's system on-device language model without shipping weights | Foundation Models framework; use Python Apple FM SDK for supported Python access |

## Decision Workflow

1. Decide whether the need is a local inference server for a client or an app-packaged runtime/artifact. Use LM Studio for the former; identify the source artifact for the latter.
2. Identify the deployment API: Python research, Swift app, ExecuTorch C++/mobile, or Foundation Models.
3. Consult the dated maturity and availability matrix in `references/apple-model-tooling.md`, then confirm OS, Xcode, SDK, device, architecture, operator, dynamic-shape, state/cache, and precision requirements against the current official source.
4. Select the shortest supported conversion path. Do not round-trip through formats merely because converters exist.
5. Prototype one representative subgraph and one stateful generation step before converting the full model.
6. Evaluate numerical/behavioral parity on the exact packaged artifact.
7. Benchmark on the target device with `benchmark-model-runtime`.
8. Return the selected runtime, maturity class, source revision/date checked, unmet availability gates, and implementation owner. Hand Core AI authoring/compression to Apple's named skills and app-facing Swift/Xcode work to `apple-dev-skills`.

## Important Distinctions

- Core AI and Core ML are related Apple deployment surfaces but are not interchangeable artifact formats or APIs.
- MLX is a general Apple-silicon array framework; MLX LM and MLX Swift are distinct higher-level/use-language surfaces.
- ExecuTorch's MLX delegate is marked experimental and under active development upstream. Treat support as revision-specific and compare it separately with the Core ML backend.
- Foundation Models uses Apple's system model and availability contract; it is not a route for packaging arbitrary user-supplied weights.
- LM Studio is a local model server and control plane, not a Core AI, Core ML, MLX, or Foundation Models artifact/runtime. Its endpoint compatibility does not prove model tool use or structured-output behavior.
- Apple research repositories vary from reusable frameworks to benchmark or paper-reproduction code. Classify the repository before recommending it as infrastructure.

## References

Read `references/apple-model-tooling.md` for the official source map and verification checklist.
