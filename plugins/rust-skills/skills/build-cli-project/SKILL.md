---
name: build-cli-project
description: Implement Rust command-line tools after the project shape is chosen, including argument parsing boundaries, command dispatch, stdin/stdout/stderr behavior, exit codes, configuration input, error messages, tests, and Cargo validation. Use for Rust CLI feature work, CLI refactors, or new binary crate implementation.
license: Apache-2.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: rust-implementation
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(cargo:*) Bash(rustc:*) Bash(rustup:*)
---

# Build Rust CLI Project

## Purpose

Implement Rust command-line behavior with a clear boundary between user input, command execution, domain logic, and output.

The practical goal is a CLI that is easy to test, has descriptive operator-facing messages, and validates with the repository's Cargo commands.

## Source Check

Use official Rust and Cargo documentation first:

- [The Rust Programming Language](https://doc.rust-lang.org/book/)
- [The Cargo Book](https://doc.rust-lang.org/cargo/)
- [Cargo package layout](https://doc.rust-lang.org/cargo/guide/project-layout.html)
- [Cargo tests guide](https://doc.rust-lang.org/cargo/guide/tests.html)
- [`std::process::ExitCode`](https://doc.rust-lang.org/std/process/struct.ExitCode.html)
- [`std::env::args`](https://doc.rust-lang.org/std/env/fn.args.html)

For third-party argument parsers, error crates, config crates, terminal styling, or snapshot tools, prefer the repository's existing dependencies first. Add a new crate only when it removes real implementation complexity and comes from a fetchable registry or repository.

## Workflow

1. Inspect the CLI shape:
   - `Cargo.toml`
   - `src/main.rs`
   - `src/bin/`
   - `src/lib.rs`
   - existing argument parser or command modules
   - existing tests in `tests/` or near command code
2. Identify the command surface:
   - command name
   - subcommands
   - flags and options
   - positional arguments
   - stdin, stdout, stderr, files, or environment variables
   - exit-code expectations
3. Keep behavior testable:
   - parse user input into explicit command data
   - put domain work in functions that accept normal Rust values
   - keep printing and process exit decisions at the edge
   - return structured errors or clear result types from internal functions
4. Implement output deliberately:
   - stdout for requested command output
   - stderr for diagnostics, warnings, and failures
   - descriptive errors that name the failed operation and likely cause
   - stable text only where tests or downstream users depend on it
5. Validate with targeted Cargo commands.

## Dependency Decisions

Use the standard library for small internal tools when argument parsing is simple.

Use the repo's existing parser or error-handling crate when one is already established. If adding a new dependency, explain:

- what repeated parsing, validation, help, or error behavior it replaces
- why the standard library or existing dependency is not enough
- how the dependency affects MSRV, binary size, and package policy

Do not add a CLI framework only because one is popular.

## Testing Strategy

Prefer fast tests around parsing and command execution functions:

```rust
#[test]
fn parses_verbose_flag() {
    let command = parse_args(["tool", "--verbose", "input.txt"]).unwrap();
    assert!(command.verbose);
}
```

Use process-level integration tests only for behavior that truly depends on the executable boundary, such as stdout, stderr, current directory, environment, or exit status.

Keep error-message tests focused on stable user-facing text.

## Validation

Choose the narrowest command that proves the change:

```bash
cargo test -p package-name
cargo clippy -p package-name --all-targets --all-features
cargo fmt --check
```

Use workspace-wide commands when the CLI change crosses package boundaries.

## Output Shape

Return:

1. `Command surface`: subcommands, flags, inputs, outputs, and exit behavior changed.
2. `Implementation boundary`: what lives in parsing, execution, domain logic, and output code.
3. `Dependencies`: reused, added, or intentionally avoided dependencies.
4. `Tests`: unit, integration, or process-level coverage added or recommended.
5. `Validation`: exact Cargo commands run or skipped with the concrete reason.
6. `Next skill`: usually `rust:testing-workflow`, `rust:tooling-style-workflow`, or `rust:package-workflow`.

## Guardrails

- Do not put domain behavior directly inside argument parsing code.
- Do not call `std::process::exit` deep inside reusable functions.
- Do not write vague errors like `failed` without naming the operation and likely cause.
- Do not add new CLI dependencies without naming the implementation problem they solve.
- Do not make stdout/stderr text unstable if tests, scripts, or users depend on it.
