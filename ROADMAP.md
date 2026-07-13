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
- [Milestone 11: AgentDeck plugin](#milestone-11-agentdeck-plugin)
- [Milestone 12: Xcode 27 agentic tooling workflows](#milestone-12-xcode-27-agentic-tooling-workflows)
- [Milestone 13: Reverse Engineering skills plugin](#milestone-13-reverse-engineering-skills-plugin)
- [Milestone 14: Core AI and Foundation Models workflow ownership](#milestone-14-core-ai-and-foundation-models-workflow-ownership)
- [Milestone 15: Android Dev Skills plugin](#milestone-15-android-dev-skills-plugin)
- [Milestone 16: Server-Side JVM skills plugin](#milestone-16-server-side-jvm-skills-plugin)
- [Milestone 17: Cross-agent skill and plugin portability](#milestone-17-cross-agent-skill-and-plugin-portability)
- [Milestone 18: Swift Lang shared language plugin](#milestone-18-swift-lang-shared-language-plugin)
- [Milestone 19: Project audit skills plugin](#milestone-19-project-audit-skills-plugin)
- [Milestone 20: Game Dev Skills plugin](#milestone-20-game-dev-skills-plugin)
- [Milestone 21: Cloud Deployment Skills plugin](#milestone-21-cloud-deployment-skills-plugin)
- [Milestone 22: Network Protocol Skills plugin](#milestone-22-network-protocol-skills-plugin)
- [Milestone 23: Cloud Inference Skills plugin](#milestone-23-cloud-inference-skills-plugin)
- [Milestone 24: Apple system integration, runtime evidence, and distribution workflows](#milestone-24-apple-system-integration-runtime-evidence-and-distribution-workflows)
- [Milestone 25: Apple Creator Studio operator workflows](#milestone-25-apple-creator-studio-operator-workflows)
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
- Keep the base `main` checkout clean for coordination and release verification; do implementation work in branch-backed worktrees unless Gale explicitly approves direct-main work.

## Milestone Progress

- Milestone 5: SwiftASB skills plugin - Completed
- Milestone 6: Dotnet skills plugin - Completed
- Milestone 7: Python skills plugin expansion - Completed
- Milestone 8: Server-Side Swift skills plugin - Completed
- Milestone 9: Rust skills plugin - Completed
- Milestone 10: Expo inline native modules workflow - Completed
- Milestone 11: AgentDeck plugin - In Progress
- Milestone 12: Xcode 27 agentic tooling workflows - In Progress
- Milestone 13: Reverse Engineering skills plugin - In Progress
- Milestone 14: Core AI and Foundation Models workflow ownership - Completed
- Milestone 15: Android Dev Skills plugin - Completed
- Milestone 16: Server-Side JVM skills plugin - In Progress
- Milestone 17: Cross-agent skill and plugin portability - Planned
- Milestone 18: Swift Lang shared language plugin - Completed
- Milestone 19: Project audit skills plugin - Planned
- Milestone 20: Game Dev Skills plugin - Completed
- Milestone 21: Cloud Deployment Skills plugin - Completed
- Milestone 22: Network Protocol Skills plugin - Completed
- Milestone 23: Cloud Inference Skills plugin - Completed
- Milestone 24: Apple system integration, runtime evidence, and distribution workflows - Planned
- Milestone 25: Apple Creator Studio operator workflows - Planned

## Milestone 5: SwiftASB skills plugin

### Status

Completed

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
- [x] Refresh `swiftasb-skills` for SwiftASB `v1.8.0`, including Codex CLI `0.142.x` compatibility guidance, the compatible `0.141.x` prior-minor window, `CodexTurnItem.Kind.sleep`, and ASBPresentation/ASBAppKit/ASBSwiftUI product guidance across the existing skill set.

### Exit Criteria

- [x] The Socket marketplace exposes `swiftasb-skills` as an installable child plugin.
- [x] The new skills can help an agent explain SwiftASB to a user before implementation, including when SwiftASB is not the right fit.
- [x] The new skills guide SwiftUI, AppKit, and Swift package integrations without duplicating broad Apple framework guidance that belongs to `apple-dev-skills`.
- [x] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.

## Milestone 6: Dotnet skills plugin

### Status

Completed

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

Completed

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
- [ ] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.

### Exit Criteria

- [x] The child validator passes without requiring a child `README.md`.
- [x] The Python skill inventory covers project choice, implementation, diagnostics, packaging, tooling/style alignment, CI, and upgrades in addition to existing scaffold, integration, and pytest workflows.
- [x] The Python plugin guidance consistently uses `uv` for command examples and official documentation as the source of truth for Python packaging, pytest, Ruff, mypy, FastAPI, FastMCP, and CI behavior.
- [x] Root Socket docs, marketplace wiring, child validation, and root validation agree on the exported Python skill surface.

## Milestone 8: Server-Side Swift skills plugin

### Status

Completed

### Scope

- [x] Add a Socket-hosted `server-side-swift` child plugin that owns server-side Swift workflow guidance separately from `apple-dev-skills`.
- [x] Keep the plugin as a guidance surface rather than a bundled runtime: do not add local daemons, template feeds, deployment services, or MCP servers until a later plan explicitly calls for that scope.
- [x] Keep Apple-platform app, simulator, preview, and Xcode project workflow rules delegated to `apple-dev-skills`, with this plugin focused on SwiftPM-first service work.
- [x] Expand the plugin beyond the first Vapor workflow into a small family of framework, protocol, runtime, observability, and deployment-adjacent server-side Swift skills.

### Tickets

- [x] Create `plugins/server-side-swift/` with its own `.codex-plugin/plugin.json`, `AGENTS.md`, and authored `skills/` source.
- [x] Add `server-side-swift:vapor-server-workflow` as the first skill for Vapor service creation, route work, middleware, Fluent migrations, environment configuration, local run commands, tests, and deployment handoffs.
- [x] Wire `server-side-swift` into the root Socket marketplace as a normal local child plugin.
- [x] Add `server-side-swift:hummingbird-server-workflow` for Hummingbird services, including route composition, middleware, request/response modeling, local run commands, tests, and SwiftPM-first validation.
- [x] Add `server-side-swift:persistence-workflow` for server-side Swift persistence, including Fluent models, database migrations, query design, Hummingbird database handoffs, tests, and docs routing through official docs, GitHub sources, or checked Dash docsets.
- [x] Add an OpenAPI workflow for generating, serving, validating, or consuming OpenAPI descriptions in server-side Swift services without tying the skill to one web framework by default.
- [x] Add an RPC workflow for Swift service boundaries that may use JSON-RPC, gRPC, MCP-like transports, or framework-specific client/server contracts, with explicit guidance for when plain HTTP routes are the simpler fit.
- [x] Add a SwiftNIO workflow for lower-level event-loop, channel, bootstrap, byte-buffer, back-pressure, and nonblocking-I/O work when a service needs NIO directly instead of a higher-level framework.
- [x] Add Swift observability and tracing guidance that covers Swift Logging, Metrics, Distributed Tracing, and OpenTelemetry-style instrumentation for service diagnostics.
- [x] Add a server authentication and authorization workflow covering Vapor and Hummingbird auth boundaries, sessions, JWT, OAuth/OIDC handoffs, password storage, middleware placement, and security-sensitive testing without duplicating client Keychain guidance.
- [x] Add a server app-sync workflow covering sync contracts, conflict handling, incremental change feeds, idempotent writes, cursor/token semantics, background job handoffs, and API-shape coordination without absorbing the separate OpenAPI or RPC workflow.
- [x] Add a Docker workflow for server-side Swift packages, including Dockerfile shape, Compose-local development, Linux image concerns, environment configuration, and build/test handoffs.
- [x] Add an Apple Containerization workflow for Apple's container tooling, keeping it distinct from generic Docker guidance and tied to current official Apple documentation.
- [x] Add a Fly.io deployment workflow for Vapor and Hummingbird services, including Dockerfile handoffs, `fly.toml`, secrets, health checks, Postgres attachment, process groups, and deploy validation.
- [x] Update Hummingbird guidance to prefer the official `hb` CLI for fresh apps, and record a Vapor 5 alpha adoption posture that keeps Vapor 4 as the stable default until Vapor 5 is stable.
- [x] Add `server-side-swift:bootstrap-hummingbird-service` and `server-side-swift:bootstrap-vapor-service` for CLI-first fresh service creation, repo-local `AGENTS.md` guidance assets, Hummingbird configuration support, Vapor `Environment`, Fluent ORM, PostgreSQL, CLI-generated Docker files, and Docker Compose local database defaults.
- [x] Update Hummingbird guidance for current `hb` Server and Lambda prompts, generated `swift-configuration`, OpenAPIHummingbird plus `hummingbird-lambda` Lambda shape, and the separate `swift-openapi-lambda` transport distinction.
- [x] Add `server-side-swift:sync-hummingbird-service-guidance` for existing Hummingbird repositories that need repo-local `AGENTS.md`, Codex local environment files, `hb` CLI assumptions, Server or Lambda shape, OpenAPI transport notes, and SwiftPM command guidance refreshed.
- [x] Update plugin metadata prompts and keywords as new server-side Swift skill surfaces ship.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py` after each metadata or marketplace-facing update.

### Exit Criteria

- [x] The Socket marketplace exposes `server-side-swift` as an installable child plugin with metadata that matches its shipped skill inventory.
- [x] The plugin gives agents clear framework-specific paths for Vapor, Hummingbird, and persistence work without duplicating generic SwiftPM or Apple-platform workflow guidance.
- [x] Protocol, runtime, observability, tracing, Docker, and Apple Containerization guidance each has a clear owner skill or an explicit reason to stay backlog-only.
- [x] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.

## Milestone 9: Rust skills plugin

### Status

Completed

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

Completed

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

## Milestone 11: AgentDeck plugin

### Status

In Progress

### Scope

- [x] Add a Socket-hosted `agentdeck` child plugin for local Codex runtime utilities that do not belong to a language-specific skill pack, app integration, or repository-maintenance plugin.
- [x] Keep the first slice capture-only: record real `SessionStart` hook payloads before mutating thread titles.
- [x] Prefer Codex App Server metadata operations for future thread renaming instead of invoking `codex exec` as a separate agent run.
- [x] Keep explicit `capture` and `dry-run` modes so the same hook can test title prefixing without changing thread metadata.
- [x] Enable thread-title mutation by default after a real new-thread test confirmed the captured `session_id` maps to the target thread id and Codex GUI hook settings provide the behavior toggle.
- [x] Prefix titles on the second `Stop` hook by default so Codex's own generated-title writer has settled before the plugin writes the project prefix.
- [x] Add a diagnostic `PostToolUse` hook log so title-generation timing can be compared against hook-visible tool activity.
- [ ] Add a desktop bridge MCP and skill surface that talks to the separate `AgentDeck` app instead of bundling a macOS app inside the plugin.
- [ ] Add Codex GUI restart request/cancel/status tools and a narrow skill that delegates waiting and final restart execution to `AgentDeck`.
- [ ] Add an agent configuration sync surface that lets `AgentDeck` discover, diff, and safely render compatible guidance/config for normal Codex, Xcode Codex, and Xcode Claude while `agentdeck` owns the agent-facing adapter and policy.
- [x] Record the Simulator browser and SwiftUI preview-host investigation plan, keeping `AgentDeck` as the prospective installed runtime and `agentdeck` as the Codex-facing adapter.

### Tickets

- [x] Create `plugins/agentdeck/` with its own `.codex-plugin/plugin.json`, `AGENTS.md`, `hooks/`, `scripts/`, and local design note.
- [x] Add a `SessionStart` hook that captures stdin to a local JSONL runtime log.
- [x] Add a Node stdlib App Server control-socket client for opt-in `thread/name/set` tests.
- [x] Wire `agentdeck` into the root Socket marketplace as a normal local child plugin.
- [x] Update root README so users can see the new installable plugin surface.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.
- [x] Run a hook test from the Codex GUI and inspect `thread-title-decisions.jsonl`.
- [x] Install or refresh the plugin locally, trust the hook, start a real new thread, and compare captured `session_id` with the created thread id.
- [x] Record the desktop bridge MCP and skill plan in `plugins/agentdeck/docs/desktop-bridge-mcp-skill-plan.md`.
- [ ] Add a bridge-status-only MCP server once `AgentDeck` exposes a local status endpoint.
- [ ] Add a `desktop-bridge` skill after the MCP status surface exists.
- [x] Extend the desktop bridge MCP and skill plan with Codex GUI restart coordination.
- [ ] Add a `codex-gui-restart` skill after `AgentDeck` exposes restart request, cancellation, and status endpoints.
- [ ] Implement `if-idle` restart requests before `when-idle`; keep automatic waiting blocked until the app has a supported thread-status source.
- [x] Record the AgentDeck agent configuration sync plan in `plugins/agentdeck/docs/agent-configuration-sync-plan.md`.
- [ ] Add a read-only bridge/status tool for agent configuration sync after `AgentDeck` can report detected target homes, versions, and compatibility-profile status.
- [ ] Add an agent-facing sync skill after the app exposes dry-run previews and backup-backed apply endpoints.
- [x] Record the Device Hub-backed Simulator browser and Swift Package preview-host plan in `plugins/agentdeck/docs/simulator-browser-preview-host-plan.md`.
- [ ] Verify, through a small local prototype, whether `AgentDeck` can use Xcode Device Hub as the operator-facing device selector while a local-only bridge captures and drives the selected normal iOS Simulator.
- [ ] Add a read-only Simulator mirror only after the prototype proves reliable frame capture, device identity, cleanup, and local-only transport behavior.
- [ ] Add guarded simulator input forwarding only after the read-only mirror and Device Hub handoff are proven.
- [ ] Evaluate a disposable Swift Package preview host with dynamic reload only after the mirror exists; keep Xcode Canvas and ordinary app-run workflows as first-class alternatives.

### Exit Criteria

- [x] The Socket marketplace exposes `agentdeck` as an installable child plugin.
- [ ] The first hook captures `SessionStart` payloads without writing captured data into the Socket repository.
- [ ] Thread-title automation has a confirmed target-thread identity before it calls `thread/name/set`.
- [x] Opt-in thread-title automation can be tested without invoking `codex exec` or starting a separate agent run.
- [x] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.
- [ ] Desktop bridge MCP and skill surfaces are available without packaging the signed macOS app inside the plugin cache.
- [ ] Codex GUI restart requests require explicit user intent, report pending/cancelled/blocked/completed status clearly, and never infer thread idleness from process state alone.
- [ ] Agent configuration sync previews omit unsupported keys by default, preserve target-owned files, and route writes through `AgentDeck` rather than direct plugin-side filesystem mutation.
- [ ] Any Simulator browser uses the selected standard CoreSimulator device, stays local by default, and has explicit teardown and device-ownership diagnostics.
- [ ] Any preview hot-reload host is disposable, Swift-Package-scoped, does not edit the user's project, and proves reload without relaunching the host process.

## Milestone 12: Xcode 27 agentic tooling workflows

### Status

In Progress

### Scope

- [x] Record the detailed implementation plan in [`docs/maintainers/xcode-27-agentic-tooling-plan.md`](./docs/maintainers/xcode-27-agentic-tooling-plan.md).
- [x] Add Xcode 27 coding-intelligence support to the existing `apple-dev-skills` plugin instead of creating a separate `apple-dev-beta` plugin.
- [ ] Keep ACP-specific exploration outside Socket unless a future Xcode workflow needs to mention Xcode's ACP agent setup.
- [ ] Update existing SwiftUI, AppKit, UIKit, Icon Composer, build, and testing guidance where Xcode 27 beta docs change real workflow behavior.

### Tickets

- [x] Add `apple-dev-skills:xcode-coding-intelligence-workflow` for Xcode Intelligence setup, Xcode-hosted agents, chat providers, ACP agent entries, Xcode-only config homes, command/tool permissions, and external-agent access through `xcrun mcpbridge`.
- [x] Add `apple-dev-skills:xcode-localization-workflow` for durable String Catalog setup, default bootstrap and guidance-sync coverage, source extraction, translator context, plural/device variants, XLIFF, human review, locale validation, and optional Xcode 27 agent-assisted translation.
- [x] Add `apple-dev-skills:xcode-device-hub-workflow` for simulated and physical device inspection, interaction, screenshots, videos, pairing, environment configuration, and diagnostics handoffs.
- [x] Extend `xcode-testing-workflow`, `xcode-device-hub-workflow`, and `xcode-debugger-mcp-workflow` with iOS XCUITest simulator-versus-physical-device decisions, destination evidence, bounded `devicectl` support, and physical-device debugging handoffs.
- [x] Add `apple-dev-skills:macos-window-management-workflow` for native SwiftUI/AppKit window scenes, chrome, drag regions, placement, resize/zoom, restoration, and validation.
- [x] Add `apple-dev-skills:apple-runtime-telemetry-workflow` for focused unified logging, privacy-aware `Logger` use, `OSSignposter`, and runtime-evidence handoffs.
- [ ] Add `apple-dev-skills:apple-beta-docs-triage-workflow` for new Apple beta drops, current-docs checks, availability gates, SDK requirements, and skill-routing decisions.
- [ ] Investigate the Xcode MCP surface against the current Xcode 27 beta, including `mcpbridge` command help, tool names, permission gates, session behavior, and differences from the last checked surface. Live beta `run-agent --dry-run codex` behavior was verified on 2026-06-23; a direct beta-scoped `codex skills export` attempt failed, and tool names, permission gates, project-session behavior, and runtime plug-in execution still need follow-up.
- [x] Add `apple-dev-skills:xcode-debugger-mcp-workflow` for active Xcode-session LLDB work and explicit Xcode 27 beta standalone `lldb-mcp` capability checks. Beta 3 (`27A5218g`) still fails before startup with the unresolved `lib_CompilerSwiftIDEUtils.dylib` rpath dependency, so the workflow keeps standalone server use blocked and routes normal work through Xcode's active debugger session.
- [ ] Add `apple-dev-skills:xcode-agent-plugin-workflow` now that the live Xcode 27 beta plug-in import paths are verified through installed Codex state, local folder import, and public Git URL import.
- [x] Refresh `xcode-build-run-workflow` and `xcode-testing-workflow` so setup and permissions route to the new coding-intelligence skill while build/test execution stays owned by the existing skills.
- [x] Document Xcode command-line toolchain selection for stable and beta Xcode installs, including command-scoped `DEVELOPER_DIR`, explicit global `xcode-select --switch`, restore steps, and current system-wide beta app paths.
- [ ] Refresh SwiftUI guidance for Xcode 27 APIs such as `ContentBuilder`, `@State` macro behavior, reorderable containers, generalized swipe actions, toolbar overflow, URL-backed documents, AsyncImage request/session APIs, and gesture input kinds.
- [ ] Refresh AppKit, UIKit, and Icon Composer guidance for the Xcode 27 beta changes recorded in the plan.

### Exit Criteria

- [ ] Apple Dev Skills exposes clear Xcode 27 agentic-tooling workflows without a separate beta plugin.
- [ ] Existing build and test workflows keep execution ownership and link to the setup workflow only where needed.
- [ ] Beta-specific claims are source-linked, dated, and clearly separated from stable guidance.
- [ ] Socket root docs, Apple Dev Skills metadata, and validation agree on the exported skill surface.

## Milestone 13: Reverse Engineering skills plugin

### Status

In Progress

### Scope

- [x] Add a Socket-hosted `reverse-engineering-skills` child plugin for binary inspection, decompilation, disassembly, symbol, and artifact-analysis workflows.
- [x] Keep the plugin as a guidance surface rather than a bundled runtime: do not add decompilers, disassemblers, debugger integrations, sample binaries, MCP servers, or machine-local tool state until a later plan explicitly calls for that scope.
- [x] Keep the skill surface technical: artifact triage, tool selection, copied working files, observed output, inferred behavior, and reproducible evidence notes.
- [x] Add first-slice skills for artifact triage and evidence notes before platform-specific decompilation workflows.
- [ ] Add platform and tool workflows after Gale has tried representative artifacts in Cutter, Ghidra, Malimite, Hopper, and adjacent tools.

### Tickets

- [x] Record the detailed plan in [`docs/maintainers/reverse-engineering-skills-plugin-plan.md`](./docs/maintainers/reverse-engineering-skills-plugin-plan.md).
- [x] Create `plugins/reverse-engineering-skills/` with `.codex-plugin/plugin.json` and `AGENTS.md`.
- [x] Wire `reverse-engineering-skills` into the root Socket marketplace as `NOT_AVAILABLE` while it was a placeholder.
- [x] Update root README and planning docs so users understand the shipped first skill surface.
- [x] Add `reverse-engineering:triage-artifact`.
- [x] Add `reverse-engineering:evidence-notes-workflow`.
- [ ] Add `reverse-engineering:tool-selection-workflow` after the first hands-on tool comparison.
- [ ] Add .NET, Unity, Apple binary, and decompiler-output review workflows after the first two common workflows land.
- [x] Switch the root marketplace entry to installable only after real skill content exists.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.

### Exit Criteria

- [x] The Socket marketplace exposes `reverse-engineering-skills` as an installable child plugin after real skill content lands.
- [x] The first skills can help an agent triage artifacts and write reproducible analysis notes before platform-specific decompilation work starts.
- [ ] Unity, .NET, Apple binary, and tool-selection workflows each have a clear owner skill or an explicit reason to stay backlog-only.
- [x] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.

## Milestone 14: Core AI and Foundation Models workflow ownership

### Status

Completed

### Scope

- [ ] Record the ownership split for Apple's app-facing Foundation Models workflows, Core AI model runtime and conversion workflows, and adjacent MLX/Core ML guidance before adding another installable child plugin or Apple Dev Skills surface.
- [ ] Keep stable Apple developer pages, beta WWDC26 Foundation Models claims, and Apple-owned open-source Core AI repositories separated by status and date checked.
- [ ] Decide whether Core AI work should be handled by Apple Dev Skills, a future Socket `coreai-skills` child plugin, a future `mlx-skills` or `coreml-skills` plugin, or a handoff to Apple-owned `coreai-models` skills.

### Tickets

- [x] Record the first source-linked plan in [`docs/maintainers/core-ai-foundation-models-skill-plan.md`](./docs/maintainers/core-ai-foundation-models-skill-plan.md).
- [ ] Design the first app-facing Foundation Models workflow only after the boundary between Apple Intelligence app integration and model-runtime work is clear.
- [ ] Evaluate Apple-owned Core AI GitHub repos before deciding whether Socket should duplicate, wrap, or simply hand off to their skill surfaces.
- [ ] Keep Music Intelligence and Media Analyzer as explicit open investigations until official Apple developer docs or source references are verified.
- [ ] Revisit the existing `mlx-skills` and `coreml-skills` backlog candidates once the Core AI ownership plan has enough evidence.

### Exit Criteria

- [ ] Socket has a clear skill/plugin ownership decision for Foundation Models, Private Cloud Compute, Core AI, MLX, Core ML, and adjacent Apple Intelligence surfaces.
- [ ] Any shipped skill distinguishes stable, beta, and exploratory/open-source claims and links to official Apple docs or Apple-owned source.

## Milestone 15: Android Dev Skills plugin

### Status

Completed

### Scope

- [x] Turn the placeholder `android-dev-skills` child plugin into an installable Android guidance plugin.
- [x] Keep Android guidance Kotlin-first while preserving Java interoperability and Java-only project support where repo defaults require it.
- [x] Make Kotlin Android guidance deep enough for common Compose and XML UI implementation tasks.
- [x] Keep emulator operation and device debugging handoffs aligned with the existing Android testing plugin instead of duplicating runtime tooling.
- [x] Include release automation routing in release-readiness guidance without starting publish workflows by default.
- [x] Keep Android app and platform guidance separate from server-side JVM backend and shared non-Android JVM library guidance.

### Tickets

- [x] Keep `plugins/android-dev-skills/` as a placeholder with `.codex-plugin/plugin.json` and `AGENTS.md`.
- [x] Keep the root Socket marketplace entry as `NOT_AVAILABLE` while it is a placeholder.
- [x] Record the detailed plan in [`docs/maintainers/android-dev-skills-plugin-plan.md`](./docs/maintainers/android-dev-skills-plugin-plan.md).
- [x] Add `android-dev:choose-project-shape` for Android app, library, multi-module, Kotlin, Java, Compose, XML view, test, lint, signing, release, and dependency-maintenance routing.
- [x] Add `android-dev:gradle-agp-workflow` for Gradle wrapper, Android Gradle Plugin, Kotlin plugin, Java toolchain, SDK, variants, flavors, signing config, namespace, dependency, and targeted task alignment.
- [x] Add `android-dev:build-kotlin-android` for Kotlin-first Android implementation, common Compose and XML UI tasks, coroutines, lifecycle-aware work, AndroidX, state, persistence, and validation.
- [x] Add `android-dev:java-android-workflow` for Java-only Android maintenance and Kotlin/Java interop boundaries.
- [x] Add `android-dev:testing-lint-workflow` for local unit tests, instrumentation and Compose UI test handoffs, lint configuration, targeted Gradle tasks, and emulator-aware validation handoffs.
- [x] Add `android-dev:release-readiness-workflow` for versioning, signing, release builds, R8/ProGuard, app bundles, APKs, Play delivery handoffs, permissions, privacy checks, and release automation routing.
- [x] Update plugin metadata after real skills land, including `skills`, keywords, prompts, and accurate installable descriptions.
- [x] Switch the root marketplace entry to installable only after real skill content exists.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.

### Exit Criteria

- [x] The Socket marketplace exposes `android-dev-skills` as an installable child plugin after real skill content lands.
- [x] The new skills can help an agent choose an Android project shape before implementation.
- [x] Kotlin-first Android guidance and Java interoperability are both clear without making Java or Scala backend work Android-owned.
- [x] Kotlin Android guidance is deep enough for common Compose and XML UI implementation tasks.
- [x] Emulator operation and device debugging stay delegated to the Android testing plugin instead of being duplicated here.
- [x] Release readiness includes release automation routing without starting publish workflows by default.
- [x] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.

## Milestone 16: Server-Side JVM skills plugin

### Status

In Progress

### Scope

- [x] Turn the placeholder `server-side-jvm` child plugin into an installable JVM backend guidance plugin.
- [x] Treat Java and Scala as equal first-party JVM language choices, with future Clojure support planned without renaming the plugin.
- [x] Prefer functional style where it fits the selected language and framework, especially for Scala and future Clojure guidance.
- [x] Keep server-side JVM backend and shared non-Android JVM library guidance separate from Android app and platform guidance.

### Tickets

- [x] Create `plugins/server-side-jvm/` with `.codex-plugin/plugin.json` and `AGENTS.md`.
- [x] Wire `server-side-jvm` into the root Socket marketplace as `NOT_AVAILABLE` while it is a placeholder.
- [x] Record the detailed plan in [`docs/maintainers/server-side-jvm-skills-plugin-plan.md`](./docs/maintainers/server-side-jvm-skills-plugin-plan.md).
- [x] Add `server-side-jvm:choose-service-shape` for Java, Scala, future Clojure, shared JVM libraries, Gradle, Maven, SBT, framework, package, CI, deployment, and diagnostics routing.
- [x] Add `server-side-jvm:build-tooling-workflow` for Gradle, Maven, SBT, Java toolchains, dependencies, multi-module boundaries, test, package, and local run commands.
- [x] Add `server-side-jvm:build-java-service` for idiomatic Java backend implementation.
- [x] Add `server-side-jvm:build-scala-service` for idiomatic Scala backend implementation with functional design treated as first-class.
- [x] Add `server-side-jvm:testing-workflow` for Gradle, Maven, SBT, JUnit, ScalaTest, MUnit, unit, integration, contract, service-level tests, and readable failure summaries.
- [ ] Add package/runtime, persistence, observability, CI, and upgrade workflows after the first skill slice lands.
- [ ] Keep `server-side-jvm:build-clojure-service` as a future candidate until the Java and Scala foundations are stable.
- [x] Update plugin metadata after real skills land, including `skills`, keywords, prompts, and accurate installable descriptions.
- [x] Switch the root marketplace entry to installable only after real skill content exists.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.

### Exit Criteria

- [x] The Socket marketplace exposes `server-side-jvm` as an installable child plugin after real skill content lands.
- [x] The new skills can help an agent choose a JVM backend shape before implementation.
- [x] Java and Scala guidance are first-class, with future Clojure support planned without renaming the plugin.
- [x] Android app guidance stays owned by `android-dev-skills`; backend and shared non-Android JVM library guidance stays owned by `server-side-jvm`.
- [x] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.

## Milestone 17: Cross-agent skill and plugin portability

### Status

Planned

### Scope

- [x] Record the first source-linked platform comparison in [`docs/maintainers/agent-portability-options.md`](./docs/maintainers/agent-portability-options.md).
- [x] Focus the first implementation pass on locally installed Xcode 27 beta and OpenCode CLI/Desktop, with Zed deferred until the first source-of-truth and export decisions are proven.
- [x] Record the detailed Xcode install-support plan in [`docs/maintainers/xcode-plugin-install-support-plan.md`](./docs/maintainers/xcode-plugin-install-support-plan.md).
- [ ] Treat Agent Skills as the first portability layer while keeping Codex plugins, hooks, MCP registration, custom agents, and host package formats as target-specific adapters.
- [ ] Keep Socket's root Codex marketplace model intact until a concrete non-Codex package or export target proves it needs a broader distribution abstraction.
- [x] Rename `agent-plugin-skills` to `agent-portability-skills` so the child plugin name matches the cross-host compatibility role.
- [ ] Keep Socket Steward tied into this milestone as the repo-local audit, plan, and proposal engine, while `agent-portability-skills` owns reusable agent-facing portability workflows.
- [ ] Route complex local orchestration through AgentUtils once that app exposes supported discovery, dry-run, backup, and apply contracts instead of expanding Socket plugin payloads into broad machine-management code.
- [ ] Keep Hermes Agent support research-blocked until an official documentation or source repository is identified.

### Tickets

- [ ] Add a root portability inventory command that reports every `SKILL.md`, `.codex-plugin/plugin.json`, `.mcp.json`, hook, app config, and custom-agent definition with host-specific compatibility notes.
- [ ] Add `agent-portability-skills:audit-agent-surface-portability`.
- [ ] Add `agent-portability-skills:design-agent-host-adapter`.
- [ ] Add `agent-portability-skills:maintain-codex-plugin-surface`.
- [ ] Add common skill constraint checks for Codex and OpenCode first, then include Zed as an informational follow-up target.
- [ ] Add a dry-run OpenCode skills export plan for `.agents/skills` and `.opencode/skills`, starting with project-local fixtures and temporary homes.
- [ ] Evaluate OpenCode adapters for `.opencode/skills`, `opencode.json`, MCP config, permissions, and TypeScript plugin modules.
- [ ] Evaluate Xcode 27 beta adapters using command-scoped `DEVELOPER_DIR` for the intended system-wide beta app, including Xcode-launched Codex configuration, MCP bridge behavior, and Xcode plug-in imports through the official Settings UI. Initial live beta bridge and plug-in import evidence was captured on 2026-06-23.
- [ ] Add a Socket-to-Xcode install support assessment that classifies each child plugin across Xcode-launched Codex, Xcode internal plug-ins, and external agents using Xcode MCP.
- [ ] Add disposable Xcode import fixture generation for skill-only, skill-plus-MCP, and hook-recognition probes.
- [ ] Capture a public Socket Git URL import matrix from Xcode Beta before claiming user-facing Xcode install support.
- [ ] Runtime-validate representative Xcode imports before claiming hooks, MCP servers, app config, or custom-agent behavior works inside Xcode.
- [x] Record Zed Codex external-agent compatibility evidence. Local testing on 2026-06-26 showed Zed's bundled `codex-acp` session running with `__CFBundleIdentifier=dev.zed.Zed`, inherited `HOME=/Users/galew`, no explicit `CODEX_HOME`, Socket plugins at `7.2.1`, and the normal Codex MCP list available.
- [ ] Evaluate Zed Agent native adapters separately from Codex-in-Zed, including Zed skills roots, Zed MCP configuration, and any export or install path that should stay distinct from Codex plugin marketplace guidance.
- [ ] Evaluate Claude Code adapters for `.claude/skills`, `.claude/agents`, project settings, MCP settings, and plugin policy after the Xcode and OpenCode first pass.
- [ ] Add temporary-home smoke tests for any adapter that becomes write-capable.

### Exit Criteria

- [ ] Socket can report which authored skills are portable without changing installed user state.
- [ ] At least one OpenCode dry-run can show exactly what would be added, skipped, or transformed for a non-Codex host.
- [x] Xcode 27 beta support claims are backed by explicit beta-toolchain evidence rather than the default Xcode 26.5 command-line selection.
- [x] Docs clearly distinguish common Agent Skills from Codex plugins, Claude Code plugins, OpenCode plugins, Xcode plug-ins, Zed extensions, and MCP servers.
- [ ] No non-Codex support claim is user-facing unless it is backed by official docs, local smoke evidence, or both.

## Milestone 18: Swift Lang shared language plugin

### Status

Completed

### Scope

- [x] Add a Socket-hosted `swift-lang` child plugin for shared Swift language guidance across Apple apps, server-side Swift services, Swift packages, command-line tools, and libraries.
- [x] Keep the plugin as a normal marketplace plugin rather than a hidden include layer for `apple-dev-skills` or `server-side-swift`.
- [x] Move shared Swift style, formatting, source organization, modernization, and cleanup guidance into a dedicated language layer while preserving Apple Dev's standalone install behavior during the first migration release.
- [x] Encode Gale's preferred Swift style: Swifty, ergonomic, human-friendly APIs; functional data modeling; composable pipelines; clear monadic flow where practical; compact fluent chains when they improve readability; and explicit fallbacks when imperative code is clearer.

### Tickets

- [x] Record the detailed plan in [`docs/maintainers/swift-lang-plugin-plan.md`](./docs/maintainers/swift-lang-plugin-plan.md).
- [x] Create `plugins/swift-lang/` with `.codex-plugin/plugin.json`, `AGENTS.md`, and authored `skills/` source.
- [x] Add `swift-lang:swift-api-style-workflow` for API naming, call-site ergonomics, access control, typed result shapes, consistency across sibling APIs, and human-friendly errors.
- [x] Add `swift-lang:swift-functional-pipelines-workflow` for functional data modeling, `Optional`, `Result`, `throws`, `async throws`, `AsyncSequence`, chained transforms, and monadic composition boundaries.
- [x] Add `swift-lang:swift-error-handling-style-workflow` for language-level failure-shape decisions, typed throws guidance, domain errors, Cocoa bridging, and concise diagnostics.
- [x] Add `swift-lang:swift-format-style-workflow` for SwiftFormat, SwiftLint, formatter/linter responsibility, style defaults, Git hooks, and CI guidance.
- [x] Add `swift-lang:swift-source-organization-workflow` for file splitting, feature/layer layout, extension-file extraction, `// MARK:` discipline, file headers, source cleanup ledgers, and stricter split thresholds.
- [x] Add `swift-lang:swift-modernization-cleanup-workflow` for complete modernization passes that sequence formatting, source inventory, file splitting, API cleanup, pipeline cleanup, concurrency cleanup, tests, docs handoffs, and validation.
- [x] Wire `swift-lang` into the root Socket marketplace as an installable child plugin.
- [x] Update Apple Dev and Server-Side Swift guidance to hand off shared Swift cleanup work to `swift-lang` when it is available.
- [x] Keep Apple Dev's existing `format-swift-sources` and `structure-swift-sources` available during the first release so standalone Apple-only installs do not break.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py` and any new child-plugin validation added for `swift-lang`.

### Exit Criteria

- [x] The Socket marketplace exposes `swift-lang` as an installable child plugin.
- [x] The plugin gives agents clear Swift language guidance without duplicating Apple-platform or server-framework ownership.
- [x] The functional Swift style policy is explicit enough to guide implementation, review comments, and modernization passes.
- [x] Apple Dev and Server-Side Swift guidance can route shared Swift cleanup work to `swift-lang` while preserving standalone Apple-only behavior for the first migration release.

Implemented Milestone 18 by adding the `swift-lang` child plugin with shared Swift language skills, wiring it into the Socket marketplace, documenting the Swift language ownership split, preserving Apple Dev's standalone formatting and structure skills, and validating the plugin, skill metadata, root marketplace, and Apple Dev docs.

## Milestone 19: Project audit skills plugin

### Status

Planned

### Scope

- [x] Record the first plugin plan in [`docs/maintainers/project-audit-skills-plugin-plan.md`](./docs/maintainers/project-audit-skills-plugin-plan.md).
- [ ] Decide whether unfamiliar-project exploration, architecture mapping, quality grading, adoption-risk evaluation, and slop-risk review belong in a dedicated `project-audit-skills` child plugin or as a focused `productivity-skills` expansion.
- [ ] Keep the first version guidance-only unless repeated use proves that a runtime scanner, MCP server, or structured report generator is worth the additional surface.
- [ ] Route stack-specific findings to the existing language and platform plugins instead of duplicating Swift, Python, Rust, JVM, Android, web, or reverse-engineering guidance.

### Tickets

- [ ] Create `plugins/project-audit-skills/` only after the plugin boundary is approved.
- [ ] Add `project-audit:explore-project` for read-only project intake maps.
- [ ] Add `project-audit:audit-project-quality` for evidence-backed quality, maintainability, and slop-risk grading.
- [ ] Add later skills for architecture mapping, adoption-risk decisions, and remediation planning after the first two workflows prove useful.
- [ ] Wire the plugin into the root marketplace as `NOT_AVAILABLE` while it is a placeholder, then switch it to installable only after real skill content exists.
- [ ] Update root README and ROADMAP when the plugin becomes installable.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.

### Exit Criteria

- [ ] Socket has a clear ownership decision for unfamiliar-project intake and quality grading.
- [ ] The first workflows produce evidence-backed maps and grades without making repository changes by default.
- [ ] Stack-specific implementation advice routes to owning Socket plugins.
- [ ] Root Socket docs, marketplace wiring, and validation agree on the exported project-audit surface.

## Milestone 20: Game Dev Skills plugin

### Status

Completed

### Scope

- [x] Add a Socket-hosted `game-dev-skills` child plugin for game-specific authoring, rendering-stack choice, simulation, input, haptics, profiling handoffs, and validation guidance.
- [x] Keep the first slices Apple-platform-first rather than a broad engine plugin: SpriteKit, SceneKit, GameplayKit simulation, Game Controller input, Core Haptics game feedback, Xcode game profiling, and Apple game-stack routing.
- [x] Keep the plugin as a companion guidance surface rather than a runtime plugin: do not bundle a game engine, template feed, simulator wrapper, profiler automation, MCP server, or local game runtime.
- [x] Keep generic Swift, Xcode project integrity, simulator, signing, asset-catalog mechanics, and Apple docs exploration delegated to `apple-dev-skills` and shared Swift language guidance delegated to `swift-lang`.

### Tickets

- [x] Record the detailed plan in [`docs/maintainers/game-dev-skills-plugin-plan.md`](./docs/maintainers/game-dev-skills-plugin-plan.md).
- [x] Create `plugins/game-dev-skills/` with `.codex-plugin/plugin.json`, `AGENTS.md`, and authored `skills/` source.
- [x] Add `game-dev-skills:choose-apple-game-stack`.
- [x] Add `game-dev-skills:spritekit-game-workflow`.
- [x] Add `game-dev-skills:scenekit-game-workflow`.
- [x] Add `game-dev-skills:gameplaykit-simulation-workflow`.
- [x] Add `game-dev-skills:game-controller-input-workflow`.
- [x] Add `game-dev-skills:core-haptics-game-feedback-workflow`.
- [x] Add `game-dev-skills:xcode-game-profiling-workflow`.
- [x] Keep `game-dev-skills:metal-game-rendering-workflow` on the roadmap for a later shader and Metal rendering architecture slice.
- [x] Wire `game-dev-skills` into the root Socket marketplace as an installable child plugin.
- [x] Update root README and ROADMAP so users understand the new plugin surface.
- [x] Run skill-folder validation and plugin-manifest validation for the new child plugin.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.

### Exit Criteria

- [x] The Socket marketplace exposes `game-dev-skills` as an installable child plugin.
- [x] The first skill slices can route and guide Apple game work across SpriteKit, SceneKit, GameplayKit simulation, Game Controller input, Core Haptics feedback, Xcode game profiling, and Apple Dev Skills handoffs.
- [x] The plugin boundary is clear enough that reverse-engineering Unity artifacts stay with `reverse-engineering-skills`, generic Apple mechanics stay with `apple-dev-skills`, and game-specific authoring/profiling work stays here.
- [x] Root Socket docs, marketplace wiring, and validation agree on the exported game-dev skill surface.

Completed Milestone 20 by adding the `game-dev-skills` child plugin, shipping the Apple-platform game-development workflow slices, wiring the Socket marketplace entry, documenting the plugin boundary, and validating skill metadata, plugin metadata, and root marketplace wiring. Metal rendering and shader architecture remain planned as a later dedicated slice.

## Milestone 21: Cloud Deployment Skills plugin

### Status

Completed

### Scope

- [x] Add a thin Socket-hosted `cloud-deployment-skills` child plugin for cloud provider routing, official provider plugin selection, credential and mutation boundary checks, and cross-provider deployment handoffs.
- [x] Delegate AWS MCP configuration, AWS CLI setup, AWS SAM setup, and curated AWS skill content to the official [`aws/agent-toolkit-for-aws`](https://github.com/aws/agent-toolkit-for-aws) marketplace and its `aws-core` plugin.
- [x] Keep framework-specific deployment implementation in the owning stack plugins, such as Server-Side Swift Fly.io deployment guidance.
- [x] Keep the first Socket slice guidance-only: do not bundle AWS MCP config, copied AWS skills, credential setup scripts, provider templates, or local cloud state.

### Tickets

- [x] Record the detailed plan in [`docs/maintainers/cloud-deployment-skills-plugin-plan.md`](./docs/maintainers/cloud-deployment-skills-plugin-plan.md).
- [x] Create `plugins/cloud-deployment-skills/` with `.codex-plugin/plugin.json`, `AGENTS.md`, an icon asset, and authored `skills/` source.
- [x] Add `cloud-deployment-skills:cloud-deployment-routing-workflow` for provider routing, AWS Agent Toolkit handoff, mutation boundaries, and validation choices.
- [x] Wire `cloud-deployment-skills` into the root Socket marketplace as an installable child plugin.
- [x] Update root README and ROADMAP so users understand the new plugin surface and the AWS delegation decision.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.

### Exit Criteria

- [x] The Socket marketplace exposes `cloud-deployment-skills` as an installable child plugin.
- [x] AWS work routes to the official AWS Agent Toolkit for AWS by default instead of duplicated Socket-owned AWS MCP, AWS CLI, or AWS SAM setup guidance.
- [x] The plugin boundary is clear enough for future provider slices without absorbing framework-specific deployment workflows.
- [x] Root Socket docs, marketplace wiring, and validation agree on the exported cloud-deployment skill surface.

Completed Milestone 21 by adding the `cloud-deployment-skills` child plugin, shipping the provider-routing workflow, wiring the Socket marketplace entry, documenting the AWS Agent Toolkit delegation, and keeping future provider expansion scoped to small official-tool routing slices.

## Milestone 22: Network Protocol Skills plugin

### Status

Completed

### Scope

- [x] Add a Socket-hosted `network-protocol-skills` child plugin that owns protocol-level routing and diagnostics separately from stack-specific implementation plugins.
- [x] Cover modern application transports and real-time protocols, including HTTP/3, QUIC, WebRTC, and Media over QUIC.
- [x] Keep protocol maturity explicit: QUIC and HTTP/3 are RFC-backed, WebRTC uses W3C and IETF standards plus runtime-specific behavior, and Media over QUIC remains draft-driven.
- [x] Keep implementation handoffs clear for `server-side-swift`, `rust-skills`, `python-skills`, `server-side-jvm`, `web-dev-skills`, `apple-dev-skills`, `android-dev-skills`, and `cloud-deployment-skills`.

### Tickets

- [x] Create `plugins/network-protocol-skills/` with `.codex-plugin/plugin.json`, `AGENTS.md`, an icon asset, and authored `skills/` source.
- [x] Add `network-protocol-skills:choose-network-transport` for choosing HTTP, SSE, WebSocket, HTTP/3, direct QUIC, WebRTC, MoQ, gRPC/RPC, or mixed transport shapes.
- [x] Add `network-protocol-skills:http3-quic-workflow` for HTTP/3, QUIC, ALPN, Alt-Svc, UDP reachability, TLS, datagrams, and fallback planning.
- [x] Add `network-protocol-skills:realtime-media-over-quic-workflow` for MoQ draft-state checks, relay/client/server topology, media packaging, live latency, and fallback planning.
- [x] Add `network-protocol-skills:webrtc-workflow` for WebRTC signaling, ICE, STUN/TURN, DTLS, SRTP, data channels, media devices, SFU/MCU topology, and runtime constraints.
- [x] Add `network-protocol-skills:network-protocol-diagnostics` for evidence-first diagnosis across HTTP version negotiation, QUIC, WebRTC, MoQ, proxies, CDNs, firewalls, NAT, qlog, and packet captures.
- [x] Wire `network-protocol-skills` into the root Socket marketplace as an installable child plugin.
- [x] Add icon assets to the new plugin and to existing Socket plugins that were missing manifest icon fields.
- [x] Update root README, CONTRIBUTING, and ROADMAP so users and maintainers understand the new plugin surface.
- [x] Run skill-folder validation and root metadata validation.

### Exit Criteria

- [x] The Socket marketplace exposes `network-protocol-skills` as an installable child plugin.
- [x] The shipped skills route and guide protocol work across MoQ, HTTP/3, QUIC, WebRTC, transport selection, and diagnostics without absorbing stack-specific implementation ownership.
- [x] Existing Socket plugin manifests that lacked icons now point at repo-owned icon assets.
- [x] Root Socket docs, marketplace wiring, and validation agree on the exported network-protocol skill surface.

Completed Milestone 22 by adding the `network-protocol-skills` child plugin, shipping five protocol and diagnostics workflows, wiring the Socket marketplace entry, adding missing plugin icon assets, and keeping implementation handoffs delegated to the owning stack plugins.

## Milestone 23: Cloud Inference Skills plugin

### Status

Completed

### Scope

- [x] Add a Socket-hosted `cloud-inference-skills` child plugin for cloud AI inference, model training, model conversion, and GPU infrastructure routing.
- [x] Prefer Gale's familiar provider lanes when they fit: Runpod for quick GPU Pods, Serverless endpoints, Flash, and agent-managed resources; Hugging Face for model, dataset, conversion, endpoint, Space, and Hub-native workflows; AWS for existing account, IAM, S3, Lambda, SageMaker, Bedrock, ECS, EKS, and Batch surfaces.
- [x] Include Vast.ai for cheap flexible GPU rentals and CoreWeave for cluster-shaped GPU infrastructure without pretending either is the default for quick experiments.
- [x] Keep official-provider ownership explicit: bundle Runpod's official MCP config, install Runpod's upstream `companion-clis`, `flash`, and `runpodctl` skills through `npx skills add runpod/skills`, and hand Hugging Face/AWS work to their first-party plugins and CLIs when those fit.

### Tickets

- [x] Record the detailed plan in [`docs/maintainers/cloud-inference-skills-plugin-plan.md`](./docs/maintainers/cloud-inference-skills-plugin-plan.md).
- [x] Create `plugins/cloud-inference-skills/` with `.codex-plugin/plugin.json`, `.mcp.json`, `AGENTS.md`, an icon asset, and authored `skills/` source.
- [x] Add `cloud-inference-skills:cloud-inference-routing-workflow` for provider selection, model/workload triage, credential boundaries, cost boundaries, mutation checks, and validation choices.
- [x] Bundle Runpod's official `runpod` and `runpod-docs` MCP server configuration without committing API keys.
- [x] Install Runpod's upstream `companion-clis`, `flash`, and `runpodctl` skills into the exported plugin `skills/` tree, with `.agents/skills` kept as a symlink discovery mirror.
- [x] Wire `cloud-inference-skills` into the root Socket marketplace as an installable child plugin.
- [x] Update root README, CONTRIBUTING, and ROADMAP so users and maintainers understand the new plugin surface.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.

### Exit Criteria

- [x] The Socket marketplace exposes `cloud-inference-skills` as an installable child plugin.
- [x] The shipped skill routes cloud inference and GPU work across Runpod, Hugging Face, AWS, Vast.ai, CoreWeave, and adjacent providers without absorbing provider-specific setup owned by official plugins and CLIs.
- [x] Runpod MCP config is available through the plugin, while Runpod's upstream skills are exported through `skills/` and tracked by `skills-lock.json`.
- [x] Root Socket docs, marketplace wiring, and plugin metadata agree on the exported cloud inference surface.

Completed Milestone 23 by adding the `cloud-inference-skills` child plugin, shipping the provider-routing workflow, bundling Runpod MCP server configuration, installing the upstream Runpod skill mirror, adding the neon cloud GPU icon, wiring the Socket marketplace entry, and documenting first-party Runpod, Hugging Face, and AWS handoffs.

## Milestone 24: Apple system integration, runtime evidence, and distribution workflows

### Status

Planned

### Scope

- [ ] Expand the existing `apple-dev-skills` payload with five focused workflows where the installed OpenAI-curated Apple skills provide material coverage that Socket does not yet own.
- [ ] Keep each workflow docs-first, grounded in current Apple documentation and real local/Xcode evidence; use the installed curated skills only as task-shape inspiration, not copied source material.
- [ ] Preserve existing owners: Xcode build/run and testing retain workspace execution, SwiftUI architecture retains component and scene design, AppKit architecture retains AppKit ownership, and provisioning retains account-side certificate/profile automation.
- [ ] Keep the first slice guidance-only. Do not bundle a simulator browser server, ETTrace helper, release service, signing credential manager, or app-runtime daemon.

### Tickets

- [ ] Add `apple-dev-skills:app-intents-workflow` for choosing and implementing narrow App Intent, App Entity, App Shortcut, and system-surface integrations. Cover Siri, Shortcuts, Spotlight, widgets, controls, deep-link or in-app handoff, availability, privacy, and validation; hand Xcode target, extension, build, and simulator work to the existing Xcode workflows.
- [ ] Add `apple-dev-skills:swiftui-liquid-glass` for iOS and macOS Liquid Glass decisions, native API use, modifier ordering, container grouping, interactive affordances, shape consistency, availability checks, and non-glass fallbacks. Keep it separate from general SwiftUI architecture because it owns a version-sensitive visual-system contract rather than component ownership.
- [ ] Add `apple-dev-skills:swiftui-performance-audit` for code-first diagnosis of invalidation fan-out, unstable identity, heavy body work, layout churn, image cost, and broad animation. Require a clear distinction between suspected code smells and trace-backed evidence, then hand Instruments and `xctrace` capture to `xcode-testing-workflow` or `swift-package-testing-workflow`.
- [ ] Add `apple-dev-skills:ios-runtime-forensics-workflow` with explicit `performance-trace` and `memory-graph` modes for simulator ETTrace/symbolication and memgraph/leak ownership evidence. Keep it focused on reproducible before/after runtime proof, and route normal simulator build, launch, UI driving, and logs through `xcode-build-run-workflow`.
- [ ] Add `apple-dev-skills:macos-distribution-workflow` for exported-artifact inspection, signing identities, entitlements, hardened runtime, nested-code signatures, Gatekeeper assessment, notarization readiness/failure classification, stapling, and release-only validation. Keep developer-account provisioning, certificate/profile creation, and Xcode project signing changes with `apple-developer-provisioning-workflow` and `xcode-build-run-workflow`.
- [ ] Add `apple-dev-skills:tips-helpviewer-workflow` for consistent local discovery of user guides for installed Apple apps. Use the `com.apple.helpviewer` Tips catalog as the primary UI target rather than the empty `com.apple.tips` shell observed on this Mac; route exact app/version help searches through the catalog, verify the opened guide matches the installed app, and keep official in-app Help, Xcode-local docs, Dash, and vendor documentation as the authoritative sources when the catalog is unavailable or incomplete.
- [ ] Add skill-local references, deterministic validation expectations, handoff contracts, and targeted tests for all five workflows. Update Apple Dev Skills inventory, root documentation, and marketplace metadata only if the exported skill surface changes.
- [ ] After the five workflows are implemented and validated, explore the installed iOS Simulator browser and SwiftUI hot-reload surface with Gale in a dedicated research pass. Decide together whether it belongs as a Socket workflow, a documented external-tool handoff, or no durable Socket addition; do not bundle or install browser/runtime tooling before that decision.

### Exit Criteria

- [ ] The five workflows have distinct entry conditions, owned decisions, Apple documentation anchors, validation evidence, and clear handoffs without duplicating the existing Xcode, SwiftUI, AppKit, or provisioning skills.
- [ ] Each runtime or distribution workflow states its evidence boundary: code-level suspicion, simulator trace, memgraph ownership proof, signed artifact inspection, or notarization result.
- [ ] The new skills pass their targeted tests, the Apple Dev Skills validation suite, shared-snippet checks, repository-doc validation, and root Socket metadata validation.
- [ ] The simulator-browser and hot-reload investigation remains an explicit post-implementation conversation with Gale rather than an assumed dependency or unreviewed bundled runtime.

## Milestone 25: Apple Creator Studio operator workflows

### Status

Planned

### Scope

- [x] Add a dedicated `apple-creator-studio-skills` child plugin for safe, human-readable, Computer Use-aware workflows in Apple’s creative applications. Keep it separate from `apple-dev-skills`, which owns Apple framework, Swift, Xcode, and media-code work.
- [x] Treat this as a durable guidance plugin, not an app-control daemon or macro runner. Do not bundle undocumented automation, a media-processing runtime, machine-local app paths, a local service, or copied Apple help content.
- [ ] Ship Creator Studio coverage in focused skills: Final Cut Pro, Motion, Compressor, Logic Pro, MainStage, and Pixelmator Pro. Treat GarageBand as a companion skill because it is not currently a Creator Studio subscription app. Final Cut Pro and Motion are complete; Pixelmator Pro remains.
- [ ] Keep Acorn and RetroBatch outside this plugin. Evaluate a future independent `mac-image-workflows` plugin only after their common operator workflows, ownership boundaries, and validation fixtures are concrete.

### Tickets

- [x] Use [`docs/maintainers/apple-creator-studio-skills-plugin-plan.md`](./docs/maintainers/apple-creator-studio-skills-plugin-plan.md) as the implementation source of truth.
- [x] Implement the first Creator Studio slice: `compressor-workflow`, `logic-pro-workflow`, and `mainstage-workflow`, with official-help research, Computer Use safety checkpoints, reusable fixture contracts, and focused skill validation.
- [x] Decide that the three validated initial-slice skills justify the child plugin and marketplace entry.
- [x] Implement Final Cut Pro and Motion after Compressor handoff/relink/export contracts were proven in controlled disposable fixtures. Keep library, source-project, template-publication, and delivery confirmation boundaries explicit.
- [x] Require MainStage’s initial implementation to include explicit live-performance safety, audio/MIDI device preflight, and no-surprise-change controls.
- [ ] Implement Pixelmator Pro after Mac/iPad scope, source-layer preservation, and cross-app image handoff requirements are tested.
- [x] Add `garageband-workflow` as a companion workflow after Logic Pro. Keep its project/import/export handoffs explicit and do not imply GarageBand is included in Apple Creator Studio.
- [ ] Publish `mac-image-workflows` only if Acorn and RetroBatch share enough durable asset-preparation contracts to earn a common owner without absorbing Pixelmator Pro or generic image-code workflows.
- [ ] Investigate a `tips-app-workflow` skill after the first Creator Studio skills ship. Verify whether macOS Tips exposes current, task-specific content for Creator Studio and other Apple apps through an accessible, stable Computer Use surface; compare it against in-app Help and official user guides, preserve Tips as an optional discovery aid rather than an authoritative documentation source, and do not add a plugin or skill until a real fixture proves its value.
- [x] Update root README, marketplace metadata, plugin metadata, and validation now that the installable plugin surface has shipped. Add active-skill inventory tests only when a Socket-level inventory assertion becomes necessary.

### Exit Criteria

- [x] Every shipped skill has one concrete operator domain, authoritative Apple or vendor documentation anchors, a readable human path, and a Computer Use execution contract.
- [x] Every write or destructive UI action has a visible confirmation, output path, source-preservation rule, and post-action verification requirement.
- [x] Compressor, Logic Pro, and MainStage have been forward-tested against disposable, version-recorded fixtures before broader app coverage ships.
- [ ] The plugin neither duplicates Apple Dev Skills framework guidance nor makes unsafe claims about unattended creative-app automation.

## Small Tickets

- [ ] Record issue-sized fixes, TODO/FIXME imports, and cleanup work that is too small or too unplanned for a milestone.

- [x] Add a browse-only root `Socket.xcworkspace` for Xcode 27 beta Markdown editing and repository navigation without introducing a root build surface.
- [x] Record Gale's coordinator-shaped, MVVM-C-adjacent Swift app-structure alignment plan for future Apple Dev Skills guidance updates.
- [x] GitHub #61: Teach repo-maintenance prerelease GitHub metadata ([#61](https://github.com/gaelic-ghost/socket/issues/61))
- [x] GitHub #60: Apple Dev Skills workflow helper is missing PyYAML runtime dependency ([#60](https://github.com/gaelic-ghost/socket/issues/60))
- [x] Hardened `web-dev-skills:expo-inline-native-modules-workflow` with native-shape decision and validation reference tables.
- [x] Added Server-Side Swift ecosystem package preference guidance for Vapor, Vapor Community, and Hummingbird-aligned packages.
- [x] Added `productivity-skills:codex-gui-worktree-workflow` for general Codex GUI worktree-first planning, plus Apple and server-side Swift local environment templates in their owning stack plugins.
- [ ] Explore adding a DCO/sign-off status check for pull requests. Keep the investigation focused on enforcing sign-offs for command-line contributors without blocking Gale's direct-main maintenance workflow.
- [x] Audit and update the default and recommended GitHub repository settings in relevant repo-maintenance, skill-repo, and Apple bootstrap/sync workflows.
- [x] Add `productivity-skills:maintain-github-repository` as the dedicated owner for GitHub repository settings audits and requested alignment, while keeping release and publish choreography in `maintain-project-repo`.
- [x] GitHub #81: Strengthen `maintain-project-repo` release, publish, tag, protected-main, cleanup, and branch-accounting triggers while routing settings-only requests to `maintain-github-repository` ([#81](https://github.com/gaelic-ghost/socket/issues/81)).
- [x] Migrated the remaining root `TODO.md` backlog into canonical `ROADMAP.md` milestones, Small Tickets, or Backlog Candidates, then removed `TODO.md` in a reviewed documentation pass.
- [ ] Investigate `uv audit` as a Socket validation and release-evidence input. Decide whether the first adoption belongs in root validation, Python-backed child plugin validation, release evidence capture, or reusable Python project-maintenance guidance, and test the `--locked`, `--frozen`, JSON output, ignore, and OSV service options before making it a required gate.
- [ ] Explore an `ErrorHandles` Swift helper package for consistent, concise error construction, diagnostic context, typed wrapping, and recovery helpers. Use [`docs/maintainers/errorhandles-package-plan.md`](./docs/maintainers/errorhandles-package-plan.md) to keep the Swift package source outside Socket while keeping skills and adoption guidance in `plugins/swift-lang`.
- [ ] Generalize Codex GUI local environment templates across stack plugins. Start from the root Socket `uv sync --dev` environment, preserve customized `.codex/environments/*.toml` files, keep setup scripts repo-relative, and let each stack plugin own templates for its common project shapes instead of installing global tool dependencies.
- [ ] Investigate guidance consolidation opportunities that reduce repeated setup, routing, validation, and handoff text across skills while preserving the owner boundaries needed for accurate tool use and lower token load.
- [ ] Investigate further standardization and automation for shared skill scaffolding, evidence capture, validation prompts, and generated references so common workflow knowledge is maintained once and reused with lower token load.
- [ ] Redesign the Socket release flow around branch-backed worktrees. Split pre-merge feature-branch gates from post-merge `main` gates, make the release-ready failure mode more helpful when run from a worktree, preserve the rule that tags and release evidence come from reviewed `main`, and document how a release-prep branch should carry version bumps without making the base checkout dirty.
- [ ] Centralize Socket validation behind one root command before adding more plugin-specific validators. The first pass should gather marketplace metadata, plugin manifests, icon assets, child `AGENTS.md`, `SKILL.md` frontmatter, `agents/openai.yaml`, shared version inventory, release-prep checks, and optional child-local tests into a clear report while keeping heavyweight behavior tests opt-in.
- [ ] Add a future Apple Developer Portal Driver for accessible, interactive portal-only provisioning tasks. Keep Apple authentication, two-factor authentication, account/team selection, and destructive operations behind explicit user-visible confirmation gates; retain official App Store Connect REST, Xcode-aware discovery, `cktool`, and CKTool JS as the primary surfaces, and do not automate unsupported portal forms until a reviewed driver design exists.

## Backlog Candidates

- [ ] Add `game-dev-skills:metal-game-rendering-workflow` for a later shader and Metal rendering architecture slice. Scope it after concrete use cases decide whether it owns shader code, render-pass architecture, command encoding, resource layout, Metal debugger workflow, GPU counters, or all of those.
- [x] Add the first repo-local Socket Steward prototype as a Python `uv` project under `.agents/socket-steward`, using deterministic read-only audits plus an optional OpenAI Agents SDK `ask` path before any write, LaunchAgent, or app behavior.
- [x] Expand Socket Steward with a docs-sync planning command that emits structured recommended edits for README, CONTRIBUTING, AGENTS, ROADMAP, marketplace metadata, and child plugin guidance without applying them.
- [x] Add `docs/agents/` as the repo-local report surface and let Socket Steward write reviewable docs-sync proposal reports there without applying the proposed documentation edits.
- [x] Add a serialized Socket Steward `prepare docs-sync` workflow and first guarded `apply docs-sync --confirm` mode that refreshes proposal reports without mutating durable docs.
- [x] Extend `productivity-skills:maintain-project-roadmap` with explicit checklist ticket add/update flags so repo-local agents can delegate roadmap TODO mutations to the roadmap skill instead of duplicating roadmap editing logic.
- [ ] Add a read-only Socket Steward fan-out experiment for broad docs and guidance scans. Start with deterministic sharding by file count or total line count, keep workers read-only, merge findings into one bounded report, and compare the result against the single-process audit before deciding whether subagent fan-out belongs in the durable steward workflow.
- [ ] Add a guarded Socket Steward write mode only after the read-only audit and planning contracts are stable, with explicit approval boundaries for file edits, validation, git operations, release workflow, and future background execution.
- [x] Overhaul `agent-portability-skills` so its docs, tests, generated bootstrap content, and sync audit logic target Codex/OpenAI plus the open `.agents/skills` discovery mirror only. Remove stale expectations for retired child maintainer docs such as reality-audit and install-surface docs, and keep the wording away from unsupported non-Codex or generic multi-agent surfaces.
- [x] Add a `productivity-skills:maintain-project-docs` umbrella workflow after `maintain-project-roadmap` owns small-ticket tracking. It should run the individual docs skills together, enforce the splits between `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `ACCESSIBILITY.md`, and `ROADMAP.md`, and prevent repeated content from drifting across files.
- [x] Add a first `productivity-skills:design-agent-automation-workflow` planning skill for agent and automation design. It chooses between Codex app automations, `codex exec`, Codex subagents, OpenAI Agents SDK services, LangGraph graphs, Hermes-specific workflows, or no automation yet while delegating stack-specific implementation to the owning plugin.
- [x] Added `productivity-skills:design-agent-eval-workflow` for agent, skill, prompt, and automation eval planning, and skewed automation guidance toward safe full automation with exact escalation gates instead of broad human review.
- [x] Aligned Apple Xcode app guidance around strict MVVM source structure, including view-adjacent view models/controllers, directional `Services/` subdirectories, and `sync-xcode-project-guidance` structure-audit reporting for repeatable downstream drift detection.
- [x] Create a quicker full-auto Socket patch-refresh script for trusted maintainer use. It should bump the shared patch version, validate metadata, satisfy release-ready and subtree gates, push `main` and any required subtree split, tag and publish the GitHub release, verify branch accounting, and run `codex plugin marketplace upgrade socket`.
- [x] Reduce hand-carried patch-release work by capturing commit-bound temporary `CODEX_HOME` marketplace smoke evidence and the final Dependabot alert query, then incorporating both into generated release notes without changing release-ready, subtree, branch-accounting, tag, GitHub release, or final marketplace-upgrade gates.
- [ ] Explore steward-assisted release and worktree orchestration. Start with Socket Steward release preflights and cache-refresh checks, then evaluate whether `swift-steward` or sibling roles should handle read-only release readiness, PR merge sequencing, branch accounting, and parallel worktree status reports while the main thread keeps write, merge, tag, and publish ownership.
- [ ] Design a worker-thread orchestration workflow for Codex GUI and Socket Steward use. Capture the decisions before implementation: whether the durable surface is a new Productivity Skill, a Socket Steward command, or both; which fields belong in the worker launch envelope; how model and reasoning budgets are selected; how workers report branch, worktree, validation, and cleanup state back to the coordinator; which actions remain main-thread only; and when a finished worker thread or worktree should be archived, removed, or kept for follow-up.
- [ ] Keep Socket Steward tied into cross-Socket docs, marketplace, audit, plan, and proposal workflows as the repo-local coordination surface.
- [ ] Add `agent-portability-skills:audit-agent-surface-portability` for inventorying `SKILL.md`, `.codex-plugin`, `.mcp.json`, hooks, app config, custom agents, and host compatibility notes across Socket child plugins.
- [ ] Add `agent-portability-skills:design-agent-host-adapter` for deciding whether a host needs docs-only guidance, `.agents/skills` export, native MCP config, a plugin or package adapter, or no Socket-specific support.
- [ ] Add `agent-portability-skills:maintain-codex-plugin-surface` for Codex-specific marketplace, plugin manifest, hooks, MCP, app config, and enablement wording.
- [ ] Keep Git-backed Codex marketplace install and update guidance ahead of local authoring notes.
- [ ] Keep repo-local discovery mirror guidance separate from install guidance.
- [ ] Add or refine troubleshooting language for confusing Codex plugin expectations.
- [ ] Add a maintainer workflow for moving or re-homing skills between repositories.
- [ ] Add durable process support for noticing changes in OpenAI Codex docs and the open `.agents` skill discovery convention.
- [ ] Add Claude Code marketplace, plugin, skills, subagent, and MCP compatibility guidance after the first Socket portability audit and adapter-design skills land.
- [ ] Keep `cardhop-contact-workflow`, bundled MCP server docs, `.mcp.json`, and plugin metadata aligned.
- [ ] Validate the bundled Cardhop MCP server from `plugins/cardhop-app/mcp/`.
- [ ] Add root or child Cardhop validation coverage once the Cardhop skill or MCP surface grows beyond the current single workflow.
- [ ] Add `productivity-skills:maintain-project-security` for canonical `SECURITY.md` maintenance.
- [ ] Add `productivity-skills:maintain-project-support` for canonical `SUPPORT.md` maintenance.
- [ ] Add a future `productivity-skills:maintain-project-hooks` workflow for repositories that intentionally use Codex Hooks.
- [ ] Forward-test `productivity-skills:design-agent-automation-workflow` and `productivity-skills:design-agent-eval-workflow` against real agent, automation, and eval planning requests before adding deterministic scaffolding scripts.
- [ ] Add lightweight Productivity validation tooling for `SKILL.md`, frontmatter, and `agents/openai.yaml` alignment.
- [ ] Add Productivity validation checks for README layout and active skill inventory consistency.
- [ ] Add server-side Swift validation coverage for skill metadata and exported skill inventory once central Socket child-skill validation exists.
- [ ] Decide whether future server-side Swift skills should cover SwiftNIO, deployment, authentication, app sync, or additional database workflows as separate skills.
- [ ] Cover server-side JVM package/runtime handoffs, persistence, observability, CI, and upgrades after the first project-shape, build-tooling, implementation, and testing slice.
- [ ] Cover reverse-engineering workflows for .NET assemblies, Unity managed and IL2CPP artifacts, Apple binaries, symbols, crash logs, and decompiler or disassembler output review.
- [ ] Add tool-specific reverse-engineering guidance for Cutter, Ghidra, Malimite, Hopper, and adjacent tools after hands-on workflow preferences are clearer.
- [ ] Finish Things guidance and maintenance modernization for the mixed Things skill plus bundled MCP server repo.
- [ ] Keep root README and AGENTS guidance clear about whether Things changes belong in `skills/`, `mcp/`, or plugin metadata.
- [ ] Expand Things repo-root maintainer tooling once more than one root skill needs Python-backed verification.
- [ ] Add broader Things bundled-server smoke coverage when new tool families or auth-sensitive update flows are introduced.
- [ ] Revisit Things packaging mirrors if the repo starts shipping additional Codex discovery surfaces.
- [ ] Author the first real Spotify-focused Codex workflow.
- [ ] Add the first maintained Spotify skill, app, or MCP-backed workflow under the canonical exported surface.
- [ ] Update Socket docs and validation once the exported Spotify surface is real.
- [ ] Decide whether Socket remains Spotify's canonical home after the first real shipped workflow.
- [ ] Investigate Socket-owned F# `.fsx` hook and maintenance-script conventions as the first step toward migrating repo maintenance scripts to .NET 10. Define where scripts live, how Codex hook commands launch `dotnet fsi --exec`, which repo-local `DOTNET_CLI_HOME` cache paths must be gitignored, how event-specific hook JSON input/output types are modeled, which validation commands prove portability, when a script should graduate into a compiled F# console tool for frequently fired hooks, and how Python scripts such as release/version and metadata validation should be replaced or wrapped during migration.
- [ ] Plan a small evidence-first demo and comparison series for local-first AI-assisted macOS development. Show Socket and Gale-built local workflows against mainstream Codex, Xcode-integrated, courseware, or cloud-first workflows using concrete tasks such as Swift repo guidance sync, release maintenance, local inference handoff, worktree coordination, privacy-preserving docs audits, and quality-focused Apple-platform validation.
- [x] Add root validator coverage for the first Swift Steward subagent role drafts, keeping custom-agent TOML parseable, read-only, name-aligned, and review-oriented before any write-capable steward workflow exists.
- [x] Set the first Swift Steward roles to a role-local `gpt-5.4-mini` default and document when read-heavy custom subagents should pin a smaller model versus deferring to the parent session.
- [x] Inventory bundled subagent role candidates across Socket plugins and rank the strongest read-heavy candidates before adding more `.codex/agents` files.
- [x] Add `productivity-skills:repo-docs-auditor` as the next bundled read-only custom-agent role. Keep it evidence-first across README, CONTRIBUTING, AGENTS, ACCESSIBILITY, ROADMAP, and command drift, and have it return review packets for the main thread to apply through the owner docs skills.
- [x] Add `productivity-skills:code-slice-tracer` as a bounded code-reading custom-agent role for call-site tracing, test/doc correlation, and multi-slice explanation support without owning final prose or architecture-file writes.
- [x] Add `agent-portability-skills:skills-repo-guidance-sync` as a read-only custom-agent role for plugin-root policy audits, marketplace wording checks, Codex docs freshness, `.agents/skills` discovery mirrors, and generated guidance drift.
- [ ] Add privacy-fenced app plugin auditor roles only after their read/write boundaries are explicit: `things-app:things-route-auditor` for read-only Things route and digest planning, and `cardhop-app:cardhop-contact-auditor` for schema, health, route, and dry-run preview checks.
- [x] Add `productivity-skills:dice-job-search-workflow` after verifying Dice's official MCP docs and setup pages. Keep the first pass guidance-only around Dice's remote `search_jobs` MCP tool, bundle the remote MCP config for automatic setup, and preserve explicit authentication, rate-limit, saved-search, application-state, and privacy boundaries.
- [ ] Investigate a Drafts.app MCP and automation skill covering the official Drafts MCP Server for Mac, JavaScript action scripting, Shortcuts, URL schemes, AppleScript, AI action helpers, and safe draft read/write boundaries. Decide whether the durable home is a dedicated Drafts app plugin, `productivity-skills`, or a general macOS automation skill before adding implementation guidance.
- [ ] Investigate an iTerm2 automation and integration skill covering AI Chat, the Python API, scripting fundamentals, variables, shell integration, tmux integration, and deprecated AppleScript boundaries. Keep the first pass docs-first and decide whether the skill should expose terminal-control workflows, app integration guidance, or only safe handoffs to existing shell and Codex GUI worktree guidance.
- [ ] Add language validation triager roles after one shared contract is agreed: `python-skills:python-validation-triager`, `rust-skills:rust-validation-triager`, and `dotnet-skills:dotnet-validation-triager`, each report-first and scoped to logs, manifests, CI, test, tooling, package, and upgrade evidence.
- [ ] Add Codex GUI local environment templates and auto-copy/install behavior to `dotnet-skills` for F#, C#, and mixed `.NET` repos, keeping setup/actions portable and preserving customized `.codex/environments/*.toml` files the same way the SwiftPM and Xcode workflows do.
- [ ] Revisit maybe-later subagent roles only after the owning plugin surface justifies them: `productivity-skills:roadmap-triage-worker`, `productivity-skills:automation-plan-designer`, `swiftasb-skills:swiftasb-steward`, and `web-dev-skills:expo-native-boundary-scout`.
- [ ] Keep placeholder or write-heavy surfaces out of bundled roles for now: do not add `android-dev-skills:android-steward`, `spotify`, or a `maintain-project-repo` worker role until those surfaces have enough read-heavy workflow evidence and safe boundaries.
- [x] Grow Swift Steward from read-heavy guidance-sync and repo-maintenance scans into reviewable patch artifacts that can be saved, edited, or applied by the main thread, then decide whether any apply-mode behavior belongs in the main thread, a guarded report workflow, or a future repo-local sidecar.
- [x] Turn the placeholder `android-dev-skills` child plugin into an installable Android guidance plugin. It covers Kotlin-first Android project work, Java interoperability or Java-only maintenance when a repo requires it, Gradle and Android Gradle Plugin alignment, emulator-aware validation, release readiness, and clear handoffs to existing mobile testing plugins instead of duplicating emulator tooling.
- [ ] Add an `mlx-skills` guidance plugin for Apple Silicon MLX project work. It should cover project-shape discovery, Python and Swift integration choices, model conversion or loading workflows, local performance validation, reproducibility notes, and clear boundaries with broader Python, Apple, and AI automation skills.
- [ ] Add a `coreml-skills` guidance plugin for Core ML model integration and maintenance. It should cover model packaging, conversion handoffs, Swift and Apple-platform app integration, on-device validation, performance and memory checks, release readiness, and boundaries with `apple-dev-skills` so generic Xcode or SwiftUI work stays owned there.
- [x] Expand Apple Dev Skills with dedicated SwiftUI animation, Core Animation, SF Symbols, and Apple typography workflows. Shipped `sf-symbols-workflow`, `swiftui-animation-workflow`, `core-animation-layer-workflow`, and `apple-typography-workflow` from [`docs/maintainers/apple-design-animation-skills-plan.md`](./docs/maintainers/apple-design-animation-skills-plan.md), keeping the skills under `plugins/apple-dev-skills`, using Xcode-local docs, Dash, official Apple docs, and local Apple developer apps as evidence, and avoiding absorption into the existing SwiftUI architecture skill.
- [x] Add an `apple-dev-skills:appkit-app-architecture-workflow` skill so AppKit has a first-party architecture decision surface parallel to SwiftUI. It covers menu bar apps, status items, responder-chain menus, window and view-controller ownership, app and window restoration, AppKit MVC, object archiving and persistence choices, Observation with AppKit, and mixed AppKit/SwiftUI composition without steering agents inordinately toward either framework. Started from [`docs/agents/appkit-skills-coverage-plan.md`](./docs/agents/appkit-skills-coverage-plan.md).
- [x] Complete Phase 2 of the Apple Dev Skills Socket migration. Treat `plugins/apple-dev-skills` as monorepo-owned source, remove Apple Dev Skills from subtree release gates, update Socket docs and duplicate-install guidance, add the compatibility marketplace smoke test, run full Socket validation, and publish the Socket release that makes the ownership change durable.
- [ ] Evaluate a centralized Socket validation setup, preferably backed by the .NET 10/F# script migration, that can check marketplace metadata, plugin manifests, icon assets, child AGENTS shape, `SKILL.md` frontmatter, `agents/openai.yaml` alignment, shared version inventory, and release-prep state from one root command while still leaving child-local tests where behavior needs them.
- [x] Track the remaining Speak Swiftly duplicate-enable repair behavior in the standalone `SpeakSwiftlyServer` plugin workflow rather than keeping the completed Socket catalog split open: [gaelic-ghost/SpeakSwiftlyServer#98](https://github.com/gaelic-ghost/SpeakSwiftlyServer/issues/98).
- [x] Restore Socket and the Apple Dev Skills compatibility surface to Apache License 2.0 after the source-available licensing experiment proved less useful than the adoption and goodwill of a standard permissive license.

## History

- Re-contained SwiftData persistence guidance in a dedicated Apple Dev skill and SwiftUI composition in its architecture skill, while introducing the explicit three-letter Swift prefix and Xcode-friendly concatenated filename grammar.
- Made Socket worktree-first for implementation work while keeping the base `main` checkout as the clean coordination and release-verification surface.
- Aligned Socket documentation-source routing away from generic documentation aggregators by making Xcode MCP `DocumentationSearch` the Apple SDK default, Dash MCP/HTTP the preferred local-docs path for installed docsets across supported stacks, and canonical upstream docs/source the fallback when Dash/local coverage is missing or stale.
- Added the first repo-local Socket Steward prototype under `.agents/socket-steward`, giving the superproject a Python and OpenAI Agents SDK maintainer-agent scaffold with offline docs, guidance, and marketplace audits before any write-capable or background-service behavior.
- Added Socket Steward's first docs-sync planner so the repo-local agent can produce structured read-only documentation alignment work before any guarded write mode exists.
- Added `docs/agents/` for repo-local agent report artifacts and limited Socket Steward proposal writes to that directory.
- Planned an `agentdeck` desktop bridge MCP and skill surface that talks to the separate `AgentDeck` macOS app over a local transport instead of bundling a signed app in the plugin cache.
- Planned Codex GUI restart request/cancel/status tools and a narrow skill that keep restart execution in `AgentDeck` and leave automatic `when-idle` waiting blocked until a supported thread-status source exists.
- Planned an AgentDeck agent configuration sync surface so normal Codex, Xcode Codex, and Xcode Claude can be discovered, diffed, and rendered through target-specific compatibility rules while `agentdeck` remains the Codex-facing adapter.
- Added serialized Socket Steward prepare/apply commands so maintainers can run audit, docs-sync planning, and proposal refresh in one guarded pass.
- Extended the roadmap maintainer skill with one-ticket add/update flags and updated automation-design guidance to prefer existing skills, plugins, scripts, and official workflow owners as the source of truth for workflow knowledge.
- Removed the stale Apple Dev Skills release-time subtree push gate after the standalone Apple Dev Skills repository became a compatibility marketplace pointer to Socket's canonical `plugins/apple-dev-skills` payload.
- Completed the Apple Dev Skills Phase 2 ownership cleanup: Socket now documents `plugins/apple-dev-skills` as monorepo-owned, the standalone `gaelic-ghost/apple-dev-skills` repository is pruned to a compatibility marketplace pointer, and the compatibility install smoke path is documented alongside the Socket install tests.
- Released `v6.7.0` after aggressively simplifying Socket documentation: root README and CONTRIBUTING split, child roadmap consolidation into root planning docs, child README collapse with user-owned `TBD` overview sections, nested maintainer doc cleanup, workflow atlas removal, and unsupported non-Codex surface removal.
- Queued future `mlx-skills` and `coreml-skills` guidance plugins for Apple Silicon ML and Core ML workflows.
- Audited AppKit coverage against SwiftUI and queued an Apple Dev Skills AppKit app-architecture workflow so menu bar apps, restoration, MVC, archiving, Observation, and mixed AppKit/SwiftUI work get first-class guidance.
- Implemented `apple-dev-skills:appkit-app-architecture-workflow` with AppKit ownership, menu bar, responder-chain, restoration, MVC, archiving, Observation, and mixed AppKit/SwiftUI references plus targeted tests.
- Added draft `swift-steward` and `server-swift-steward` custom-agent roles plus root validator coverage so the steward contracts remain read-only and review-oriented until a guarded draft-patch workflow exists.
- Tuned the Swift Steward custom-agent contracts and shared subagent guidance around a role-local `gpt-5.4-mini` default for bounded read-heavy scans, while keeping write ownership and harder reasoning in the main thread or stronger model choices.
- Tightened Swift Steward output around review packets with proposed patch sets and validation handoff so future draft-patch behavior has a stable report contract before any apply mode exists.
- Added a bundled subagent role candidate inventory covering docs audit, code tracing, plugin guidance sync, Things and Cardhop auditors, validation triage roles, and no-for-now placeholder plugins.
- Added the first Productivity Skills bundled custom-agent role, `repo-docs-auditor`, for read-only repo-document audits and review-packet planning before the main thread applies owner-doc skill edits.
- Added `code-slice-tracer` as a read-only Productivity Skills custom-agent role for bounded call-site maps, branch tracing, test/doc correlation, and comparison support before the main thread writes the final code-slice explanation.
- Added `skills-repo-guidance-sync` as a read-only Agent Portability Skills custom-agent role for Codex docs freshness, plugin-root policy, discovery mirror drift, marketplace wording, and review-packet guidance sync.
- Completed the first Swift Steward release set by aligning `swift-steward`, `server-swift-steward`, adjacent documentation and skills guidance, and the shared review-packet validator contract around read-only subagent discovery with main-thread apply ownership.
- Added the placeholder `android-dev-skills` child plugin surface and queued a Kotlin-first Android guidance plugin for future Socket work.
- Published `apple-dev-skills` `v6.14.1` as the Phase 1 compatibility release: the standalone repository now points its marketplace at Socket's `plugins/apple-dev-skills` payload while preserving `codex plugin marketplace upgrade apple-dev-skills` for existing standalone users.
- Removed redundant monorepo-owned child root READMEs after making `AGENTS.md`, plugin manifests, skill metadata, MCP server READMEs, and root Socket docs the maintained documentation surfaces. `apple-dev-skills` keeps its public README because it still has a standalone compatibility marketplace.
- Completed the Speak Swiftly plugin catalog split by exposing `speak-swiftly` from the canonical `gaelic-ghost/SpeakSwiftlyServer` Git-backed source, retiring the local `plugins/SpeakSwiftlyServer/` mirror, validating isolated marketplace install paths, and keeping standalone SpeakSwiftlyServer as the plugin payload source of truth.
- Completed the release and sync discipline milestone by aligning release-mode docs, subtree sync rules, shared-version workflow, release-ready gates, and marketplace refresh ordering around the current mixed monorepo model.
- Completed the subtree workflow hardening milestone by documenting subtree add, pull, and push paths, adding the root marketplace audit pass, and adding a public child plugin removal checklist.
- Completed [#35](https://github.com/gaelic-ghost/socket/issues/35) / [#37](https://github.com/gaelic-ghost/socket/issues/37) by hardening release and PR scripts around delayed GitHub state.
- Completed [#39](https://github.com/gaelic-ghost/socket/issues/39) by adding the Swift Package Index add-package gate and one-shot script around the documented `SwiftPackageIndex/PackageList` Add Package issue form.
- Planned a `swiftasb-skills` child plugin to help agents explain SwiftASB and build SwiftUI, AppKit, and Swift package integrations from a Socket-visible guidance surface.
- Added and exposed a `web-dev-skills` Expo inline native modules workflow for SDK 56+ inline Swift/Kotlin modules, `expo-type-information`, CNG/prebuild validation, and Apple Dev Skills handoffs.
- Updated `productivity-skills:maintain-project-repo` so heavy remote CI can be deferred after full local validation, branch push, PR creation, and initial check discovery, with Codex expected to use native thread Timer/Wakeup or heartbeat automation to resume the release instead of keeping an idle CI-waiting script open.
- Added root `docs/media` screenshot assets and README media guidance so the Codex plugin-directory catalog surface is visible without weakening text-first documentation.
- Added coordinated OpenAI Codex Hooks guidance across `agent-portability-skills` and `productivity-skills`, with future `maintain-project-hooks` work tracked in the productivity roadmap.
- Added `productivity-skills:maintain-project-docs` as an umbrella documentation sweep that runs the owner README, CONTRIBUTING, AGENTS, ACCESSIBILITY, and ROADMAP workflows serially while auditing cross-document responsibility drift.
- Updated `socket` and plugin guidance so ordinary user installs and updates default to Git-backed Codex marketplace sources and official marketplace add/upgrade commands.
- Loosened coordinated Codex subagent guidance so skills preserve OpenAI's explicit-trigger model while allowing narrower workflow guidance, such as Codex Security repository-wide scans, to ask for and use subagents when the task depends on parallel file-pass review.
- Added coordinated Codex subagent guidance across `agent-portability-skills` and `productivity-skills`, grounding skill wording in OpenAI's current explicit-trigger `subagents` model while keeping the root docs clear about why the pass belongs in `socket`.
- Added `productivity-skills:codex-gui-worktree-workflow` as the general Codex GUI worktree-first planning surface, while keeping SwiftPM, Xcode, Vapor, Hummingbird, and server-side Swift local environment templates inside their stack-specific plugins.
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
