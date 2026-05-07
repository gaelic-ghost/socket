# Instruments Performance Profiling

Use this reference when Xcode-managed testing or diagnostics crosses into Instruments, `xctrace`, or trace artifact interpretation for performance-sensitive Apple-platform work.

## Apple Documentation Anchors

- [Xcode command-line tool reference](https://developer.apple.com/documentation/xcode/xcode-command-line-tool-reference) documents `xctrace` as the command-line tool for Instruments `.trace` files.
- [Installing the command-line tools](https://developer.apple.com/documentation/xcode/installing-the-command-line-tools) states that `xcodebuild` and `xctrace` require full Xcode rather than only the standalone Command Line Tools for Xcode package.
- [`OSSignposter`](https://developer.apple.com/documentation/os/ossignposter) records intervals and events that Instruments can display on a trace timeline.
- [Metal developer workflows](https://developer.apple.com/documentation/xcode/metal-developer-workflows) describes Metal System Trace as the Instruments timeline for CPU/GPU work and Metal memory usage.
- [Analyzing the performance of your Metal app](https://developer.apple.com/documentation/xcode/analyzing-the-performance-of-your-metal-app) describes the Game Performance template and its timeline instruments.
- [Gathering information about memory use](https://developer.apple.com/documentation/xcode/gathering-information-about-memory-use) describes the Allocations instrument and generation-based memory investigation.

## Apple Silicon Baseline

- Treat Apple silicon as the default architecture for current Xcode and Instruments performance guidance.
- Do not add Intel Mac-specific profiling branches unless the target repository explicitly declares Intel support.
- Record chip family, macOS version, Xcode version, destination, build configuration, thermal state when relevant, workload fixture, and package resolved versions before comparing traces.
- For Metal, MLX, Audio, and local AI work, interpret CPU samples, GPU timelines, unified-memory pressure, and model/resource residency together.

## Instrument Selection

- Time Profiler: use for CPU call stacks, Swift runtime overhead, expensive decoding, actor or queue overhead, thread contention symptoms, and CPU-bound model preparation.
- Metal System Trace: use for CPU/GPU overlap, command buffer timing, GPU scheduling, Metal resource events, GPU gaps, and Metal-backed ML or compute workloads.
- Allocations: use for heap growth, allocation churn, retained object growth, bridging overhead, and per-phase allocation deltas.
- VM Tracker or Virtual Memory Trace: use for mapped model weights, dirty memory growth, resident memory pressure, mapped files, and large memory regions that Allocations does not explain clearly.
- Points of Interest: use with `OSSignposter` intervals and events to align package-defined workload phases with the trace timeline.
- Processor Trace: use only when the active Apple silicon hardware and Xcode/Instruments version support it and the user needs lower-overhead CPU execution evidence beyond Time Profiler.

## Trace Capture Flow

1. State the performance question before recording.
2. Confirm the active Xcode and `xctrace` availability.
3. Choose the narrowest template that answers the question.
4. Prefer Release builds when optimization affects the behavior under investigation.
5. Use signposts or stable workload output to mark phases before recording long-running or multi-phase workloads.
6. Save `.trace` artifacts outside tracked source unless the repository explicitly owns trace evidence.
7. Report the trace path, template, target command or scheme, duration, build configuration, hardware, and the decision the trace supports.

## Command Guidance

- Verify tool availability:

```bash
xcode-select -p
xcrun --find xctrace
xcrun xctrace version
```

- List templates before assuming a template exists on the current Xcode version:

```bash
xcrun xctrace list templates
```

- Record an app, tool, or package executable:

```bash
xcrun xctrace record --template 'Time Profiler' --output traces/<name>.trace --launch -- <command> <args>
```

- Bound recordings that might otherwise run too long:

```bash
xcrun xctrace record --template 'Time Profiler' --time-limit 30s --output traces/<name>.trace --launch -- <command> <args>
```

- Attach to a running app or helper only when launch would hide the issue:

```bash
xcrun xctrace record --template 'Time Profiler' --time-limit 30s --output traces/<name>.trace --attach <pid-or-process-name>
```

- Capture Metal timeline evidence:

```bash
xcrun xctrace record --template 'Metal System Trace' --time-limit 30s --output traces/<name>.trace --launch -- <command> <args>
```

- Capture allocation evidence:

```bash
xcrun xctrace record --template 'Allocations' --output traces/<name>.trace --launch -- <command> <args>
```

- Redirect workload output into the trace evidence directory:

```bash
xcrun xctrace record --template 'Time Profiler' --target-stdout traces/<name>.stdout.txt --output traces/<name>.trace --launch -- <command> <args>
```

## Trace Interpretation Expectations

- Summarize what the trace shows, what it does not show, and whether the evidence is enough for the decision being made.
- For Time Profiler, report the hot stack or subsystem, whether samples are on the expected threads, and whether signposted intervals line up with the hot work.
- For Metal System Trace, report CPU/GPU overlap, command buffer gaps, GPU occupancy symptoms when visible, Metal memory/resource events, and whether the workload appears GPU-bound, CPU-bound, synchronization-bound, or memory-bound.
- For Allocations, report per-phase growth, allocation categories, churn versus retained growth, and whether generation marks or signposts isolate the feature under investigation.
- For VM Tracker or Virtual Memory Trace, report mapped regions, dirty memory growth, resident pressure, and whether model/resource residency matches expectations.
- Do not overstate trace results. If Instruments UI inspection is required and only a command-line capture was performed, say that the trace was captured but not fully interpreted.

## Xcode Testing Handoffs

- Use this workflow when traces are tied to schemes, destinations, `.xctestplan` configurations, runtime diagnostics, app-hosted package tests, or Instruments UI inspection.
- Hand off to `swift-package-testing-workflow` when the remaining work is package workload design, test harness shape, signpost placement, or SwiftPM-first Release validation.
- Hand off to `xcode-build-run-workflow` when scheme mutation, file membership, Metal build settings, shader compilation, app launch behavior, entitlements, or other project-integrity work becomes central.
