# Agent Portability Options

This document records the first research pass for making Socket skills and plugins more portable across agent hosts while keeping the current Codex marketplace honest.

Date checked: 2026-07-19.

## Current Recommendation

Treat Agent Skills as the first portability layer.

Socket already keeps authored skills as `skills/<name>/SKILL.md` with optional `references/`, `scripts/`, and `assets/` folders. That shape maps cleanly to the emerging Agent Skills convention used by several current tools. The lowest-risk next step is to validate and, where needed, render those skill folders for each host's documented discovery paths.

Treat plugins as host-specific package adapters.

Codex, Claude Code, OpenCode, Xcode, and Zed each expose different plugin or extension concepts. Socket should not redefine its root as a generic plugin bundle until a concrete target needs that shape. Keep the current root as a Codex marketplace catalog, then add per-host export or install support as deliberate adapter outputs.

### Implemented Claude Adapter

Claude Code and Cowork now have a deliberate Socket adapter rather than a
future evaluation placeholder. The root
[`/.claude-plugin/marketplace.json`](../../.claude-plugin/marketplace.json)
reuses Socket's existing plugin roots with Claude marketplace metadata, while
[`claude-compatibility.md`](./claude-compatibility.md) records the complete
per-plugin boundary. Claude Code supports the full classified catalog; Cowork
uses the same skills but only public remote MCP servers. Local Mac MCP servers
remain Claude Code-only.

Use `agent-portability-skills` as the reusable skill layer for these decisions. Socket Steward remains the repo-local audit, plan, and proposal engine under `.agents/socket-steward/`; Agent Portability Skills should own the agent-facing workflows that decide what is portable, what is Codex-specific, and what needs a host adapter.

## Near-Term Focus

Keep Xcode, Claude, Hermes, Codex, ACP, and Zed as active compatibility targets;
retain OpenCode as a skills-first follow-up surface.

Current locally installed evidence:

- Xcode 27 beta: `/Applications/Xcode-beta.app`, bundle metadata checked on 2026-07-19 as Xcode 27.0 build 27A5218g. The selected command-line toolchain remains Xcode 26.6 build 17F113.
- Xcode 27 beta live bridge: verified on 2026-06-23 with the beta app open and selected through `MCP_XCODE_PID`; `run-agent --dry-run codex` resolved the beta-scoped Codex runtime and Xcode-specific `CODEX_HOME`. A direct `codex skills export` attempt through that runtime failed in this beta with `unrecognized subcommand 'export'`, so do not rely on that as an install or export path.
- Xcode 27 beta plug-in import: verified on 2026-06-23 through the Xcode Beta Settings UI. `Import from Codex`, `Add from file`, and `Add from URL` all recognized agentic plug-in payloads; `Add from URL` accepted `https://github.com/gaelic-ghost/socket.git` and enumerated Socket child plug-ins before import.
- Active command-line Xcode: `/Applications/Xcode.app/Contents/Developer`, currently Xcode 26.6 build 17F113 through the default `xcodebuild -version`.
- Hermes CLI: local 0.17.0 (2026.6.19); published PyPI 0.18.2. `hermes update --check` reports an update available, while the local checkout has one carried commit and is one commit ahead/behind `origin/main`.
- Hermes ACP: `hermes acp --check` passes locally. The source repository ships a 0.18.2 registry manifest, but the live canonical ACP Registry does not currently contain `hermes-agent`.
- Zed: 1.8.2 build 20260624.160235, checked from the installed app bundle on 2026-07-19.
- Claude Code CLI: 2.1.211, checked on 2026-07-19.
- Codex CLI: 0.144.6, checked on 2026-07-19.
- OpenCode CLI: `/opt/homebrew/bin/opencode`, verified as 1.17.9.
- OpenCode Desktop: `/Applications/OpenCode.app`, present locally.

Treat Zed as three separate surfaces: Zed Agent, ACP External Agents, and Terminal Threads. Zed's Codex external agent can use normal Codex state, while Zed Agent has its own skills, instructions, profiles, permissions, and MCP configuration.

Treat AgentUtils as the future home for complex local orchestration.

