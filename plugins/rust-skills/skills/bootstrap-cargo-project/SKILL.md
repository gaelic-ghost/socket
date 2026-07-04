---
name: bootstrap-cargo-project
description: Bootstrap or guide a reproducible Rust Cargo project with explicit package or workspace shape, cargo new or cargo init usage, edition and MSRV checks, rust-toolchain handling, test layout, and initial validation commands. Use after the Rust project shape is settled or when adding a new Cargo package to an existing repository.
license: Apache-2.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: rust-bootstrap
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(cargo:*) Bash(rustc:*) Bash(rustup:*)
---

# Bootstrap Cargo Project

## Purpose

Create or guide a reproducible Rust project scaffold without hiding important Cargo, edition, MSRV, or workspace decisions.

The user should leave with a clear package or workspace layout and validation commands that prove the scaffold works.

## Source Check

Use repo-local Rust files, checked-out dependency sources, Dash MCP or Dash HTTP for installed Rust docsets, and then official Rust documentation when Dash/local coverage is missing or stale:

- [The Cargo Book](https://doc.rust-lang.org/cargo/)
- [`cargo new`](https://doc.rust-lang.org/cargo/commands/cargo-new.html)
- [`cargo init`](https://doc.rust-lang.org/cargo/commands/cargo-init.html)
- [Cargo package layout](https://doc.rust-lang.org/cargo/guide/project-layout.html)
- [The rustup book](https://rust-lang.github.io/rustup/)
- [Rust editions](https://doc.rust-lang.org/edition-guide/editions/)

Cargo currently defaults new packages to the current Rust edition documented by Cargo. Do not hard-code an older edition in new scaffolds unless the repository compatibility policy calls for it.

## Required Inputs

- target path
- package or workspace name
- project shape
- binary, library, or workspace expectation
- edition expectation
- MSRV expectation
- test expectation
- toolchain pinning expectation
- git initialization or commit expectation

If the user has not selected a package or workspace shape, use `rust:choose-project-shape` first.

## Guidance Workflow

1. Inspect the target:
   - existing files
   - git state
   - `Cargo.toml`
   - `Cargo.lock`
   - `rust-toolchain.toml` or `rust-toolchain`
   - `.cargo/config.toml`
   - CI workflows
2. Confirm the project shape and target path.
3. Choose Cargo creation command:
   - use `cargo new` for a new package directory
   - use `cargo init` for an existing directory
   - use `--bin` for executable packages
   - use `--lib` for library packages
   - use `--vcs none` when inside an existing repository
4. Choose edition and MSRV behavior:
   - preserve existing edition in established repos
   - use Cargo's current default for new standalone packages unless the user asks for a specific edition
   - add `rust-toolchain.toml` only when reproducibility or contributor setup needs it
   - do not invent an MSRV without a repository or user decision
5. Add test layout:
   - unit tests near implementation for private behavior
   - `tests/` for integration tests that use the crate externally
   - doctests when public examples should compile
6. Run validation appropriate to the scaffold.
7. Report generated paths and exact commands.

## Command Recipes

Binary package:

```bash
cargo new my-tool --bin
cd my-tool
cargo test
```

Library package:

```bash
cargo new my-library --lib
cd my-library
cargo test
```

Package inside an existing Git repository:

```bash
cargo new crates/my-crate --lib --vcs none
cargo test -p my-crate
```

Existing directory:

```bash
cargo init --lib --vcs none
cargo test
```

Minimal workspace root:

```toml
[workspace]
resolver = "3"
members = [
    "crates/my-crate",
]
```

Check the resolver against the repository's edition and Cargo policy before adding it.

## Validation

Prefer the smallest validation that proves the scaffold:

```bash
cargo fmt --check
cargo clippy --all-targets --all-features
cargo test
```

Use `cargo build` when tests are intentionally absent. Use `cargo package` only for publishable crate surfaces.

## Output Shape

Return:

1. `Created or planned layout`: package, crate targets, workspace members, tests, and examples.
2. `Cargo commands`: exact commands run or recommended.
3. `Compatibility behavior`: edition, MSRV, toolchain, and feature constraints.
4. `Validation`: format, lint, build, test, or package results.
5. `Next skill`: implementation, testing, or tooling handoff.

## Guardrails

- Do not scaffold into a non-empty directory without checking the user's intent.
- Do not initialize nested Git repositories inside an existing repository unless the user explicitly asks for that.
- Do not add `rust-toolchain.toml` or pin nightly without a concrete reproducibility reason.
- Do not add dependencies before the project shape and validation path are clear.
- Do not commit generated files unless the user asks for a commit or the active repo workflow calls for one.
