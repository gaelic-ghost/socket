---
name: research-model-representations
description: Design causal research into model activations, features, attention, residual streams, probes, and circuits. Use when locating behavior, testing a direction or feature, comparing layers, or reproducing interpretability research.
---

# Research Model Representations

## Start With A Causal Question

Name the behavior, candidate representation, intervention point, predicted behavioral change, and falsifying result. A decodable probe or correlated activation is evidence of information, not evidence that the model uses it causally.

## Workflow

1. Pin the checkpoint, tokenizer, template, framework, and source-code revision.
2. Construct matched positive, negative, and neutral examples. Control length, topic, syntax, and token positions where practical.
3. Define hook names by verified model architecture rather than assuming layer paths from a related model.
4. Decide local versus remote instrumentation. Before remote execution, classify prompts and activations, confirm authorization, retention/logging behavior, network exposure, and paid-compute budget; keep proprietary or sensitive inputs local unless explicitly approved.
5. Collect activations with explicit batch, dtype, device, token-selection, pooling, and normalization rules.
6. Split probe training and evaluation examples by the true contamination boundary.
7. Establish selectivity controls: random labels, random directions, held-out concepts, and simple surface-feature baselines.
8. Test causality through ablation, patching, steering, or counterfactual replacement at held-out examples.
9. Measure target behavior and unrelated capability guardrails across layers, positions, and intervention strengths.
10. Report unstable seeds, negative results, multiple-comparison choices, and architecture-specific limitations.

## Tool Selection

- [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) provides activation caching and hook-oriented analysis for supported architectures.
- [NNsight](https://github.com/ndif-team/nnsight) provides model instrumentation and remote-capable intervention workflows.

Verify the pinned model and operation against the selected tool. Use direct framework hooks when a small, explicit intervention is clearer than adding a large abstraction.

## References

Read `references/causal-representation-evidence.md` before interpreting a probe or direction as a mechanism.
