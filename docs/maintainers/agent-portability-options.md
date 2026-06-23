# Agent Portability Options

This document records the first research pass for making Socket skills and plugins more portable across agent hosts while keeping the current Codex marketplace honest.

Date checked: 2026-06-23.

## Current Recommendation

Treat Agent Skills as the first portability layer.

Socket already keeps authored skills as `skills/<name>/SKILL.md` with optional `references/`, `scripts/`, and `assets/` folders. That shape maps cleanly to the emerging Agent Skills convention used by several current tools. The lowest-risk next step is to validate and, where needed, render those skill folders for each host's documented discovery paths.

Treat plugins as host-specific package adapters.

Codex, Claude Code, OpenCode, Xcode, and Zed each expose different plugin or extension concepts. Socket should not redefine its root as a generic plugin bundle until a concrete target needs that shape. Keep the current root as a Codex marketplace catalog, then add per-host export or install support as deliberate adapter outputs.

## Near-Term Focus

Start with Xcode 27 beta and OpenCode.

Those are the two locally installed targets available for immediate smoke tests on Gale's machine:

- Xcode 27 beta: `/Users/galew/Applications/Betas/Xcode-beta.app`, verified with `DEVELOPER_DIR=/Users/galew/Applications/Betas/Xcode-beta.app/Contents/Developer xcodebuild -version` as Xcode 27.0 build 27A5194q.
- Xcode 27 beta live bridge: verified on 2026-06-23 with the beta app open and selected through `MCP_XCODE_PID`; `run-agent --dry-run codex` resolved the beta-scoped Codex runtime, and `run-agent skills export` produced seven Xcode-visible skills for inspection.
- Active command-line Xcode: `/Applications/Xcode.app`, currently Xcode 26.5 build 17F42 through the default `xcodebuild -version`.
- OpenCode CLI: `/opt/homebrew/bin/opencode`, verified as 1.17.9.
- OpenCode Desktop: `/Applications/OpenCode.app`, present locally.

Defer Zed until the Xcode and OpenCode paths prove the source-of-truth and export model. Zed is likely a strong skill-only target because it reads `.agents/skills`, but it should not drive the first adapter design.

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

### Xcode

Apple documents Xcode agent customization through Xcode Intelligence settings, Xcode-only agent configuration folders, command and tool permissions, built-in skills, MCP, and Xcode plug-ins. The official page says product-specific configuration files live under `~/Library/Developer/Xcode/CodingAssistant`, with separate folders such as `codex`, `ClaudeAgentConfig`, and `gemini`, and that those configurations only affect agents launched in Xcode.

Apple also documents an Xcode plug-in UI that can install plug-ins containing subagents, MCP servers, and skills, but the public page does not expose enough package-format detail to author a Socket-to-Xcode plugin adapter yet.

Local validation target:

- Use `DEVELOPER_DIR=/Users/galew/Applications/Betas/Xcode-beta.app/Contents/Developer` for Xcode 27 beta checks until the active command-line developer directory is intentionally changed.
- Open `/Users/galew/Applications/Betas/Xcode-beta.app` for live beta UI, MCP, agent, and plug-in checks instead of treating a closed app as a blocker.
- Use `MCP_XCODE_PID` when stable and beta Xcode processes could both exist or when the bridge must target the beta process explicitly.
- Keep the default Xcode 26.5 path untouched unless a task explicitly needs `xcode-select` changes.

Practical Socket implication:

- Support Xcode Codex as a separate Codex target, not as a raw mirror of normal `~/.codex`.
- Add an Xcode export plan only after the Xcode plug-in package shape is verified locally.
- Keep Xcode-specific workflow guidance in `apple-dev-skills`, especially `xcode-coding-intelligence-workflow`.
- Treat Xcode-exported skills as comparison evidence unless a later task deliberately imports or adapts them into Socket-authored skill roots.
- Prefer a read-only local probe first: inspect Xcode's CodingAssistant folders, Xcode MCP bridge behavior, and any plug-in import artifacts before writing config.

Sources:

