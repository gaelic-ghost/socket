---
name: apple-containerization-workflow
description: Plan, build, test, and diagnose Apple Containerization and apple/container CLI workflows for server-side Swift services on Apple silicon, keeping Apple's container tooling distinct from generic Docker guidance.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Apple's Containerization package, apple/container CLI, OCI images, SwiftPM, Vapor, Hummingbird, and server-side Swift services on Apple silicon Macs.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-apple-containerization
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(container:*) Bash(curl:*)
---

# Apple Containerization Workflow

## SwiftData And SwiftUI Rule

When a task combines SwiftData with SwiftUI, keep SwiftData directly coupled to SwiftUI through Apple's data-driven path: `modelContainer`, environment `modelContext`, `@Query`, SwiftData model objects, and bindings. Do not add repositories, stores, service layers, DTO mirrors, view-model caches, wrapper objects, or other abstraction layers between SwiftData and SwiftUI. If this skill is not the right owner for SwiftData-backed SwiftUI work, hand off to `apple-dev-skills:swiftui-app-architecture-workflow` instead of inventing an intermediate data layer.

## Purpose

Build, run, test, or diagnose server-side Swift container work that specifically uses Apple's Containerization project or the `apple/container` command-line tool.

The practical decision is whether the task needs Apple's macOS-native container runtime, the lower-level Containerization Swift APIs, or ordinary Docker-compatible files. This skill keeps those paths separate so Docker deployment guidance does not accidentally become Apple-only runtime guidance.

## When To Use

- Use this skill when a user asks for Apple Containerization, Apple's `container` CLI, Containerization Swift APIs, OCI image work on Apple silicon, or native macOS container runtime behavior.
- Use this skill when diagnosing `container system start`, `container build`, `container run`, image pull or push, registry login, kernel setup, lightweight VM startup, networking, Rosetta, or Apple silicon runtime behavior.
- Use this skill when comparing Apple Containerization to Docker for local server-side Swift development.
- Use this skill when deciding whether a server-side Swift package should add Apple-container-specific docs, tests, or local development guidance.
- Do not use this skill for ordinary Dockerfile, Compose, CI image build, registry publish, or generic Linux deployment work unless the task explicitly asks how it behaves under Apple's tooling. Use `docker-workflow` for generic Docker work.
- Do not use this skill for Apple-platform app, simulator, signing, SwiftUI, or Xcode project work unless the container task is part of a macOS tool that embeds Containerization APIs.

## Source Check

Use current official Apple and project documentation before claiming behavior, because this surface is young and changes quickly:

