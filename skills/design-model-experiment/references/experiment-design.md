# Experiment Design Rules

## Manifest Semantics

- `hypothesis` must predict an observable difference; “try model X” is an activity, not a hypothesis.
- `decision` says what changes if the hypothesis is supported or rejected.
- `controlled_variable` names the one primary difference being tested.
- `baseline` and `treatment` identify concrete, recoverable artifacts or configurations.
- provenance revisions must be immutable identifiers when the source supports them.
- primary metrics answer the hypothesis; guardrail metrics detect unacceptable regressions.
- failure thresholds and stop conditions are written before results are observed.

## Fair Comparison

Use the same prompt set, chat template, tokenizer behavior, sampling configuration, evaluator, and runtime where those are not the controlled variable. If perfect control is impossible, record the confound and narrow the claim.

## Minimum Artifact Set

Retain the filled manifest, command/config snapshot, environment lock or package inventory, per-case raw results, aggregate calculation, stdout/stderr logs, and a short report distinguishing observations from interpretation.
