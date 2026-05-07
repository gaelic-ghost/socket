# Performance-Sensitive Testing and Profiling

Use this reference when a Swift package contains performance-sensitive Apple-platform work, especially Audio, Metal, MLX, local AI models, streaming generation, real-time rendering, or large memory-mapped resources.

## Apple Documentation Anchors

- [`OSSignposter`](https://developer.apple.com/documentation/os/ossignposter) records signposted intervals and events through the unified logging system so Instruments can show package-defined phases on a trace timeline.
- [Xcode command-line tool reference](https://developer.apple.com/documentation/xcode/xcode-command-line-tool-reference) documents `xctrace` as the command-line tool for recording, importing, exporting, and symbolicating Instruments `.trace` files.
- [Installing the command-line tools](https://developer.apple.com/documentation/xcode/installing-the-command-line-tools) states that `xcodebuild` and `xctrace` ship with full Xcode, not the standalone Command Line Tools for Xcode package.
- [Metal developer workflows](https://developer.apple.com/documentation/xcode/metal-developer-workflows) describes Metal System Trace as the Instruments tool for CPU/GPU timeline and Metal memory analysis.
- [Analyzing the performance of your Metal app](https://developer.apple.com/documentation/xcode/analyzing-the-performance-of-your-metal-app) describes the Instruments Game Performance template and its included instruments, including Points of Interest, Time Profiler, Virtual Memory Trace, Metal Resource Events, Metal Application, and GPU.
- [Gathering information about memory use](https://developer.apple.com/documentation/xcode/gathering-information-about-memory-use) describes the Allocations instrument for heap and anonymous virtual memory allocations.

## Apple Silicon Baseline

- Treat Apple silicon Macs as the default profiling target for current and forward-looking Swift package performance guidance.
- Do not add Intel-specific tuning, benchmark interpretation, architecture switches, or fallback expectations unless the target repository explicitly declares Intel Mac support.
- Record the Apple silicon device class, chip family when known, macOS version, Xcode version, Swift version, package resolved versions, model identifier, model dtype or quantization, and workload fixture before comparing trace results.
- For Metal, MLX, and Audio workloads, treat unified memory, GPU scheduling, thermal state, and model/resource residency as first-class evidence instead of CPU time alone.
- Prefer measuring on a quiet machine. Do not run heavy package tests, model loads, build jobs, or trace captures concurrently with other expensive validation.

## Decision Model

- Use ordinary `swift test` for correctness, small unit coverage, fixture validation, and regression checks that do not depend on runtime performance.
- Use package-level performance tests or executable harnesses when the package needs repeatable timing, allocation, or resource-pressure evidence.
- Use `xctrace` or Instruments when the question is where CPU time is spent, how CPU and GPU work overlap, where heap or virtual memory grows, or how package-defined phases align with system behavior.
- Use Xcode-managed test plans when sanitizers, runtime API checking, destinations, or named test configurations are part of the repeatable performance contract.
- Use an app host when the package behavior depends on app lifecycle, audio session behavior, UI event loops, display timing, sandboxing, entitlements, or simulator/device state.

## Package Workload Shape

- Build before profiling so the trace captures the workload, not package resolution or compilation.
- Profile Release builds when optimization, inlining, specialization, ARC behavior, or Metal/MLX performance is the question.
- Keep Debug traces only when diagnosing debug-only assertions, sanitizer failures, or development-time runtime warnings.
- Prefer a dedicated executable target or test harness that performs one workload at a time with deterministic fixtures.
- Separate cold model load, warmup, steady-state execution, streaming or chunk generation, audio rendering, and teardown into distinct phases.
- For MLX and large local model work, run one heavy workload at a time unless the test is explicitly about concurrent model pressure.
- For Audio work, capture sample rate, buffer size, channel count, device or route assumptions, and whether playback is live, synthetic, or file-backed.
- For benchmark-style tests, keep fixture inputs stable and report whether results are wall-clock timings, CPU samples, GPU timeline evidence, allocation counts, resident memory, or virtual memory activity.

## Signpost Contract

- Use `OSSignposter` for durable package-defined trace intervals when profiling will be repeated or compared across runs.
- Keep signpost names stable, short, and phase-oriented so traces from different branches can be compared.
- Prefer one subsystem per package or executable harness and categories that describe the workload family, such as `audio`, `mlx`, `inference`, `streaming`, or `benchmark`.
- Avoid signposting every low-level helper call. Mark phases that a maintainer can interpret in Time Profiler, Points of Interest, Metal System Trace, Allocations, or VM views.
- Recommended interval names for Audio and MLX packages:
  - `model.load`
  - `model.warmup`
  - `audio.decode`
  - `audio.render`
  - `inference.prefill`
  - `inference.generate`
  - `stream.chunk`
  - `resource.teardown`
- Recommended event names:
  - `fixture.ready`
  - `first.audio.buffer`
  - `first.token`
  - `first.chunk`
  - `playback.started`
  - `playback.completed`

## Instrument Selection

- Use Time Profiler when the question is CPU call stacks, Swift runtime overhead, actor or task scheduling overhead, lock contention symptoms, expensive decoding, or non-GPU model-preparation work.
- Use Metal System Trace when the question is CPU/GPU overlap, command buffer timing, GPU scheduling, Metal resource events, GPU workload gaps, or whether compute work is actually reaching the GPU as expected.
- Use Allocations when the question is heap growth, allocation churn, retained object graphs, unexpected bridging, autorelease-like spikes, or per-phase allocation deltas.
- Use VM Tracker or Virtual Memory Trace when the question is mapped model weights, dirty memory growth, resident memory pressure, memory-mapped files, or large region behavior that heap allocation summaries do not explain.
- Use Points of Interest or signpost views to align package-defined phases with the system timeline.
- Use Processor Trace only when supported by the active Xcode/Instruments version and the user specifically needs lower-overhead Apple-silicon CPU execution evidence beyond Time Profiler.

## Command Guidance

- Verify full Xcode is active before relying on `xctrace`:

```bash
xcode-select -p
xcrun --find xctrace
xcrun xctrace version
```

- Inspect available trace templates on the current machine:

```bash
xcrun xctrace list templates
```

- Build the package workload before recording:

```bash
swift build -c release --product <ExecutableProduct>
```

- Record a built executable with Time Profiler:

```bash
xcrun xctrace record --template 'Time Profiler' --output traces/<name>.trace --launch -- .build/release/<ExecutableProduct> <args>
```

- Record a bounded run when the workload would otherwise continue indefinitely:

```bash
xcrun xctrace record --template 'Time Profiler' --time-limit 30s --output traces/<name>.trace --launch -- .build/release/<ExecutableProduct> <args>
```

- Record Metal work when the package executable or host app exercises GPU-backed work:

```bash
xcrun xctrace record --template 'Metal System Trace' --time-limit 30s --output traces/<name>.trace --launch -- .build/release/<ExecutableProduct> <args>
```

- Record allocation behavior:

```bash
xcrun xctrace record --template 'Allocations' --output traces/<name>.trace --launch -- .build/release/<ExecutableProduct> <args>
```

- Redirect target output when the harness prints structured workload metadata:

```bash
xcrun xctrace record --template 'Time Profiler' --target-stdout traces/<name>.stdout.txt --output traces/<name>.trace --launch -- .build/release/<ExecutableProduct> <args>
```

## Artifact Expectations

- Preserve `.trace` artifacts when they justify a performance fix, tuning decision, or regression report.
- Keep trace artifacts out of git unless the repository explicitly tracks performance evidence fixtures or release artifacts.
- Report the workload command, build configuration, hardware, OS, Xcode, Swift version, model/resource versions, trace path, and the specific question the trace answered.
- Do not pretend text export replaces opening Instruments for timeline-heavy Metal, GPU, or memory-pressure investigation.
- If a trace cannot be captured because `xctrace` is unavailable, Xcode is not active, privacy prompts block recording, or the template is missing, report that exact blocker.

## Handoff Rules

- Stay in `swift-package-testing-workflow` when the work is package workload design, Swift Testing/XCTest organization, signpost placement, Release package builds, or executable-harness profiling.
- Hand off to `xcode-testing-workflow` when the next step depends on Instruments UI, `.xctestplan` configurations, Xcode destinations, app-hosted test execution, or interpretation of `.trace` timelines.
- Hand off to `xcode-build-run-workflow` when the work becomes Metal toolchain setup, shader compilation, app launch profiling, entitlements, project membership, scheme configuration, or Xcode-managed build settings.
