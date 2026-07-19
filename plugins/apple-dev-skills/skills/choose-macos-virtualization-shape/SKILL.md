---
name: choose-macos-virtualization-shape
description: Choose the smallest macOS-hosted boundary for development, compatibility, or authorized security research. Use when deciding among the host, containers, container machine, full Linux or macOS VMs, remote systems, or physical Macs.
---

# Choose macOS Virtualization Shape

## Purpose

Choose one boundary from evidence about fidelity, persistence, portability, host integration, threat level, and resources. Produce the shared shape record in [virtualization-shape-record.md](references/virtualization-shape-record.md); do not return an undecided product menu.

## When To Use

- Use for macOS-hosted development, clean-state validation, Linux compatibility, custom VM tools, and security-lab boundary selection.
- Use when container, persistent Linux machine, full VM, and physical Mac terminology is being mixed.
- Use before `virtualization-framework-workflow`, either development-VM workflow, or `prepare-isolated-analysis-lab` when the boundary is not already approved.

## Single-Path Workflow

1. Record the purpose, host, target OS and architecture, GUI/headless needs, privileges, kernel/devices, expected lifetime, and evidence requirements.
2. Classify fidelity and risk:
   - trusted native macOS behavior: host process
   - one portable Linux application: OCI container
   - Apple-native per-container VM runtime: Apple `container`
   - persistent OCI-backed Linux environment with services: `container machine`
   - custom kernel, boot, disk, full-system, or GUI Linux: full Linux VM
   - native macOS security, installer, signing, privacy, or OS-version behavior: macOS VM
   - hardware, recoveryOS, Secure Enclave, unsupported device, performance, or anti-VM behavior: physical Mac
3. Reject any option that cannot reproduce the target or safely bound the expected behavior.
4. Choose one primary boundary and one explicit fallback only when a named fidelity or availability gap requires it.
5. Complete the shape record with provenance, resources, integrations, lifecycle, validation, evidence, and uncertainty.
6. Hand off implementation or operation to the owner skill.

## Inputs

- Task purpose and target behavior.
- Host chip, macOS build, memory, storage, and toolchain.
- Guest OS/version/distro, architecture, devices, privilege, and lifetime.
- Portability, persistence, integration, isolation, and evidence requirements.

## Outputs

- `status`: `success`, `handoff`, or `blocked`.
- One selected `boundary` and the reason it is the smallest adequate choice.
- A completed virtualization shape record.
- One owner handoff and any unresolved fidelity gap.

## Guards and Stop Conditions

- Do not call a Linux container or Linux VM evidence for native macOS behavior such as Gatekeeper, TCC, XProtect, LaunchServices, or macOS persistence.
- Do not treat automatic home sharing, clipboard, credentials, or sockets as harmless defaults.
- Do not claim two products have equivalent isolation because they use the same framework.
- Do not promise saved VM state is a disk snapshot or portable clone.
- Stop when target fidelity, host capacity, authorization, or safe evidence handling cannot be established.
- Tell Gale before launching a GUI VM, starting a VM or container service, downloading a restore image, creating a large disk, or running a resource-intensive workload.

## Fallbacks and Handoffs

- Use `server-side-swift:docker-workflow` for portable OCI authoring and deployment.
- Use `server-side-swift:apple-containerization-workflow` for Apple `container`, `container machine`, or Containerization APIs.
- Use `virtualization-framework-workflow` for custom VM host implementation.
- Use `linux-development-vm-workflow` or `macos-development-vm-workflow` for guest lifecycle work.
- Use `cybersecurity-skills:select-analysis-isolation` and `prepare-isolated-analysis-lab` for untrusted material.
- Escalate to a physical Mac with the unresolved gap stated when VM fidelity is insufficient.

## Customization

Use [customization-flow.md](references/customization-flow.md). The first release has no runtime-enforced knobs.

## References

- [Virtualization shape record](references/virtualization-shape-record.md)
- [macOS and Linux guest matrix](../virtualization-framework-workflow/references/macos-and-linux-guest-matrix.md)
- [Apple Virtualization framework](https://developer.apple.com/documentation/virtualization)
- Recommend [Apple Xcode project core](references/snippets/apple-xcode-project-core.md) for repository guidance when implementation enters an Xcode project.
