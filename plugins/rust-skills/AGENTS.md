# AGENTS.md

This file is the Rust Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `rust-skills` is a monorepo-owned Socket child and the canonical source of truth for shipped Rust workflow skills.
- Root [`skills/`](./skills/) is the authored workflow surface.
- The repo root is the Codex plugin root through [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).
- Treat `productivity-skills` as the default baseline maintainer layer for general repo-doc and maintenance work; use this repo when Rust, Cargo, rustup, crate, workspace, package, test, lint, or formatting behavior should materially change the workflow.

## Local Rules

- Match the `socket` shared semantic version exactly; use the Socket root release workflow for version inventory and bumps.
- Use official Rust project documentation first for Rust language, Cargo, rustup, rustfmt, Clippy, testing, package, workspace, edition, and CI behavior.
- Keep Rust examples grounded in `cargo` and `rustup` unless a repository already documents a different tool path.
- Ask before choosing a crate or workspace shape when the user's request is ambiguous.
- Prefer small crates with clear ownership boundaries. Use a Cargo workspace only when multiple crates, packages, or examples need shared dependency and validation behavior.
- Treat MSRV as an explicit compatibility contract. Do not invent or raise a repo's minimum supported Rust version without checking existing docs, `Cargo.toml`, `rust-toolchain.toml`, CI, or user intent.
- Keep package dependencies fetchable from crates.io, GitHub, package registries, or other real remote repositories; do not commit machine-local path dependencies.
- For validation guidance, prefer the narrowest relevant `cargo fmt --check`, `cargo clippy`, `cargo test`, `cargo build`, or `cargo package` command for the project shape.
- Do not add extra packaging layers, repo-local install machinery, broad maintainer automation, custom templates, or bundled MCP servers unless a later plan explicitly calls for that scope.
