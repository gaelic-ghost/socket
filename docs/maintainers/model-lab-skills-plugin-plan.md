# Model Lab Skills Plugin Plan

## Purpose

The `model-lab-skills` plugin should help agents design, run, compare, and
document reproducible language-model experiments without mixing model behavior
research with cloud-provider operations, application implementation, or
host-specific agent packaging.

The plugin should cover the path from source model and dataset through
fine-tuning or model intervention, evaluation, runtime comparison, and an
evidence-backed artifact decision. It should support ordinary capability work,
fine-tuning, preference optimization, interpretability, activation steering,
refusal-direction ablation, authorized jailbreak research, local inference,
and model or agent harness comparisons.

This is a durable building-block plugin, not a temporary collection of tool
notes. Its core primitive is a reproducible experiment record that keeps model,
data, transformation, runtime, evaluation, and artifact provenance connected.

## Decision

Create one new Socket child plugin named `model-lab-skills`.

Do not expand `cloud-inference-skills` into the model-research owner. Its
existing provider, credential, GPU, cost, endpoint, and teardown decisions are
already coherent. `model-lab-skills` should decide what experiment to run and
how to judge it; `cloud-inference-skills` should decide where and how to run the
required workload.

Do not create separate `mlx-skills`, `coreml-skills`, or `coreai-skills`
plugins in the first pass. Put cross-runtime Apple model selection and evidence
comparison in `model-lab-skills`, retain app-facing integration in
`apple-dev-skills`, and hand rapidly changing Core AI implementation details to
Apple's own skills in [`apple/coreai-models`](https://github.com/apple/coreai-models).
Reconsider a narrower dedicated plugin only if repeated implementation work
cannot be expressed cleanly through those three owners.

Do not bundle an MCP server in the first pass. Existing libraries, CLIs,
provider plugins, source repositories, and test runners are the correct
execution surfaces. Add an MCP declaration only after a repeated operation
shows that agent-safe discovery or mutation materially improves through MCP.

## Ownership

| Concern | Owner |
| --- | --- |
| Model experiment design, dataset shape, training recipe, intervention, model evaluation, checkpoint comparison, and model artifact decision | `model-lab-skills` |
| Provider choice, GPU infrastructure, account and credential boundaries, cost, endpoint lifecycle, storage, and teardown | `cloud-inference-skills` |
| Agent, skill, prompt, and automation evaluation design | `productivity-skills:design-agent-eval-workflow` |
| Codex, Claude, Hermes, Xcode, Zed, and other host capability or packaging compatibility | `agent-portability-skills` |
| Authorized security testing whose model or agent can reach real tools, systems, accounts, or sensitive data | `cybersecurity-skills` |
| Python project structure, environment management, packaging, tests, lint, and CI | `python-skills` |
| Swift app integration, Xcode execution, instruments, Core ML or Core AI app wiring, and Foundation Models framework use | `apple-dev-skills` |
| Core AI export, authoring, compression, and runtime details already covered upstream | Apple's `coreai-models` skills |
| Hugging Face Hub repositories, datasets, Jobs, endpoints, and publication operations | Official Hugging Face plugin and CLI surfaces |

### Model Harness Versus Agent Harness

Keep these terms separate:

- A `model harness` loads or calls a model, applies the exact tokenizer and chat
  template, generates samples, records inference settings, evaluates outputs,
  and measures runtime behavior.
- An `agent harness` adds tools, state, permissions, orchestration, approvals,
  persistence, and host-specific behavior around one or more models.

`model-lab-skills` should own model-harness selection and model-level evidence.
`productivity-skills` should own general agent-eval design.
`agent-portability-skills` should own host and packaging comparisons. A
tool-using agent evaluation should compose those owners rather than invent a
second model-evaluation path.

## Experiment Model

Every workflow should preserve this straight data flow:

```text
source model + immutable revision
    -> dataset + transformation provenance
    -> training or intervention recipe
    -> checkpoint or model artifact
    -> fixed evaluation suite
    -> comparison report
    -> keep, iterate, package, publish, or discard decision
```