- [apple/containerization repository](https://github.com/apple/containerization)
- [Containerization API documentation](https://apple.github.io/containerization/documentation/containerization/)
- [apple/container repository](https://github.com/apple/container)
- [apple/container tutorial](https://github.com/apple/container/blob/main/docs/tutorial.md)
- [apple/container technical overview](https://github.com/apple/container/blob/main/docs/technical-overview.md)
- [Apple Open Source Container page](https://opensource.apple.com/projects/container/)
- [Apple Open Source Containerization page](https://opensource.apple.com/projects/containerization/)
- [Virtualization framework documentation](https://developer.apple.com/documentation/virtualization)

Treat documentation on a repository's `main` branch as current-branch documentation. When a user needs release-stable behavior, open the matching release tag and use that version's docs instead.

## Planning Workflow

1. Inspect project shape:
   - `Package.swift`
   - executable target and `swift run` command
   - existing Dockerfile, Compose file, OCI image documentation, or Apple `container` notes
   - Vapor, Hummingbird, OpenAPI, persistence, migration, or background-service entry points
   - port, environment, volume, registry, and architecture assumptions
2. Identify the Apple-container job:
   - run an existing OCI image locally on Apple silicon
   - build an image with Apple's `container` CLI
   - compare `container` behavior with Docker behavior
   - script a local development flow around `container`
   - use Containerization Swift APIs from a macOS tool
   - diagnose kernel, VM, image, network, or registry behavior
3. Confirm the required host:
   - Apple silicon Mac
   - supported macOS version for the selected release
   - installed `container` CLI or package source checkout
   - installed Linux kernel or documented kernel setup path
   - started container system services when the selected command needs them
4. Decide whether the repository needs a committed change:
   - no change when the task is local runtime diagnosis only
   - docs or scripts when the workflow is repeatable for contributors
   - Dockerfile reuse when the image should stay OCI-compatible
   - Swift API integration only when the app's job is to manage containers directly
5. Validate with the narrowest useful `container`, SwiftPM, log, or HTTP check.

## Apple Containerization Versus Docker

Use plain language when choosing between the paths:

- Docker workflow means Dockerfile, Compose, Docker-compatible CI, registries, and generic Linux deployment expectations.
- Apple `container` workflow means Apple's macOS CLI and services for building and running OCI images locally on Apple silicon.
- Containerization Swift API work means writing Swift code against Apple's packages to manage images, registries, filesystems, VMs, or containerized processes.

Prefer Docker guidance when the service needs portable deployment artifacts for Linux hosts, CI, or common container platforms. Prefer Apple Containerization guidance when the user specifically wants Apple's local macOS runtime, lower-level Swift APIs, or a comparison on Apple silicon.

## Capability Probe

Before recommending concrete Apple `container` commands, scripts, or flags, run or request the smallest probe that proves the local tool and docs match the intended workflow:

- identify the installed `container` version or the checked source/release tag
- open the matching release documentation when release-stable behavior matters
- verify the host is an Apple silicon Mac on a supported macOS version
- verify whether the container system service is started, and start it only through the documented command path when needed
- verify kernel setup status through documented prompts, docs, or CLI diagnostics
- inspect `container --help` and the relevant subcommand help before using Docker-like flags
- record whether the task depends on Rosetta, amd64 images, registry credentials, networking, volumes, or published ports

If any probe fails, report the missing capability and stop before adding repo scripts or docs that would encode a workflow the machine cannot run.

## CLI Workflow

When using the `container` CLI:

- verify the installed CLI version and the docs version before changing behavior
- start required services with the documented `container system start` path
- follow documented kernel installation prompts or release-specific kernel setup
- inspect available commands with `container --help` and `container <command> --help`
- keep image names, tags, platform assumptions, and registry credentials explicit
- validate the service with logs, process status, published ports, and HTTP checks when applicable

Do not assume Docker Compose features, Docker Desktop behavior, or Docker CLI flags map directly to Apple's `container` CLI. Check the `container` command's own help and release docs first.

## Swift API Workflow

When using the Containerization Swift package directly:

- verify the package requirements from the current repository or release tag
- inspect the sample or `cctl` executable before writing new API code
- keep API use scoped to the actual job: image management, registry interaction, ext4 filesystem creation, VM runtime, process launch, networking, or Rosetta behavior
- keep Virtualization framework and Apple silicon requirements visible in docs or diagnostics
- add tests around pure Swift decision logic where possible, and keep host-runtime tests explicit because they require supported macOS and Apple silicon

Do not add Containerization package dependencies to an ordinary server-side Swift service just to run the service in a container. That is local runtime tooling, not service business logic.

## Vapor And Hummingbird Handoffs

For Vapor services:

- use `vapor-server-workflow` for app commands, routes, middleware, migrations, and Vapor environment behavior
- confirm whether `container run` should execute the server, a migration command, or a custom Vapor command

For Hummingbird services:

- use `hummingbird-server-workflow` for router, middleware, request context, application lifecycle, and service configuration
- confirm executable arguments, host, port, and logging behavior before encoding a run command

Use `docker-workflow` when the work is mostly Dockerfile, Compose, or portable OCI image authoring. Use `persistence-workflow` when local container work adds a database service, volume, migration timing, or seed data.

## Testing And Validation

Prefer this order:

1. Verify host and tool support with the current `container` CLI or checked release docs.
2. Validate SwiftPM behavior outside the container runtime when the issue is not runtime-specific.
3. Start Apple's container services through the documented command path.
4. Build, pull, or run the image with explicit tags, ports, and environment.
5. Inspect logs or process status from the `container` CLI.
6. Use `curl` against the running service only when HTTP behavior matters.

When a `container` command fails, report the exact command, image, runtime service, kernel state, port, registry, architecture, or API symbol involved. Include the likely cause, such as unsupported macOS, missing kernel setup, service not started, registry auth failure, port mismatch, amd64 emulation mismatch, image entry-point mismatch, or a CLI flag that belongs to Docker rather than Apple's tool.

## Output Shape

Return:

1. `Apple container shape`: CLI or Swift API path, host requirements, image source, executable target, ports, environment, and runtime services.
2. `Docs used`: Apple Containerization, apple/container release docs, Virtualization framework, SwiftPM, Vapor, Hummingbird, Docker, or persistence docs consulted.
3. `Command path`: exact `container`, SwiftPM, run, log, registry, or HTTP commands run or recommended.
4. `Runtime behavior`: system service state, image build or pull behavior, entry point, arguments, environment, ports, volumes, networking, Rosetta, and kernel assumptions.
5. `Validation`: tool version, system start, build, run, logs, HTTP check, or Swift test results.
6. `Handoffs`: Docker, Vapor, Hummingbird, persistence, macOS app integration, CI, registry publish, or deployment follow-up when the task crosses this skill's boundary.

## Guardrails

- Do not claim Apple Containerization behavior from memory when current official docs, GitHub release docs, or local CLI help can be checked.
- Do not assume Apple's `container` CLI is a drop-in replacement for Docker or Compose.
- Do not commit registry credentials, local `.env` files, machine-local paths, kernel artifacts, private images, or local runtime state.
- Do not add Containerization Swift package dependencies to a service unless the service is actually a container-management tool.
- Do not hide Apple silicon, macOS, kernel, Virtualization framework, or Rosetta requirements when they affect whether the workflow can run.
- Do not turn local Apple-container diagnostics into production deployment guidance unless the repository already deploys through that path.
