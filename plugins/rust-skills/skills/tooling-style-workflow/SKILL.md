---
name: tooling-style-workflow
description: Align Rust formatting, linting, toolchain, and CI behavior with repository policy, including cargo fmt, rustfmt style edition, cargo clippy, rust-toolchain.toml, MSRV checks, warnings-as-errors decisions, and validation command selection. Use when configuring or fixing Rust style, lint, toolchain, or CI workflows.
license: Apache-2.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: rust-tooling
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(cargo:*) Bash(rustc:*) Bash(rustup:*)
---

# Rust Tooling And Style Workflow

## Purpose

Keep Rust formatting, linting, toolchain, and CI behavior explicit and consistent with the repository.

The practical goal is to avoid accidental formatter churn, surprise MSRV changes, lint strictness jumps, or CI commands that do not match local validation.

## Source Check

Use official documentation first:

- [`cargo fmt`](https://doc.rust-lang.org/cargo/commands/cargo-fmt.html)
- [`cargo clippy`](https://doc.rust-lang.org/cargo/commands/cargo-clippy.html)
- [Rustfmt 2024 style edition guide](https://doc.rust-lang.org/stable/edition-guide/rust-2024/rustfmt-style-edition.html)
- [The rustup book](https://rust-lang.github.io/rustup/)
- [Cargo continuous integration guide](https://doc.rust-lang.org/cargo/guide/continuous-integration.html)

Treat rustfmt and Clippy as toolchain components. If they are missing locally, report the missing component and the likely install command instead of guessing at style by hand.

## Repository Inspection

Before changing tooling, inspect:

- `Cargo.toml`
- `Cargo.lock`
- `rust-toolchain.toml` or `rust-toolchain`
- `rustfmt.toml` or `.rustfmt.toml`
- `clippy.toml`
- `.cargo/config.toml`
- `.github/workflows/`
- existing Makefile, justfile, xtask, or scripts
- README, CONTRIBUTING, AGENTS, or package docs for validation commands

## Formatting

Use Cargo's formatter command by default:

```bash
cargo fmt --check
```

Apply formatting only when the user asked for implementation or formatting work:

```bash
cargo fmt
```

For Rust 2024 projects, check whether the repo needs an explicit `rustfmt.toml` with `style_edition = "2024"` so editor format-on-save and CI use the same style behavior. Do not add this file to older-edition projects without a conscious style decision.

## Linting

Use Clippy when lint behavior matters:

```bash
cargo clippy --all-targets --all-features
```

Use warnings-as-errors only when the repo already expects it or the task is explicitly tightening CI:

```bash
cargo clippy --all-targets --all-features -- -D warnings
```

Do not silence lints broadly. Prefer a local code fix, then a narrow `allow` with a concrete reason when the lint is intentionally wrong for that code.

## Toolchain And MSRV

Use `rust-toolchain.toml` when contributors or CI need a pinned channel or components:

```toml
[toolchain]
channel = "stable"
components = ["rustfmt", "clippy"]
```

Preserve existing MSRV. If the task needs a newer compiler, make that compatibility change explicit in docs, CI, and release notes.

Check local toolchain state only when implementation needs it:

```bash
rustc --version
cargo --version
rustup show
```

## CI Alignment

Local and CI validation should name the same meaningful commands. A normal Rust CI baseline is:

```bash
cargo fmt --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-targets --all-features
```

Narrow this for small crates or widen it for published libraries with feature matrices, MSRV checks, or platform-specific behavior.

## Output Shape

Return:

1. `Tooling state`: formatter, linter, toolchain, MSRV, and CI policy observed.
2. `Commands`: exact commands run or recommended.
3. `Changes`: files or settings changed, if any.
4. `Validation`: pass, fail, or skipped with the concrete reason.
5. `Compatibility impact`: whether edition, style edition, MSRV, lint strictness, or CI behavior changed.

## Guardrails

- Do not add warnings-as-errors as a casual cleanup.
- Do not add or change `rust-toolchain.toml` without a reproducibility or CI reason.
- Do not raise MSRV silently.
- Do not hand-format Rust when `cargo fmt` is available.
- Do not overwrite repo-local style, lint, or CI policy with a generic template.
