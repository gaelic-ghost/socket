---
name: testing-workflow
description: Plan, run, and triage Rust tests with Cargo, including unit tests, integration tests, documentation tests, examples compiled by cargo test, targeted reruns, feature matrices, workspace package selection, and failure explanation. Use when adding tests, running Rust validation, or diagnosing cargo test failures.
license: PolyForm-Noncommercial-1.0.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: rust-testing
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(cargo:*) Bash(rustc:*) Bash(rustup:*)
---

# Rust Testing Workflow

## Purpose

Run the narrowest useful Rust tests, explain failures clearly, and keep test layout aligned with Cargo's model.

Cargo test behavior matters because one command can compile and run unit tests, integration tests, documentation tests, and examples. The skill should make that scope explicit instead of treating `cargo test` as a black box.

## Source Check

Use repo-local Rust files, checked-out dependency sources, Dash MCP or Dash HTTP for installed Rust docsets, and then official Rust documentation when Dash/local coverage is missing or stale:

- [Cargo tests guide](https://doc.rust-lang.org/cargo/guide/tests.html)
- [`cargo test`](https://doc.rust-lang.org/cargo/commands/cargo-test.html)
- [The Rust book testing chapter](https://doc.rust-lang.org/book/ch11-00-testing.html)
- [Cargo features reference](https://doc.rust-lang.org/cargo/reference/features.html)

Translate test behavior into the concrete command and failure mode in the repository.

## Test Layout

- Put unit tests near implementation when they need private module access.
- Put integration tests under `tests/` when they should use the crate like an external caller.
- Use documentation tests when examples in public API docs should compile and run.
- Use `examples/` when sample binaries should compile as part of validation.
- Use feature-gated tests only when the crate's feature matrix is part of the public behavior.

## Command Selection

Start narrow, then widen:

```bash
cargo test
```

Target one package in a workspace:

```bash
cargo test -p package-name
```

Run all workspace tests:

```bash
cargo test --workspace
```

Run all targets and features when feature interactions matter:

```bash
cargo test --all-targets --all-features
```

Filter by test name:

```bash
cargo test some_test_name
```

Show test output:

```bash
cargo test some_test_name -- --nocapture
```

Run documentation tests only when public docs are the focus:

```bash
cargo test --doc
```

## Failure Triage

Classify failures by the first concrete break:

- compile failure: source, dependency, feature, target, or MSRV problem
- unit test failure: internal behavior changed
- integration test failure: public behavior or crate boundary changed
- doctest failure: public example or documentation drifted
- feature failure: optional dependency or cfg path broke
- workspace failure: package selection, shared dependency, or target matrix issue

Read the first relevant compiler or test error before changing code. Rust output is usually precise; preserve that precision in the user-facing explanation.

## Implementation Guidance

- Add tests at the same boundary the user cares about.
- Prefer deterministic tests over sleeps, timing assumptions, or network calls.
- Use temporary directories for filesystem behavior.
- Avoid snapshot tests unless the repo already uses them or the output is intentionally broad.
- Keep error-message assertions focused on stable, user-visible text.

## Output Shape

Return:

1. `Test scope`: package, workspace, target, feature, or doc-test boundary.
2. `Commands`: exact commands run or recommended.
3. `Result`: pass, fail, or skipped with the concrete reason.
4. `Failure mode`: compile, unit, integration, doctest, feature, or workspace issue.
5. `Fix direction`: the smallest code, test, dependency, or docs change that addresses the failure.

## Guardrails

- Do not run broad feature or workspace matrices first when a targeted command proves the change.
- Do not hide compile failures behind test summaries.
- Do not weaken tests to match broken behavior unless the user explicitly approves the behavior change.
- Do not add network-dependent tests without a repo-owned test strategy for them.
