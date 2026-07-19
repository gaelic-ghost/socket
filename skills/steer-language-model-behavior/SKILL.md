---
name: steer-language-model-behavior
description: Implement and evaluate activation steering, representation engineering, logit changes, or weight-space interventions. Use when changing model behavior without ordinary fine-tuning or sweeping layer, strength, and persistence choices.
---

# Steer Language Model Behavior

## Choose The Intervention

- Use prompt or harness controls first when they satisfy the product need and the research question is not about internals.
- Use activation steering for reversible, inference-time causal tests or runtime control.
- Use logit interventions for token-level constraints whose scope can be stated explicitly.
- Use weight-space changes for persistent behavior only after a reversible intervention establishes the direction and regression burden.

## Workflow

1. Invoke `research-model-representations` to define or validate the steering signal.
2. Freeze target and guardrail evaluation sets before selecting layers or strengths.
3. Record layer, hook point, token position, normalization, sign, magnitude, schedule, and generation settings.
4. Sweep a bounded strength range including zero and negative controls.
5. Compare with prompt-only, random-direction, and norm-matched controls.
6. Measure target success, capability regressions, fluency, calibration, diversity, and off-target behavioral changes.
7. For persistent changes, preserve the base checkpoint as immutable, write a new artifact, record both checksums and the transformation, and never edit weights in place.
8. Re-run the exact packaged or merged artifact if the intervention becomes persistent.
9. Report the smallest effective intervention and the operating range where the claim holds.

## Interpretation

A successful steering vector demonstrates controllability under tested conditions. It does not by itself establish a unique representation, a complete mechanism, or safe generalization. Stronger target behavior with broad unrelated regressions is not a clean success.

## References

Use `references/steering-controls.md` as the minimum comparison matrix.
