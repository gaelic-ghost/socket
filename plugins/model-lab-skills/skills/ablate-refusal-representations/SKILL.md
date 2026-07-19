---
name: ablate-refusal-representations
description: Reproduce, extend, or evaluate refusal-direction ablation and related model-internals interventions on locally controlled checkpoints. Use when estimating refusal representations, applying activation or weight orthogonalization, measuring refusal reduction, studying alignment mechanisms, or comparing ablated artifacts with their base model.
---

# Ablate Refusal Representations

## Research Boundary

Treat ablation as controlled model-internals research. Use models and evaluation targets the operator is authorized to modify and test. Do not turn a checkpoint experiment into unapproved probing of a third-party production service.

## Workflow

1. Invoke `design-model-experiment`; state the mechanism claim and the behavior claim separately.
2. Pin the base checkpoint and reproduce its baseline refusal, compliance, capability, and safety behavior.
3. Build matched harmful/harmless or refusal/compliance contrast sets with held-out topics and surface-form controls.
4. Estimate candidate directions across declared layers and token positions; retain searched candidates, not only the winner.
5. Test reversible activation ablation before persistent weight orthogonalization when the hypothesis permits it.
6. Compare zero, sign-reversed, random norm-matched, unrelated-concept, and shuffled-label interventions.
7. Measure refusal reduction on the target set plus benign compliance, general capability, calibration, fluency, and hazardous-behavior guardrails.
8. Evaluate the exact saved artifact after any weight edit, merge, quantization, or conversion.
9. Use `compare-model-checkpoints` and report collateral behavior changes with the headline result.

## Evidence Discipline

Reducing refusal strings is not sufficient: distinguish shallow response-format changes from increased task completion. A direction that generalizes only to the extraction template or searched topics is not a general refusal mechanism.

## References

Read `references/refusal-ablation.md` for the source research and required controls.
