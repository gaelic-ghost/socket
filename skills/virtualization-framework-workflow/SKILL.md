---
name: virtualization-framework-workflow
description: Build and diagnose custom macOS and Linux VM hosts with Apple's Virtualization framework. Use for platform and boot configuration, devices, VM bundles, lifecycle, save and restore, UI, entitlements, and framework errors.
---

# Virtualization Framework Workflow

## Purpose

Implement one explicit macOS or Linux Virtualization framework path without flattening their platform, boot, identity, or device differences.

## When To Use

- Use for `VZVirtualMachineConfiguration`, guest devices, `VZVirtualMachine`, `VZVirtualMachineView`, lifecycle, and diagnostics.
- Use when building a custom VM host app or Swift package rather than operating an existing VM manager.
- Use for save/restore capability checks, not as a general snapshot-product workflow.

## Single-Path Workflow

1. Read current Xcode-local Virtualization documentation for every selected API and availability gate.
2. Consume or create the [virtualization shape record](../choose-macos-virtualization-shape/references/virtualization-shape-record.md).
3. Choose the guest family using [macOS and Linux guest matrix](references/macos-and-linux-guest-matrix.md):
   - macOS: Mac platform identity, macOS boot loader, restore-image compatibility, auxiliary storage
   - Linux/generic: generic platform, Linux or EFI boot, kernel/initrd/command line or EFI disk
4. Separate the implementation into configuration construction, bundle/artifact persistence, VM lifecycle, and optional UI ownership. Make a headless console/service path or `VZVirtualMachineView` ownership explicit rather than creating both accidentally.
5. Add only required devices after checking [device and availability matrix](references/virtualization-device-and-availability-matrix.md).
6. Require the virtualization entitlement, supported CPU/memory values, exact OS availability, and `validate()` before start.
7. Model start, pause, resume, stop, and state transitions explicitly. Save/restore only in documented states with a configuration compatible with the saved state.
8. Validate configuration, boot, console/UI, disk, network, shares, services, shutdown, and teardown at the narrowest relevant level.
9. Preserve the failed configuration surface, VM state, host/guest versions, underlying error, and likely cause.

## Inputs

- Completed virtualization shape record.
- Guest family, boot source, identity artifacts, disks, devices, resources, UI needs, and lifecycle requirements.
- Host macOS/Xcode version and target deployment version.

## Outputs

- `status`: `success`, `handoff`, or `blocked`.
- Documented configuration and availability decisions.
- Separate configuration, artifact, lifecycle, and UI ownership.
- Validation evidence and exact diagnostics.

## Guards and Stop Conditions

- Do not start before configuration validation succeeds.
- Do not reuse a macOS hardware model, machine identifier, or auxiliary storage as if it were a generic Linux platform.
- Do not expose shares, clipboard, sockets, devices, audio input, or USB without a stated need.
- Do not call saved machine state a disk snapshot, clone, or portable VM bundle.
- Do not promise nested virtualization, Rosetta, clipboard, USB, or save/restore without guest and OS capability proof.
- Stop when the restore image, boot artifacts, entitlement, host support, configuration compatibility, or disk ownership is unresolved.
- Announce before any visible or resource-intensive launch.

## Fallbacks and Handoffs

- Use `choose-macos-virtualization-shape` when the boundary is undecided.
- Use `linux-development-vm-workflow` or `macos-development-vm-workflow` for guest preparation and reset strategy.
- Use `xcode-app-project-workflow` for target membership, entitlement wiring, and app-project integration.
- Use `xcode-build-run-workflow` and `xcode-testing-workflow` for execution and tests.
- Use `prepare-isolated-analysis-lab` for hostile-workload control policy.

## Customization

Use [customization-flow.md](references/customization-flow.md). The first release has no runtime-enforced knobs.

## References

- [macOS and Linux guest matrix](references/macos-and-linux-guest-matrix.md)
- [Device and availability matrix](references/virtualization-device-and-availability-matrix.md)
- [Apple Virtualization framework](https://developer.apple.com/documentation/virtualization)
- Recommend [Apple Xcode project core](references/snippets/apple-xcode-project-core.md) when editing an Xcode project.
