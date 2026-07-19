---
name: benchmark-model-runtime
description: Benchmark language-model and multimodal runtime artifacts across latency, throughput, memory, energy, load time, artifact size, and stability. Use when comparing Core AI, Core ML, MLX, ExecuTorch, PyTorch, quantization levels, devices, packaging formats, or runtime configurations.
---

# Benchmark Model Runtime

## Define A Fair Workload

Pin the exact model artifact, tokenizer/template, runtime and version, device and OS, precision, cache policy, batch size, prompt-length buckets, generated-token target, sampling settings, and measurement tool. Compare numerical or behavioral parity before performance.

## Workflow

1. Verify each artifact produces acceptable outputs on the same small parity set.
2. Separate cold load, warm load, prompt processing, time to first token, decode throughput, and end-to-end latency.
3. Measure peak and steady memory; include model, cache, runtime, and process overhead consistently.
4. Stabilize device power, charging, background load, and thermal state. Record deviations instead of silently rerunning only slow samples.
5. Warm up separately, then run enough measured repetitions to report median and tail percentiles.
6. Sweep representative prompt lengths, output lengths, and batch/concurrency levels.
7. Record failures, fallback execution, recompilation, memory pressure, and thermal throttling.
8. Measure energy with an appropriate system tool when the decision depends on battery or sustained deployment.
9. Retain raw samples and summarize them with units, sample counts, and uncertainty.

## Apple Runtime Checks

- Confirm delegated operator coverage and fallback behavior rather than assuming the named backend ran the whole graph.
- Distinguish compilation/conversion time from load and inference time.
- For stateful generation, include key-value cache initialization, update, and memory growth.
- Treat ExecuTorch MLX results as revision-specific while the upstream backend remains experimental.

## References

Use `references/runtime-benchmarking.md` for metric definitions and reporting requirements.
