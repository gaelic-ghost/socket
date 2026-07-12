---
name: ios-runtime-forensics-workflow
description: Capture and interpret reproducible iOS Simulator performance and memory evidence. Use when an iOS issue needs ETTrace/symbolication, a memgraph, leak ownership traces, or before/after runtime proof rather than a code-only guess.
---

# iOS Runtime Forensics Workflow

## Purpose

Provide two explicit evidence modes for a reproducible iOS Simulator issue: `performance-trace` for focused ETTrace/symbolicated latency or CPU work, and `memory-graph` for retained-object and leak ownership analysis. This skill owns evidence shape, not normal app build, launch, or UI driving.

## When To Use

- Use `performance-trace` for launch/runtime latency, CPU-heavy stacks, or comparison traces.
- Use `memory-graph` for leaks, retain cycles, memory growth, or objects that should release after a known interaction.
- Route simulator discovery, build, install, launch, logs, screenshots, and UI driving to `xcode-build-run-workflow`.

## Single-Path Workflow

1. Apply the Apple docs gate through `explore-apple-swift-docs`. Confirm the current Xcode/Simulator evidence mechanism before acting.
2. Define one reproduction, start/stop boundary, target app build, simulator UDID, OS, Xcode version, and expected release or latency behavior.
3. Select exactly one mode: `performance-trace` or `memory-graph`. Do not mix CPU and ownership conclusions in one unsupported capture.
4. For `performance-trace`, read `references/performance-trace-evidence.md`, capture a focused trace with matching symbols, and identify hot stacks only after symbolication.
5. For `memory-graph`, read `references/memory-graph-evidence.md`, drive the release-producing flow, capture a memgraph, inspect app-owned retained types, and follow ownership evidence to the retaining path.
6. Make the smallest root-cause change, then recapture the same flow on the same simulator where practical.
7. Report the exact capture boundary, tool/version context, what the artifact proves, what it does not prove, and the before/after delta.

## Inputs

- reproducible simulator flow, target app/scheme, simulator UDID, and build configuration
- expected release/lifetime or performance boundary
- mode: `performance-trace` or `memory-graph`
- existing trace, memgraph, logs, screenshots, or symbol files when available

## Outputs

- capture plan or artifact evidence with its scope and limitations
- app-owned hot stack or retaining ownership path when evidence supports it
- smallest remediation and same-flow recapture result

## Guards and Stop Conditions

- Do not call a memory graph a leak proof until the expected lifetime and retaining path are established.
- Do not compare traces with different app builds, simulator/OS state, or workload boundaries as a regression result.
- Do not claim a symbolicated root cause from an unsymbolicated stack.
- Stop when the issue cannot be reproduced or a capture would include user-sensitive content without explicit approval.

## Fallbacks and Handoffs

- Recommend `xcode-build-run-workflow` for all normal simulator execution and log/UI evidence.
- Recommend `xcode-testing-workflow` for Instruments, `xctrace`, test plans, and broader Xcode performance work.
- Recommend `swiftui-performance-audit` when the user first needs a code-first SwiftUI hypothesis.

## Customization

Use `references/customization-flow.md`. Evidence mode and reproducibility requirements are fixed; local customization cannot bypass same-flow comparison or artifact-scope reporting.

## References

- `references/performance-trace-evidence.md`
- `references/memory-graph-evidence.md`
- `references/customization-flow.md`
- Recommend `references/snippets/apple-xcode-project-core.md` when the app needs reusable Xcode-project policy alongside simulator evidence work.