- [Extending and customizing agents](https://developer.apple.com/documentation/xcode/extending-and-customizing-agents/)
- [Xcode 27 agentic tooling skill plan](./xcode-27-agentic-tooling-plan.md)

### Claude Code

Claude Code has a richer configuration hierarchy than most targets in this pass. Current documentation describes managed, user, project, and local scopes. It also documents separate locations for settings, subagents, MCP servers, plugins, and `CLAUDE.md` context.

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

- Skills can likely be exported with little transformation when names and frontmatter stay within common constraints.
- Codex `agents/openai.yaml` custom agents are not portable as-is; Claude Code needs `.claude/agents/` definitions.
- Codex marketplace metadata does not become a Claude Code marketplace automatically. A Claude adapter needs its own settings, marketplace, or plugin registration path.
- The Claude Code policy model is worth supporting explicitly because it can restrict customization to plugin-provided or managed surfaces.

Sources:

- [Claude Code settings](https://code.claude.com/docs/en/settings)
- [Claude Code MCP](https://code.claude.com/docs/en/mcp)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)

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

- Zed is a strong target for `.agents/skills` output with no remote registry promise.
- Skill descriptions need to stay concise because Zed enforces a catalog budget.
- Socket should not assume Zed external agents consume Zed Skills. A Claude or Codex session inside Zed needs that external agent's own config path.

Sources:

- [Zed Skills](https://zed.dev/docs/ai/skills)
- [Zed Agent Panel](https://zed.dev/docs/ai/agent-panel)
- [Zed MCP](https://zed.dev/docs/ai/mcp)
- [Zed External Agents](https://zed.dev/docs/ai/external-agents)

### Hermes Agent

No official Hermes Agent documentation source was found in this pass. Search results only exposed secondary academic references that mention Hermes Agent as an agent harness or always-on personal-agent stack. That is not enough evidence to define a Socket adapter.

Practical Socket implication:

- Keep Hermes Agent as research-blocked.
- Do not add files, docs claims, or install instructions for Hermes until an authoritative documentation or source repository is identified.
- If Hermes is confirmed later, start with its documented skill discovery paths, config files, tool/MCP model, and permission or persistence boundaries.

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

- Build Xcode plug-in packages before the package format and import behavior are verified.
- Convert Codex hooks to OpenCode or Claude plugins without a security and permission model pass.
- Promise Hermes Agent support without official docs.
- Create an aggregate cross-host Socket package before one target clearly needs that distribution shape.

## Proposed Implementation Slices

### Slice 1: Inventory And Constraints

- Add a root portability report command that inventories every `SKILL.md`, plugin manifest, MCP config, hook, app config, and custom-agent definition.
- Validate common skill-name and description constraints for Codex and OpenCode first.
- Include Zed constraints in the report as informational follow-up, but do not let Zed-specific choices drive the first implementation.
- Report host-specific blockers instead of mutating files.

### Slice 2: OpenCode Skills-Only Export

- Add a dry-run exporter for OpenCode-compatible skill output from the authored Socket skill roots.
- Decide whether the first output should be `.agents/skills`, `.opencode/skills`, symlink mirrors, generated copies, or install instructions.
- Keep generated or consumer-side install output out of git unless the output is intentionally committed as a project-local fixture.

### Slice 3: Xcode 27 Beta Probe And Adapter Plan

- [x] Probe the Xcode 27 beta target through explicit `DEVELOPER_DIR`.
- [x] Open the beta Xcode app and target the live process through `MCP_XCODE_PID`.
- [x] Inspect Xcode `run-agent --dry-run codex` and skill export behavior without mutating user state.
- Inspect Xcode CodingAssistant config folders in more detail before writing any Xcode-launched Codex config.
- Record the concrete Xcode plug-in import/package evidence before adding a Socket export or package adapter.

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
- What is the official Hermes Agent documentation or source repository?
- What package format does Xcode expect for an imported agentic coding plug-in?

## Decision Gate

Do not change marketplace metadata, packaged plugin roots, or production install guidance until Slice 1 produces a real inventory and at least one target-specific dry-run shows what Socket would add, skip, or transform.
