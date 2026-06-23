---
name: docker-workflow
description: Plan, build, test, and diagnose Docker image and Compose workflows for server-side Swift packages, including multi-stage Dockerfiles, Linux runtime concerns, environment configuration, image validation, and deployment handoffs.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Docker, Dockerfile, Compose, SwiftPM, Vapor, Hummingbird, and server-side Swift services on macOS or Linux.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-docker
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(docker:*) Bash(curl:*)
---

# Docker Workflow

## Purpose

Build, modify, test, or diagnose Docker support for a server-side Swift service.

The practical decision is which Swift executable becomes the container entry point, which Linux base image builds it, which slimmer runtime image ships it, how environment reaches the service, how local dependencies run through Compose, and which command proves the image starts and answers the expected service surface.

## When To Use

- Use this skill when adding or changing a `Dockerfile`, `.dockerignore`, `compose.yaml`, `docker-compose.yml`, image build command, container entry point, local database service, or container runtime configuration for a server-side Swift package.
- Use this skill when diagnosing `docker build`, `docker run`, `docker compose`, Linux dependency, architecture, permissions, port binding, environment, or image-size problems in a Swift service.
- Use this skill when preparing a Vapor or Hummingbird service for a generic Docker-compatible runtime, registry, CI image build, or hosted Linux deployment.
- Use this skill when deciding whether Docker belongs in the current change or should stay a deployment handoff.
- Use `bootstrap-vapor-service` or `bootstrap-hummingbird-service` instead when the Docker work is the CLI-generated Dockerfile, CLI-generated Compose file, or default local PostgreSQL Compose surface for a fresh service.
- Do not use this skill for normal Vapor routes, Hummingbird routes, persistence models, OpenAPI contracts, or SwiftPM package work unless container behavior is the reason for the change.
- Do not use this skill for Apple's `container` CLI or Containerization Swift APIs unless the task is a comparison with Docker. Use `apple-containerization-workflow` for Apple Containerization work.

## Source Check

