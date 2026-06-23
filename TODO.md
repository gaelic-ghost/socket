# TODO

This file is the Socket-level backlog for child plugins that no longer keep their own `ROADMAP.md` files. `apple-dev-skills` keeps its public roadmap in `plugins/apple-dev-skills/ROADMAP.md` because it still has a standalone compatibility marketplace.

## Active Child Plugins

### agent-plugin-skills

- [x] Overhaul the exported skills around Codex/OpenAI plus the open `.agents/skills` discovery mirror only.
- [x] Remove stale sync-audit expectations for retired child maintainer docs such as reality-audit and install-surface docs.
- [x] Refresh tests and bootstrap output so generated guidance matches the current collapsed Socket docs model.
- [ ] Keep Git-backed Codex marketplace install and update guidance ahead of local authoring notes.
- [ ] Keep repo-local discovery mirror guidance separate from install guidance.
- [ ] Add or refine troubleshooting language for confusing Codex plugin expectations.
- [ ] Add a maintainer workflow for moving or re-homing skills between repositories.
- [ ] Add durable process support for noticing changes in OpenAI Codex docs and the open `.agents` skill discovery convention.
- [x] Move framework-neutral agent and skill eval design into `productivity-skills:design-agent-eval-workflow`; keep runtime-specific eval implementation with the owning plugin or repo.

### android-dev-skills

- [ ] Author the first real Android-focused skill tranche for Codex.
- [x] Record the detailed first skill plan in [`docs/maintainers/android-dev-skills-plugin-plan.md`](./docs/maintainers/android-dev-skills-plugin-plan.md).
- [ ] Start Kotlin-first while preserving Java interoperability and Java-only project support where repo defaults require it.
- [ ] Cover project-shape discovery, Gradle and Android Gradle Plugin alignment, build variants, dependency updates, unit tests, lint, emulator-aware validation handoffs, and release readiness.
- [ ] Keep emulator operation and device debugging handoffs aligned with the existing Android testing plugin instead of duplicating runtime tooling.
- [ ] Keep Android app/platform guidance separate from `server-side-jvm` backend and shared non-Android JVM library guidance.
- [ ] Update docs and validation once the exported Android skill surface is real.
- [ ] Decide whether the long-term home remains Socket-owned or becomes standalone.

### cardhop-app

- [ ] Keep `cardhop-contact-workflow`, bundled MCP server docs, `.mcp.json`, and plugin metadata aligned.
- [ ] Validate the bundled MCP server from `plugins/cardhop-app/mcp/`.
- [ ] Add root or child validation coverage once the Cardhop skill or MCP surface grows beyond the current single workflow.

### dotnet-skills

- [x] Author the first real .NET-focused skill tranche for Codex.
- [x] Update docs to describe shipped behavior once real skill content exists.
- [x] Add the minimum validation or smoke coverage needed for the shipped skill surface.
- [ ] Add Codex GUI local environment templates and auto-copy/install behavior for F#, C#, and mixed `.NET` repos.
- [ ] Decide whether the long-term home remains Socket-owned or becomes standalone.

### productivity-skills

- [x] Fold issue-sized TODO/FIXME and bug-fix ticket tracking into `maintain-project-roadmap` through the canonical `Small Tickets` section instead of adding a separate `maintain-project-todo` workflow.
- [x] Add `maintain-project-docs` after `maintain-project-roadmap` owns small-ticket tracking so one umbrella workflow can coordinate README, CONTRIBUTING, AGENTS, ACCESSIBILITY, and ROADMAP splits.
- [x] Add `maintain-github-repository` for GitHub repository settings audits and requested alignment, with release and publish choreography remaining in `maintain-project-repo`.
- [ ] Add `maintain-project-security` for canonical `SECURITY.md` maintenance.
- [ ] Add `maintain-project-support` for canonical `SUPPORT.md` maintenance.
- [ ] Add a future `maintain-project-hooks` workflow for repositories that intentionally use Codex Hooks.
- [x] Add `design-agent-automation-workflow` as a framework-neutral planning skill for choosing between Codex app automations, `codex exec`, Codex subagents, OpenAI Agents SDK services, LangGraph graphs, Hermes-specific workflows, or no automation yet.
- [x] Skew `design-agent-automation-workflow` toward safe full automation by default, with exact escalation gates instead of broad human review when a task can be made reasonably safe.
- [x] Add `design-agent-eval-workflow` for agent, skill, prompt, and automation eval design before runtime-specific implementation.
- [ ] Forward-test `design-agent-automation-workflow` and `design-agent-eval-workflow` against real agent, automation, and eval planning requests before adding deterministic scaffolding scripts.
- [ ] Add lightweight validation tooling for `SKILL.md`, frontmatter, and `agents/openai.yaml` alignment.
- [ ] Add validation checks for README layout and active skill inventory consistency.

