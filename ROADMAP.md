# Project Roadmap

## Table of Contents

- [Vision](#vision)
- [Product Principles](#product-principles)
- [Milestone Progress](#milestone-progress)
- [Milestone 5: SwiftASB skills plugin](#milestone-5-swiftasb-skills-plugin)
- [Milestone 6: Dotnet skills plugin](#milestone-6-dotnet-skills-plugin)
- [Milestone 7: Python skills plugin expansion](#milestone-7-python-skills-plugin-expansion)
- [Milestone 8: Server-Side Swift skills plugin](#milestone-8-server-side-swift-skills-plugin)
- [Milestone 9: Rust skills plugin](#milestone-9-rust-skills-plugin)
- [Milestone 10: Expo inline native modules workflow](#milestone-10-expo-inline-native-modules-workflow)
- [Milestone 11: Codex Utilities plugin](#milestone-11-codex-utilities-plugin)
- [Small Tickets](#small-tickets)
- [Backlog Candidates](#backlog-candidates)
- [History](#history)

## Vision

- Keep `socket` as the honest superproject layer for a public Codex plugin and skills ecosystem, with subtree imports, root marketplace wiring, and cross-repo maintainer guidance kept consistent.

## Product Principles

- Keep the superproject focused on subtree coordination, root marketplace wiring, and cross-repo maintainer guidance.
- Keep child-repository ownership boundaries explicit instead of flattening repo-local behavior into `socket`.
- Keep public imported plugin surfaces and root marketplace wiring aligned in the same pass.
- Keep user-facing plugin install and update docs on the official Git-backed marketplace path.

## Milestone Progress

- Milestone 5: SwiftASB skills plugin - Implemented
- Milestone 6: Dotnet skills plugin - Implemented
- Milestone 7: Python skills plugin expansion - Implemented
- Milestone 8: Server-Side Swift skills plugin - In Progress
- Milestone 9: Rust skills plugin - Implemented
- Milestone 10: Expo inline native modules workflow - Implemented
- Milestone 11: Codex Utilities plugin - In Progress

## Milestone 5: SwiftASB skills plugin

### Status

Implemented

### Scope

- [x] Add a Socket-hosted `swiftasb-skills` child plugin that helps agents explain SwiftASB, choose an integration shape, and build SwiftUI, AppKit, and Swift package surfaces on top of SwiftASB.
- [x] Keep the plugin as a companion guidance surface rather than a runtime plugin: do not bundle an MCP server, duplicate SwiftASB source, or copy generated schema files into `socket`.
- [x] Keep Apple framework workflow rules delegated to `apple-dev-skills`, with this plugin focused on SwiftASB-specific explanation, decision support, integration, and troubleshooting.

### Tickets

- [x] Create `plugins/swiftasb-skills/` with its own `.codex-plugin/plugin.json` and authored `skills/` source.
- [x] Add first-slice skills for explaining SwiftASB, choosing an integration shape, and building a SwiftUI app on top of SwiftASB.
- [x] Add `swiftasb:build-appkit-app` for AppKit apps after the first slice proves useful.
- [x] Add `swiftasb:build-swift-package` for Swift package authors after the first slice proves useful.
- [x] Add an integration diagnostics skill for runtime discovery, app-server startup, threads, turns, approvals, diagnostics, MCP status, history reads, and live-test isolation.
- [x] Wire `swiftasb-skills` into the root Socket marketplace as a normal local child plugin.
- [x] Update root README and maintainer docs so users understand the split between the SwiftASB package source of truth and the Socket-hosted Codex guidance plugin.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py` and any child-plugin checks added by the new plugin.
- [x] Sync `swiftasb-skills` with current SwiftASB changes, starting from the live SwiftASB source and docs so the explanation, integration-shape, SwiftUI, AppKit, package, and diagnostics skills match the current client API and runtime behavior.
- [x] Refresh `swiftasb-skills` for SwiftASB `v1.6.0`, including plan-mode turn starts, `CodexThread.Agenda`, thread goal helpers, and plan/goal diagnostics across the existing skill set.

### Exit Criteria

- [x] The Socket marketplace exposes `swiftasb-skills` as an installable child plugin.
- [x] The new skills can help an agent explain SwiftASB to a user before implementation, including when SwiftASB is not the right fit.
- [x] The new skills guide SwiftUI, AppKit, and Swift package integrations without duplicating broad Apple framework guidance that belongs to `apple-dev-skills`.
- [x] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.

## Milestone 6: Dotnet skills plugin

### Status

Implemented

### Scope

- [x] Turn the placeholder `dotnet-skills` child plugin into an installable `.NET` guidance plugin.
- [x] Treat F# and C# as equal first-party `.NET` language choices in plugin metadata, skill descriptions, examples, scaffolding guidance, and diagnostics.
- [x] Keep the plugin as a companion guidance surface rather than a runtime plugin: do not bundle an MCP server, custom package manager, private template feed, or machine-local SDK state.

### Tickets

- [x] Record the detailed plugin plan in [`docs/maintainers/dotnet-skills-plugin-plan.md`](./docs/maintainers/dotnet-skills-plugin-plan.md).
- [x] Update `plugins/dotnet-skills/AGENTS.md` with the F#/C# parity policy and `.NET` validation expectations.
- [x] Update `plugins/dotnet-skills/.codex-plugin/plugin.json` so plugin metadata includes F# and avoids C#-only wording.
- [x] Add first-slice skills for project-shape choice, solution bootstrap, F# project implementation, C# project implementation, and test workflow.
- [x] Add second-slice skills for package workflow, diagnostics, ASP.NET Core services, F#/C# interop, CI, upgrades, and tooling/style alignment.
- [x] Switch the root marketplace entry for `dotnet-skills` from placeholder to installable only after real skill content exists.
- [x] Update root README and maintainer docs so users understand the new installable child plugin surface.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py` and any child-plugin checks added by the new plugin.

### Exit Criteria

- [x] The Socket marketplace exposes `dotnet-skills` as an installable child plugin.
- [x] The new skills can help an agent choose a `.NET` project shape before implementation.
- [x] The new skills guide F# and C# implementation without making either language a secondary path.
- [x] The testing guidance uses `dotnet test` as the stable command surface while respecting repo-local test framework choices.
- [x] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.

## Milestone 7: Python skills plugin expansion

### Status

Implemented

### Scope

- [x] Repair the `python-skills` child validator so it matches the current monorepo-owned child docs model without reintroducing a child README.
- [x] Record the detailed expansion plan in [`docs/maintainers/python-skills-plugin-plan.md`](./docs/maintainers/python-skills-plugin-plan.md).
- [x] Expand `python-skills` from scaffold-heavy coverage into ongoing project choice, implementation, diagnostics, packaging, tooling/style, CI, and upgrade workflows.
- [x] Keep the existing `uv`, FastAPI, FastMCP, and pytest skill surfaces intact unless a later cleanup deliberately renames or replaces one without leaving duplicate long-term surfaces.

### Tickets

- [x] Update `plugins/python-skills/scripts/validate_repo_metadata.py` and child tests so validation targets `AGENTS.md`, plugin metadata, and skill metadata instead of a removed child `README.md`.
- [x] Add `python-skills:choose-python-project-shape`.
- [x] Add `python-skills:build-python-project`.
- [x] Add `python-skills:diagnose-python-project`.
- [x] Add `python-skills:python-package-workflow`.
- [x] Add `python-skills:python-tooling-style-workflow`.
- [x] Add `python-skills:python-ci-workflow`.
- [x] Add `python-skills:python-upgrade-workflow`.
- [x] Keep `python-skills:uv-pytest-unit-testing` as the release-compatible pytest workflow name for now.
- [x] Update Python plugin metadata after the first new skill slice lands.
- [x] Run child validation with `uv run scripts/validate_repo_metadata.py`, `uv run pytest`, `uv run ruff check .`, and `uv run mypy .`.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.

### Exit Criteria

- [x] The child validator passes without requiring a child `README.md`.
- [x] The Python skill inventory covers project choice, implementation, diagnostics, packaging, tooling/style alignment, CI, and upgrades in addition to existing scaffold, integration, and pytest workflows.
- [x] The Python plugin guidance consistently uses `uv` for command examples and official documentation as the source of truth for Python packaging, pytest, Ruff, mypy, FastAPI, FastMCP, and CI behavior.
- [x] Root Socket docs, marketplace wiring, child validation, and root validation agree on the exported Python skill surface.

## Milestone 8: Server-Side Swift skills plugin

### Status

In Progress

### Scope

- [x] Add a Socket-hosted `server-side-swift` child plugin that owns server-side Swift workflow guidance separately from `apple-dev-skills`.
- [x] Keep the plugin as a guidance surface rather than a bundled runtime: do not add local daemons, template feeds, deployment services, or MCP servers until a later plan explicitly calls for that scope.
- [x] Keep Apple-platform app, simulator, preview, and Xcode project workflow rules delegated to `apple-dev-skills`, with this plugin focused on SwiftPM-first service work.
- [ ] Expand the plugin beyond the first Vapor workflow into a small family of framework, protocol, runtime, observability, and deployment-adjacent server-side Swift skills.

### Tickets

- [x] Create `plugins/server-side-swift/` with its own `.codex-plugin/plugin.json`, `AGENTS.md`, and authored `skills/` source.
- [x] Add `server-side-swift:vapor-server-workflow` as the first skill for Vapor service creation, route work, middleware, Fluent migrations, environment configuration, local run commands, tests, and deployment handoffs.
- [x] Wire `server-side-swift` into the root Socket marketplace as a normal local child plugin.
- [x] Add `server-side-swift:hummingbird-server-workflow` for Hummingbird services, including route composition, middleware, request/response modeling, local run commands, tests, and SwiftPM-first validation.
- [x] Add `server-side-swift:persistence-workflow` for server-side Swift persistence, including Fluent models, database migrations, query design, Hummingbird database handoffs, tests, and docs routing through official docs, GitHub sources, or checked Dash docsets.
- [x] Add an OpenAPI workflow for generating, serving, validating, or consuming OpenAPI descriptions in server-side Swift services without tying the skill to one web framework by default.
- [x] Add an RPC workflow for Swift service boundaries that may use JSON-RPC, gRPC, MCP-like transports, or framework-specific client/server contracts, with explicit guidance for when plain HTTP routes are the simpler fit.
- [ ] Add a SwiftNIO workflow for lower-level event-loop, channel, bootstrap, byte-buffer, back-pressure, and nonblocking-I/O work when a service needs NIO directly instead of a higher-level framework.
- [ ] Add Swift observability and tracing guidance that covers Swift Logging, Metrics, Distributed Tracing, and OpenTelemetry-style instrumentation for service diagnostics.
- [ ] Add a server authentication and authorization workflow covering Vapor and Hummingbird auth boundaries, sessions, JWT, OAuth/OIDC handoffs, password storage, middleware placement, and security-sensitive testing without duplicating client Keychain guidance.
- [ ] Add a server app-sync workflow covering sync contracts, conflict handling, incremental change feeds, idempotent writes, cursor/token semantics, background job handoffs, and API-shape coordination without absorbing the separate OpenAPI or RPC workflow.
- [x] Add a Docker workflow for server-side Swift packages, including Dockerfile shape, Compose-local development, Linux image concerns, environment configuration, and build/test handoffs.
- [x] Add an Apple Containerization workflow for Apple's container tooling, keeping it distinct from generic Docker guidance and tied to current official Apple documentation.
- [x] Update plugin metadata prompts and keywords as new server-side Swift skill surfaces ship.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py` after each metadata or marketplace-facing update.

### Exit Criteria

- [ ] The Socket marketplace exposes `server-side-swift` as an installable child plugin with metadata that matches its shipped skill inventory.
- [ ] The plugin gives agents clear framework-specific paths for Vapor, Hummingbird, and persistence work without duplicating generic SwiftPM or Apple-platform workflow guidance.
- [ ] Protocol, runtime, observability, tracing, Docker, and Apple Containerization guidance each has a clear owner skill or an explicit reason to stay backlog-only.
- [ ] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.

## Milestone 9: Rust skills plugin

### Status

Implemented

### Scope

- [x] Turn the placeholder `rust-skills` child plugin into an installable Rust guidance plugin.
- [x] Keep the plugin as a companion guidance surface rather than a runtime plugin: do not bundle an MCP server, custom package manager, private template feed, generated scaffold script, or machine-local toolchain state.
- [x] Keep Rust workflow guidance grounded in official Rust, Cargo, rustup, rustfmt, and Clippy documentation.

### Tickets

- [x] Record the detailed plugin plan in [`docs/maintainers/rust-skills-plugin-plan.md`](./docs/maintainers/rust-skills-plugin-plan.md).
- [x] Update `plugins/rust-skills/AGENTS.md` with Rust workflow policy and validation expectations.
- [x] Update `plugins/rust-skills/.codex-plugin/plugin.json` so plugin metadata describes shipped Rust guidance.
- [x] Add first-slice skills for project-shape choice, Cargo bootstrap, testing, and tooling/style alignment.
- [x] Add implementation skills for Rust CLI and library crate work.
- [x] Add package and CI workflow skills for publish-facing and automation guidance.
- [x] Switch the root marketplace entry for `rust-skills` from placeholder to installable only after real skill content exists.
- [x] Update root README and maintainer docs so users understand the new installable child plugin surface.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.

### Exit Criteria

- [x] The Socket marketplace exposes `rust-skills` as an installable child plugin.
- [x] The new skills can help an agent choose a Rust project shape before implementation.
- [x] The new skills guide Cargo bootstrap, CLI and library implementation, package preparation, CI alignment, testing, formatting, linting, and toolchain alignment without bundling broad runtime behavior.
- [x] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.

## Milestone 10: Expo inline native modules workflow

### Status

Implemented

### Scope

- [x] Add a narrow `web-dev-skills` workflow for Expo SDK 56+ inline native modules and `expo-type-information`.
- [x] Keep the skill docs-first and current-docs-first because Expo marks inline modules as experimental and the SDK 56 surface may change frequently.
- [x] Route Swift, Apple-platform API, Xcode, simulator, signing, and iOS validation details through `apple-dev-skills` instead of copying Apple workflow guidance into `web-dev-skills`.
- [x] Keep the first version as companion guidance only: do not bundle Expo, EAS, SourceKitten, native build tooling, an MCP server, template feed, or sample app.

### Tickets

- [x] Record the detailed plan in [`docs/maintainers/expo-inline-native-modules-skill-plan.md`](./docs/maintainers/expo-inline-native-modules-skill-plan.md).
- [x] Add `web-dev-skills:expo-inline-native-modules-workflow`.
- [x] Update `plugins/web-dev-skills/AGENTS.md` with Expo and React Native native-boundary guidance.
- [x] Update `plugins/web-dev-skills/.codex-plugin/plugin.json` metadata so the plugin advertises the Expo inline native module workflow.
- [x] Decide whether the root marketplace entry needs to move from placeholder to installable as part of the first implementation slice.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.

### Exit Criteria

- [x] The skill helps an agent inspect a live Expo app, verify SDK support, choose between inline modules, standalone Expo modules, config plugins, and direct native edits, then validate the chosen path.
- [x] The skill treats `Module.generated.ts` as volatile generated output and `Module.tsx` as the stable editable wrapper when using `expo-type-information`.
- [x] The skill requires current official Expo documentation for SDK 56 inline module and type generation behavior before making claims or edits.
- [x] Root Socket docs, marketplace wiring, and validation agree on the exported `web-dev-skills` surface.

Decision note: the root marketplace entry is installable now that `web-dev-skills` ships real skill content.

## Milestone 11: Codex Utilities plugin

### Status

In Progress

### Scope

- [x] Add a Socket-hosted `codex-utilities` child plugin for local Codex runtime utilities that do not belong to a language-specific skill pack, app integration, or repository-maintenance plugin.
- [x] Keep the first slice capture-only: record real `SessionStart` hook payloads before mutating thread titles.
- [x] Prefer Codex App Server metadata operations for future thread renaming instead of invoking `codex exec` as a separate agent run.
- [x] Add disabled-by-default `dry-run` and `rename` modes so the same hook can test title prefixing without changing the normal install behavior.
- [ ] Add thread-title mutation only after a real new-thread test confirms the captured `session_id` maps to the target thread id.

### Tickets

- [x] Create `plugins/codex-utilities/` with its own `.codex-plugin/plugin.json`, `AGENTS.md`, `hooks/`, `scripts/`, and local design note.
- [x] Add a `SessionStart` hook that captures stdin to a local JSONL runtime log.
- [x] Add a Node stdlib App Server control-socket client for opt-in `thread/name/set` tests.
- [x] Wire `codex-utilities` into the root Socket marketplace as a normal local child plugin.
- [x] Update root README so users can see the new installable plugin surface.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.
- [ ] Run a dry-run hook test from the Codex GUI and inspect `thread-title-decisions.jsonl`.
- [ ] Install or refresh the plugin locally, trust the hook, start a real new thread, and compare captured `session_id` with the created thread id.

### Exit Criteria

- [x] The Socket marketplace exposes `codex-utilities` as an installable child plugin.
- [ ] The first hook captures `SessionStart` payloads without writing captured data into the Socket repository.
- [ ] Thread-title automation has a confirmed target-thread identity before it calls `thread/name/set`.
- [x] Opt-in thread-title automation can be tested without invoking `codex exec` or starting a separate agent run.
- [x] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.

## Small Tickets

- [ ] Record issue-sized fixes, TODO/FIXME imports, and cleanup work that is too small or too unplanned for a milestone.

- [x] GitHub #61: Teach repo-maintenance prerelease GitHub metadata ([#61](https://github.com/gaelic-ghost/socket/issues/61))
- [x] GitHub #60: Apple Dev Skills workflow helper is missing PyYAML runtime dependency ([#60](https://github.com/gaelic-ghost/socket/issues/60))
- [x] Hardened `web-dev-skills:expo-inline-native-modules-workflow` with native-shape decision and validation reference tables.
- [x] Added Server-Side Swift ecosystem package preference guidance for Vapor, Vapor Community, and Hummingbird-aligned packages.

## Backlog Candidates

- [x] Add the first repo-local Socket Steward prototype as a Python `uv` project under `.agents/socket-steward`, using deterministic read-only audits plus an optional OpenAI Agents SDK `ask` path before any write, LaunchAgent, or app behavior.
- [x] Expand Socket Steward with a docs-sync planning command that emits structured recommended edits for README, CONTRIBUTING, AGENTS, ROADMAP, marketplace metadata, and child plugin guidance without applying them.
- [x] Add `docs/agents/` as the repo-local report surface and let Socket Steward write reviewable docs-sync proposal reports there without applying the proposed documentation edits.
- [x] Add a serialized Socket Steward `prepare docs-sync` workflow and first guarded `apply docs-sync --confirm` mode that refreshes proposal reports without mutating durable docs.
- [x] Extend `productivity-skills:maintain-project-roadmap` with explicit checklist ticket add/update flags so repo-local agents can delegate roadmap TODO mutations to the roadmap skill instead of duplicating roadmap editing logic.
- [ ] Add a read-only Socket Steward fan-out experiment for broad docs and guidance scans. Start with deterministic sharding by file count or total line count, keep workers read-only, merge findings into one bounded report, and compare the result against the single-process audit before deciding whether subagent fan-out belongs in the durable steward workflow.
- [ ] Add a guarded Socket Steward write mode only after the read-only audit and planning contracts are stable, with explicit approval boundaries for file edits, validation, git operations, release workflow, and future background execution.
- [x] Overhaul `agent-plugin-skills` so its docs, tests, generated bootstrap content, and sync audit logic target Codex/OpenAI plus the open `.agents/skills` discovery mirror only. Remove stale expectations for retired child maintainer docs such as reality-audit and install-surface docs, and keep the wording away from unsupported non-Codex or generic multi-agent surfaces.
- [x] Add a `productivity-skills:maintain-project-docs` umbrella workflow after `maintain-project-roadmap` owns small-ticket tracking. It should run the individual docs skills together, enforce the splits between `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `ACCESSIBILITY.md`, and `ROADMAP.md`, and prevent repeated content from drifting across files.
- [x] Add a first `productivity-skills:design-agent-automation-workflow` planning skill for agent and automation design. It chooses between Codex app automations, `codex exec`, Codex subagents, OpenAI Agents SDK services, LangGraph graphs, Hermes-specific workflows, or no automation yet while delegating stack-specific implementation to the owning plugin.
- [x] Added `productivity-skills:design-agent-eval-workflow` for agent, skill, prompt, and automation eval planning, and skewed automation guidance toward safe full automation with exact escalation gates instead of broad human review.
- [x] Create a quicker full-auto Socket patch-refresh script for trusted maintainer use. It should bump the shared patch version, validate metadata, satisfy release-ready and subtree gates, push `main` and any required subtree split, tag and publish the GitHub release, verify branch accounting, and run `codex plugin marketplace upgrade socket` as the final step.
- [x] Add root validator coverage for the first Swift Steward subagent role drafts, keeping custom-agent TOML parseable, read-only, name-aligned, and review-oriented before any write-capable steward workflow exists.
- [x] Set the first Swift Steward roles to a role-local `gpt-5.4-mini` default and document when read-heavy custom subagents should pin a smaller model versus deferring to the parent session.
- [x] Inventory bundled subagent role candidates across Socket plugins and rank the strongest read-heavy candidates before adding more `.codex/agents` files.
- [x] Add `productivity-skills:repo-docs-auditor` as the next bundled read-only custom-agent role. Keep it evidence-first across README, CONTRIBUTING, AGENTS, ACCESSIBILITY, ROADMAP, and command drift, and have it return review packets for the main thread to apply through the owner docs skills.
- [ ] Add `productivity-skills:code-slice-tracer` as a bounded code-reading custom-agent role for call-site tracing, test/doc correlation, and multi-slice explanation support without owning final prose or architecture-file writes.
- [ ] Add `agent-plugin-skills:skills-repo-guidance-sync` as a read-only custom-agent role for plugin-root policy audits, marketplace wording checks, Codex docs freshness, `.agents/skills` discovery mirrors, and generated guidance drift.
- [ ] Add privacy-fenced app plugin auditor roles only after their read/write boundaries are explicit: `things-app:things-route-auditor` for read-only Things route and digest planning, and `cardhop-app:cardhop-contact-auditor` for schema, health, route, and dry-run preview checks.
- [ ] Add language validation triager roles after one shared contract is agreed: `python-skills:python-validation-triager`, `rust-skills:rust-validation-triager`, and `dotnet-skills:dotnet-validation-triager`, each report-first and scoped to logs, manifests, CI, test, tooling, package, and upgrade evidence.
- [ ] Revisit maybe-later subagent roles only after the owning plugin surface justifies them: `productivity-skills:roadmap-triage-worker`, `productivity-skills:automation-plan-designer`, `swiftasb-skills:swiftasb-steward`, and `web-dev-skills:expo-native-boundary-scout`.
- [ ] Keep placeholder or write-heavy surfaces out of bundled roles for now: do not add `android-dev-skills:android-steward`, `spotify`, or a `maintain-project-repo` worker role until those surfaces have enough read-heavy workflow evidence and safe boundaries.
- [ ] Grow Swift Steward from read-heavy guidance-sync and repo-maintenance scans into reviewable patch artifacts that can be saved, edited, or applied by the main thread, then decide whether any apply-mode behavior belongs in the main thread, a guarded report workflow, or a future repo-local sidecar.
- [ ] Turn the placeholder `android-dev-skills` child plugin into an installable Android guidance plugin. It should cover Kotlin-first Android project work, Java interoperability or Java-only maintenance when a repo requires it, Gradle and Android Gradle Plugin alignment, emulator-aware validation, release readiness, and clear handoffs to existing mobile testing plugins instead of duplicating emulator tooling.
- [ ] Add an `mlx-skills` guidance plugin for Apple Silicon MLX project work. It should cover project-shape discovery, Python and Swift integration choices, model conversion or loading workflows, local performance validation, reproducibility notes, and clear boundaries with broader Python, Apple, and AI automation skills.
- [ ] Add a `coreml-skills` guidance plugin for Core ML model integration and maintenance. It should cover model packaging, conversion handoffs, Swift and Apple-platform app integration, on-device validation, performance and memory checks, release readiness, and boundaries with `apple-dev-skills` so generic Xcode or SwiftUI work stays owned there.
- [x] Add an `apple-dev-skills:appkit-app-architecture-workflow` skill so AppKit has a first-party architecture decision surface parallel to SwiftUI. It covers menu bar apps, status items, responder-chain menus, window and view-controller ownership, app and window restoration, AppKit MVC, object archiving and persistence choices, Observation with AppKit, and mixed AppKit/SwiftUI composition without steering agents inordinately toward either framework. Started from [`docs/agents/appkit-skills-coverage-plan.md`](./docs/agents/appkit-skills-coverage-plan.md).
- [ ] Complete Phase 2 of the Apple Dev Skills Socket migration soon. Treat `plugins/apple-dev-skills` as monorepo-owned source, remove Apple Dev Skills from subtree release gates, update Socket docs and duplicate-install guidance, add the compatibility marketplace smoke test, run full Socket validation, and publish the Socket release that makes the ownership change durable.
- [ ] Evaluate a centralized Socket validation setup that can check marketplace metadata, plugin manifests, child AGENTS shape, `SKILL.md` frontmatter, and `agents/openai.yaml` alignment from one root command while still leaving child-local tests where behavior needs them.
- [x] Track the remaining Speak Swiftly duplicate-enable repair behavior in the standalone `SpeakSwiftlyServer` plugin workflow rather than keeping the completed Socket catalog split open: [gaelic-ghost/SpeakSwiftlyServer#98](https://github.com/gaelic-ghost/SpeakSwiftlyServer/issues/98).

## History

- Added the first repo-local Socket Steward prototype under `.agents/socket-steward`, giving the superproject a Python and OpenAI Agents SDK maintainer-agent scaffold with offline docs, guidance, and marketplace audits before any write-capable or background-service behavior.
- Added Socket Steward's first docs-sync planner so the repo-local agent can produce structured read-only documentation alignment work before any guarded write mode exists.
- Added `docs/agents/` for repo-local agent report artifacts and limited Socket Steward proposal writes to that directory.
- Added serialized Socket Steward prepare/apply commands so maintainers can run audit, docs-sync planning, and proposal refresh in one guarded pass.
- Extended the roadmap maintainer skill with one-ticket add/update flags and updated automation-design guidance to prefer existing skills, plugins, scripts, and official workflow owners as the source of truth for workflow knowledge.
- Removed the stale Apple Dev Skills release-time subtree push gate after the standalone Apple Dev Skills repository became a compatibility marketplace pointer to Socket's canonical `plugins/apple-dev-skills` payload.
- Released `v6.7.0` after aggressively simplifying Socket documentation: root README and CONTRIBUTING split, child roadmap consolidation into root planning docs, child README collapse with user-owned `TBD` overview sections, nested maintainer doc cleanup, workflow atlas removal, and unsupported non-Codex surface removal.
- Queued future `mlx-skills` and `coreml-skills` guidance plugins for Apple Silicon ML and Core ML workflows.
- Audited AppKit coverage against SwiftUI and queued an Apple Dev Skills AppKit app-architecture workflow so menu bar apps, restoration, MVC, archiving, Observation, and mixed AppKit/SwiftUI work get first-class guidance.
- Implemented `apple-dev-skills:appkit-app-architecture-workflow` with AppKit ownership, menu bar, responder-chain, restoration, MVC, archiving, Observation, and mixed AppKit/SwiftUI references plus targeted tests.
- Added draft `swift-steward` and `server-swift-steward` custom-agent roles plus root validator coverage so the steward contracts remain read-only and review-oriented until a guarded draft-patch workflow exists.
- Tuned the Swift Steward custom-agent contracts and shared subagent guidance around a role-local `gpt-5.4-mini` default for bounded read-heavy scans, while keeping write ownership and harder reasoning in the main thread or stronger model choices.
- Tightened Swift Steward output around review packets with proposed patch sets and validation handoff so future draft-patch behavior has a stable report contract before any apply mode exists.
- Added a bundled subagent role candidate inventory covering docs audit, code tracing, plugin guidance sync, Things and Cardhop auditors, validation triage roles, and no-for-now placeholder plugins.
- Added the first Productivity Skills bundled custom-agent role, `repo-docs-auditor`, for read-only repo-document audits and review-packet planning before the main thread applies owner-doc skill edits.
- Added the placeholder `android-dev-skills` child plugin surface and queued a Kotlin-first Android guidance plugin for future Socket work.
- Published `apple-dev-skills` `v6.14.1` as the Phase 1 compatibility release: the standalone repository now points its marketplace at Socket's `plugins/apple-dev-skills` payload while preserving `codex plugin marketplace upgrade apple-dev-skills` for existing standalone users.
- Removed redundant monorepo-owned child root READMEs after making `AGENTS.md`, plugin manifests, skill metadata, MCP server READMEs, and root Socket docs the maintained documentation surfaces. `apple-dev-skills` keeps its public README because it remains subtree-managed and standalone-installable.
- Completed the Speak Swiftly plugin catalog split by exposing `speak-swiftly` from the canonical `gaelic-ghost/SpeakSwiftlyServer` Git-backed source, retiring the local `plugins/SpeakSwiftlyServer/` mirror, validating isolated marketplace install paths, and keeping standalone SpeakSwiftlyServer as the plugin payload source of truth.
- Completed the release and sync discipline milestone by aligning release-mode docs, subtree sync rules, shared-version workflow, release-ready gates, and marketplace refresh ordering around the current mixed monorepo model.
- Completed the subtree workflow hardening milestone by documenting subtree add, pull, and push paths, adding the root marketplace audit pass, and adding a public child plugin removal checklist.
- Completed [#35](https://github.com/gaelic-ghost/socket/issues/35) / [#37](https://github.com/gaelic-ghost/socket/issues/37) by hardening release and PR scripts around delayed GitHub state.
- Completed [#39](https://github.com/gaelic-ghost/socket/issues/39) by adding the Swift Package Index add-package gate and one-shot script around the documented `SwiftPackageIndex/PackageList` Add Package issue form.
- Planned a `swiftasb-skills` child plugin to help agents explain SwiftASB and build SwiftUI, AppKit, and Swift package integrations from a Socket-visible guidance surface.
- Added and exposed a `web-dev-skills` Expo inline native modules workflow for SDK 56+ inline Swift/Kotlin modules, `expo-type-information`, CNG/prebuild validation, and Apple Dev Skills handoffs.
- Updated `productivity-skills:maintain-project-repo` so heavy remote CI can be deferred after full local validation, branch push, PR creation, and initial check discovery, with Codex expected to use native thread Timer/Wakeup or heartbeat automation to resume the release instead of keeping an idle CI-waiting script open.
- Added root `docs/media` screenshot assets and README media guidance so the Codex plugin-directory catalog surface is visible without weakening text-first documentation.
- Added coordinated OpenAI Codex Hooks guidance across `agent-plugin-skills` and `productivity-skills`, with future `maintain-project-hooks` work tracked in the productivity roadmap.
- Added `productivity-skills:maintain-project-docs` as an umbrella documentation sweep that runs the owner README, CONTRIBUTING, AGENTS, ACCESSIBILITY, and ROADMAP workflows serially while auditing cross-document responsibility drift.
- Updated `socket` and plugin guidance so ordinary user installs and updates default to Git-backed Codex marketplace sources and official marketplace add/upgrade commands.
- Loosened coordinated Codex subagent guidance so skills preserve OpenAI's explicit-trigger model while allowing narrower workflow guidance, such as Codex Security repository-wide scans, to ask for and use subagents when the task depends on parallel file-pass review.
- Added coordinated Codex subagent guidance across `agent-plugin-skills` and `productivity-skills`, grounding skill wording in OpenAI's current explicit-trigger `subagents` model while keeping the root docs clear about why the pass belongs in `socket`.
- Prepared the `v6.1.0` minor release by adding the `maintain-project-api` productivity skill and keeping the monorepo-owned child docs, tests, and shared version surfaces aligned.
- Added explicit `standard` and `subtrees` release-mode guidance, including the pull-only `SpeakSwiftlyServer` rule for `socket` subtree sync.
- Published `apple-dev-skills` `v6.0.11` after adding direct regression coverage for SwiftPM-generated `.swiftpm/xcode/package.xcworkspace` classification and synced the released child state back into `socket`.
- Prepared the shared `v6.0.11` patch release after fixing `productivity-skills:maintain-project-repo` release-helper regressions for initial PR check discovery and approval-only review handling.
- Added the placeholder `plugins/spotify` child repository, wired it into the root marketplace, and kept the superproject docs honest about that new monorepo-owned plugin surface.
- Converted the former standalone `cardhop-mcp` checkout into the monorepo-owned `plugins/cardhop-app` child, added first-pass Codex plugin metadata plus a bundled MCP config, and recorded the new child as a normal `socket` marketplace entry.
- Retired the remaining `things-app` subtree-era wording from the root maintainer docs, removed the now-redundant local `things-app` and `things-app-mcp` sibling checkouts after verification, and prepared the `v0.11.1` plus `things-app v0.1.3` patch bump.
- Synced the `SpeakSwiftlyServer` subtree through the newer `v4.2.x` plugin and embedded live-speech updates, confirmed the root marketplace path still stayed valid, and kept the superproject release trail explicit with the `v0.11.0` bump.
- Re-checked the root packaging strategy against current OpenAI Codex plugin docs, added standalone repo-marketplace coverage for `apple-dev-skills`, normalized `SpeakSwiftlyServer`'s child marketplace path, and documented that the subtree-managed child plugins can be installed from their own clones without using `socket`.
- Added a root version-alignment script, switched `python-skills` to the monorepo-owned workflow, and documented the shared-version policy for the maintained manifest surfaces.
- Completed Milestone 1, `superproject docs and marketplace alignment`, by bringing the root README, AGENTS guidance, roadmap shape, and marketplace-path explanation back into alignment with the live mixed-monorepo model.
- Added the first root `ROADMAP.md` and established the checklist-style planning format for the superproject.
- Added a root marketplace-validation script and GitHub Actions workflow so `socket` now checks packaged plugin paths and manifest alignment instead of leaving that audit entirely manual.
- Added root `CONTRIBUTING.md`, `ACCESSIBILITY.md`, `LICENSE`, and `NOTICE` so the superproject's contributor, accessibility, and legal surfaces are explicit at the repository root.
- Collapsed the older subtree migration and plugin-alignment planning docs into this roadmap history plus the still-live root maintainer references once those plans had become historical rather than active operating guidance.
