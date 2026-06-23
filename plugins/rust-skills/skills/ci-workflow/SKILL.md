---
name: ci-workflow
description: Design, inspect, and align Rust CI workflows with local Cargo validation, including cargo fmt, cargo clippy, cargo test, cargo build, cargo doc, cargo package, workspace package selection, feature matrices, MSRV checks, rustup toolchain setup, Clippy warnings-as-errors policy, caches, artifacts, and GitHub Actions-style automation.
license: PolyForm-Noncommercial-1.0.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: rust-ci
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(cargo:*) Bash(rustc:*) Bash(rustup:*)
---

# Rust CI Workflow

## Purpose

Align Rust CI with the validation that actually protects the project.

The practical goal is to make CI prove the same behavior maintainers care about locally: formatting, linting, build, tests, docs, package readiness, MSRV, and feature or workspace matrices where those are real compatibility surfaces.

## Source Check

Use repo-local files, checked-out dependency sources, Dash MCP or Dash HTTP for installed docsets, and then official project documentation when Dash/local coverage is missing or stale:

- [Cargo continuous integration guide](https://doc.rust-lang.org/cargo/guide/continuous-integration.html)
- [Cargo workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html)
- [Cargo features reference](https://doc.rust-lang.org/cargo/reference/features.html)
- [`cargo test`](https://doc.rust-lang.org/cargo/commands/cargo-test.html)
- [`cargo package`](https://doc.rust-lang.org/cargo/commands/cargo-package.html)
- [Clippy CI documentation](https://doc.rust-lang.org/clippy/continuous_integration/)
- [The rustup book](https://rust-lang.github.io/rustup/)

Translate CI advice into the exact workflow jobs, commands, package selection, feature selection, and failure policy that match the repository.

## Repository Inspection

Inspect:

- `.github/workflows/`
- `Cargo.toml`
- workspace root `Cargo.toml`
- `Cargo.lock`
- `rust-toolchain.toml` or `rust-toolchain`
- `rustfmt.toml` or `.rustfmt.toml`
- `clippy.toml`
- README, CONTRIBUTING, AGENTS, or release docs
- Makefile, justfile, xtask, or repo scripts

## CI Shape Decisions

Pick jobs by the behavior they protect:

- format: `cargo fmt --check`
- lint: `cargo clippy --all-targets --all-features -- -D warnings`
- test: `cargo test --all-targets --all-features`
- build: `cargo build` when compile coverage is needed separately
- docs: `cargo doc --no-deps` when public docs matter
- package: `cargo package --dry-run` for publishable crates
- MSRV: run selected checks on the declared minimum supported Rust version

Do not add every job by default. Choose the smallest CI matrix that protects the repo's real support promise.

## Toolchain Setup

Prefer the repo's existing setup. If adding setup from scratch, install the channel and components the commands require:

```bash
rustup toolchain install stable --profile minimal --component rustfmt --component clippy
```

Use `rust-toolchain.toml` when local and CI contributors should share the same channel/components. Do not pin nightly unless the project truly depends on nightly behavior.

## Workspace And Feature Matrices

Use package selection intentionally:

```bash
cargo test -p package-name
cargo test --workspace
```

Use feature matrices only when features are part of the public compatibility surface:

```bash
cargo test -p package-name --no-default-features
cargo test -p package-name --all-features
```

If the project has many feature combinations, use a documented helper such as `cargo hack` only when the repo already uses it or the added dependency is justified.

## Warnings-As-Errors Policy

Clippy's CI guidance recommends `-Dwarnings`, but apply that deliberately.

Good default for maintained crates:

```bash
cargo clippy --all-targets --all-features -- -D warnings
```

Avoid turning all compiler warnings into hard failures unless the repo wants that stricter contract. If CI is newly adopting warnings-as-errors, call out the maintenance cost.

## Cache And Artifact Boundaries

Use caches to speed CI, not to define correctness. CI should still pass from a cold cache.

Only upload artifacts when users or maintainers need them, such as release binaries, generated docs, coverage, or package tarballs.

## Output Shape

Return:

1. `CI intent`: what the workflow is meant to protect.
2. `Local parity`: local commands and matching CI commands.
3. `Toolchain`: channel, components, rustup or rust-toolchain behavior, and MSRV checks.
4. `Matrix`: workspace packages, features, targets, OSes, and whether each is necessary.
5. `Changes`: workflow files or scripts changed.
6. `Validation`: commands run locally and any CI checks that still need remote confirmation.

## Guardrails

- Do not add broad CI matrices without naming the compatibility promise they protect.
- Do not make nightly a required lane unless the repo depends on nightly.
- Do not hide local validation behind CI-only scripts.
- Do not add warnings-as-errors casually to unstable or noisy repos.
- Do not treat cache hits as proof that CI is correct.