### apple-dev-skills

- [x] Publish the Phase 1 standalone compatibility release so `gaelic-ghost/apple-dev-skills` points at the Socket-hosted plugin payload while preserving `codex plugin marketplace upgrade apple-dev-skills`.
- [x] Complete Phase 2 of the Socket migration: make `plugins/apple-dev-skills` monorepo-owned, remove subtree release gates, update Socket docs and duplicate-install guidance, add compatibility marketplace smoke coverage, validate, and publish the Socket release.
- [ ] Add the Xcode 27 agentic tooling workflows from [`docs/maintainers/xcode-27-agentic-tooling-plan.md`](./docs/maintainers/xcode-27-agentic-tooling-plan.md), starting with `xcode-coding-intelligence-workflow`.

### python-skills

- [x] Tighten child-specific `AGENTS.md` and validator expectations after the README collapse.
- [x] Fix the child validator so it no longer expects a removed child `README.md`.
- [x] Record the expansion plan in [`docs/maintainers/python-skills-plugin-plan.md`](./docs/maintainers/python-skills-plugin-plan.md).
- [x] Add `choose-python-project-shape`.
- [x] Add `build-python-project`.
- [x] Add `diagnose-python-project`.
- [x] Add `python-package-workflow`.
- [x] Add `python-tooling-style-workflow`.
- [x] Add `python-ci-workflow`.
- [x] Add `python-upgrade-workflow`.
- [x] Keep `uv-pytest-unit-testing` as the release-compatible pytest workflow name for now.
- [x] Update `plugins/python-skills/.codex-plugin/plugin.json` after the new skills exist.
- [x] Confirm `uv run scripts/validate_repo_metadata.py`, `uv run pytest`, `uv run ruff check .`, and `uv run mypy .` pass after the second skill slice.

### server-side-swift

- [x] Create the Socket-owned `server-side-swift` plugin surface.
- [x] Add the first real Vapor-focused server-side Swift skill.
- [x] Add a persistence workflow for Fluent, database migrations, query design, Hummingbird database handoffs, and docs routing.
- [ ] Add validation coverage for skill metadata and exported skill inventory once central Socket child-skill validation exists.
- [ ] Decide whether future server-side Swift skills should cover SwiftNIO, deployment, authentication, app sync, or additional database workflows as separate skills.
- [ ] Decide whether the long-term home remains Socket-owned or becomes standalone.

### server-side-jvm

- [x] Create the Socket-owned `server-side-jvm` placeholder plugin surface.
- [x] Record the detailed first skill plan in [`docs/maintainers/server-side-jvm-skills-plugin-plan.md`](./docs/maintainers/server-side-jvm-skills-plugin-plan.md).
- [x] Author the first real server-side JVM skill tranche for Codex.
- [x] Treat Java and Scala as equal first-party JVM language choices, with future Clojure support planned without renaming the plugin.
- [x] Prefer functional style where it fits the selected language and framework, especially for Scala and future Clojure guidance.
- [ ] Cover package/runtime handoffs, persistence, observability, CI, and upgrades after the first project-shape, build-tooling, implementation, and testing slice.
- [x] Keep Android app/platform guidance separate from `android-dev-skills`.
- [x] Update docs and validation once the exported server-side JVM skill surface is real.
- [ ] Decide whether the long-term home remains Socket-owned or becomes standalone.

### rust-skills

