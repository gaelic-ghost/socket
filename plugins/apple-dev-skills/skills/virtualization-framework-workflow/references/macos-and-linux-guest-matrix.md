# macOS And Linux Guest Matrix

| Concern | macOS guest | Linux or generic guest |
| --- | --- | --- |
| Platform | `VZMacPlatformConfiguration` | `VZGenericPlatformConfiguration` |
| Boot | `VZMacOSBootLoader` plus compatible restore image | `VZLinuxBootLoader` or EFI boot loader |
| Identity | hardware model, machine identifier, auxiliary storage | generic platform; no Mac identity artifacts |
| Installation | restore-image and installer flow | kernel/initrd/root filesystem or EFI installer/disk |
| Graphics/UI | Mac graphics device and display | virtio graphics when supported/needed |
| Rosetta | not an assumed nested container capability | Linux Rosetta directory share when documented and supported |
| Nested virtualization | do not infer support from generic-platform APIs | capability-gated generic platform plus guest kernel/device proof |
| Security fidelity | useful for native macOS controls, with VM artifacts | cannot prove Gatekeeper, TCC, XProtect, LaunchServices, or macOS persistence |
| Physical fidelity | limited for hardware, Secure Enclave, recoveryOS, devices, performance, and anti-VM behavior | limited for host-hardware and anti-VM behavior |

Always check the current SDK documentation and host capabilities; this table identifies ownership differences, not universal availability.
