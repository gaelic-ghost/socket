# macOS Virtualization And Container Skills Plan

## Intent

Expand Socket's Apple-hosted compute guidance so an agent can choose and operate the right boundary for development, compatibility testing, and authorized security research:

- an ordinary process on the host Mac
- an OCI container
- an Apple `container` lightweight per-container Linux VM
- an Apple `container machine` persistent Linux environment
- a full Linux VM
- a full macOS VM
- a spare physical Mac when VM fidelity is insufficient

The practical result should be a clean path for building on Linux while editing on macOS, validating software on a clean macOS release, reproducing security controls such as SIP or Gatekeeper in a separate guest, and running suspicious Linux or macOS workloads without casually exposing the host's files, clipboard, credentials, devices, or network.

This is a coordinated skill expansion across existing plugins. It does not create a new virtualization plugin, ship a VM manager, install a hypervisor, bundle guest images, or turn Socket into a lab runtime.

## Source Baseline

This plan was checked on 2026-07-19 against current local and upstream evidence.

- Apple's [`container` 1.0.0 release](https://github.com/apple/container/releases/tag/1.0.0) adds persistent `container machine` environments, replaces UserDefaults-backed system properties with TOML configuration, changes structured list output, adds `container cp`, and removes compatibility with version-zero XPC APIs.
- Apple's current [`container machine` documentation](https://github.com/apple/container/blob/main/docs/container-machine.md) describes persistent OCI-image-backed Linux environments, automatic host user and home-directory integration, long-running init systems, configurable CPU and memory, optional home sharing, and nested virtualization on supported hosts with a compatible kernel. The 1.0.0 release links this current-branch document rather than a tag-contained copy, so implementation must pair it with the installed CLI's own help.
- Apple's [`container` technical overview](https://github.com/apple/container/blob/1.0.0/docs/technical-overview.md) states that ordinary `container` workloads run each Linux container in its own lightweight VM and documents the Virtualization, vmnet, XPC, Keychain, launchd, and unified-log architecture.
- The lower-level [`apple/containerization` project](https://github.com/apple/containerization) has not reached 1.0. Its current [release page](https://github.com/apple/containerization/releases) still exposes 0.x prerelease tags, so package API guidance must continue to use exact-version source and release documentation rather than treating the Swift package as source-stable.
- Apple's [Virtualization framework](https://developer.apple.com/documentation/virtualization) supports custom macOS and Linux guests, configurable devices, VM lifecycle control, and `VZVirtualMachineView` on macOS.
- Virtualization framework save and restore APIs are available on macOS 14 and later, require a compatible configuration, and are distinct from disk cloning or a complete snapshot-management product.
- Apple's public nested-virtualization control is exposed through `VZGenericPlatformConfiguration`. Treat nested virtualization for generic or Linux guests as capability-gated, and do not promise that an Apple `container` runtime can run inside a macOS guest without separate current proof.
- Automated macOS guest provisioning through `VZMacGuestProvisioningOptions` is a beta, macOS 27-or-later guest capability. Keep it version-gated and outside the stable first slice.

Local host evidence on the planning date:

- macOS 26.5.2 on arm64 Apple silicon
- Lima 2.1.4, Colima 0.10.3, and Docker CLI 29.6.2 are installed
- Apple's `container` CLI is not installed

The installed-tool observation informs forward-test sequencing only. The skills must remain portable and must discover the actual host, tool, version, guest, and configuration at runtime.

## Architecture Decision

Extend `apple-dev-skills`, `server-side-swift`, and `cybersecurity-skills` through explicit handoffs. Do not create a fourth plugin that tries to own every VM, container, and security-lab concern.

This is a durable building-block change. It creates a reusable selection contract and separate implementation and operating workflows while preserving the repositories that already own Apple framework implementation, Apple container tooling, and defensive isolation decisions.

The change unlocks these near-term uses:

- clean macOS development guests for OS-version, signing, entitlement, privacy, installer, update, and Xcode/toolchain validation
- persistent Linux development environments that can run init systems and services without being confused with application containers
- custom Virtualization framework apps and tools for macOS or Linux guests
- disposable macOS and Linux analysis labs with explicit host-integration controls
- full-OS validation of SIP-, TCC-, Gatekeeper-, XProtect-, quarantine-, persistence-, kernel-, and service-dependent behavior
- repeatable evidence export, revert, and teardown after security experiments
- explicit comparison among Docker, Apple `container`, `container machine`, Lima or Colima, a full VM, and a physical device

The simpler extension path was to enlarge `server-side-swift:apple-containerization-workflow` into a general VM and security-lab skill. That would mix OCI image work, persistent Linux development, macOS restore images, Virtualization framework app code, and hostile-workload isolation into one oversized workflow. It would also make generic macOS and security work depend on a server-side Swift plugin. Keep that skill focused on Apple's container stack and use cross-plugin handoffs instead.

## Ownership And Handoffs

| Surface | Primary owner | Responsibility |
| --- | --- | --- |
| Choosing a macOS-hosted development boundary | `apple-dev-skills:choose-macos-virtualization-shape` | Compare host execution, containers, persistent Linux machines, full Linux or macOS VMs, and physical Macs by fidelity, lifecycle, integration, and risk. |
| Implementing a custom VM host app or Swift package | `apple-dev-skills:virtualization-framework-workflow` | Own `VZVirtualMachineConfiguration`, guest/platform configuration, devices, lifecycle, UI, entitlements, save/restore support, and framework diagnostics. |
| Provisioning and operating a macOS development guest | `apple-dev-skills:macos-development-vm-workflow` | Own restore-image compatibility, VM bundle identity, installation, resources, guest setup, development-tool installation handoffs, clean baselines, and reset strategy. |
| Provisioning and operating a full Linux development guest | `apple-dev-skills:linux-development-vm-workflow` | Own kernel or EFI boot choice, disks, virtio devices, Rosetta handoff, system services, host integration, distro matrix, and persistent guest lifecycle. |
| Apple `container`, `container machine`, Containerization APIs, OCI images, and Apple-native Linux container runtime behavior | `server-side-swift:apple-containerization-workflow` | Own the 1.0 CLI split between application containers and persistent Linux machines, plus exact-version lower-level package use. |
| Dockerfile, Compose, registries, and portable OCI deployment | `server-side-swift:docker-workflow` | Keep portable image and deployment behavior independent from the selected macOS runtime. |
| Selecting an isolation level for untrusted material | `cybersecurity-skills:select-analysis-isolation` | Choose the smallest environment that reproduces the target while containing its likely behavior. |
| Preparing and tearing down a disposable security lab | `cybersecurity-skills:prepare-isolated-analysis-lab` | Convert the isolation decision into verified mount, clipboard, credential, device, network, baseline, evidence-export, revert, and teardown controls. |
| Observing malicious or suspicious behavior | `cybersecurity-skills:perform-dynamic-malware-analysis` | Own the observation plan and findings while consuming the prepared lab contract. |
| Binary internals | `reverse-engineering-skills` | Consume preserved guest artifacts and own disassembly, decompilation, symbols, and binary behavior. |

The two operating skills under Apple Dev are intentionally guest-specific. A macOS guest is installed from a compatible restore image and carries Apple identity, platform, signing, privacy, and restore constraints. A Linux guest uses a generic platform configuration, Linux or EFI boot, virtio devices, and may expose Rosetta or nested virtualization. Combining them would hide the failure modes that matter most.

## Shared Virtualization Shape Record

Every development or implementation workflow should produce or consume one compact record:

- purpose: development, compatibility, CI-like validation, security analysis, framework implementation, or runtime diagnosis
- host: Mac model or chip family, architecture, macOS build, memory, storage budget, and selected Xcode or Swift toolchain when relevant
- workload: target OS, target version or distro, architecture, GUI or headless mode, privileged behavior, kernel needs, devices, and expected lifetime
- boundary: host, OCI container, Apple per-container VM, Apple container machine, full Linux VM, full macOS VM, remote environment, or physical Mac
- provenance: CLI, framework, VM manager, restore image, OCI image, kernel, init filesystem, and exact versions or digests
- resources: CPU, memory, disks, ballooning expectations, graphics, audio, USB, and performance constraints
- integration: mounts or directory shares, clipboard, sockets, port forwarding, bridged or NAT networking, SSH agent, credentials, browser profiles, developer identities, and cloud accounts
- lifecycle: create, install, start, pause, save, restore, stop, clone, reset, update, export, and remove semantics supported by the selected tool
- validation: configuration validation, guest boot, identity, network, filesystem, service, application, and teardown checks
- evidence: logs, guest artifacts, packet capture, hashes, screenshots, state files, and an explicit safe export path
- uncertainty: unsupported combinations, beta-only APIs, anti-VM or hardware fidelity gaps, and claims still requiring a physical Mac

Use this record as a handoff shape, not as a new runtime abstraction or serialized compatibility layer. Each owning skill should retain its platform-specific types and commands.

## Boundary Selection Rules

### Host Process

Use the host directly when the work needs native macOS behavior, the dependency set is trusted, and isolation or clean-state reproduction is not part of the question.

### OCI Application Container

Use an OCI container when the job is one application or service, disposable Linux user space is sufficient, and image portability matters. Keep Dockerfile and image design portable even when Apple's `container` CLI is the local runtime.

### Apple Per-Container Lightweight VM

Use Apple `container` when the job is an OCI workload on a supported Apple silicon Mac and per-container VM isolation is useful. Keep host mounts, SSH-agent forwarding, credentials, capabilities, network selection, and kernel overrides explicit.

### Apple Container Machine

Use `container machine` when the job is a persistent Linux development environment with an init system, services, distro-specific state, or repeated interactive shell access. Treat its automatic user and home-directory integration as a development convenience, not a safe default for hostile code or security research.

### Full Linux VM

Use a full Linux VM when the work needs a custom kernel, installer or boot flow, full-system observation, separate disk lifecycle, stronger control over host integration, GUI Linux, or behavior that does not fit an OCI-image-backed environment.

### Full macOS VM

Use a macOS VM when the work needs native macOS frameworks, installers, signing, quarantine, Gatekeeper, XProtect, TCC, SIP-enabled customer-like behavior, launch services, persistence, or clean OS-version state. Do not substitute a Linux container or Linux VM for these questions.

### Physical Mac

Use a spare physical Mac when the behavior depends on hardware, Secure Enclave identity, unsupported devices, VM detection, performance characteristics, recoveryOS, or another capability that the selected VM cannot reproduce faithfully.

## Phase 1: Selection And Stable Framework Foundation

### `apple-dev-skills:choose-macos-virtualization-shape`

- Classify workload fidelity, persistence, portability, host integration, guest OS, threat level, and resource needs before recommending a tool.
- Distinguish an application container from a persistent container machine and both from a full VM.
- Route OCI authoring to Docker, Apple runtime behavior to Apple Containerization, full-VM implementation to Virtualization framework, and hostile-workload selection to Cybersecurity.
- Return the shared virtualization shape record and one primary path, not a menu without a decision.
- Keep third-party products behind capability discovery and official documentation rather than making any one installed tool the default.

### `apple-dev-skills:virtualization-framework-workflow`

- Cover macOS and Linux guest configuration without flattening their platform and boot differences.
- Require `com.apple.security.virtualization`, `validate()`, supported CPU and memory ranges, and exact availability checks before start.
- Cover storage, network, shared directories, sockets, serial or console, graphics, input, audio, clipboard, USB, Rosetta, memory balloon, and nested-virtualization decisions only when the guest and OS version support them.
- Keep VM configuration, VM bundle persistence, lifecycle state, and UI ownership separate.
- Treat save/restore state as configuration-compatible paused-machine state, not as a complete disk snapshot or cloning system.
- Preserve framework errors with the failed configuration surface, guest state, host capability, and likely cause.

### Existing-skill alignment

- Update `cybersecurity-skills:select-analysis-isolation` to hand custom VM implementation to `virtualization-framework-workflow` and development-shape selection to `choose-macos-virtualization-shape`.
- Update Apple Dev and Cybersecurity routing references so a macOS VM is the stable high-fidelity answer for SIP-sensitive behavior while local sandbox, TCC, or failure injection remain explicitly lower-fidelity approximations.

Phase 1 exit criteria: an agent can choose the correct boundary and implement or diagnose a custom Virtualization framework host without confusing macOS guests, Linux guests, containers, saved state, disk snapshots, or physical-device proof.

## Phase 2: Apple Container 1.0 And Persistent Linux Development

### Expand `server-side-swift:apple-containerization-workflow`

- Add a current version gate that distinguishes `container` CLI 1.x from the still-0.x Containerization Swift package.
- Add `container machine` as a first-class job alongside build, pull, run, registry, and lower-level API work.
- Cover create, run, inspect, set-default, resource changes, stop, and remove semantics for persistent machines.
- Cover the TOML configuration migration and structured-output changes from 1.0 without preserving removed `container system property` commands as compatibility shims.
- Separate ordinary container mounts from a container machine's automatic user and home sharing.
- Require `home-mount=none` or an equivalently isolated configuration before treating a container machine as a security boundary.
- Cover nested virtualization only after checking host support, compatible Apple silicon, OS version, kernel configuration, and `/dev/kvm` exposure.
- Keep `container machine` positioned as Linux development, not macOS virtualization and not a Docker Compose replacement.
- Add exact-version source checks for the lower-level Containerization package because its public API is not 1.0-stable.

### `apple-dev-skills:linux-development-vm-workflow`

- Compare `container machine`, Lima or Colima, and a full Virtualization framework Linux guest by required fidelity rather than brand.
- Own persistent distro environments, system services, kernel or EFI boot, disks, resource budgets, virtio integration, networking, Rosetta, nested virtualization, guest provisioning, and repeatable reset.
- Keep portable OCI image authoring in Docker and Apple CLI behavior in Apple Containerization.
- Provide a distro-matrix validation shape for toolchain, build, test, service, filesystem, architecture, and cleanup evidence.

Phase 2 exit criteria: an agent can use the 1.0 Apple CLI for either a disposable OCI workload or a persistent Linux development machine, and can choose a full Linux VM when container-machine integration or image constraints are the wrong fit.

## Phase 3: macOS Development Guests

### `apple-dev-skills:macos-development-vm-workflow`

- Verify Apple silicon, host build, restore-image support, guest build, hardware model, machine identifier, auxiliary storage, disk, CPU, memory, and graphics requirements before installation.
- Treat the restore image, VM bundle, machine identity, disk contents, saved machine state, and exported evidence as separate artifacts with separate lifecycle rules.
- Support clean baseline, named development checkpoint, update-testing checkpoint, and disposable clone strategies without promising a framework-level snapshot feature that was not verified.
- Keep directory sharing, clipboard, audio input, USB, iCloud, developer accounts, signing identities, and network access opt-in and purpose-bound.
- Hand Xcode installation, signing, project build, and test work to their existing Apple Dev owners after the guest itself is ready.
- Add stable manual or tool-specific guest provisioning first. Add macOS 27 automated guest provisioning only as an availability-gated beta reference after current Xcode documentation and runtime behavior are verified.
- Record which questions still require a physical Mac, recoveryOS, or device-attached validation.

Phase 3 exit criteria: an agent can prepare and reset a clean macOS development guest, explain exactly which host integrations and identities cross the boundary, and produce evidence for OS-version or security-control validation without calling a VM a container.

## Phase 4: Disposable Security Labs

### `cybersecurity-skills:prepare-isolated-analysis-lab`

- Consume an approved isolation decision and produce a concrete lab configuration before executing untrusted content.
- Default host folders, home sharing, clipboard, drag and drop, sockets, SSH agents, browser profiles, cloud credentials, Apple accounts, signing identities, USB, microphone, camera, and unrestricted networking to absent.
- Require a trusted base image or restore image, exact host and guest builds, clock strategy, resource limits, baseline hashes or state, and an explicit evidence-export directory.
- Provide distinct profiles for offline static tooling, monitored Linux dynamic analysis, monitored macOS dynamic analysis, network-service research, and nested-virtualization experiments.
- Keep evidence collection separate from guest control. Hand observations to dynamic malware analysis, binaries to Reverse Engineering, and VM implementation defects to Apple Dev.
- Verify teardown by stopping the workload, exporting only intended evidence, scanning the export, reverting or removing disposable state, revoking temporary credentials, and confirming that no share, forwarded port, or helper remains active.
- Stop when target-platform fidelity, isolation controls, legal authorization for active testing, or safe evidence export cannot be verified.

### Security workflow alignment

- Update `perform-dynamic-malware-analysis` to require the prepared-lab record for active execution.
- Update macOS threat and runtime workflows to distinguish guest-observed behavior from host-observed behavior and to record virtualization artifacts that may affect conclusions.
- Add explicit anti-VM, hardware, Secure Enclave, recoveryOS, kernel-extension, system-extension, and device-access limitations to the isolation reference.
- Keep images, kernels, malware samples, credentials, privileged helpers, and runtime services out of the plugin payload.

Phase 4 exit criteria: an agent can create a reviewable lab plan for Linux or macOS security work, prove the intended isolation controls before execution, export evidence through a narrow path, and verify teardown afterward.

## Tool Adapter Policy

Do not create tool-specific skills during the first pass merely because a tool is installed or popular.

- Keep Apple Virtualization framework and Apple `container` as first-party owner workflows.
- Treat Lima, Colima, Tart, UTM, VMware Fusion, Parallels Desktop, OrbStack, and similar products as adapters behind the guest and boundary workflows when current official documentation is available.
- Add a dedicated adapter skill only after repeated real tasks show that the tool has a distinct lifecycle, configuration model, or failure surface that cannot remain concise in the owner skill.
- Do not claim that two products provide equivalent isolation merely because both use Virtualization framework or both launch a Linux VM.
- Do not instruct an agent to launch a GUI VM product, start a VM, start Apple's container system service, or execute a guest workload without first telling Gale the exact visible or resource-intensive action.

The first implementation pass should forward-test Apple framework and Apple container paths, then use the already installed Lima and Colima tools only for comparative read-only discovery or explicitly approved execution. Third-party installation is outside this plan unless Gale requests it separately.

## Reusable References

Keep the new `SKILL.md` files procedural and concise. Prefer directly linked references for details that are version-sensitive or shared across workflows:

- `virtualization-shape-record.md`: shared inputs, outputs, and handoff vocabulary
- `macos-and-linux-guest-matrix.md`: platform, boot, identity, device, sharing, save/restore, and fidelity differences
- `virtualization-device-and-availability-matrix.md`: framework device families and OS availability
- `macos-vm-artifact-lifecycle.md`: restore images, VM bundles, auxiliary storage, disks, machine identity, saved state, clones, and evidence exports
- `apple-container-version-matrix.md`: CLI 1.x versus Containerization package versions and breaking surfaces
- `security-lab-control-profile.md`: mounts, clipboard, credentials, devices, networking, baseline, export, and teardown controls

Do not duplicate the same matrix in multiple plugins. Put Apple framework facts under Apple Dev, Apple CLI and package facts under Server-Side Swift, and threat-driven control policy under Cybersecurity. Cross-link the owning reference from handoff sections.

## Validation And Forward Tests

### Static validation

- Generate or refresh `agents/openai.yaml` from final skill content.
- Run the Apple Dev docs validator and pytest suite for Apple Dev changes.
- Run the Cybersecurity child metadata validator for security changes.
- Run root Socket metadata validation after every skill inventory or plugin metadata change.
- Export portable skills through Hermes and update Claude and Cowork classifications in the same pass.
- Keep all repository documentation links portable and all runtime paths discovered rather than machine-coded.

### Forward-test scenarios

1. Choose between host, Apple container, container machine, full Linux VM, macOS VM, and physical Mac for a server-side Swift service that needs Linux compatibility and a local database.
2. Build a minimal Virtualization framework Linux VM configuration, validate it, boot headlessly, and explain each exposed device.
3. Install and run a macOS guest from a supported restore image, then prove a clean SIP-enabled error path without weakening the host.
4. Save and restore a paused compatible VM, then reject an incompatible configuration instead of describing the state file as a portable snapshot.
5. Use `container` 1.x for a disposable OCI service and `container machine` for a persistent systemd-based development environment; show why their mount and lifecycle policies differ.
6. Attempt a nested-virtualization workflow on a supported and unsupported configuration, preserving the exact host, kernel, and capability evidence.
7. Prepare an offline Linux analysis lab with no host home mount, clipboard, agent socket, credentials, or network, then verify evidence export and teardown.
8. Prepare a macOS analysis guest for a benign persistence fixture and distinguish guest evidence from host evidence.
9. Reject a Linux container as proof of macOS Gatekeeper, TCC, XProtect, LaunchServices, or native persistence behavior.
10. Escalate a hardware-, recoveryOS-, Secure Enclave-, or anti-VM-dependent question to a spare physical Mac with the unresolved fidelity gap stated plainly.

Do not run untrusted payloads as forward-test fixtures. Use locally authored benign fixtures or public redistributable test artifacts, and obtain approval before starting visible VM apps, installing Apple `container`, downloading large restore images, creating large VM disks, or launching resource-intensive guests.

## Documentation And Release Impact

The planning slice changes only this maintainer plan and `ROADMAP.md`. It does not change the shipped skill inventory, plugin manifests, marketplace metadata, compatibility exports, or README inventory.

Implementation should land in coherent phases:

1. selection record, router, and Virtualization framework foundation
2. Apple `container` 1.0 expansion and Linux development VM workflow
3. macOS development VM workflow
4. disposable security-lab workflow and security-owner alignment

Each phase should update its owning plugin skill metadata, tests, references, Hermes export, Claude and Cowork compatibility record, root architecture metadata, README inventory text when user-visible coverage changes, and `ROADMAP.md`. A phase that adds only portable guidance needs no MCP server or native host plugin.

## Explicit Non-Goals

- no new aggregate virtualization plugin
- no VM, container, kernel, init filesystem, restore image, malware sample, or tool database bundled in Socket
- no automatic Apple `container`, Lima, Colima, Tart, UTM, Docker, VMware, Parallels, or OrbStack installation
- no privileged helper, daemon, launch agent, guest agent, remote lab service, or credential broker
- no claim that Apple `container` runs macOS containers
- no claim that a macOS VM faithfully reproduces every hardware, recoveryOS, Secure Enclave, anti-VM, or device behavior
- no claim that saved machine state is equivalent to a complete disk snapshot or portable VM clone
- no automatic execution of suspicious content
- no weakening of host SIP, Gatekeeper, XProtect, TCC, App Sandbox, or other platform protections to make a lab easier to use
