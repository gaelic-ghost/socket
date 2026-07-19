---
name: compare-model-checkpoints
description: Compare base, adapter, merged, quantized, converted, or intervention-derived checkpoints. Use when selecting an artifact, investigating regression, verifying packaging, or balancing quality, safety, size, and runtime.
---

# Compare Model Checkpoints

## Normalize Before Comparing

Identify the exact model and tokenizer revisions, chat template, adapter/merge state, quantization or conversion recipe, prompt set, generation parameters, evaluator, runtime, and hardware. Treat any uncontrolled difference as a confound.

## Workflow

1. Preserve every source artifact as immutable, snapshot its provenance with `scripts/snapshot_model_provenance.py`, and write the snapshot outside the artifact directory.
2. Verify that every comparison artifact can be loaded and produces output on the same smoke cases.
3. Use `evaluate-language-model` for paired quality and behavior evidence.
4. Use `benchmark-model-runtime` when deployment properties affect the decision.
5. Compare primary metrics, guardrails, per-slice regressions, artifact size, memory, latency, and load reliability.
6. Inspect high-impact case changes rather than choosing by one aggregate score.
7. Copy `assets/model-comparison-report.md` and give a conditional recommendation when tradeoffs differ by deployment target.

## Comparison Rules

- Evaluate the exact artifact that will ship; an unmerged adapter does not prove the merged or quantized export.
- Do not compare stochastic generations without repeated samples or a fixed sampling contract.
- Do not call two checkpoints equivalent because their average scores match; inspect paired disagreements and guardrails.
- Report missing provenance as a finding, not as an implied default.

## Resources

- `assets/model-comparison-report.md`: selection report.
- `references/checkpoint-provenance.md`: provenance field guide.
- `scripts/snapshot_model_provenance.py`: deterministic local artifact inventory.
