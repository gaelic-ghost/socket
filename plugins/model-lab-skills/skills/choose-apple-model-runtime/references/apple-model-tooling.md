# Apple Model Tooling Source Map

## Dated Maturity And Availability Snapshot

Official sources checked 2026-07-28. These are routing gates, not permanent guarantees; record the exact source revision or release and re-check before implementation.

| Surface | Maturity at check | Availability gate to verify |
| --- | --- | --- |
| [Core AI models](https://github.com/apple/coreai-models), [coreai-torch](https://github.com/apple/coreai-torch), and [coreai-optimization](https://github.com/apple/coreai-optimization) | New, actively developing Apple open-source stack | `coreai-models` runtime integration currently states macOS/iOS 27+ and Xcode 27+; verify device, operator, compiler, and package requirements |
| [Core ML Tools](https://github.com/apple/coremltools) and Core ML | Established Apple conversion and deployment route | Verify the selected `coremltools` release, deployment target, operator coverage, compute units, state/cache support, and Swift API availability |
| [MLX](https://github.com/ml-explore/mlx), [MLX Swift](https://github.com/ml-explore/mlx-swift), and [MLX LM](https://github.com/ml-explore/mlx-lm) | Active Apple-silicon research/runtime ecosystem | Verify Apple-silicon/Metal platform support, language/package version, model architecture, quantization, and target-device memory |
| [LM Studio](https://lmstudio.ai/docs/developer/rest) local server | Local inference server and model-management control plane | Use `http://localhost:1234/v1` only for OpenAI-compatible client APIs; use native `/api/v1` for model lifecycle, stateful chats, authentication, and MCP control. Keep loopback-only unless an explicit authenticated exposure decision exists. |
| [ExecuTorch Core ML backend](https://github.com/pytorch/executorch/tree/main/backends/apple/coreml) | Documented ExecuTorch Apple backend | Verify the pinned ExecuTorch release, Apple deployment target, partition coverage, fallback, state, and packaging requirements |
| [ExecuTorch MLX delegate](https://github.com/pytorch/executorch/tree/main/backends/mlx) | Experimental and under active development | Current upstream targets Apple Silicon M1+ and requires a full Xcode Metal compiler; verify exact revision, build/platform support, partition/operator coverage, portable-runtime fallback, parity, and performance |
| Apple Foundation Models framework and [Python Apple FM SDK](https://github.com/apple/python-apple-fm-sdk) | Apple system-model SDK plus Apple-owned Python bridge | Current Python SDK states macOS 26+, Xcode 26+, Python 3.10+, a compatible Apple-silicon Mac, and Apple Intelligence availability; re-check all requirements |
| [Foundation Models utilities](https://github.com/apple/foundation-models-utilities) | Emerging/experimental utilities around the system model | Pin the revision and verify each utility against the current Foundation Models SDK; do not treat it as a stable arbitrary-weight runtime |

Core AI and Core ML are distinct artifact and API lanes. MLX is a general array framework; MLX Swift and MLX LM are separate integration layers. Foundation Models exposes Apple's system model, not arbitrary user-supplied weights.

## LM Studio Local Server Gate

LM Studio is appropriate when a macOS developer needs to host a downloaded
model for a local client, agent framework, or developer tool. It is not a path
for compiling an `.aimodel`, shipping an iOS model, using Apple's system model,
or proving ANE use.

- Use the OpenAI-compatible `/v1/responses`, `/v1/chat/completions`,
  `/v1/embeddings`, and `/v1/models` endpoints when an existing client needs a
  compatible base URL; the documented default is `http://localhost:1234/v1`.
- Use native `/api/v1` endpoints when the workflow needs model download/load/
  unload, stateful chats, API-token authentication, MCP control, or server
  lifecycle observation.
- Keep the server loopback-only by default. LAN or public exposure requires an
  explicit authentication, network, secret, and recovery decision.
- Before attaching tools or external writes, prove the exact model/server pair
  returns schema-conforming structured output, makes valid and unnecessary
  no-call decisions, recovers from malformed output, stops within its bound,
  and handles tool calls only where the model genuinely supports them.

## Implementation Handoffs

- Use Apple's `coreai-models` skills `working-with-coreai` and `model-authoring` for Core AI implementation details.
- Use Apple's `model-compression-exploration` skill plus `coreai-optimization` for Core AI compression experiments.
- Use `apple-dev-skills` for Swift, Xcode, application lifecycle, packaging, and UI integration after runtime selection.
- Keep cross-runtime experiment design, parity evaluation, checkpoint evidence, and benchmarking in Model Lab Skills.

## Apple Research And Evaluation Repositories

Reusable-tool candidates include [Embedding Atlas](https://github.com/apple/embedding-atlas), [DNIKit](https://github.com/apple/dnikit), and [CoreNet](https://github.com/apple/corenet). Research and benchmark candidates include [ml-agent-evaluator](https://github.com/apple/ml-agent-evaluator), [ml-persona-red-teaming](https://github.com/apple/ml-persona-red-teaming), [ml-mmtoolsandbox](https://github.com/apple/ml-mmtoolsandbox), [ml-compress-and-compare](https://github.com/apple/ml-compress-and-compare), and [ml-mia-bench](https://github.com/apple/ml-mia-bench).

Before recommending one, return:

1. repository and exact revision/date checked;
2. classification: maintained framework, benchmark/dataset, paper reproduction, model/checkpoint, sample, or exploratory prototype;
3. supported input/model/runtime contract;
4. maintenance and release evidence;
5. license and artifact-publication boundary;
6. the experiment or implementation role it replaces;
7. a smaller project-native alternative considered first.

For Apple SDK lifecycle behavior, prefer Xcode Documentation Search or Xcode-local documentation. GitHub README claims do not replace current SDK availability checks.
