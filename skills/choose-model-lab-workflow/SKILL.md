---
name: choose-model-lab-workflow
description: Route language-model training, data, evaluation, checkpoint, representation, steering, ablation, jailbreak, tool-calling, Apple-runtime, and benchmark requests. Use when the primary workflow or Socket owner is unclear.
---

# Choose Model Lab Workflow

## Outcome

Select one primary workflow, name any supporting workflows, and make the evidence boundary explicit before work begins.

## Route The Request

| Requested outcome | Primary skill |
| --- | --- |
| Define a hypothesis, controls, budget, and artifacts | `design-model-experiment` |
| Curate, transform, split, or document examples | `prepare-language-model-dataset` |
| Run SFT, LoRA, QLoRA, or a full parameter update | `fine-tune-language-model` |
| Measure capability, behavior, quality, or safety | `evaluate-language-model` |
| Decide which checkpoint is better and why | `compare-model-checkpoints` |
| Choose Core AI, Core ML, MLX, ExecuTorch, or Foundation Models | `choose-apple-model-runtime` |
| Locate or test internal representations | `research-model-representations` |
| Apply activation or weight-space behavior steering | `steer-language-model-behavior` |
| Remove or suppress a refusal direction | `ablate-refusal-representations` |
| Measure jailbreak or prompt-injection robustness | `evaluate-jailbreak-resilience` |
| Measure tool selection, arguments, execution, or recovery | `evaluate-tool-calling-model` |
| Compare latency, memory, energy, throughput, or artifact size | `benchmark-model-runtime` |
| Run preference optimization such as DPO/ORPO | Keep the experiment and eval here; use the supported TRL workflow through `fine-tune-language-model` until a stable standalone skill is earned |
| Pretrain or continue pretraining a foundation model | Do not collapse it into fine-tuning; define the distributed/corpus contract and treat `train-language-model` as a deferred skill candidate |
| Merge adapters or quantize/package an artifact | Use `compare-model-checkpoints` around the exact transformation; use the project-native tool and evaluate the deployable output |
| Evaluate an agent skill, plugin, or host harness rather than a model protocol | Hand off to `productivity-skills` and `agent-portability-skills` |

## Respect Ownership Boundaries

- Use `cloud-inference-skills` for provider, GPU, endpoint, cost, and teardown decisions.
- Use `python-skills` for Python packaging and environment repair.
- Use `apple-dev-skills` for Swift/Xcode application integration after the runtime has been chosen.
- Use `productivity-skills` for evaluating agent skills, prompts, or plugin packages rather than model checkpoints.
- Use `cybersecurity-skills` when an authorized evaluation targets a deployed system instead of a model artifact.

## Return A Routing Contract

State:

1. the primary skill;
2. supporting skills in execution order;
3. the controlled variable;
4. the artifact or metric that proves completion;
5. any paid compute, data-access, or deployment authorization required.

Do not silently turn research planning into a paid run, model publication, or production-system test.