The experiment record should capture:

- source repository, model identifier, immutable revision, configuration,
  tokenizer, chat template, license, and checksums
- dataset sources, licenses, transformations, deduplication, contamination
  checks, splits, and prompt/response schema
- code revision, dependency lock, seed, dtype, quantization, hardware, driver,
  runtime, environment, and budget
- training, optimization, merge, steering, or ablation parameters
- checkpoint cadence, resume behavior, intermediate artifacts, logs, and
  cleanup policy
- evaluation cases, graders, thresholds, baselines, confidence or variance,
  and known limitations
- publication boundary for weights, adapters, datasets, prompts, reports, and
  generated artifacts

## First Skill Slice

### `choose-model-lab-workflow`

Route requests across dataset work, supervised fine-tuning, preference
optimization, full training, evaluation, checkpoint comparison,
interpretability, steering, ablation, quantization, merging, runtime
benchmarking, Apple on-device deployment research, and agent-harness handoffs.

Return the experiment goal, evidence already available, selected owner skill,
runtime or provider handoff, artifact boundary, cost boundary, and next
validation checkpoint.

### `design-model-experiment`

Create the reproducible experiment manifest before expensive or irreversible
work begins. Define the hypothesis, control, candidate, independent variable,
fixed inference conditions, case set, metrics, stop conditions, budget, and
artifact retention policy.

Keep experimental claims narrower than the evidence. Do not call a conversion,
training run, or intervention successful merely because it produced an
artifact that loads.

### `prepare-language-model-dataset`

Guide acquisition, cleaning, normalization, chat formatting, deduplication,
contamination checks, train/validation/test separation, sampling, balancing,
and dataset-card production.

Keep supervised examples, preference pairs, reward-model labels, synthetic
data, adversarial cases, and evaluation fixtures as explicit schemas. Do not
silently coerce them into one generic conversation format.

### `fine-tune-language-model`

Choose full fine-tuning or parameter-efficient fine-tuning from model size,
hardware, data volume, target behavior, and artifact requirements. Cover
supervised fine-tuning, LoRA, QLoRA, checkpointing, resumption, overfitting
checks, held-out evaluation, and adapter handling.

