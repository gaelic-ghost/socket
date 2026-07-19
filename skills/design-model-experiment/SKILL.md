---
name: design-model-experiment
description: Design a reproducible model experiment with hypotheses, controls, baselines, metrics, budgets, provenance, artifacts, and stop conditions. Use before model work whose results must support a decision.
---

# Design Model Experiment

## Outcome

Produce an experiment manifest that another operator can run, audit, and compare without reconstructing unstated choices.

## Workflow

1. Write one falsifiable hypothesis and the decision it informs.
2. Define the experimental unit: model revision, adapter, prompt set, intervention, runtime, or harness.
3. Name exactly one primary controlled variable per comparison. Record every intentional difference.
4. Select a baseline and explain why it is a fair comparator.
5. Pin model, tokenizer, dataset, code, dependency, template, evaluator, and seed provenance.
6. Define primary metrics, guardrail metrics, uncertainty treatment, and failure thresholds before the run.
7. Estimate compute, storage, time, and paid cost. Set smoke-test and full-run stop conditions.
8. Define raw and derived artifacts, retention, and sensitive-data handling.
9. Copy `assets/experiment-manifest.yaml`, fill it, then run:

```bash
python3 scripts/validate_experiment_manifest.py path/to/experiment.yaml
```

10. Run the smallest experiment capable of detecting configuration or pipeline failure before spending the full budget.

## Evidence Contract

Keep configuration validation, smoke-run evidence, and final experimental evidence separate. A successful process exit proves execution, not model quality. Report deviations from the manifest before interpreting results.

## Resources

- `assets/experiment-manifest.yaml`: portable experiment template.
- `references/experiment-design.md`: field semantics and comparison rules.
- `scripts/validate_experiment_manifest.py`: deterministic structural validation.
