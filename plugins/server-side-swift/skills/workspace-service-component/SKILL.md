---
name: workspace-service-component
description: Add or align a Hummingbird or Vapor executable under Services/ in an existing canonical Xcode workspace. Use only behind bootstrap-xcode-workspace add-component; local development is native macOS with Homebrew services, while Linux artifacts and deployments run in GitHub Actions.
license: Apache-2.0
compatibility: macOS workspace authoring with SwiftPM, XcodeGen, Homebrew services, Hummingbird hb, Vapor Toolbox, and GitHub Actions.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-workspace-component
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(brew:*) Bash(swift:*) Bash(hb:*) Bash(vapor:*) Bash(xcodegen:*)
---

# Workspace Service Component

## Purpose

Own the framework-specific adapter behind the single public `bootstrap-xcode-workspace --operation add-component --component-kind service` entrypoint. A service is a SwiftPM executable under `Services/`; it does not become a standalone repository and does not require converting the product later.

## Contract

1. Require an existing canonical root workspace with `project.yml` and `Services/services-shared.yml`.
2. Generate Hummingbird with `hb init` or Vapor with `vapor new`; preserve framework-owned Swift package and application structure.
3. Remove generated local Compose files and nested Git metadata. Preserve a Dockerfile only as GitHub Actions cloud-build input; never build it locally.
4. Add the package to `Services/services-shared.yml` so the root XcodeGen project and workspace expose it.
5. Install a native local dependency check that discovers the repository's one installed PostgreSQL formula or uses its explicit `SERVICE_POSTGRES_FORMULA` override, then requires it to be running through `brew services`. Missing or ambiguous prerequisites block with explicit install/start guidance; the workflow never installs them or starts a container fallback.
6. Install GitHub Actions as the only Linux artifact, live-test deployment, and production deployment surface. Deployment jobs use protected GitHub environments and repository-owned deploy scripts.
7. Validate with native `swift build` and `swift test` unless skipped.

## Guards

- Do not create a standalone server repository.
- Do not add Docker Compose, Colima, Lima, Docker Desktop, QEMU, Apple container machines, or Linux VMs to local development.
- Do not build Linux archives or OCI images on the Mac.
- Do not retain the retired standalone Hummingbird/Vapor bootstrap or guidance-sync paths as wrappers.
- Use Soto as the default AWS SDK when service code needs AWS; use the official AWS SDK for Swift only for an explicit capability or compatibility requirement.

## References

- [Homebrew PostgreSQL 18 formula](https://formulae.brew.sh/formula/postgresql@18)
- [Hummingbird hb CLI](https://github.com/hummingbird-project/hb)
- [Vapor Toolbox](https://github.com/vapor/toolbox)
