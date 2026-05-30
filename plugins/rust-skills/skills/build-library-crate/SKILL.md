---
name: build-library-crate
description: Implement reusable Rust library crates after the project shape is chosen, including public API design, module visibility, error types, feature flags, documentation examples, unit tests, integration tests, doctests, and Cargo validation. Use for Rust library implementation, API refactors, crate-boundary cleanup, or package-facing behavior.
license: Apache-2.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: rust-implementation
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(cargo:*) Bash(rustc:*) Bash(rustup:*)
---

# Build Rust Library Crate

## Purpose

Implement reusable Rust library behavior with a small public API, clear module visibility, and tests at the boundary users actually call.

The practical goal is a crate that is easy to use from downstream code, easy to test inside the repository, and honest about compatibility, features, and errors.

## Source Check

Use official Rust and Cargo documentation first:

- [The Rust Programming Language](https://doc.rust-lang.org/book/)
- [The Cargo Book](https://doc.rust-lang.org/cargo/)
- [Cargo package layout](https://doc.rust-lang.org/cargo/guide/project-layout.html)
- [Cargo features reference](https://doc.rust-lang.org/cargo/reference/features.html)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Cargo tests guide](https://doc.rust-lang.org/cargo/guide/tests.html)

Use the repository's existing API style before introducing a new pattern.

## Workflow

1. Inspect the crate shape:
   - `Cargo.toml`
   - `src/lib.rs`
   - modules under `src/`
   - `tests/`
   - public examples and documentation comments
   - features and optional dependencies
   - package metadata if the crate is publishable
2. Identify the caller:
   - internal binary
   - sibling workspace crate
   - external library user
   - FFI or generated-code caller
   - tests and examples only
3. Shape the public API:
   - expose the smallest set of types and functions users need
   - keep implementation modules private by default
   - re-export stable public types deliberately from `lib.rs`
   - prefer explicit inputs and outputs over hidden global state
   - make ownership and borrowing convenient for likely callers
4. Shape errors:
   - use concrete error types when callers need to match variants
   - use opaque errors only when callers only need display/debug behavior
   - include operation context in error messages
   - preserve source errors when that helps diagnostics
5. Add tests and docs at the right boundary.

## Module And Visibility Guidance

Prefer private modules with explicit public re-exports:

```rust
mod parser;

pub use parser::{ParseError, parse_document};
```

Use `pub(crate)` for shared internal behavior that crosses modules inside one crate. Avoid `pub` just to make tests easy; use unit tests in the module for private behavior and integration tests for public behavior.

Split modules when a file starts owning unrelated jobs such as parsing, validation, rendering, and I/O.

## Feature Guidance

Use Cargo features for real optional behavior:

- optional dependencies
- format or backend support
- `std` versus `no_std`
- expensive integrations

Do not add feature flags for uncertain future work. Every feature should have tests or at least a documented validation path.

## Testing Strategy

Use unit tests for private transformations and edge cases.

Use integration tests under `tests/` when the public API should be exercised like a downstream caller:

```rust
use my_crate::parse_document;

#[test]
fn parses_empty_document() {
    let document = parse_document("").unwrap();
    assert!(document.items().is_empty());
}
```

Use doctests when examples in public documentation should stay compiling and accurate.

## Validation

Choose the narrowest command that proves the change:

```bash
cargo test -p package-name
cargo test -p package-name --doc
cargo clippy -p package-name --all-targets --all-features
cargo fmt --check
```

For publishable crates, defer packaging details to `rust:package-workflow`.

## Output Shape

Return:

1. `Library surface`: public types, functions, modules, features, and errors changed.
2. `Caller impact`: who uses the API and what becomes easier or safer.
3. `Visibility`: what is public, `pub(crate)`, or private and why.
4. `Tests`: unit, integration, doctest, or feature coverage added or recommended.
5. `Validation`: exact Cargo commands run or skipped with the concrete reason.
6. `Next skill`: usually `rust:testing-workflow`, `rust:tooling-style-workflow`, or `rust:package-workflow`.

## Guardrails

- Do not expose implementation modules as public API by accident.
- Do not add feature flags without a real optional behavior and validation path.
- Do not hide compatibility changes to MSRV, edition, or public API.
- Do not use local path dependencies in shared or publishable crate surfaces.
- Do not make test convenience the reason for broad public visibility.
