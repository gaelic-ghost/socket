---
name: inspect-macos-runtime-activity
description: Correlate suspicious macOS process, file, network, permission, and log activity. Use for unexpected processes, child execution, downloads, open files, DNS/connections, privacy prompts, XProtect or Gatekeeper events, file mutations, injected or deleted executables, and Endpoint Security or eslogger evidence when exact permissions and telemetry gaps must remain visible.
---

# Inspect macOS Runtime Activity

## Overview

Build a time-correlated view of what ran, what changed, and what communicated. Prefer focused native observations and existing telemetry over installing a broad privileged monitor on an affected host.

Read [references/macos-runtime-evidence.md](references/macos-runtime-evidence.md) for telemetry sources and permission boundaries.

## Workflow

1. Fix host/build, user/session, time window, process/artifact identity, and reported symptom.
   - Label every observation as physical-host, affected-host, or macOS-guest evidence. For a guest, record VM tool/framework, virtual hardware, restore-image/build, shares/devices/network, baseline/reset state, and virtualization artifacts that may alter behavior.
2. Capture current process context.
   - Record PID, executable path/hash/signature, user, parent/ancestry, arguments, environment when authorized, start time, code state, and deleted/replaced executable clues.
3. Correlate files and registrations.
   - Record open files, working directory, mapped images, created/modified paths, quarantine/provenance, persistence registrations, and permission failures.
4. Correlate network behavior.
   - Record process-to-socket mapping, local/remote endpoints, DNS, protocol clues, timing, and whether a connection completed.
5. Inspect focused logs/events.
   - Query relevant unified logs and existing Endpoint Security/XProtect/Gatekeeper evidence for the narrow time window.
   - Record Full Disk Access, root, Endpoint Security entitlement, or other permissions required and what absence hides.
6. Build a timeline.
   - Separate user action, launch, child processes, file changes, prompts, network, persistence, detection, and termination.
7. Assess behavior and gaps.
   - Route binary internals, dynamic reproduction, containment, or hunting as needed.
   - State anti-VM, hardware, Secure Enclave, recoveryOS, kernel/system-extension, and device-access limitations before treating guest evidence as physical-Mac proof.

## Output

Return process identity/ancestry, file/network/log timeline, permissions and coverage, observed versus inferred behavior, confidence, and next action.
