---
name: macos-development-vm-workflow
description: Prepare and reset clean macOS development guests on Apple silicon. Use for restore-image compatibility, VM identity, installation, resources, OS-version testing, signing, privacy, and disposable macOS research guests.
---

# macOS Development VM Workflow

## Purpose

Prepare a reproducible macOS guest while keeping restore images, identity, disks, saved state, clones, integrations, and exported evidence as separate lifecycle artifacts.

## When To Use

- Use for clean macOS releases, installers, updates, signing, entitlements, quarantine, Gatekeeper, XProtect, TCC, SIP-enabled behavior, LaunchServices, and native persistence.
- Use after custom host implementation or with an existing documented VM manager.
- Use for development guests and benign security fixtures; security controls still require `prepare-isolated-analysis-lab` for untrusted execution.

## Single-Path Workflow

1. Consume the [virtualization shape record](../choose-macos-virtualization-shape/references/virtualization-shape-record.md).
2. Verify Apple silicon host, host build, current framework/tool docs, restore-image support, guest build, storage, memory, and installation time budget.
3. Record each artifact using [macOS VM artifact lifecycle](references/macos-vm-artifact-lifecycle.md): restore image, hardware model, machine identifier, auxiliary storage, disk, bundle metadata, saved state, clone, and evidence export.
4. Build or verify a compatible Mac platform, boot loader, disk, CPU/memory, graphics/display, network, input, and entropy configuration; validate before installation or boot.
5. Install with the documented restore-image flow and preserve exact progress/errors. Do not invent or duplicate Mac identity artifacts.
6. Configure guest purpose and integrations. Directory sharing, clipboard, audio input, USB, Apple account, iCloud, developer account, signing identities, browser profiles, and network are opt-in.
7. Establish a clean baseline, then choose named development/update checkpoints or disposable clones using only lifecycle operations the selected tool actually supports.
8. Validate guest build/architecture, SIP and relevant controls, network/shares, reboot, toolchain, target behavior, evidence export, and reset.
9. Record VM artifacts and physical-hardware gaps that may affect the conclusion.

## Inputs

- Completed virtualization shape record.
- Host and target guest builds, restore-image source, resources, selected VM tool/framework, integrations, and validation purpose.
- Required toolchains, identities, accounts, security controls, reset strategy, and evidence path.

## Outputs

- Compatible restore/image and VM identity record.
- Separate artifact lifecycle and integration decisions.
- Installation, baseline/checkpoint, validation, export, and reset evidence.
- Explicit physical-Mac or unsupported-capability gaps.

## Guards and Stop Conditions

- Do not treat an arbitrary restore image as compatible with the host/platform configuration.
- Do not conflate saved machine state with disk state, a clone, or a portable snapshot.
- Do not copy identity artifacts between independent VMs without documented tool support and an explicit identity decision.
- Do not add personal Apple accounts, developer identities, credentials, shares, clipboard, devices, or microphone by default.
- Treat automated macOS guest provisioning as beta and availability-gated until current SDK/runtime evidence proves the selected path.
- Stop for unsupported restore compatibility, unresolved disk ownership, insufficient capacity, unclear identity, or a hardware/recoveryOS/Secure Enclave fidelity requirement.
- Announce before downloads, large disk creation, installation, or visible/resource-intensive launch.

## Fallbacks and Handoffs

- Use `virtualization-framework-workflow` for custom host configuration or lifecycle defects.
- Use `apple-developer-provisioning-workflow` only after the guest boundary is approved and ready.
- Use `xcode-build-run-workflow`, `xcode-testing-workflow`, or `macos-distribution-workflow` for work inside the prepared guest.
- Use `prepare-isolated-analysis-lab` before executing untrusted content.
- Use a spare physical Mac when hardware, recoveryOS, Secure Enclave, device, performance, or anti-VM fidelity is required.

## Customization

Use [customization-flow.md](references/customization-flow.md). The first release has no runtime-enforced knobs.

## References

- [macOS VM artifact lifecycle](references/macos-vm-artifact-lifecycle.md)
- [macOS and Linux guest matrix](../virtualization-framework-workflow/references/macos-and-linux-guest-matrix.md)
- [Apple Virtualization framework](https://developer.apple.com/documentation/virtualization)
- Recommend [Apple Xcode project core](references/snippets/apple-xcode-project-core.md) for a custom Xcode VM host.