If a target needs user-home discovery, app-bundle detection, dry-run previews, backup-backed writes, service status, or cross-agent config rendering, the durable architecture should route that through Gale's local macOS utility app rather than putting broad machine-management behavior into Socket plugin payloads. Socket should own the agent-facing policy, docs, and lightweight adapter contract; AgentUtils should own macOS integration, filesystem safety, and local apply operations.

## Platform Snapshot

### Codex

Socket's current primary surface is Codex-specific:

- root marketplace catalog: `.agents/plugins/marketplace.json`
- child plugin root: `plugins/<child>/.codex-plugin/plugin.json`
- bundled Codex surfaces: `skills/`, `.mcp.json`, `hooks/`, `.app.json`, `agents/openai.yaml`, and related assets
- user install path: `codex plugin marketplace add gaelic-ghost/socket`
- refresh path: `codex plugin marketplace upgrade socket`

The current root docs correctly say Socket is a marketplace catalog, not an aggregate plugin payload. That remains the right base model.

### 2026-07-19 Compatibility Audit Result

- Codex remains the source package model. Current docs and manifests agree on
  skills, MCP, hooks, apps, custom agents, marketplace enablement, and hook
  trust boundaries.
- Claude Code and Cowork retain their validated marketplace adapter. Current
  Claude-specific component types are classified explicitly instead of being
  assumed portable; the pinned Speak Swiftly hook still depends on a Codex
  cache path and remains excluded.
- Hermes now has current operator, extension-development, messaging-gateway,
  and Nous Research service guidance in addition to skill-tap and MCP
  compatibility.
- The Xcode source audit is implemented and deterministic. It reports likely,
  partial, blocked, and unknown support separately for Xcode-launched Codex,
  Xcode internal agents, and external agents using Xcode MCP. Runtime claims
  remain limited to the dated live evidence below.

### Xcode

Apple documents Xcode agent customization through Xcode Intelligence settings, Xcode-only agent configuration folders, command and tool permissions, built-in skills, MCP, and Xcode plug-ins. The official page says product-specific configuration files live under `~/Library/Developer/Xcode/CodingAssistant`, with separate folders such as `codex`, `ClaudeAgentConfig`, and `gemini`, and that those configurations only affect agents launched in Xcode.

Apple also documents an Xcode plug-in UI that can install plug-ins containing subagents, MCP servers, and skills. A local Xcode 27 beta probe confirms that the UI can import from Claude Code, Codex, a local folder, or a Git URL.

Xcode support needs three different answers:

- Xcode-launched Codex: supportable as a separate Codex target. Xcode gives Codex its own home under `~/Library/Developer/Xcode/CodingAssistant/codex`, writes imported plug-ins into that target's `plugins/cache`, and records enabled plug-ins in that target's `config.toml`. Socket should treat this as a separate Codex install target with its own preview/apply flow, not as normal `~/.codex`.
- Xcode internal agents through Xcode plug-ins: supportable for existing Socket child plug-ins that Xcode can recognize through its official import UI. The live beta recognized `.codex-plugin/plugin.json`, skill folders, hooks, and `.mcp.json` declarations. Xcode normalized imported plug-ins into `~/Library/Developer/Xcode/CodingAssistant/AgentPlugins/<plugin>/plugin.json`, registered plug-ins in `AgentPlugins/PluginsManifest.json`, and wrote MCP servers into `CodingAssistant/mcp-servers.json`.
- External agents controlling Xcode: already have a documented integration path through `xcrun mcpbridge`. External agents usually need Socket installed in their own host plus Xcode's external-agent MCP toggle and an open project in Xcode. They do not need a Socket Xcode plug-in merely to control Xcode.

Local validation target:

- For bundle-presence and build-number audits, read Xcode bundle metadata without changing the selected toolchain.
- Open the intended stable or beta Xcode app for live UI, MCP, agent, and plug-in checks instead of treating a closed app as a blocker.
- Use `MCP_XCODE_PID` when stable and beta Xcode processes could both exist or when the bridge must target the beta process explicitly.
- When the task explicitly needs beta command-line execution, record the previous `xcode-select -p` value, switch intentionally with `xcode-select`, verify the selected toolchain, run Apple CLI tools normally, and restore the previous selection when the check is finished. Do not inject `DEVELOPER_DIR` overrides or guess build-product paths.

