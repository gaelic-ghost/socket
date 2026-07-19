# Apple Model Tooling Source Map

Verify moving requirements and APIs against these primary sources:

- [Apple coreai-models](https://github.com/apple/coreai-models): `.aimodel` recipes, Python authoring primitives, Swift runtime utilities, and official agent skills.
- [Apple coreai-torch](https://github.com/apple/coreai-torch): `torch.export.ExportedProgram` conversion through `TorchConverter`, custom lowerings, composite operations, and Metal-kernel support.
- [Apple coreai-optimization](https://github.com/apple/coreai-optimization): Core AI quantization, palettization, and pruning.
- [Apple coremltools](https://github.com/apple/coremltools): Core ML conversion, optimization, and model-package tooling.
- [MLX](https://github.com/ml-explore/mlx), [MLX Swift](https://github.com/ml-explore/mlx-swift), and [MLX LM](https://github.com/ml-explore/mlx-lm): Apple-silicon-native arrays, Swift integration, and language-model workflows.
- [ExecuTorch MLX backend](https://github.com/pytorch/executorch/tree/main/backends/mlx): experimental MLX delegation for exported Edge programs.
- [ExecuTorch Core ML backend](https://github.com/pytorch/executorch/tree/main/backends/apple/coreml): Core ML delegation; evaluate independently from MLX.
- [Foundation Models utilities](https://github.com/apple/foundation-models-utilities) and [Python Apple FM SDK](https://github.com/apple/python-apple-fm-sdk): utilities and Python access around Apple's system model.

Apple's broader organization includes reusable tools such as [Embedding Atlas](https://github.com/apple/embedding-atlas), [DNIKit](https://github.com/apple/dnikit), and [CoreNet](https://github.com/apple/corenet), plus research repositories including `ml-agent-evaluator`, `ml-persona-red-teaming`, `ml-mmtoolsandbox`, `ml-compress-and-compare`, and `ml-mia-bench`. Before adoption, classify each as a maintained framework, benchmark/dataset, paper-specific reproduction, model/checkpoint, sample, or prototype; then pin the reviewed revision.

For Apple-owned SDK and lifecycle behavior, prefer Xcode Documentation Search or Xcode-local documentation. GitHub README claims do not replace current SDK availability checks.