Use [Hugging Face TRL](https://huggingface.co/docs/trl/) and
[PEFT](https://huggingface.co/docs/peft/) as a preferred documented Python lane
when they fit. Do not make one trainer mandatory when a repository already has
a sound training stack.

Hand provider, GPU, storage, and teardown decisions to
`cloud-inference-skills`. Hand Python project maintenance to `python-skills`.

### `evaluate-language-model`

Build and run model-level evaluation suites across task quality, instruction
following, behavioral quality, refusal, over-refusal, jailbreak resistance,
calibration, memorization, regressions, latency, throughput, peak memory, and
artifact size as applicable.

Normalize model revision, tokenizer, chat template, system prompt, sampling,
context length, stop conditions, and runtime before comparing outputs. Prefer
deterministic graders first, then task-specific scorers, and use model graders
only where judgment is the behavior being measured.

Use [EleutherAI's Language Model Evaluation
Harness](https://github.com/EleutherAI/lm-evaluation-harness) for suitable
standard model benchmarks and reproducible task definitions. Use
[Inspect](https://inspect.aisi.org.uk/) when sandboxed agents, tools, limits,
or stateful evaluation are the real test surface.

### `compare-model-checkpoints`

Compare base, control, intermediate, and candidate checkpoints under identical
inference conditions. Produce paired samples, aggregate metrics, variance or
confidence where available, regression categories, and a keep/iterate/discard
recommendation.

Treat absence of a measured regression as scoped evidence, not proof that the
model is unchanged outside the tested distribution.

### `choose-apple-model-runtime`

Choose among Apple's system Foundation Models surface, Core AI, Core ML,
direct MLX, ExecuTorch with the Core ML backend, ExecuTorch with the MLX
delegate, or a hosted/local chat-completions model before implementation.

Base the choice on target OS and hardware, app/runtime language, artifact
format, operator coverage, dynamic-shape needs, tokenizer and resource
packaging, quantization, accelerator goal, portability, debugging needs, and
current stability. Return an explicit runtime comparison and the owning
implementation handoff.

Do not duplicate Apple's `working-with-coreai`, `model-authoring`, or
`model-compression-exploration` skills. Load or recommend the Apple-owned
skills for implementation details and keep Socket's skill focused on
cross-runtime choice, reproducibility, and evidence comparison.

## Second Skill Slice

### `research-model-representations`

Guide activation capture, probing, attribution, causal interventions, circuit
or feature hypotheses, and controlled comparisons. Use
[TransformerLens](https://github.com/TransformerLensOrg/TransformerLens),
[NNsight](https://nnsight.net/), or another repo-owned framework when it fits
the model and research question.

Require a falsifiable hypothesis, control prompts, exact hook points, tensor
shape and dtype records, intervention strength, and downstream behavioral
evaluation.

### `steer-language-model-behavior`

Guide reversible activation steering, representation engineering, task
vectors, adapter composition, and inference-time interventions. Separate
activation-only changes from saved weight changes and keep steering strength,
layers, token positions, prompt populations, and evaluation results explicit.

### `ablate-refusal-representations`

Give refusal-direction ablation, commonly called abliteration, its own
research workflow. Start from the method and code associated with
[Refusal in Language Models Is Mediated by a Single
Direction](https://arxiv.org/abs/2406.11717) while treating the single-direction
model as a hypothesis to test on each architecture and checkpoint.

Require an untouched base model, harmless and harmful control sets, held-out
prompts, multiple refusal measures, ordinary capability tests, coherence and
calibration checks, exact layer and projection records, reversible artifacts,
and pre/post comparisons. Do not define success as a lower refusal rate alone.

### `evaluate-jailbreak-resilience`

Evaluate owned open-weight models, local models, and explicitly authorized
endpoints against direct, encoded, role-play, multi-turn, contextual,
indirect-prompt-injection, and tool-mediated attacks.

Version the target model, system prompt, tokenizer, chat template, sampler,
tool schema, attack corpus, evaluator, and success rubric. Preserve successful
and unsuccessful cases. Hand tests that can mutate real systems or reach
sensitive data to `cybersecurity-skills` for authorization, isolation, and
impact controls.

### `evaluate-tool-calling-model`

Measure schema adherence, tool selection, argument correctness, recovery from
tool errors, multi-step completion, state tracking, and unnecessary tool use.
Keep the model's native tool-call protocol separate from the surrounding agent
harness and report both model-level and harness-level failures.

### `benchmark-model-runtime`

Measure load time, time to first token, prompt processing, decode throughput,
memory, accelerator utilization, thermals, power where available, artifact
size, and output parity. Require warm and cold runs, fixed prompts, fixed
generation lengths, current hardware/software identity, and repeated samples.

For Apple Silicon work, compare runtime routes on the same model slice before
generalizing. Hand Instruments, Metal, MLX, Core ML, Core AI, and Swift package
execution to the applicable Apple Dev Skills workflow.

## Later Skill Candidates

- `train-language-model`
- `preference-optimize-language-model`
- `distill-language-model`
- `merge-model-adapters`
- `quantize-model-artifact`
- `package-model-research-artifacts`
- `generate-synthetic-training-data`
- `evaluate-multimodal-model`
- `research-agent-harness`
- `evaluate-agent-harness`

Do not add all candidates at once. Add a skill after a real task demonstrates a
distinct trigger, workflow, output contract, and validation boundary that does
not fit an existing skill cleanly.

`train-language-model` should own pretraining and continued-pretraining work
that is materially different from fine-tuning: tokenizer and corpus scale,
distributed training, optimizer and scheduler behavior, checkpoint topology,
fault recovery, scaling evidence, data curriculum, and sustained compute
budget. Until those requirements are present, route smaller full-parameter
adaptation through `fine-tune-language-model` rather than pretending every
weight-updating run is foundation-model pretraining.

## Apple AI And Open-Source Tooling Lane

### Runtime And Deployment Stack

Official sources checked on 2026-07-19:

| Surface | Current role | Model Lab treatment |
| --- | --- | --- |
| [`apple/coreai-models`](https://github.com/apple/coreai-models) | Export recipes, Python authoring primitives, Swift runtime utilities, `.aimodel` resources, CLI tools, and upstream coding-agent skills; current README requires macOS/iOS 27 and Xcode 27 for runtime integration | Preferred Core AI implementation handoff and model catalog; do not copy its skills |
| [`apple/coreai-torch`](https://github.com/apple/coreai-torch) | Converts `torch.export.ExportedProgram` graphs to Core AI IR and supports composite ops, custom lowerings, submodule externalization, and inline Metal kernels | Record conversion path, operator coverage, custom-kernel boundary, compiler/runtime versions, and parity evidence |
| [`apple/coreai-optimization`](https://github.com/apple/coreai-optimization) | `coreai-opt` quantization, palettization, and pruning for PyTorch models targeting Core AI | Treat optimization as an experiment with size, quality, latency, memory, and hardware comparisons |
| [`apple/coremltools`](https://github.com/apple/coremltools) | Established model conversion, editing, optimization, and validation for Core ML artifacts | Preserve as a distinct Core ML route; do not treat Core AI as a transparent rename or automatic replacement |
| [`ml-explore/mlx`](https://github.com/ml-explore/mlx) | Apple-silicon array and machine-learning framework with CPU/GPU execution and unified-memory-oriented primitives | Use for direct local experimentation and runtime baselines when a native MLX path fits |
| [`ml-explore/mlx-swift`](https://github.com/ml-explore/mlx-swift) | Swift API for MLX on Apple silicon | Hand app/package implementation to Apple Dev Skills while Model Lab owns model and runtime evidence |
| [`ml-explore/mlx-lm`](https://github.com/ml-explore/mlx-lm) | MLX language-model inference and fine-tuning utilities | Use as an Apple-silicon-native model harness when model support and experiment needs fit |
| [ExecuTorch MLX delegate](https://github.com/pytorch/executorch/tree/main/backends/mlx) | Experimental ExecuTorch backend that lowers exported PyTorch graphs into an MLX-backed `.pte` runtime for Apple Silicon GPUs | Include in runtime comparisons, but require current source, operator support, fallback, output parity, and performance evidence before recommending it |
| [ExecuTorch Core ML backend](https://docs.pytorch.org/executorch/stable/ios-coreml.html) | ExecuTorch deployment through Core ML on Apple platforms | Compare separately from the MLX delegate because artifact, platform, accelerator, partitioning, and fallback behavior differ |

The ExecuTorch MLX delegate should be named precisely as a `delegate`, not a
generic adapter. Its upstream README currently marks it experimental and under
active development. Treat API shape, supported operations, quantization,
fallback behavior, build requirements, platform coverage, and performance as
versioned evidence.

### Foundation Models And Harness Integration

- [`apple/foundation-models-utilities`](https://github.com/apple/foundation-models-utilities)
  adds Apple-owned utilities and agent skills around the Foundation Models
  framework, including custom skills, history management, and a
  chat-completions-backed `LanguageModel` implementation.
- [`apple/python-apple-fm-sdk`](https://github.com/apple/python-apple-fm-sdk)
  provides Python access to the on-device system model and explicitly supports
  batch evaluation of Swift Foundation Models features.

Keep system-model and application-session work in Apple Dev Skills. Use Model
Lab when those surfaces become a model/harness comparison, batch evaluation,
or reproducible experiment. Never imply that system-model access exposes model
weights or the same intervention surface as an open-weight model.

### Reusable Apple Research Tools

- [`apple/embedding-atlas`](https://github.com/apple/embedding-atlas) provides
  interactive, multimodal embedding visualization, filtering, search, notebook
  integration, and an MCP query surface. Consider it in dataset, representation,
  and error-analysis workflows without making visualization mandatory.
- [`apple/dnikit`](https://github.com/apple/dnikit) provides model and dataset
  introspection workflows. Treat it as a candidate for data/model diagnostics,
  subject to current framework compatibility.
- [`apple/corenet`](https://github.com/apple/corenet) is Apple's reusable
  deep-learning training toolkit with foundation-model, language, vision, and
  multimodal research projects. Route to it when an existing repo or research
  reproduction already uses CoreNet; do not replace a sound project-native
  trainer merely because CoreNet is Apple-owned.

### Apple Research-Code Watchlist

Apple's `ml-*` repositories are growing quickly. Classify each repository
before recommending it:

- `reusable tool or framework`
- `benchmark or dataset`
- `paper-specific reproduction code`
- `model or checkpoint release`
- `sample application`
- `exploratory prototype`

Useful current examples include:

- [`apple/ml-agent-evaluator`](https://github.com/apple/ml-agent-evaluator)
  for research on tool-assisted LLM-as-a-judge evaluation
- [`apple/ml-persona-red-teaming`](https://github.com/apple/ml-persona-red-teaming)
  for persona-driven automated red-team research
- [`apple/ml-mmtoolsandbox`](https://github.com/apple/ml-mmtoolsandbox) for
  multimodal tool-calling agent evaluation in a stateful sandbox
- [`apple/ml-compress-and-compare`](https://github.com/apple/ml-compress-and-compare)
  for interactive compression experiment comparison
- [`apple/ml-mia-bench`](https://github.com/apple/ml-mia-bench) for multimodal
  instruction-following evaluation

Do not turn this watchlist into copied workflow guidance. Inspect the current
README, source, release or commit, dependencies, license, datasets, and tests
when a task actually selects one of these repositories.

## Tool Selection Principles

- Choose the information model before choosing a library: training,
  generation, standardized benchmark, agent sandbox, representation trace,
  model modification, deployment conversion, or runtime profiling.
- Prefer repository-native code and official upstream tools before adding a
  wrapper.
- Pin versions or immutable commits for experimental and research code.
- Validate tokenizer and chat-template parity before diagnosing model quality.
- Prove a small hosted or local sample before paying for conversion or
  fine-tuning of a candidate model.
- Keep evaluation fixtures independent from training data and intervention
  prompt sets.
- Keep model weights, private datasets, caches, provider credentials, and
  generated artifacts out of source control unless the repository explicitly
  owns sanitized, distributable fixtures.
- Separate artifact creation from publication. Producing a checkpoint locally
  does not authorize uploading it.

## Planned Resources

The first implementation should create only resources earned by repeated
workflow needs:

```text
plugins/model-lab-skills/
├── .codex-plugin/plugin.json
├── AGENTS.md
├── assets/
│   └── model-lab-icon.svg
└── skills/
    ├── choose-model-lab-workflow/
    ├── design-model-experiment/
    │   └── assets/experiment-manifest.yaml
    ├── prepare-language-model-dataset/
    │   └── assets/dataset-card.md
    ├── fine-tune-language-model/
    ├── evaluate-language-model/
    │   └── assets/eval-case-set.jsonl
    ├── compare-model-checkpoints/
    │   └── assets/model-comparison-report.md
    └── choose-apple-model-runtime/
```

Likely deterministic scripts after the contracts settle:

- `validate_experiment_manifest.py`
- `snapshot_model_provenance.py`
- `compare_eval_runs.py`

Do not add these scripts as placeholders. Add and test them when the first
implemented skill needs their deterministic behavior.

## Compatibility

- Design the first slice as portable Agent Skills with ordinary files and
  commands rather than Codex-only runtime extensions.
- Add every portable skill to Socket's Hermes tap export and validate it in the
  same implementation pass.
- Classify the plugin for Claude Code and Cowork using the existing Socket
  compatibility workflow.
- Keep provider plugins, Apple-owned agent skills, MCP servers, and local
  runtimes as explicit external handoffs instead of embedding private config or
  pretending their host packaging is portable.

## Safety, Authorization, And Publication Boundaries

- Model modification and refusal research may proceed on owned open-weight
  models and explicitly authorized targets.
- Jailbreak and prompt-injection research must record the target and
  authorization boundary. Route real-system impact through
  `cybersecurity-skills`.
- Never claim a model is safe, uncensored, aligned, unbiased, or capability
  preserving from a narrow benchmark alone.
- Treat refusal reduction, harmful-compliance increase, ordinary capability,
  over-refusal, calibration, and coherence as separate measurements.
- Keep private datasets, model licenses, redistribution terms, and publication
  decisions explicit. Private experiments do not automatically imply public
  redistribution rights.

## Delivery Plan

### Slice 1: Plugin Foundation And Routing

- Create the plugin scaffold, child `AGENTS.md`, icon, and
  `choose-model-lab-workflow`.
- Add the experiment ownership matrix and handoffs.
- Add Codex, Hermes, Claude Code, and Cowork compatibility classifications.
- Keep marketplace installation unavailable until useful workflow content
  exists.

### Slice 2: Reproducible Training And Evaluation

- Add `design-model-experiment`, `prepare-language-model-dataset`,
  `fine-tune-language-model`, `evaluate-language-model`, and
  `compare-model-checkpoints`.
- Add only the templates and deterministic validators required by those skills.
- Forward-test representative local, cloud, and adapter-based experiments.

### Slice 3: Apple Runtime Selection

- Add `choose-apple-model-runtime` with current official-source references.
- Validate handoffs to Apple-owned Core AI skills and Apple Dev Skills.
- Compare Core AI, Core ML, direct MLX, ExecuTorch Core ML, and experimental
  ExecuTorch MLX without claiming runtime results that were not executed.

### Slice 4: Model Internals And Adversarial Evaluation

- Add representation research, steering, ablation, jailbreak-resilience, and
  tool-calling evaluation skills.
- Require stronger forward tests because these workflows are sensitive to
  hidden assumptions, contaminated case sets, and misleading success metrics.

### Slice 5: Runtime Benchmarking And Artifact Workflow

- Add runtime benchmarking after at least two real runtime-comparison tasks.
- Decide whether quantization, merging, packaging, and publication each earn a
  separate skill.
- Reconsider a bundled MCP server only from demonstrated repeated need.

## Checklist

- [x] Record the plugin decision and ownership split.
- [x] Record the initial skill inventory and delivery slices.
- [x] Integrate Core AI, Core ML, MLX, ExecuTorch Core ML, and ExecuTorch MLX
  into the runtime-selection plan.
- [x] Record Apple's current Core AI repositories and upstream agent-skill
  handoff.
- [x] Record the Apple open-source AI toolkit and research-code classification
  policy.
- [x] Run root metadata validation for the documentation-only planning pass.
- [ ] Scaffold `plugins/model-lab-skills/` on an implementation branch.
- [ ] Add the first skill slice and targeted validation.
- [ ] Add Socket marketplace metadata only after real skill content exists.
- [ ] Add Hermes, Claude Code, and Cowork compatibility surfaces.
- [ ] Run root metadata validation.

## Exit Criteria

- Socket has one installable plugin with a clear model-research contract rather
  than overlapping training, evaluation, MLX, Core ML, and Core AI plugins.
- The first skills preserve reproducible source-model, dataset, recipe,
  checkpoint, evaluation, runtime, and artifact provenance.
- Cloud resource operations, agent eval design, host portability, application
  integration, and real-system security testing retain their current owners.
- Apple runtime selection distinguishes Core AI, Core ML, direct MLX,
  ExecuTorch Core ML, experimental ExecuTorch MLX, and Foundation Models.
- Apple-owned Core AI skills are reused rather than copied.
- Refusal ablation and jailbreak workflows measure ordinary behavior and
  regressions in addition to bypass or refusal outcomes.
- Root docs, marketplace state, compatibility exports, and validation agree on
  the shipped skill inventory.