Practical Socket implication:

- Support Xcode Codex as a separate Codex target, not as a raw mirror of normal `~/.codex`.
- Add an Xcode export or install plan against the official import paths, not a custom installer.
- Keep Xcode-specific workflow guidance in `apple-dev-skills`, especially `xcode-coding-intelligence-workflow`.
- Treat Xcode-exported or Xcode-generated files as comparison evidence unless a later task deliberately imports or adapts them into Socket-authored skill roots.
- Prefer a dry-run or inspect-first local probe: inspect Xcode's CodingAssistant folders, Xcode MCP bridge behavior, and any plug-in import artifacts before writing config.
- Add a Socket-to-Xcode install assessment before adding a writer. The assessment should classify each Socket child plugin as skill-only, MCP-backed, app-backed, hook-backed, or custom-agent-backed, then report which parts can work in Xcode-launched Codex, Xcode internal agents, and external agents.
- Treat Codex apps and `agents/openai.yaml` as non-portable by default until Xcode exposes a matching component contract. Xcode's UI does recognize hooks in imported Socket payloads, but hook behavior still needs a permission and execution probe before claiming full functionality. Skills are the most portable component; MCP servers are portable when the command path, dependencies, auth, and permissions work from Xcode's CodingAssistant environment.

Live Xcode 27 beta import evidence:

- `Import from Codex` listed installed Codex plug-ins and imported `apple-dev-skills` as `6 Skills - Hooks`.
- `Add from file` accepted a local fixture folder containing `.codex-plugin/plugin.json`, `skills/<name>/SKILL.md`, and `.mcp.json`, then installed it as `1 Skill - 1 MCP Server`.
- `Add from URL` rejected a local `file://` Git URL as invalid, but accepted `https://github.com/gaelic-ghost/socket.git` and enumerated Socket child plug-ins from the public repository before import.
- Xcode writes imported plug-ins to `~/Library/Developer/Xcode/CodingAssistant/AgentPlugins`, mirrors them into Xcode's Codex and Gemini homes, and writes MCP declarations into `~/Library/Developer/Xcode/CodingAssistant/mcp-servers.json`.

Sources:

