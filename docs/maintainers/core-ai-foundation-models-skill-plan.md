# Core AI and Foundation Models Skill Plan

This plan records Socket's ownership decision for Apple's Core AI, Foundation
Models, and adjacent Apple Intelligence workflow coverage. It is coordinated
with the broader [`model-lab-skills` plugin
plan](./model-lab-skills-plugin-plan.md).

## Current Recommendation

Do not add a broad "Apple AI" catch-all skill or separate `coreai-skills`,
`mlx-skills`, and `coreml-skills` plugins in the first implementation pass.

Use three explicit tracks:

- App-facing Apple Intelligence and Foundation Models workflows may belong in `apple-dev-skills` when the request is about Swift app integration, model/session choice, tool use, evaluations, Private Cloud Compute boundaries, App Intents, or Xcode validation.
- Cross-runtime model research, reproducible comparisons, and the choice among
  Core AI, Core ML, direct MLX, ExecuTorch Core ML, and ExecuTorch MLX belong in
  the planned `model-lab-skills` plugin.
- Core AI export, authoring, compression, and runtime implementation details
  should hand off to Apple-owned `coreai-models` skills rather than being
  copied into Socket.

## Source Evidence

Official and Apple-owned sources checked initially on 2026-06-22 and refreshed
on 2026-07-19:

