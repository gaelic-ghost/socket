---
name: select-analysis-isolation
description: Select and configure an isolation boundary before inspecting or executing untrusted content. Use when choosing among local read-only analysis, a disposable container, Linux VM, macOS VM, remote sandbox, or spare physical device and deciding network, mount, clipboard, credential, device, snapshot, evidence-export, and teardown controls.
---

# Select Analysis Isolation

## Overview

Choose the smallest environment that contains the behaviors the analysis may trigger and can still reproduce the target platform. Treat isolation as a set of controls to verify, not a label supplied by a product.

Read [references/isolation-matrix.md](references/isolation-matrix.md) before selecting an environment for execution or privileged tooling.

## Workflow

1. Identify the behavior to contain.
   - Record target OS/runtime, expected privilege, kernel or device access, persistence, networking, anti-VM behavior, and data sensitivity.

2. Choose the environment.
   - Use local read-only inspection for non-executing metadata and text extraction.
   - Use a disposable container for bounded Linux user-space tooling when VM-level isolation and target-platform behavior are unnecessary.
   - Use a disposable VM for installers, services, dynamic behavior, or full-OS effects.
   - Use a macOS VM or spare Mac for macOS payload behavior; do not substitute a Linux container.
   - Use a remote sandbox only after data-egress approval and provider-capability review.

3. Remove ambient authority.
   - Exclude personal accounts, host directories, shared clipboard, drag/drop, host sockets, USB/device passthrough, SSH agent, developer certificates, browser profiles, password stores, cloud tokens, and unrelated secrets.

4. Constrain networking.
   - Default to no network or a simulated service.
   - If external traffic is required, allow only recorded destinations through a monitored boundary and capture DNS/routes/packets proportionately.

5. Establish lifecycle evidence.
   - Record base image or restore image, OS build, tool versions, configuration, snapshot, clocks, and baseline state.
   - Define exactly which evidence may be exported and how it will be scanned before reaching the host.

6. Verify teardown.
   - Stop the workload, export intended evidence, revert or destroy disposable state, revoke temporary credentials, and confirm no host share or forwarded port remains.

## Stop Conditions

Stop before execution when the environment cannot reproduce the target platform, the isolation controls cannot be verified, or the task requires host secrets or privileges beyond the approved analysis plan.
