---
name: fine-tune-language-model
description: Plan and execute supervised fine-tuning, LoRA, QLoRA, or full-parameter language-model training with reproducible provenance and evaluation gates. Use when adapting a checkpoint to new behavior, style, domain, schema, or task and when choosing adapter rank, precision, optimizer, schedule, checkpointing, or resume behavior.
---

# Fine-Tune Language Model

## Choose The Update Strategy

- Prefer LoRA or another parameter-efficient adapter for a bounded behavior/domain change, limited compute, or rapid comparisons.
- Prefer QLoRA when base-model memory is the binding constraint and the selected stack supports the target architecture correctly.
- Use full-parameter tuning only when the hypothesis requires broad weight updates and the compute, storage, optimizer state, and regression burden are justified.
- Do not use fine-tuning to repair a prompt, retrieval, tool schema, or harness defect that can be isolated without changing model weights.

## Workflow

1. Invoke `design-model-experiment`; pin the base checkpoint and tokenizer revisions.
2. Invoke `prepare-language-model-dataset`; freeze train, validation, and untouched test splits.
3. Confirm model/license terms and artifact-publication scope once before training.
4. Record framework and package versions, precision, quantization, optimizer, learning-rate schedule, effective batch size, sequence length, packing, seed, and chat template.
5. Run one batch forward/backward and a short overfit test on a tiny sample. Diagnose loss, masking, labels, and gradient flow before scaling.
6. Save configuration, logs, checkpoints, and adapter metadata together. Test resume from a checkpoint before relying on it.
7. Monitor training and validation signals without choosing the final model solely by training loss.
8. Evaluate the untouched test set plus capability and behavior guardrails using the same decoding configuration as the baseline.
9. Use `compare-model-checkpoints` for the selection decision.

## Failure Modes

- A falling loss with broken answer masking can train the model to copy prompts.
- Different chat templates between training and inference can erase apparent gains.
- Repeated test-set inspection converts the test set into a tuning set.
- Adapter merges and quantization can change behavior; evaluate the exact deployable artifact.
- Resuming with a changed dataset order, optimizer, scheduler, or world size may not reproduce the original run.

## References

Read `references/training-stack.md` before selecting a framework or publishing a training recipe.
