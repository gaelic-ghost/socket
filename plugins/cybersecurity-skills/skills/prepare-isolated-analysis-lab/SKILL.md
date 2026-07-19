---
name: prepare-isolated-analysis-lab
description: Prepare a verified disposable Linux or macOS analysis lab from an approved isolation decision. Use before active research to control host integration, networking, baseline, monitoring, evidence export, reset, and teardown.
---

# Prepare Isolated Analysis Lab

## Overview

Turn the boundary selected by `select-analysis-isolation` into a concrete, reviewable control profile before executing untrusted content. Evidence collection and analysis remain owned by their specialist skills.

Read [security-lab-control-profile.md](references/security-lab-control-profile.md) before approving a lab.

## Workflow

1. Consume the approved isolation decision.
   - Record authorization, unresolved question, target OS/architecture/privilege, expected behavior, selected boundary, host/guest builds, and VM artifacts that may affect conclusions.
2. Select one profile.
   - offline static tooling
   - monitored Linux dynamic analysis
   - monitored macOS dynamic analysis
   - network-service research
   - nested-virtualization experiment
3. Verify a trusted base.
   - Record image/restore provenance and digest, guest build, tool versions, clock strategy, resource limits, baseline state or hashes, reset mechanism, and virtualization artifacts that may change observed behavior.
4. Remove ambient authority.
   - Default host folders/home sharing, clipboard, drag/drop, sockets, SSH agent, browser profiles, cloud credentials, Apple accounts, signing identities, USB, microphone, camera, and unrelated devices to absent.
5. Constrain and observe networking.
   - Default to offline or simulated services.
   - When external connectivity is authorized, record destinations, routes, DNS, monitoring/capture, ingress, egress, and forwarded ports.
6. Define a narrow evidence path.
   - Name the guest staging location, allowed artifact types, host export directory, hashing and scanning steps, size limits, and owner.
7. Run a preflight without executing the target.
   - Verify accounts, shares, clipboard, devices, sockets, credentials, network, monitoring, clock, baseline, stop controls, export path, and reset operation.
8. Hand the prepared-lab record to `perform-dynamic-malware-analysis` or the relevant observation skill.
9. Verify teardown.
   - Stop the workload; export only intended evidence; hash/scan it; revert or remove disposable state; revoke temporary credentials; remove shares/ports/helpers; confirm no workload or integration remains active.

## Output

Return the approved isolation decision, selected profile, trusted-base identity, full control profile, preflight evidence, observation handoff, export manifest, teardown evidence, and remaining fidelity limits.

## Stop Conditions

- Stop when authorization for active testing, target-platform fidelity, trusted-base provenance, isolation controls, observation coverage, safe evidence export, or reset/teardown cannot be verified.
- Stop when the task requires host secrets, personal accounts, developer identities, or uncontrolled devices.
- Stop when anti-VM, hardware, Secure Enclave, recoveryOS, kernel/system-extension, or device behavior makes VM evidence insufficient; state the physical-device gap.
- Never weaken host SIP, Gatekeeper, XProtect, TCC, App Sandbox, or other protections to make the lab convenient.
- Never start a guest, service, network capture, or payload without announcing the exact visible or resource-intensive action first.

## Handoffs

- Use `perform-dynamic-malware-analysis` for controlled execution and observation.
- Use Reverse Engineering skills for exported binaries, disassembly, decompilation, and symbols.
- Use `reverse-engineering-skills:research-macos-security-control` for exact-build TCC, sandbox, entitlement, Gatekeeper, XProtect, SIP, or system-policy research that needs public/private evidence separation.
- Use `apple-dev-skills:virtualization-framework-workflow` for custom VM implementation defects.
- Use `apple-dev-skills:macos-development-vm-workflow` or `linux-development-vm-workflow` for benign guest provisioning and lifecycle mechanics.
- Return to `select-analysis-isolation` when the chosen boundary fails fidelity or containment preflight.