- [x] Author the first real Rust-focused skill tranche for Codex.
- [x] Add Rust CLI and library implementation guidance after the first planning and validation slice.
- [x] Add Rust package and CI workflow guidance.
- [x] Update docs to describe shipped behavior once real skill content exists.
- [x] Switch the root marketplace entry for `rust-skills` from placeholder to installable after real skill content exists.
- [ ] Add focused validation only if the plugin gains generated examples, scripts, or metadata checks that need more than root marketplace validation.
- [ ] Decide whether the long-term home remains Socket-owned or becomes standalone.

### reverse-engineering-skills

- [x] Author the first real reverse-engineering skill tranche for Codex.
- [x] Start with artifact triage and evidence notes before platform-specific decompilation workflows.
- [ ] Cover .NET assemblies, Unity managed and IL2CPP artifacts, Apple binaries, symbols, crash logs, and decompiler or disassembler output review.
- [ ] Add tool-specific guidance for Cutter, Ghidra, Malimite, Hopper, and adjacent tools only after hands-on workflow preferences are clearer.
- [x] Update docs and validation once the exported reverse-engineering skill surface is real.
- [ ] Decide whether the long-term home remains Socket-owned or becomes standalone.

### swiftasb-skills

- [x] Sync `swiftasb-skills` with current SwiftASB source and docs.
- [x] Re-check explanation, integration-shape, SwiftUI, AppKit, package, and diagnostics skills against the current SwiftASB client API and runtime behavior.
- [ ] Add focused validation only if the plugin gains metadata, examples, or generated checks that need more than root marketplace validation.

### things-app

- [ ] Finish guidance and maintenance modernization for the mixed Things skill plus bundled MCP server repo.
- [ ] Keep root README and AGENTS guidance clear about whether a change belongs in `skills/`, `mcp/`, or plugin metadata.
- [ ] Expand repo-root maintainer tooling once more than one root skill needs Python-backed verification.
- [ ] Add broader bundled-server smoke coverage when new Things tool families or auth-sensitive update flows are introduced.
- [ ] Revisit packaging mirrors if the repo starts shipping additional Codex discovery surfaces.

### web-dev-skills

- [x] Author the first real web-focused skill for Codex.
- [x] Update docs to describe shipped behavior once real skill content exists.
- [x] Add the minimum validation or smoke coverage needed for the shipped skill surface.
- [ ] Decide whether the long-term home remains Socket-owned or becomes standalone.

## Cross-Child Validation

- [ ] Evaluate one root validation command for marketplace metadata, plugin manifests, child AGENTS shape, `SKILL.md` frontmatter, and `agents/openai.yaml` alignment.
- [ ] Decide which checks belong centrally in Socket and which should remain child-local behavior tests.
- [ ] Retire or update stale child validators when their expected docs have been collapsed into root docs.
- [x] Remediate the 2026-06-15 Dependabot alert inventory, starting with the Cardhop and Things MCP server lockfiles recorded in [`docs/maintainers/dependabot-alert-triage-2026-06-15.md`](./docs/maintainers/dependabot-alert-triage-2026-06-15.md).
- [x] Merge the 2026-06-21 Dependabot `pydantic-settings` 2.14.2 lockfile bumps for Cardhop and Things MCP servers after child validation passes.

## Legal And Licensing

- [x] Move future Socket versions from Apache 2.0 to PolyForm Noncommercial 1.0.0 plus separate commercial licensing.
- [x] Preserve historical Apache 2.0 text for previously licensed versions in `LICENSE-HISTORICAL-APACHE-2.0`.
- [x] Add `COMMERCIAL-USE.md` with Gale's commercial-use policy and commercial licensing contact.
- [x] Use [`docs/maintainers/source-available-licensing-options.md`](./docs/maintainers/source-available-licensing-options.md) as the maintainer record for legal review and migration planning.
- [x] Require DCO sign-off plus an outbound commercial licensing grant before accepting outside contributions.
- [x] Install-test and publish the changed marketplace metadata with the new license surface.

## Placeholder Child Plugins

### spotify

- [ ] Author the first real Spotify-focused Codex workflow.
- [ ] Add the first maintained Spotify skill, app, or MCP-backed workflow under the canonical exported surface.
- [ ] Update docs and validation once the exported Spotify surface is real.
- [ ] Decide whether Socket remains the canonical home after the first real shipped workflow.
