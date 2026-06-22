# Core AI and Foundation Models Skill Plan

This plan records the first Socket pass for Apple's Core AI, Foundation Models, and adjacent Apple Intelligence workflow coverage.

## Current Recommendation

Do not add a broad "Apple AI" catch-all skill yet.

Split the work into two candidate tracks:

- App-facing Apple Intelligence and Foundation Models workflows may belong in `apple-dev-skills` when the request is about Swift app integration, model/session choice, tool use, evaluations, Private Cloud Compute boundaries, App Intents, or Xcode validation.
- Model-runtime, conversion, optimization, and artifact-debugging workflows probably need a future dedicated Socket plugin, or a handoff to Apple-owned `coreai-models` skills, because Core AI model export and optimization are larger than ordinary Apple app workflow guidance.

## Source Evidence

Official and Apple-owned sources checked on 2026-06-22:

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

Observed source status:

- Apple Intelligence and Core AI landing pages are public Apple developer pages.
- Foundation Models API documentation exists as Apple Developer Documentation, but the page body is JavaScript-rendered in this environment.
- WWDC26 transcripts are readable and useful for beta-era Foundation Models details.
- `apple/coreai-models`, `apple/coreai-torch`, and `apple/coreai-optimization` are public Apple-owned GitHub repositories.
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

### Dedicated Core AI Plugin Candidate

A future dedicated Core AI or model-runtime plugin should own:

- Core AI `.aimodel` artifact integration beyond ordinary app wiring
- PyTorch model export through `coreai-torch`
- model compression and optimization through `coreai-opt`
- Core AI Debugger and model graph inspection
- model catalog, tokenizer, and resource-folder handling from `apple/coreai-models`
- model-authoring constraints, op coverage, custom Metal kernels, quantization, palettization, pruning, and performance investigation
- coordination with future `mlx-skills` and `coreml-skills`

### Handoff To Apple-Owned Skills

Apple's `coreai-models` repository already advertises coding-agent skills for Core AI workflows. Before Socket duplicates that work, inspect whether those skills satisfy the request or should be installed/used as the source of truth.

## Stable, Beta, And Exploratory Boundaries

- Stable: Public Apple landing pages and source repositories can anchor high-level planning.
- Beta: WWDC26 Foundation Models and Xcode 27 claims must carry the date checked and target SDK/Xcode version.
- Exploratory/open-source: Apple GitHub projects can anchor source-level planning, but package behavior should be verified from each repository's README, tags, docs, and tests before Socket ships workflow claims.

## Open Questions

- Should Apple Dev Skills ship an app-facing `foundation-models-app-workflow`, or should that wait until the Xcode 27 and Foundation Models beta APIs settle?
- Should Socket add a dedicated `coreai-skills` child plugin, or rely on Apple-owned `coreai-models` skills for model export, authoring, compression, and runtime details?
- How should future `mlx-skills` and `coreml-skills` divide model conversion, on-device inference, app integration, and performance validation?
- Are Music Intelligence and Media Analyzer public Apple developer surfaces, internal names, or future docs that are not yet available?

## Decision Checkpoints

- If a task requires model export, compression, custom kernels, Core AI Debugger, or model artifact validation, pause before pushing it into Apple Dev Skills.
- If a task is app-facing and mostly about Swift integration, Foundation Models sessions, App Intents, Xcode validation, or privacy boundaries, Apple Dev Skills is the likely owner.
- If official Apple docs cannot be found for a named surface, mark the claim unresolved instead of creating workflow guidance around it.