- [Apple Intelligence](https://developer.apple.com/apple-intelligence/)
- [What's new in Apple Intelligence](https://developer.apple.com/apple-intelligence/whats-new/)
- [Foundation Models framework](https://developer.apple.com/documentation/FoundationModels)
- [What's new in the Foundation Models framework](https://developer.apple.com/videos/play/wwdc2026/241/)
- [Build agentic app experiences with the Foundation Models framework](https://developer.apple.com/videos/play/wwdc2026/242/)
- [Build with the new Apple Foundation Model on Private Cloud Compute](https://developer.apple.com/videos/play/wwdc2026/319/)
- [Bring an LLM provider to the Foundation Models framework](https://developer.apple.com/videos/play/wwdc2026/339/)
- [Core AI](https://developer.apple.com/core-ai/)
- [apple/coreai-models](https://github.com/apple/coreai-models)
- [apple/coreai-torch](https://github.com/apple/coreai-torch)
- [apple/coreai-optimization](https://github.com/apple/coreai-optimization)
- [apple/coremltools](https://github.com/apple/coremltools)
- [apple/foundation-models-utilities](https://github.com/apple/foundation-models-utilities)
- [apple/python-apple-fm-sdk](https://github.com/apple/python-apple-fm-sdk)
- [MLX](https://github.com/ml-explore/mlx)
- [MLX Swift](https://github.com/ml-explore/mlx-swift)
- [MLX LM](https://github.com/ml-explore/mlx-lm)
- [ExecuTorch MLX delegate](https://github.com/pytorch/executorch/tree/main/backends/mlx)
- [ExecuTorch Core ML backend](https://docs.pytorch.org/executorch/stable/ios-coreml.html)

Observed source status:

- Apple Intelligence and Core AI landing pages are public Apple developer pages.
- Foundation Models API documentation exists as Apple Developer Documentation, but the page body is JavaScript-rendered in this environment.
- WWDC26 transcripts are readable and useful for beta-era Foundation Models details.
- `apple/coreai-models`, `apple/coreai-torch`, `apple/coreai-optimization`,
  `apple/coremltools`, `apple/foundation-models-utilities`, and
  `apple/python-apple-fm-sdk` are public Apple-owned GitHub repositories.
- `apple/coreai-models` now ships `working-with-coreai`, `model-authoring`, and
  `model-compression-exploration` agent skills. Its current README describes
  `.aimodel` export recipes, Python primitives, Swift runtime utilities, and
  macOS/iOS 27 plus Xcode 27 runtime requirements.
- `coreai-torch` lowers `torch.export.ExportedProgram` graphs into Core AI IR
  and exposes composite operations, custom lowerings, submodule
  externalization, and inline Metal kernels.
- `coreai-optimization` provides Core AI-targeted quantization, palettization,
  and pruning experiments through `coreai-opt`.
- The ExecuTorch MLX delegate is maintained under `pytorch/executorch`, not the
  Apple GitHub organization. Its current upstream README marks it experimental
  and under active development.
- GitHub repository searches for official Apple `Music Intelligence` and `Media Analyzer` developer/source surfaces did not find a verified Apple-owned match in this pass. Keep those as open investigation items.

## First Ownership Split

### Apple Dev Skills Candidate

Apple Dev Skills can own app-facing guidance for:

- choosing `SystemLanguageModel`, `PrivateCloudComputeLanguageModel`, third-party `LanguageModel` provider packages, or no model
- distinguishing stable Apple Intelligence app integration from beta Foundation Models APIs
- Private Cloud Compute privacy, entitlement, cost, and availability boundaries
- dynamic profiles, instructions, tools, multimodal prompts, Vision tools, Spotlight-backed retrieval, and evaluations at the app-integration level
- Xcode build, run, test, Instruments, and preview handoffs for AI features
- App Intents, Visual Intelligence, Image Playground, and Siri integration when the work is Apple app integration rather than model authoring

### Model Lab Skills

The planned `model-lab-skills` plugin should own:

- choosing among Core AI, Core ML, direct MLX, ExecuTorch Core ML, experimental
  ExecuTorch MLX, Foundation Models, and hosted or local chat-completions models
- reproducible conversion, optimization, quantization, runtime, memory,
  quality, and output-parity comparisons
- model-level experiment and artifact provenance
- handoffs to Apple-owned implementation skills and Apple Dev Skills

### Handoff To Apple-Owned Skills

Apple's `coreai-models` repository ships coding-agent skills for Core AI
workflows. Use those skills as the implementation source of truth for Core AI
export, authoring, and compression. Socket should own the cross-runtime choice
and evidence contract, not a copied version of Apple's rapidly changing
implementation guidance.

## Stable, Beta, And Exploratory Boundaries

- Stable: Public Apple landing pages and source repositories can anchor high-level planning.
- Beta: WWDC26 Foundation Models and Xcode 27 claims must carry the date checked and target SDK/Xcode version.
- Exploratory/open-source: Apple GitHub projects can anchor source-level planning, but package behavior should be verified from each repository's README, tags, docs, and tests before Socket ships workflow claims.

## Resolved Questions

- Apple Dev Skills remains the app-facing Foundation Models and Swift/Xcode
  integration owner.
- Model Lab Skills will own cross-runtime model experiments and Apple runtime
  selection.
- Apple-owned `coreai-models` skills will own fast-moving Core AI export,
  authoring, and compression implementation details.
- Separate `mlx-skills`, `coreml-skills`, and `coreai-skills` plugins are
  deferred unless real tasks prove the combined ownership model insufficient.

## Open Investigations

- Are Music Intelligence and Media Analyzer public Apple developer surfaces,
  internal names, or future docs that are not yet available?
- Which Foundation Models and Core AI APIs remain beta-only at each future
  Xcode and SDK refresh?
- When does the experimental ExecuTorch MLX delegate become stable enough for
  a default recommendation rather than an evidence-gated comparison option?

## Decision Checkpoints

- If a task requires model export, compression, custom kernels, Core AI
  Debugger, or model artifact validation, route through Model Lab Skills and
  Apple-owned Core AI skills rather than pushing it into Apple Dev Skills.
- If a task is app-facing and mostly about Swift integration, Foundation Models sessions, App Intents, Xcode validation, or privacy boundaries, Apple Dev Skills is the likely owner.
- If official Apple docs cannot be found for a named surface, mark the claim unresolved instead of creating workflow guidance around it.
