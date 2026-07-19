# Security Lab Control Profile

Every field must be explicit. Use `absent`, `disabled`, `read-only`, `allowlisted`, or another verified state instead of relying on a product default.

## Identity And Base

- authorization and research question
- host model/chip/build; guest OS/build/architecture
- base image or restore-image source and digest
- VM manager/framework/CLI and exact version
- accounts, privilege, clock/time zone, CPU, memory, disk, and reset operation
- baseline hashes/state and virtualization artifacts that may change behavior

## Host Integration

- host folders and home sharing
- clipboard and drag/drop
- host/guest sockets and SSH agent
- browser profiles, password stores, developer certificates, signing identities
- Apple/cloud accounts, tokens, registries, package-manager credentials
- USB, microphone, camera, graphics, audio, and other passthrough devices

Default every item above to absent. Approve an exception only when it is required by the named observation and has a removal check.

## Network

- offline, simulated, allowlisted egress, or monitored network mode
- DNS, gateway, routes, packet/log capture, ingress, egress, and time source
- external destinations and authorization
- forwarded/listening ports and their teardown checks

## Observation And Stop Controls

- process, filesystem, persistence, service, security-control, DNS/network, and log telemetry
- minimum stimulus, execution identity, stop command/control, resource/time limits
- anti-VM and coverage limitations

## Evidence Export

- guest staging directory and host export directory
- allowed artifact types and maximum size
- hashes, archive format, metadata, malware scanning, and human review
- prohibition on exporting live credentials, sockets, whole home directories, or unrelated guest state

## Teardown Proof

- workload and guest stopped
- intended evidence exported and scanned
- disposable state reverted or removed
- temporary credentials revoked
- shares, clipboard, sockets, devices, routes, captures, and forwarded ports removed
- no helper, service, or workload remains active

## Profiles

- `offline-static`: no target execution, no network, read-only sample input, narrow report export
- `monitored-linux-dynamic`: disposable Linux guest, no home sharing, monitored or simulated network, process/filesystem/service capture
- `monitored-macos-dynamic`: disposable macOS guest, native control telemetry, no personal Apple/developer identities, VM-fidelity caveats
- `network-service`: isolated test network, explicit clients/servers, allowlisted ingress/egress, packet capture, port teardown
- `nested-virtualization`: verified host/guest/kernel capability, no home sharing, inner and outer lifecycle/evidence ownership, resource limits
