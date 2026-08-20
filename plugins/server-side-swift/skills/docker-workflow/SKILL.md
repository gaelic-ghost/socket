---
name: docker-workflow
description: Author and diagnose Dockerfile and OCI runtime definitions for server-side Swift while GitHub Actions exclusively builds, tests, publishes, and deploys Linux images.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Dockerfile, OCI, SwiftPM, Vapor, Hummingbird, and GitHub Actions.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-docker
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(curl:*)
---

# Docker Workflow

## Purpose

Own the checked-in Dockerfile, `.dockerignore`, Linux runtime assets, and OCI
contract for a Swift service. On Gale-owned product repositories this is a
definition-only local workflow: GitHub Actions exclusively builds Linux images,
runs image smoke tests, publishes immutable identities, and supplies deployment
artifacts.

## When To Use

- Use this skill to author or diagnose Dockerfile stages, entrypoints, runtime
  libraries, resources, non-root execution, ports, and GitHub image jobs.
- Inspect GitHub Actions logs and artifacts for Linux failures. On the Mac, run
  native Swift checks and edit definitions only.
- Use `cloud-deployment-skills:dockerized-service-release-deployment-workflow`
  for the build-once, digest-recorded, environment-gated release contract.
- Do not offer Compose, Colima, Docker Desktop, Apple containers, a container
  machine, or a Linux VM for product development or image validation.
- Do not use this skill for ordinary route, model, persistence, or SwiftPM work.

## Source Check

Use repo-local definitions and official sources before making container claims:

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Docker build best practices](https://docs.docker.com/build/building/best-practices/)
- [Docker multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [Swift Docker images](https://github.com/swiftlang/swift-docker)
- [GitHub Actions publishing Docker images](https://docs.github.com/actions/publishing-packages/publishing-docker-images)

The Docker Compose reference is not part of the Gale-product path.

## Single-Path Workflow

1. Inspect `Package.swift`, the executable target, `Dockerfile`,
   `.dockerignore`, runtime resources, port/binding, graceful shutdown, and the
   owning GitHub workflow.
2. Confirm native behavior first with the nearest package's `swift build` and
   `swift test` when the issue is not Linux-specific.
3. Use a named multi-stage Dockerfile: match the supported Swift/Linux builder,
   build release output, and copy only the executable, required resources, and
   runtime libraries into the final image.
4. Run as a non-root user where possible; set `WORKDIR`, entrypoint, port, file
   ownership, writable paths, and `SIGTERM` behavior explicitly.
5. Keep `.dockerignore` free of source-control state, native build output,
   secrets, editor state, and host-only artifacts.
6. In GitHub Actions, build once from a clean checkout, run the image smoke test
   there, publish it, resolve its registry digest, and record that digest in the
   release manifest. Never rebuild during deployment.
7. Use protected GitHub environments for live-test and production. Deploy the
   exact recorded digest, verify health, and retain the previous digest as the
   rollback identity.
8. Diagnose failures from the exact GitHub job, image digest, stage,
   instruction, executable, resource, architecture, port, or health check.

## Inputs

- repository and service root
- executable target and runtime command
- Dockerfile and `.dockerignore` paths
- required runtime resources, port, environment names, and health signal
- GitHub image workflow, registry, and immutable artifact contract

## Outputs

- Dockerfile/runtime definition and explicit runtime assets
- GitHub-only build, smoke-test, publish, and deployment ownership
- immutable digest identity, health evidence, and rollback identity
- focused Vapor, Hummingbird, persistence, or cloud-deployment handoff

## Guards and Stop Conditions

- Do not execute or recommend local `docker build`, `docker run`, image
  inspection, Compose, Colima, container-machine, or VM commands for a
  Gale-owned product.
- Do not add or preserve Compose as a local dependency path; use native
  Homebrew services.
- Do not use a mutable tag as deployment identity or rebuild source in a deploy
  job.
- Do not put secrets in build arguments, environment layers, logs, definitions,
  or committed local configuration.
- Stop when the GitHub job cannot prove the final image digest, smoke test, or
  runtime asset set.

## Fallbacks and Handoffs

- Use `hummingbird-server-workflow` or `vapor-server-workflow` for application
  lifecycle, binding, routes, and readiness behavior.
- Use `persistence-workflow` for schema, migrations, and native Homebrew-backed
  local dependencies.
- Use `cloud-deployment-skills:dockerized-service-release-deployment-workflow`
  for immutable GitHub release and deployment orchestration.
- For a provider such as Fly.io, hand over only after GitHub has produced and
  recorded the exact image identity.

## Customization

This workflow has no alternate local/runtime mode. Repository-specific ports,
entrypoints, resources, registries, and health signals stay in checked-in
Dockerfile and GitHub workflow sources.

## References

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Swift Docker images](https://github.com/swiftlang/swift-docker)
- [GitHub Actions publishing Docker images](https://docs.github.com/actions/publishing-packages/publishing-docker-images)
