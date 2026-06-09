---
name: choose-project-shape
description: Choose the right Rust project shape before implementation, including crate type, Cargo package or workspace layout, edition and MSRV checks, validation commands, package boundaries, and documentation updates. Use when a user wants to start, restructure, or extend a Rust project and the binary, library, workspace, CLI, service, proc macro, FFI, embedded, no_std, or maintenance shape is not already settled.
license: PolyForm-Noncommercial-1.0.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: rust-planning
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(cargo:*) Bash(rustc:*) Bash(rustup:*)
---

# Choose Rust Project Shape

## Purpose

Pick the smallest correct Rust project shape before code changes begin.

The practical decision is what kind of crate or workspace the user needs, where package boundaries should sit, whether MSRV or edition policy already exists, and which validation commands should prove the work.

## Source Check

Use official Rust documentation first before making claims about Rust, Cargo, rustup, formatting, linting, testing, or package behavior:

- [Rust documentation](https://doc.rust-lang.org/)
- [The Cargo Book](https://doc.rust-lang.org/cargo/)
- [`cargo new`](https://doc.rust-lang.org/cargo/commands/cargo-new.html)
- [Cargo tests guide](https://doc.rust-lang.org/cargo/guide/tests.html)
- [Cargo continuous integration guide](https://doc.rust-lang.org/cargo/guide/continuous-integration.html)
- [The rustup book](https://rust-lang.github.io/rustup/)
- [Clippy documentation](https://doc.rust-lang.org/clippy/)

Translate any documentation rule into the concrete repository decision it changes.

## Classification Workflow

1. Inspect the repository shape:
   - `Cargo.toml`
   - `Cargo.lock`
   - `rust-toolchain.toml` or `rust-toolchain`
   - `.cargo/config.toml`
   - `rustfmt.toml` or `.rustfmt.toml`
   - `clippy.toml`
   - `src/main.rs`
   - `src/lib.rs`
   - `tests/`
   - `examples/`
   - `benches/`
   - `crates/`
   - existing CI commands
2. Identify the user-visible job:
   - binary crate
   - library crate
   - CLI tool
   - service or daemon
   - Cargo workspace
   - proc macro
   - FFI boundary
   - embedded or `no_std` target
   - package maintenance or upgrade pass
3. Choose the project boundary intentionally:
   - use one package for a small app or library
   - use a workspace when multiple packages need shared dependency and validation behavior
   - split a library from a binary when reusable API and executable concerns are meaningfully separate
   - split proc macros into their own crate
   - keep FFI boundaries explicit and narrow
4. Check compatibility policy:
   - preserve existing Rust edition unless the task is an edition migration
   - preserve existing MSRV unless the user approves changing it
   - read CI before recommending toolchain or feature matrix changes
5. Choose validation:
   - `cargo fmt --check` for formatting-sensitive changes
   - `cargo clippy --all-targets --all-features` when lint coverage matters
   - `cargo test` for behavior
   - `cargo build` for compile checks without tests
   - `cargo package` for publishable crate surfaces

## Recommendations

### Binary Crate Or CLI

Use a single binary package for small command-line tools. Add a library target only when the CLI has reusable logic that tests or downstream callers should exercise directly.

Handoff:

- `rust:bootstrap-cargo-project` for new project creation
- `rust:testing-workflow` for behavior coverage
- `rust:tooling-style-workflow` for formatting, linting, and toolchain alignment

### Library Crate

Use a library package when the primary output is an API consumed by tests, examples, binaries, or downstream users. Keep public API surface small and document package validation if publishing is expected.

Handoff:

- `rust:testing-workflow` for unit, integration, and doctest coverage
- `rust:package-workflow` when crate metadata or publication matters

### Cargo Workspace

Use a workspace only when more than one package needs shared dependency resolution, coordinated tests, or separate crate boundaries.

Good reasons include a library plus CLI package, a proc macro companion crate, integration-test support crates, or multiple crates that ship together. Avoid a workspace when a module split inside one crate would be enough.

### Proc Macro

Use a dedicated proc macro crate. Keep parsing and code generation tests explicit because failures are often easier to understand with fixture-style coverage.

### FFI, Embedded, Or `no_std`

Treat these as explicit constraint-driven shapes. Check existing target, build script, linker, feature, and CI configuration before changing layout.

## Output Shape

Return:

1. `Chosen shape`: binary crate, library crate, CLI, service, workspace, proc macro, FFI, embedded or `no_std`, or maintenance pass.
2. `Project boundary`: package, crate, workspace member, or module split.
3. `Compatibility policy`: edition, MSRV, toolchain, and feature constraints.
4. `Validation path`: exact format, lint, build, test, or package commands.
5. `Documentation updates`: README, roadmap, package notes, or repo-local guidance.
6. `Next skill`: the next Rust skill to use.

## Guardrails

- Do not create a workspace when one package and clear modules are enough.
- Do not invent or raise MSRV without evidence and user intent.
- Do not add local path dependencies to public or shared package surfaces.
- Do not publish packages by default.
- Do not use nightly-only features unless the repo already depends on nightly or the user approves that constraint.
