# Rust Checks

## Detection

Treat repository as Rust when `Cargo.toml` exists.
Additional signals:
- `rust-toolchain.toml`
- `[workspace]` in `Cargo.toml`

## Alignment Expectations

- Docs should include standard cargo command guidance:
  - `cargo build`
  - `cargo test`
- When tests are present in repo and docs omit test command, flag a gap.

## Safe Fix Scope

- Insert concise quickstart lines with `cargo build` and `cargo test` when missing and project type is unambiguous.
- Do not rewrite crate-level architecture or feature-flag documentation.
