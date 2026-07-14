---
name: perform-apple-dynamic-analysis
description: Plan and record bounded dynamic analysis of Apple binaries using supported LLDB, Xcode, Instruments, unified logging, Simulator, physical-device, macOS VM, or research-device surfaces. Use when Codex must verify a static hypothesis at runtime, launch or attach, inspect images, memory regions, registers, exceptions, or generated data, correlate runtime addresses, or explain how Developer Mode, signing, get-task-allow, SIP, security policy, Rosetta, hardware, and exact OS build constrain the observation.
---

# Perform Apple Dynamic Analysis

## Overview

Choose the least privileged runtime surface that can answer the question. Record the environment and security state so a result is not generalized beyond the tested host or device.

Read [references/apple-dynamic-analysis.md](references/apple-dynamic-analysis.md) for environment records, launch and attach distinctions, address correlation, and authoritative sources.

## Workflow

1. State the runtime hypothesis and stop condition.
   - Name the static observation being tested and the smallest runtime evidence that would confirm, contradict, or narrow it.

2. Choose the environment.
   - Distinguish macOS host, physical iPhone or iPad, Simulator, macOS VM, translated process, and approved research device.
   - Record device or Mac model, SoC, OS build, Xcode and SDK build, architecture, Developer Mode, and translation state.

3. Record artifact and security state.
   - Record hash, UUID, bundle build, signature and entitlements, provisioning, `get-task-allow`, sandbox or hardened-runtime context, SIP or security policy, and whether the artifact was transformed.

4. Choose launch, attach, trace, log, or profile.
   - Prefer ordinary supported Xcode or LLDB launch for development artifacts.
   - Treat attach, remote debugging, system tracing, and device collection as separate paths with explicit prerequisites.
   - Use logging or Instruments when they answer the question without debugger mutation.

5. Capture a bounded observation.
   - Record breakpoints or trace points, image list, load addresses, memory regions, registers, exception state, thread, timestamp, and relevant logs.
   - Avoid changing execution state beyond what the question requires.

6. Correlate addresses.
   - Match runtime image UUID and architecture to the preserved binary.
   - Record load address, slide, pointer normalization, and database translation.

7. Compare with static evidence.
   - State whether the runtime result confirms, contradicts, or leaves the static inference unresolved.
   - Preserve environment-specific limitations.

8. Hand ordinary Xcode debugging, test authoring, app fixes, or Instruments development profiling to `apple-dev-skills` after the artifact-analysis question is resolved.

## Guardrails

- Do not change SIP, system security policy, Developer Mode, signing, or device configuration without explicit user direction.
- Do not treat Simulator or VM results as proof of physical-device secure boot, PAC, Secure Enclave, or memory-integrity behavior.
- Do not attribute a re-signed or patched copy's behavior to the original artifact.
- Do not collect broad logs or sysdiagnose data when a narrower trace answers the question.

## Output

Return hypothesis, environment manifest, artifact and security state, method, bounded runtime observations, address correlation, comparison with static evidence, and remaining uncertainty.
