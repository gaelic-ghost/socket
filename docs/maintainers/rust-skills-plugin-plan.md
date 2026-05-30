# Rust Skills Plugin Plan

This plan records the first durable shape for a Socket-hosted Rust skills plugin.

The plugin's job is to help agents choose Rust project shapes, bootstrap Cargo crates and workspaces, implement CLI and library crates, prepare package surfaces, align CI, test and validate Rust projects, and keep Rust tooling guidance grounded in official Rust documentation.

## Intent

The `rust-skills` plugin should help agents do five things:

- choose a Rust crate, package, workspace, or maintenance shape before implementation starts
- bootstrap reproducible Cargo projects without inventing local-only templates or package sources
- implement Rust CLI and library crates with clear public boundaries, diagnostics, tests, and validation
- prepare package surfaces and run Rust build, test, lint, format, package, and CI workflows
- keep Rust guidance grounded in official Rust language, Cargo, rustup, rustfmt, and Clippy documentation

This is a companion guidance plugin, not a runtime plugin. The first version should not bundle an MCP server, custom package manager, private template feed, generated scaffold script, or machine-local toolchain state.

## Packaging Direction

Package the guidance as an independent child plugin under:

```text
plugins/rust-skills/
```

The child plugin owns its Codex-facing guidance surface:

- `.codex-plugin/plugin.json`
- `skills/`
- plugin metadata, skill metadata, `AGENTS.md`, and maintainer notes that explain the plugin's role
- any validation scripts needed for the plugin's own authored guidance

The root Socket marketplace now lists `rust-skills` as an installable child plugin because the first real skills have landed. If the plugin ever loses its exported skill content, switch the marketplace entry back to `NOT_AVAILABLE` in the same pass.

## Rust Workflow Policy

Rust guidance should stay close to the standard toolchain:

- use `cargo` as the default project, package, build, test, and metadata command surface
- use `rustup` for toolchain installation, overrides, and components
- treat MSRV as an explicit compatibility contract, not a guess
- preserve existing repository decisions for edition, workspace layout, lint strictness, and CI matrices
- prefer narrow validation commands that match the change risk
- do not add local path dependencies, private registries, custom templates, or extra package managers without an explicit repository reason

When a user has not chosen a project shape, ask or return a decision point before scaffolding.

## Documentation Sources

Use official Rust documentation first:

- [Rust documentation](https://doc.rust-lang.org/)
- [The Rust Programming Language](https://doc.rust-lang.org/book/)
- [The Cargo Book](https://doc.rust-lang.org/cargo/)
- [`cargo new`](https://doc.rust-lang.org/cargo/commands/cargo-new.html)
- [Cargo manifest format](https://doc.rust-lang.org/cargo/reference/manifest.html)
- [`cargo package`](https://doc.rust-lang.org/cargo/commands/cargo-package.html)
- [`cargo publish`](https://doc.rust-lang.org/cargo/commands/cargo-publish.html)
- [Cargo workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html)
- [Cargo features reference](https://doc.rust-lang.org/cargo/reference/features.html)
- [Cargo tests guide](https://doc.rust-lang.org/cargo/guide/tests.html)
- [Cargo continuous integration guide](https://doc.rust-lang.org/cargo/guide/continuous-integration.html)
- [The rustup book](https://rust-lang.github.io/rustup/)
- [Clippy documentation](https://doc.rust-lang.org/clippy/)
- [Rustfmt 2024 style edition guide](https://doc.rust-lang.org/stable/edition-guide/rust-2024/rustfmt-style-edition.html)

When a skill relies on documentation, translate the relevant rule into practical workflow guidance. Do not drop citations into a skill as a substitute for explaining the effect on scaffolding, validation, project layout, or user-facing behavior.

## Shipped Skill Inventory

### `rust:choose-project-shape`

Help an agent decide how Rust should fit into a user's project before implementation starts.

This skill classifies the requested work:

- binary crate
- library crate
- Cargo workspace
- CLI tool
- service or daemon
- proc macro
- FFI boundary
- embedded or `no_std` target
- package maintenance or upgrade pass

The output recommends crate shape, workspace boundaries, edition and MSRV checks, validation commands, package boundaries, and documentation updates.

### `rust:bootstrap-cargo-project`

Create or guide a reproducible Cargo project scaffold.

This skill covers:

- `cargo new` versus `cargo init`
- binary versus library packages
- workspace layout
- Rust edition and MSRV handling
- `rust-toolchain.toml`
- test layout
- initial build, test, format, and lint validation

### `rust:build-cli-project`

Guide agents through implementing Rust command-line tools.

This skill covers:

- keeping CLI parsing separate from domain behavior
- choosing dependencies from existing repo policy or explicit user approval
- shaping user-facing output and exit behavior
- testing command behavior without turning every test into a shell process
- handing off to Cargo validation and packaging workflows

### `rust:build-library-crate`

Guide agents through implementing reusable Rust library crates.

This skill covers:

- public API ownership
- module visibility
- error types
- feature flags
- documentation examples
- unit, integration, and doctest boundaries

### `rust:testing-workflow`

Guide agents through Rust test execution and failure triage.

This skill covers:

- unit tests
- integration tests
- documentation tests
- examples compiled by `cargo test`
- feature-gated test matrices
- failure filtering and targeted reruns

### `rust:package-workflow`

Guide agents through publish-facing Cargo package preparation.

This skill covers:

- manifest metadata
- `rust-version` and MSRV checks
- lockfile policy
- path dependency restrictions
- package inclusion and exclusion
- dry-run package validation
- publish versus no-publish decisions

### `rust:ci-workflow`

Guide agents through Rust CI validation design.

This skill covers:

- local-to-CI command alignment
- format, lint, build, test, docs, package, and MSRV checks
- workspace and feature matrix choices
- toolchain component setup
- warnings-as-errors policy
- cache and artifact boundaries

### `rust:tooling-style-workflow`

Align Rust formatting, linting, toolchain, and CI behavior with repository policy.

This skill covers:

- `cargo fmt --check`
- `cargo clippy`
- `rustfmt.toml`
- Rust 2024 style edition behavior
- `rust-toolchain.toml`
- CI command shape
- lint strictness and warnings-as-errors decisions

## Next Skill Candidates

- `rust:upgrade-workflow`
- `rust:ffi-workflow`
- `rust:wasm-workflow`
- `rust:embedded-workflow`

## Completion Checklist

- [x] Update `plugins/rust-skills/AGENTS.md` with Rust workflow policy and validation expectations.
- [x] Update `plugins/rust-skills/.codex-plugin/plugin.json` so plugin metadata describes shipped Rust guidance.
- [x] Add first-slice skills for project-shape choice, Cargo bootstrap, testing, and tooling/style alignment.
- [x] Add implementation skills for Rust CLI and library crate work.
- [x] Add package and CI workflow skills for publish-facing and automation guidance.
- [x] Switch the root marketplace entry for `rust-skills` to installable only after real skill content exists.
- [x] Update root README and TODO so users understand the new installable child plugin surface.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.

## Exit Criteria

- [x] The Socket marketplace exposes `rust-skills` as an installable child plugin.
- [x] The new skills can help an agent choose a Rust project shape before implementation.
- [x] The new skills guide Cargo bootstrap, CLI and library implementation, package preparation, CI alignment, testing, formatting, linting, and toolchain alignment without bundling a runtime service.
- [x] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.
