---
name: evaluate-language-model
description: Design and run repeatable language-model capability, quality, behavior, regression, or safety evaluations. Use when creating eval cases, choosing deterministic or model-graded metrics, running a benchmark, comparing a treatment with a baseline, or deciding whether a checkpoint is acceptable.
---

# Evaluate Language Model

## Define The Claim

State the population, task, model artifact, prompt/template, decoding settings, and decision threshold. A benchmark score supports only the conditions it measured.

## Build The Evaluation

1. Separate development cases from a held-out decision set.
2. Give every case a stable ID, inputs, tags, expected behavior, and scoring method. Start from `assets/eval-cases.jsonl`.
3. Prefer executable or deterministic graders for exact structure, tests, schemas, and calculations.
4. For model judges, pin the judge model/revision, rubric, prompt, sampling settings, and parser. Calibrate against human-labeled examples and test order/position effects.
5. Record refusals, invalid outputs, timeouts, and grader failures as outcomes; do not silently drop them.
6. Run baseline and treatment on the same cases and settings.
7. Preserve per-case results, then aggregate by meaningful slices as well as globally.
8. Quantify uncertainty with repeated runs, confidence intervals, or paired tests appropriate to the metric.
9. Inspect regressions and disagreements before accepting the aggregate result.

## Evidence Classes

- Configuration validation: cases and graders parse.
- Smoke evidence: a small subset completes end to end.
- Evaluation evidence: the frozen set completes with retained per-case outputs.
- Decision evidence: thresholds, uncertainty, regressions, and limitations support the stated choice.

## Resources

- `assets/eval-cases.jsonl`: starter case schema.
- `assets/evaluation-report.md`: comparison report template.
- `references/evaluation-methods.md`: grader and uncertainty rules.
- `scripts/compare_eval_runs.py`: paired JSONL comparison.
