# Virtualization Shape Record

Record this compact handoff before implementation. It is a reasoning shape, not a serialized compatibility layer.

- `purpose`: development, compatibility, CI-like validation, security analysis, framework implementation, or runtime diagnosis
- `host`: Mac/chip, architecture, macOS build, memory/storage budget, and selected toolchain
- `workload`: target OS/version/distro, architecture, GUI/headless, privileges, kernel/devices, and lifetime
- `boundary`: host, OCI container, Apple per-container VM, Apple container machine, full Linux VM, full macOS VM, remote environment, or physical Mac
- `provenance`: tool/framework, restore or OCI image, kernel/init filesystem, and exact versions/digests
- `resources`: CPU, memory, disks, graphics, audio, USB, ballooning, and performance limits
- `integration`: shares, clipboard, sockets, ports, network, agents, credentials, identities, accounts, and browser profiles
- `lifecycle`: supported create/install/start/pause/save/restore/stop/clone/reset/update/export/remove operations
- `validation`: configuration, boot, identity, network, filesystem, service, application, and teardown checks
- `evidence`: logs, artifacts, capture, hashes, screenshots, state, and safe export path
- `uncertainty`: unsupported combinations, beta APIs, VM artifacts, hardware gaps, and physical-device requirements

Use `absent`, `disabled`, or `not supported` instead of leaving a security-sensitive integration implicit.
