---
name: choose-apple-model-runtime
description: Choose among Apple Core AI model authoring, Core ML, MLX, MLX Swift, MLX LM, ExecuTorch Core ML or experimental MLX delegation, and Apple Foundation Models. Use when converting, optimizing, training, packaging, or deploying a model on Apple silicon or deciding which Apple-owned open-source stack fits a model workflow.
---

# Choose Apple Model Runtime

## Route By Artifact And Constraint

| Need | Start with |
| --- | --- |
| Author `.aimodel` packages with editable Python primitives and Swift runtime utilities | Apple `coreai-models` |
| Lower `torch.export.ExportedProgram` into Core AI IR | `coreai-torch` |
| Quantize, palettize, or prune Core AI models | `coreai-optimization` |
| Convert and deploy established Core ML model packages | `coremltools` plus Core ML |
| Train or run tensor programs natively on Apple silicon | MLX |
| Integrate MLX models in Swift | MLX Swift |
| Fine-tune or serve supported language models with MLX | MLX LM |
| Use one ExecuTorch `.pte` pipeline with Apple acceleration | Compare ExecuTorch Core ML and the experimental MLX backend |
| Use Apple's system on-device language model without shipping weights | Foundation Models framework; use Python Apple FM SDK for supported Python access |

## Decision Workflow

1. Identify the source artifact: PyTorch module/export, safetensors checkpoint, Core ML package, Core AI package, ExecuTorch program, or system model.
2. Identify the deployment API: Python research, Swift app, ExecuTorch C++/mobile, or Foundation Models.
3. Confirm OS, Xcode, SDK, device, architecture, operator, dynamic-shape, state/cache, and precision requirements against the current official source.
4. Select the shortest supported conversion path. Do not round-trip through formats merely because converters exist.
5. Prototype one representative subgraph and one stateful generation step before converting the full model.
6. Evaluate numerical/behavioral parity on the exact packaged artifact.
7. Benchmark on the target device with `benchmark-model-runtime`.

## Important Distinctions

- Core AI and Core ML are related Apple deployment surfaces but are not interchangeable artifact formats or APIs.
- MLX is a general Apple-silicon array framework; MLX LM and MLX Swift are distinct higher-level/use-language surfaces.
- ExecuTorch's MLX backend is marked experimental and under active development upstream. Treat support as revision-specific and compare it separately with the Core ML backend.
- Foundation Models uses Apple's system model and availability contract; it is not a route for packaging arbitrary user-supplied weights.
- Apple research repositories vary from reusable frameworks to benchmark or paper-reproduction code. Classify the repository before recommending it as infrastructure.

## References

Read `references/apple-model-tooling.md` for the official source map and verification checklist.