- [Extending and customizing agents](https://developer.apple.com/documentation/xcode/extending-and-customizing-agents/)
- [Xcode 27 agentic tooling skill plan](./xcode-27-agentic-tooling-plan.md)
- [Xcode plug-in install support plan](./xcode-plugin-install-support-plan.md)

### Claude Code and Cowork

Claude Code has a richer configuration hierarchy than most targets in this pass. Current documentation describes managed, user, project, and local scopes. It also documents separate locations for settings, subagents, MCP servers, plugins, and `CLAUDE.md` context. Socket now ships the validated marketplace adapter described in [Claude compatibility](./claude-compatibility.md).

Important current paths and surfaces:

- project skills: `.claude/skills/`
- user skills: `~/.claude/skills/`
- project subagents: `.claude/agents/`
- user subagents: `~/.claude/agents/`
- project settings: `.claude/settings.json`
- local settings: `.claude/settings.local.json`
- project MCP servers: `.mcp.json`
- context files: `CLAUDE.md` or `.claude/CLAUDE.md`
- plugin control: `enabledPlugins`, `extraKnownMarketplaces`, `strictKnownMarketplaces`, and `strictPluginOnlyCustomization`

Practical Socket implication:

- The checked-in `.claude-plugin/marketplace.json` exposes every non-excluded Socket plugin root with `strict: false`, preserving a single authored skill payload.
- Codex `agents/openai.yaml` custom agents are not portable as-is; Claude `agents/*.md` definitions are a selective future addition only when a role has a genuine delegated job.
- Cowork consumes the same skill bundles, but only public remote MCP servers are usable there. Local Mac services remain Claude Code-only.
- The Claude Code policy model remains relevant because it can restrict customization to plugin-provided or managed surfaces.

Sources:

- [Claude Code settings](https://code.claude.com/docs/en/settings)
- [Claude Code MCP](https://code.claude.com/docs/en/mcp)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Cowork plugins](https://claude.com/docs/cowork/guide/plugins)

### OpenCode

OpenCode documents first-class Agent Skills support and explicitly searches several compatible skill roots:

- `.opencode/skills/<name>/SKILL.md`
- `~/.config/opencode/skills/<name>/SKILL.md`
- `.claude/skills/<name>/SKILL.md`
- `~/.claude/skills/<name>/SKILL.md`
- `.agents/skills/<name>/SKILL.md`
- `~/.agents/skills/<name>/SKILL.md`

It recognizes `name`, `description`, `license`, `compatibility`, and string-map `metadata` frontmatter fields. Unknown frontmatter fields are ignored. Skill names must be lowercase alphanumeric with single hyphen separators and must match the directory name.

OpenCode plugins are a different surface: JavaScript or TypeScript modules loaded from `.opencode/plugins/` or `~/.config/opencode/plugins/`, plus npm package names listed in `opencode.json`.

Practical Socket implication:

- The `.agents/skills` discovery mirror is the strongest low-effort portability win for OpenCode.
- OpenCode plugin support would require JavaScript or TypeScript adapter modules, not reuse of `.codex-plugin/plugin.json`.
- OpenCode config can express MCP servers, permissions, agents, commands, plugins, and instructions, so a later adapter could render `opencode.json` for project-local testing.
- The first OpenCode implementation target should be project-local and reversible: a dry-run report plus optional `.opencode/skills` or `.agents/skills` fixture in a temporary checkout, not a global user install.

Sources:

- [OpenCode Agent Skills](https://opencode.ai/docs/skills/)
- [OpenCode Config](https://opencode.ai/docs/config/)
- [OpenCode Plugins](https://opencode.ai/docs/plugins/)
- [OpenCode MCP servers](https://opencode.ai/docs/mcp-servers/)

### Zed

Zed documents Agent Skills for the Zed Agent. Skills live in:

- global: `~/.agents/skills/`
- project-local: `<worktree>/.agents/skills/`

Zed's skill format is a folder containing `SKILL.md`, with optional `scripts/`, `references/`, and `assets/`. It currently requires `name` and `description`, supports `disable-model-invocation`, and says other Agent Skills specification fields are planned. Zed has a 50KB catalog budget for skill names and descriptions, requires project-local skills to come from trusted worktrees, and does not discover remote registries at runtime.

Zed extensions are separate from Agent Skills. Zed also supports MCP and external agents, but its docs state that Zed Skills apply to the Zed Agent; external agents and terminal threads use their own native systems.

Practical Socket implication:

- Codex-in-Zed through the bundled Codex ACP adapter should use the normal Codex marketplace path. Local testing on 2026-06-26 showed a Zed-hosted Codex session with `__CFBundleIdentifier=dev.zed.Zed`, inherited `HOME=/Users/galew`, no explicit `CODEX_HOME`, Socket plugins at `7.2.1`, and the normal Codex MCP server list available.
- Zed is a strong target for `.agents/skills` output with no remote registry promise.
- Skill descriptions need to stay concise because Zed enforces a catalog budget.
- Socket should not assume Zed external agents consume Zed Skills. A Claude or Codex session inside Zed needs that external agent's own config path.
- Use `operate-zed-agent` to choose between Zed Agent, an ACP External Agent,
  and a Terminal Thread.
- Check the canonical ACP Registry before recommending registry installation.
  Hermes is not currently published there despite its source manifest and
  documentation; use the official `hermes` plus `args: ["acp"]` custom-agent
  path after `hermes acp --check` until the registry feed changes.

Sources:

- [Zed Skills](https://zed.dev/docs/ai/skills)
- [Zed Agent Panel](https://zed.dev/docs/ai/agent-panel)
- [Zed MCP](https://zed.dev/docs/ai/mcp)
- [Zed External Agents](https://zed.dev/docs/ai/external-agents)

### Agent Client Protocol

ACP is the shared editor-to-agent boundary for Zed, Xcode, and other clients.
The editor/client owns the conversation and review UI; the launched agent owns
its runtime, provider authentication, model, native skills, and persistent
state. ACP can carry client-provided MCP server configuration, but ACP and MCP
remain separate protocols and security boundaries.

Socket now routes this work through:

- `choose-agent-integration-protocol` for ACP versus MCP, terminal, native host,
  Hermes TUI gateway, or HTTP API selection.
- `operate-acp-agent-integration` for registry discovery, launch commands,
  authentication, capability negotiation, sessions, permissions, and logs.
- `build-acp-agent` for protocol implementation, testing, package publication,
  and canonical registry submission.
- `operate-zed-agent` and
  `apple-dev-skills:xcode-coding-intelligence-workflow` for client-owned setup.

The current stable ACP wire version is 1. Clients and agents negotiate it and
optional capabilities during initialization; SDK or schema-package versions do
not determine wire compatibility by themselves.

Sources:

- [ACP architecture](https://agentclientprotocol.com/get-started/architecture)
- [ACP initialization](https://agentclientprotocol.com/protocol/v1/initialization)
- [ACP Registry](https://agentclientprotocol.com/get-started/registry)
- [Xcode coding intelligence setup](https://developer.apple.com/documentation/xcode/setting-up-coding-intelligence)

### Hermes Agent

Hermes is now a shipped Socket compatibility target backed by the official
Hermes user guide, developer guide, reference, and public source repository.
Socket publishes a generated GitHub skill tap, checked-in MCP translations, a
compatibility validator, and a focused operator/developer workflow set.

Current Hermes extension systems include portable Agent Skills, MCP,
config-driven integrations, general Python plugins, messaging platform
adapters, model/memory/context/secret/media/search/browser providers, gateway
hooks, desktop plugins, dashboard plugins, ACP, TUI gateway JSON-RPC, and the
OpenAI-compatible API server. These are not interchangeable package shapes.

Practical Socket implication:

- Keep `SKILL.md` as the portable authored unit and root `skills/` as the generated Hermes tap.
- Translate Socket MCP declarations into reviewed `mcp_servers` fragments; do not copy Codex config verbatim.
- Route Hermes use through `choose-hermes-agent-workflow`, `operate-hermes-agent`, `build-hermes-agent-extensions`, `operate-hermes-agent-gateway`, and `use-nous-research-services`.
- Keep Codex manifests, apps, hooks, and custom-agent metadata host-specific until a concrete Hermes surface is designed.
- Distinguish the Hermes messaging gateway, Nous Tool Gateway, and TUI gateway in every compatibility decision.

Sources:

- [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs/)
- [Build a Hermes Plugin](https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin)
- [Nous Portal](https://hermes-agent.nousresearch.com/docs/integrations/nous-portal)
- [Hermes compatibility guide](./hermes-compatibility.md)

## Likely Socket Work

### Low-Risk Work

- Add a root `skills` portability audit that validates common skill constraints across Codex, OpenCode, and Zed.
- Keep or generate `.agents/skills` discovery mirrors for skill-only consumers.
- Add concise compatibility notes to skill metadata where a host ignores unknown frontmatter.
- Add a current-docs checklist for each target before claiming support.
- Add an export dry-run command that reports what would be written for each target without mutating user homes.

### Medium-Risk Work

- Render project-local config examples for OpenCode and Claude Code.
- Render Claude `.claude/agents/` equivalents for Codex `agents/openai.yaml` custom-agent roles.
- Add per-target docs in `docs/maintainers/` and route them from the root packaging strategy.
- Add install-surface smoke tests with temporary homes for OpenCode and Claude Code once their CLIs are locally available.

### High-Risk Work

- Build Xcode plug-in writers before the official import behavior is represented by a dry-run assessment and at least one reversible smoke test.
- Convert Codex hooks to OpenCode or Claude plugins without a security and permission model pass.
- Present a Codex/Claude/Xcode package as a Hermes plugin without selecting the real Hermes extension surface.
- Create an aggregate cross-host Socket package before one target clearly needs that distribution shape.

## Proposed Implementation Slices

### Slice 1: Inventory And Constraints

- Add a root portability report command that inventories every `SKILL.md`, plugin manifest, MCP config, hook, app config, and custom-agent definition.
- Validate common skill-name and description constraints for Codex and OpenCode first.
- Include Zed's flat roots, trusted-worktree rule, catalog budget, and native-versus-external boundary in the report.
- Report host-specific blockers instead of mutating files.

### Slice 2: OpenCode Skills-Only Export

- Add a dry-run exporter for OpenCode-compatible skill output from the authored Socket skill roots.
- Decide whether the first output should be `.agents/skills`, `.opencode/skills`, symlink mirrors, generated copies, or install instructions.
- Keep generated or consumer-side install output out of git unless the output is intentionally committed as a project-local fixture.

### Slice 3: Xcode 27 Beta Probe And Adapter Plan

- [x] Probe the Xcode 27 beta target through the intentionally selected beta toolchain. The original 2026-06-23 evidence used a command-scoped override; current workflow guidance uses `xcode-select` and does not inject `DEVELOPER_DIR`.
- [x] Open the beta Xcode app and target the live process through `MCP_XCODE_PID`.
- [x] Inspect Xcode `run-agent --dry-run codex` behavior and verify that direct `codex skills export` is not a usable beta path.
- [x] Inspect Xcode CodingAssistant config folders after official plug-in imports.
- [x] Probe Xcode's Plug-ins import UI with a harmless fixture before adding a Socket export or package adapter.
- [x] Record the concrete Xcode plug-in import/package evidence before adding a Socket export or package adapter.

### Slice 3A: Xcode Install Support Assessment

- [x] Add a dry-run report for Xcode support that inventories every Socket child plugin and classifies its skills, MCP servers, hooks, apps, and custom-agent metadata.
- [x] For each child plugin, report support separately for Xcode-launched Codex, Xcode internal agents through plug-ins, and external agents using Xcode MCP.
- [x] Mark skill-only payloads as likely-first candidates for Xcode internal agents.
- [x] Mark local MCP payloads as requiring install-path and dependency handling before claiming full-fidelity Xcode internal-agent support.
- [x] Mark hooks as recognized-but-unverified for Xcode until execution behavior is probed.
- [x] Mark Codex apps and OpenAI custom-agent metadata as Codex-specific unless Xcode exposes equivalent component types.

### Slice 4: Host Config Adapters

- Add target-specific renderers for:
  - OpenCode `opencode.json` and `.opencode/skills`
  - Xcode-launched Codex config under the Xcode CodingAssistant home
  - Claude Code project settings and `.claude/skills`
  - Zed project-local `.agents/skills`
- Keep all writes behind dry-run, backup, and explicit apply gates.
- Route heavier local discovery and apply operations through AgentUtils when the app exposes a supported contract.

### Slice 5: Plugin And Tool Adapters

- Evaluate whether Codex hooks, MCP registrations, and custom-agent roles have safe equivalents in Claude Code, OpenCode, Xcode, or Zed.
- Add only adapters with a clear trust and permission story.
- Keep host-specific adapters separate from Socket's existing Codex marketplace catalog.

## Open Questions

- Does the Agent Skills specification require any frontmatter fields or size limits beyond what Zed and OpenCode currently document?
- Should Socket's source of truth stay as per-child `skills/`, or should a root export index own cross-host skill publishing?
- Should project-local `.agents/skills` output be a generated mirror, symlink tree, or documented install command?
- Which CLI surfaces are installed locally and stable enough for smoke tests?
- When will the official Hermes 0.18.2 `uvx` manifest be accepted into the canonical ACP Registry?
- Which Socket child plug-ins can be imported from the public Git URL without path, dependency, auth, hook, or MCP execution issues?

## Decision Gate

Do not change marketplace metadata, packaged plugin roots, or production install guidance until Slice 1 produces a real inventory and at least one target-specific dry-run shows what Socket would add, skip, or transform.
