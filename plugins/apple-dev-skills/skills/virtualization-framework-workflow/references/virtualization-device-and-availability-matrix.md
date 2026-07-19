# Virtualization Device And Availability Matrix

Check current Xcode-local documentation for every concrete class before implementing it. Record host OS, guest family, minimum deployment target, required guest support, and whether the device crosses a security boundary.

| Family | Decision to record |
| --- | --- |
| Storage | image/block device ownership, caching/synchronization, read-only state, attachment lifetime |
| Network | NAT or bridged attachment, MAC address, ports, monitoring, external reachability |
| Directory sharing | exact host directory, read/write state, tag/mount point, hostile-workload prohibition |
| Socket/console | endpoint ownership, authentication, serial console/log retention |
| Graphics/input | display dimensions, headless/UI path, keyboard and pointing devices |
| Audio | output/input need; microphone access remains opt-in |
| USB | controller/device support and explicit passthrough need |
| Memory balloon | guest support and expected pressure behavior |
| Entropy | guest random device requirement |
| Rosetta | supported Linux guest path and installation/share requirements |
| Nested virtualization | host/chip/OS support, generic-platform setting, guest kernel, `/dev/kvm` proof |
| Save/restore | host API availability, paused/stopped state rule, compatible configuration and artifacts |

Never add a device merely because the API exists. Each device expands behavior, failure surface, or host integration.
