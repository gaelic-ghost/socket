---
name: package-workflow
description: Prepare and validate Rust Cargo package surfaces, including Cargo.toml metadata, rust-version and MSRV policy, license/readme/repository fields, include and exclude rules, path dependency restrictions, Cargo.lock policy, cargo package dry runs, and publish versus no-publish decisions. Use for publishable crates, package metadata cleanup, crates.io readiness, or release-adjacent Rust package checks.
license: Apache-2.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: rust-packaging
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(cargo:*) Bash(rustc:*) Bash(rustup:*)
---

# Rust Package Workflow

## Purpose

Prepare a Cargo package surface so it is honest, fetchable, and ready for the user's intended distribution path.

The practical goal is to catch package metadata drift, local-only dependencies, missing compatibility policy, and accidental publishing before a release or publication step.

## Source Check

Use repo-local Cargo files, checked-out dependency sources, Dash MCP or Dash HTTP for installed Cargo docsets, and then official Cargo documentation when Dash/local coverage is missing or stale:

- [Cargo manifest format](https://doc.rust-lang.org/cargo/reference/manifest.html)
- [`cargo package`](https://doc.rust-lang.org/cargo/commands/cargo-package.html)
- [`cargo publish`](https://doc.rust-lang.org/cargo/commands/cargo-publish.html)
- [Cargo workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html)
- [Cargo features reference](https://doc.rust-lang.org/cargo/reference/features.html)
- [Cargo SemVer compatibility](https://doc.rust-lang.org/cargo/reference/semver.html)

Translate packaging rules into the exact package field, dependency, command, or release decision they affect.

## Repository Inspection

Inspect:

- `Cargo.toml`
- `Cargo.lock`
- workspace root `Cargo.toml`
- `README.md`
- `LICENSE` or `LICENSE-*`
- package docs and examples
- `.cargo/config.toml`
- CI workflows
- git status and ignored files if package inclusion matters

## Manifest Checks

For publishable crates, check the relevant `[package]` fields:

- `name`
- `version`
- `edition`
- `rust-version`
- `description`
- `license` or `license-file`
- `repository`
- `homepage` or `documentation` when appropriate
- `readme`
- `keywords`
- `categories`
- `include` or `exclude` when package contents need curation
- `publish` when publication should be restricted or disabled

Do not invent metadata. If a package is not meant to publish, prefer an explicit `publish = false` or equivalent repo policy instead of polishing crates.io metadata for a private crate.

## Dependency Checks

Cargo package validation is especially useful because publishable packages cannot rely on local-only dependency paths unless version metadata makes the registry dependency usable.

Check for:

- path dependencies
- git dependencies that cannot be fetched by intended users
- optional dependencies tied to features
- dev-dependencies that are only needed for tests/examples
- workspace-inherited dependency versions
- unpublished sibling crates

Do not commit machine-local dependency paths in public or shared packages.

## Lockfile Policy

Preserve the repo's existing lockfile policy.

General guidance:

- commit `Cargo.lock` for binaries, applications, examples that must reproduce, and most workspaces with executable surfaces
- library-only crates may choose not to commit `Cargo.lock`, but follow existing repo policy
- do not delete or regenerate `Cargo.lock` as package cleanup unless dependency resolution is part of the task

## Validation Commands

Use dry-run package validation before publishing or release-adjacent package changes:

```bash
cargo package --dry-run
```

Package one workspace member:

```bash
cargo package -p package-name --dry-run
```

Validate publish-facing behavior with selected features when needed:

```bash
cargo package -p package-name --all-features --dry-run
```

Run normal validation before or alongside package checks:

```bash
cargo test -p package-name
cargo clippy -p package-name --all-targets --all-features
cargo fmt --check
```

Do not run `cargo publish` unless the user explicitly asks to publish and the repository release process is ready.

## Output Shape

Return:

1. `Package intent`: publishable crate, private crate, binary distribution, workspace member, or no-publish package.
2. `Manifest state`: metadata, license, repository, readme, rust-version, publish, include, and exclude findings.
3. `Dependency state`: registry, git, path, optional, dev, and workspace dependency concerns.
4. `Lockfile policy`: observed policy and whether it changed.
5. `Validation`: exact package, test, lint, and format commands run or skipped.
6. `Release impact`: whether publishing, SemVer, MSRV, or downstream compatibility is affected.

## Guardrails

- Do not publish by default.
- Do not invent crates.io metadata for private crates.
- Do not hide local path dependencies behind package docs.
- Do not raise MSRV or change SemVer meaning silently.
- Do not remove lockfiles without checking repo policy and executable surfaces.
