---
name: linux-development-vm-workflow
description: Prepare and reset persistent Linux development guests on macOS. Use when comparing container machine, Lima or Colima, and full VMs for distros, init systems, services, custom boot, disks, Rosetta, or nested virtualization.
---

# Linux Development VM Workflow

## Purpose

Prepare one persistent Linux development environment whose lifecycle, host integrations, provenance, validation, and reset path are explicit.

## When To Use

- Use for distro-specific builds, services, systemd or another init system, repeated shells, full-system tests, custom kernels, EFI boot, or GUI Linux.
- Use to decide between `container machine`, Lima/Colima, and a full VM by required fidelity rather than product preference.
- Do not use for a single portable application image; use the container owner skills.

## Single-Path Workflow

1. Consume the [virtualization shape record](../choose-macos-virtualization-shape/references/virtualization-shape-record.md).
2. Discover current official documentation and installed versions/help for every candidate tool.
3. Select the smallest adequate path:
   - `container machine`: OCI-backed persistent Linux, init/services, repeated interactive development
   - Lima/Colima adapter: tool-managed Linux environment when its documented lifecycle and integration match the task
   - full Virtualization framework VM: custom boot/kernel/disk/devices, full-system or GUI behavior, or tighter integration control
4. Record distro/image/kernel provenance, architecture, CPU, memory, disks, network, mounts, sockets, credentials, and expected lifetime.
5. Keep host home, writeable shares, SSH agent, credentials, clipboard, and unrestricted network opt-in. A development convenience is not a security boundary.
6. Configure Linux or EFI boot, virtio devices, provisioning, services, Rosetta, and nested virtualization only when the selected path and current host/guest support them.
7. Define create, provision, start, shell/SSH, stop, update, checkpoint/reset, export, and remove semantics using the selected tool's vocabulary.
8. Validate the distro matrix: identity, architecture, toolchain, build, tests, services, filesystem semantics, network, reboot persistence, and cleanup.

## Inputs

- Completed virtualization shape record.
- Distro/version, architecture, system services, boot/kernel needs, toolchain, resources, integrations, and reset frequency.
- Exact selected tool version and official documentation.

## Outputs

- Selected Linux guest path and rejected alternatives.
- Provenance and resource/integration record.
- Exact lifecycle and provisioning path.
- Distro-matrix validation and reset/teardown evidence.

## Guards and Stop Conditions

- Do not call `container machine` a macOS VM, ordinary application container, or Compose replacement.
- Do not assume Docker, Apple `container`, Lima, Colima, or a custom VM share flags or lifecycle semantics.
- Do not enable home sharing for untrusted work; hand security research to `prepare-isolated-analysis-lab`.
- Do not promise Rosetta or nested virtualization without host, OS, kernel, and device proof.
- Do not commit images, kernels, disks, credentials, or machine-local runtime state.
- Stop when provenance, capacity, reset strategy, host integration, or required fidelity cannot be verified.
- Announce before starting a VM/service, downloading an image, or creating a large disk.

## Fallbacks and Handoffs

- Use `server-side-swift:apple-containerization-workflow` for `container machine` command semantics.
- Use `server-side-swift:docker-workflow` for Dockerfiles, Compose, registries, and portable OCI deployment.
- Use `virtualization-framework-workflow` for custom full-VM implementation.
- Use `xcode-build-run-workflow`, `swift-package-build-run-workflow`, or stack-specific skills after the guest is ready.
- Use `prepare-isolated-analysis-lab` for disposable hostile-workload controls.

## Customization

Use [customization-flow.md](references/customization-flow.md). The first release has no runtime-enforced knobs.

## References

- [Linux development guest matrix](references/linux-development-guest-matrix.md)
- [macOS and Linux guest matrix](../virtualization-framework-workflow/references/macos-and-linux-guest-matrix.md)
- [Apple container machine documentation](https://github.com/apple/container/blob/main/docs/container-machine.md)
- [Lima documentation](https://lima-vm.io/docs/)
- [Colima repository](https://github.com/abiosoft/colima)
- Recommend [Apple Xcode project core](references/snippets/apple-xcode-project-core.md) for a custom Xcode VM host.
