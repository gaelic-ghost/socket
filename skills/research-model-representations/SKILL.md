---
name: research-model-representations
description: Design causal research into language-model activations, features, attention, residual streams, probes, circuits, and representation geometry. Use when locating a behavior inside a model, testing whether a direction or feature is causally involved, comparing layers or token positions, or reproducing mechanistic-interpretability research.
---

# Research Model Representations

## Start With A Causal Question

Name the behavior, candidate representation, intervention point, predicted behavioral change, and falsifying result. A decodable probe or correlated activation is evidence of information, not evidence that the model uses it causally.

## Workflow

1. Pin the checkpoint, tokenizer, template, framework, and source-code revision.
2. Construct matched positive, negative, and neutral examples. Control length, topic, syntax, and token positions where practical.
3. Define hook names by verified model architecture rather than assuming layer paths from a related model.
4. Collect activations with explicit batch, dtype, device, token-selection, pooling, and normalization rules.
5. Split probe training and evaluation examples by the true contamination boundary.
6. Establish selectivity controls: random labels, random directions, held-out concepts, and simple surface-feature baselines.
7. Test causality through ablation, patching, steering, or counterfactual replacement at held-out examples.
8. Measure target behavior and unrelated capability guardrails across layers, positions, and intervention strengths.
9. Report unstable seeds, negative results, multiple-comparison choices, and architecture-specific limitations.

## Tool Selection

- [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) provides activation caching and hook-oriented analysis for supported architectures.
- [NNsight](https://github.com/ndif-team/nnsight) provides model instrumentation and remote-capable intervention workflows.

Verify the pinned model and operation against the selected tool. Use direct framework hooks when a small, explicit intervention is clearer than adding a large abstraction.

## References

Read `references/causal-representation-evidence.md` before interpreting a probe or direction as a mechanism.