Use repo-local Docker files, checked-out dependency sources, Dash MCP or Dash HTTP for installed Docker docsets, and then official docs when Dash/local coverage is missing or stale. Check one of those source-specific paths before claiming Docker behavior:

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Docker build best practices](https://docs.docker.com/build/building/best-practices/)
- [Docker multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Docker BuildKit documentation](https://docs.docker.com/build/buildkit/)
- [Swift Docker image repository](https://github.com/swiftlang/swift-docker)
- [Swift official Docker images on Docker Hub](https://hub.docker.com/_/swift)

Use Vapor, Hummingbird, SwiftPM, or Linux distribution documentation when the container work depends on framework commands, package targets, runtime libraries, or OS packages.

Use Fly.io documentation and `fly-io-deployment-workflow` when Docker image work is being prepared for Fly-specific `fly.toml`, `fly launch`, `fly deploy`, Fly secrets, Fly process groups, Fly health checks, or Fly Postgres attachment.

## Planning Workflow

1. Inspect project shape:
   - `Package.swift`
   - executable target name and `swift run` command
   - Vapor, Hummingbird, OpenAPI, persistence, migration, or background-service entry points
   - existing `Dockerfile`, `.dockerignore`, Compose files, deployment files, and CI image-build steps
   - environment-variable names, secrets handling, ports, volumes, health checks, and database services
2. Identify the container job:
   - production image
   - local development image
   - CI build or test image
   - Compose stack for local service dependencies
   - registry publish handoff
   - diagnostic reproduction for Linux-only behavior
3. Choose the smallest fitting container surface:
   - Dockerfile only when the service just needs an image
   - Compose when multiple local services must start together
   - fresh Vapor and Hummingbird services preserve CLI-generated Docker files and get Compose-local PostgreSQL from their bootstrap skills
   - separate debug or test target only when it proves a real failure mode
   - no Docker change when SwiftPM local validation is enough for the user's task
4. Prefer a multi-stage Dockerfile for production images.
5. Keep build inputs explicit and cache-friendly.
6. Keep secrets out of images, layers, build args, logs, and committed Compose files.
7. Check runtime safety before treating an image as production-ready.
8. Validate the image with the narrowest useful build, test, run, or HTTP check.

## Dockerfile Shape

For production server-side Swift images:

- use a Swift builder image that matches the package's supported Swift toolchain and Linux target
- copy package manifests before source files when that fits the repository, so dependency resolution can reuse build cache
- build the executable in release mode
- copy only the built executable, needed resources, and required runtime assets into the final image
- use a runtime base image that matches the Swift runtime and Linux distribution requirements
- set `WORKDIR` explicitly
- run as a non-root user when the service does not need privileged container behavior
- expose only the documented service port when `EXPOSE` is useful for readers or tooling
- define `ENTRYPOINT` as the server executable when the image should run like the service command
- use `CMD` only for default arguments that operators may override
- keep `SIGTERM` and graceful shutdown behavior visible when the service, framework, or deployment target depends on clean shutdown
- choose platform and architecture deliberately when building on Apple silicon for Linux deployment, CI, or multi-architecture registries

Use named build stages such as `build`, `test`, `debug`, and `runtime` when the image has more than one stage. Named stages make later `COPY --from=<stage>` instructions easier to maintain when the Dockerfile changes.

Do not leave build tools, package-manager caches, source checkout credentials, test fixtures, or debugging tools in the production runtime image unless the runtime truly needs them.

## Build Context And Runtime Assets

Check `.dockerignore` as part of every Dockerfile change. It should normally exclude build output, source-control internals, editor state, local secrets, and host-only test artifacts that do not belong in image layers.

For Swift services, inspect whether the executable needs runtime assets beyond the compiled binary:

- package resources declared through SwiftPM
- Vapor public files, Leaf templates, migrations, or command resources
- Hummingbird static files, certificates, fixture data, or generated assets
- OpenAPI documents or generated support files that the service reads at runtime
- configuration examples that are safe to ship versus ignored local overrides

If a resource is needed at runtime, copy it intentionally into the final image and name why it is required. If it is only for tests, local development, or docs, keep it out of the production runtime stage.

## Runtime Safety

Before calling an image production-ready, check:

- non-root execution, file ownership, and writable directories used by the app
- graceful shutdown behavior for `SIGTERM` and the hosting platform's stop timeout
- health check shape when the deployment target expects container health reporting
- explicit port binding and host binding, especially when a framework defaults to localhost
- whether debug flags, package caches, shell history, test data, or diagnostic tools survived into the runtime image
- whether the chosen platform and architecture match the deployment target, especially when building on Apple silicon

Do not add a health check endpoint just to satisfy Docker if the service does not have a real readiness or liveness signal. Hand route design to the Vapor or Hummingbird workflow when the application needs a new health route.

## Compose Shape

Use Compose when local development needs multiple services, such as a Swift app plus Postgres, Redis, or another dependency.

For fresh Vapor and Hummingbird services, CLI-generated Docker files and Compose-local PostgreSQL are part of the bootstrap baseline. Keep that baseline in `bootstrap-vapor-service` and `bootstrap-hummingbird-service`; use this skill when the generated container stack needs to change beyond the default local database or when registry publishing, CI image builds, deployment runtime, or nonstandard image hardening needs design.

When adding or editing Compose files:

- name the Swift service, dependency services, ports, volumes, networks, and health checks plainly
- keep local-only credentials fake, documented, and scoped to development
- use environment variables or an ignored local override for real secrets
- avoid mounting the whole host checkout into a production-like runtime image unless the task is explicitly live development
- ensure the app's configured host and port match the container and published port behavior
- include database migration timing only when the service already has a documented migration command or the user asked for that scope

Do not make Compose the production deployment model unless the repository already treats it that way.

## Vapor And Hummingbird Handoffs

For Vapor services:

- confirm the executable name, often `App`
- confirm whether the image should run `serve`, `migrate`, or a custom command
- use `vapor-server-workflow` for route, middleware, command, Fluent migration, and Vapor environment behavior

For Hummingbird services:

- confirm the executable and any command-line options exposed by the package
- confirm host, port, logging, and service-lifecycle configuration
- use `hummingbird-server-workflow` for router, middleware, request context, application lifecycle, and framework testing behavior

Use `persistence-workflow` when Compose or runtime configuration adds a database service, migration timing, seed data, or test database setup.

## Testing And Validation

Prefer this order:

1. Validate SwiftPM behavior outside Docker first when the failure is not Linux-specific.
2. Build the image with the repository's documented tag.
3. Build a specific target such as `test`, `debug`, or `runtime` when the Dockerfile provides one.
4. Run the container with explicit port and environment values.
5. Inspect the final image enough to catch root-user, missing-resource, entry-point, or accidental-debug-tool problems when production readiness is in scope.
6. Use `curl` against the running service only when runtime HTTP behavior matters.
7. Use `docker compose up --build` only when multiple services are part of the behavior being proven.

When a Docker command fails, report the exact image, stage, instruction, service, port, environment variable, or mounted path involved. Include the likely cause, such as a Swift toolchain mismatch, missing Linux package, wrong executable name, wrong working directory, missing resource copy, architecture mismatch, bad secret path, or service dependency not ready.

## Output Shape

Return:

1. `Container shape`: Dockerfile path, build stages, executable target, runtime base, ports, Compose services, and configuration source.
2. `Docs used`: Docker, Swift Docker image, SwiftPM, Vapor, Hummingbird, or persistence docs consulted.
3. `Command path`: exact Docker, Compose, SwiftPM, run, migration, or HTTP commands run or recommended.
4. `Runtime behavior`: entry point, arguments, environment, ports, volumes, dependency services, health checks, and deployment handoffs.
5. `Validation`: build, test, image run, Compose run, logs, or HTTP check results.
6. `Handoffs`: Vapor, Hummingbird, persistence, OpenAPI, CI, registry publish, cloud deployment, or Apple Containerization follow-up when the task crosses this skill's boundary.

## Guardrails

- Do not commit secrets, registry credentials, local `.env` files, machine-local paths, or private image references.
- Do not bake credentials into `ARG`, `ENV`, image layers, build logs, or checked-in Compose defaults.
- Do not claim Docker, Compose, BuildKit, or Swift image behavior from memory when current official docs can be checked.
- Do not add Docker files to an ordinary route or model change unless deployment scope was requested.
- Do not leave duplicate production and development Dockerfiles when one multi-stage Dockerfile plus Compose overrides would be clearer.
- Do not treat Docker Desktop as the only possible Docker-compatible runtime unless the user's machine or repository explicitly requires it.
- Do not ship a production runtime image as root, with missing SwiftPM resources, or with avoidable debug tooling unless the repository documents that requirement.
