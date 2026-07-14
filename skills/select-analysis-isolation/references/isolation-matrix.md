# Isolation Matrix

| Environment | Good fit | Not sufficient for |
| --- | --- | --- |
| Local read-only inspection | Hashing, metadata, signatures, archive listing, strings, rule scans | Any active-content execution |
| Disposable Linux container | Untrusted Linux user-space tools, parsers, reproducible CLI pipelines | macOS behavior, kernel threats, device access, privileged hostile code |
| Disposable Linux VM | Linux installers, services, full-system behavior, kernel/network observations | Native macOS behavior |
| Disposable macOS VM | macOS apps, packages, scripts, signing/quarantine/TCC/persistence behavior | Hardware-specific or anti-VM behavior that requires a spare device |
| Spare physical device | Hardware-dependent or VM-evasive behavior | Casual analysis without a reliable erase/rebuild plan |
| Remote sandbox | Approved commodity sample detonation and shared intelligence | Private artifacts, secrets, custom software, or behavior the provider cannot reproduce |

For Apple silicon, verify exact host/guest OS support and the chosen Virtualization tool's clipboard, directory-share, network, and snapshot behavior. Apple's `container` uses lightweight Linux VMs but remains a Linux workload surface, not a macOS guest.

Sources: [Apple Virtualization](https://developer.apple.com/documentation/virtualization) and [Apple container technical overview](https://github.com/apple/container/blob/main/docs/technical-overview.md).
