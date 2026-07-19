---
name: evaluate-jailbreak-resilience
description: Evaluate authorized language-model jailbreak and prompt-injection resilience with reproducible attack families, target policies, adaptive budgets, graders, and side-effect boundaries. Use for model checkpoints, local harnesses, or explicitly authorized systems when measuring attack success, refusal behavior, instruction hierarchy, or regression after a defense.
---

# Evaluate Jailbreak Resilience

## Establish Authorization And Scope

Name the model or system owner, allowed target, data boundary, attack surfaces, maximum attempts, tool/network permissions, retention policy, and stop condition. Default to local checkpoints and inert test tools. Real external systems require explicit authorization.

## Build The Evaluation

1. Define the prohibited or protected behaviors as observable policy cases rather than vague “safety.”
2. Separate direct jailbreaks, role-play/encoding transformations, multi-turn attacks, indirect prompt injection, tool-output injection, and adaptive attacks.
3. Freeze a non-adaptive suite for regression tracking; isolate adaptive attacks and record their query budget.
4. Include benign hard negatives that resemble attacks but should succeed normally.
5. Pin model, system prompt, template, sampling, harness, defense, and grader revisions.
6. Grade policy outcome, task completion, refusal correctness, benign over-refusal, tool side effects, and detection/recovery separately.
7. Manually audit a stratified sample and all high-severity successes.
8. Report attack success by family and budget with uncertainty and invalid-case counts.

## Safe Harness Rules

- Replace destructive or privileged tools with deterministic fakes unless the system test explicitly requires a sandboxed real tool.
- Block network and credential access by default.
- Redact secrets and personal data from cases and logs.
- Do not publish reusable exploit payloads or harmful generations beyond what the authorized evidence requires.

## References

Use `references/jailbreak-evaluation.md` for suite construction and disclosure rules.
