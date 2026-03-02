# apple-dev-skills

Codex skills for Apple development workflows focused on Swift, Xcode, and Apple tooling.

## What These Agent Skills Help With

This repository is a practical skill bundle for Apple-platform development work in Codex and similar agents.
It is designed for:

- Swift engineers using Xcode, or working across multiple IDEs
- Maintainers of Swift package repositories
- Agent users who want safer Apple workflow automation
- Teams that want local-first documentation access with Dash docsets
- Anyone who needs smooth access to Apple/Swift/DocC documentation

In short: if you or your users are building, testing, packaging, documenting, or maintaining Apple/Swift projects, these skills provide repeatable workflows and safer defaults.

## Skill Guide (When To Use What)

### Hybrid Apple/Xcode execution and safety

- `apple-xcode-hybrid-orchestrator`
  - Use when you need one entrypoint to route Apple/Swift tasks across MCP-first execution, official CLI fallback, docs policy, and mutation safety checks.
  - Helps by standardizing decision flow so agents do the right thing automatically.

- `xcode-mcp-first-executor`
  - Use when the task should run through Xcode MCP tools first (workspace, read/search, diagnostics, build/test, preview/snippet, structured mutation).
  - Helps by reducing unsafe direct edits and improving Xcode-aware operations.

- `apple-swift-cli-fallback`
  - Use when MCP tools are unavailable, timing out, or missing a needed capability.
  - Helps by automatically switching to official tooling (`xcodebuild`, `xcrun`, `swift`, `swift package`, `swiftly`) with clear guidance and minimal friction.

- `apple-dev-safety-and-docs`
  - Use when mutation risk or documentation source selection matters.
  - Helps by enforcing hard safety gates for risky edits in Xcode-managed projects and applying Dash local-docset-first docs routing.

### Dash docset workflows

- `dash-docset-search`
  - Use when you need to search installed Dash docsets and reason across local docs quickly.
  - Helps by preferring Dash MCP/API paths first and giving deterministic fallback behavior.

- `dash-docset-install-generate`
  - Use when a needed docset is missing and you need install or generation guidance.
  - Helps by making docset availability predictable and improving local docs quality for agents.

### Swift package creation and maintenance

- `bootstrap-swift-package`
  - Use when creating new Swift packages with consistent defaults and first-pass validation.
  - Helps by reducing setup drift and getting package repos to a good baseline quickly.

- `swift-package-agents-maintainer`
  - Use when creating or syncing canonical `AGENTS.md` policy files across Swift package repos.
  - Helps by keeping agent behavior consistent across repositories.

## Customization Workflow Matrix

| Skill | Chat Customization Flow (SKILL.md) | Durable Config (`template` + persisted `customization.yaml`) | Automation Knobs | README Migration Status |
| --- | --- | --- | --- | --- |
| `apple-xcode-hybrid-orchestrator` | Yes | Yes | No | README removed |
| `xcode-mcp-first-executor` | Yes | Yes | No | README removed |
| `apple-swift-cli-fallback` | Yes | Yes | No | README removed |
| `apple-dev-safety-and-docs` | Yes | Yes | No | README removed |
| `dash-docset-search` | Yes | Yes | Yes | README removed |
| `dash-docset-install-generate` | Yes | Yes | Yes | README removed |
| `bootstrap-swift-package` | Yes | Yes | Yes | README removed |
| `swift-package-agents-maintainer` | Yes | Yes | Yes | README removed |

## Quick Start (Vercel Skills CLI)

Use the Vercel `skills` CLI against this repository to install any skill directory you want to use. Or install them all conveniently with one command.

```bash
# Install your choice of skill(s) via the Vercel `skills` CLI
# Using `npx` fetches `skills` without installing it on your machine
npx skills add gaelic-ghost/apple-dev-skills
```

```bash
# Install all skills with one command
npx skills add gaelic-ghost/apple-dev-skills --all
```

The CLI will prompt you to choose which skill(s) to install from this repo.

Notes on `skills` CLI flags (see https://www.npmjs.com/package/skills):

- `-a` targets a specific agent (for example `codex`).
- `-g` installs to the global profile.

## Install individually by Skill or Skill Pack

```bash
# Xcode Skill Pack (4 Skills)
# Install Skill Packs as a set to ensure proper functionality
# Use Xcode and Swift tooling safely and effectively with platform guidance
npx skills add gaelic-ghost/apple-dev-skills \
--skill apple-xcode-hybrid-orchestrator \
--skill xcode-mcp-first-executor \
--skill apple-swift-cli-fallback \
--skill apple-dev-safety-and-docs
```

```bash
# Dash.app Skills Pack (2 Skills)
# Install Skill Packs as a set to ensure proper functionality
# Search, Install, and Generate Dash.app Docsets and Cheatsheets
npx skills add gaelic-ghost/apple-dev-skills \
	--skill dash-docset-search \
	--skill dash-docset-install-generate
```

```bash
# Bootstrap a Swift package with consistent defaults
npx skills add gaelic-ghost/apple-dev-skills \
	--skill bootstrap-swift-package
```
```bash
# Automate maintaining a consistent `AGENTS.md` across many Swift repos
npx skills add gaelic-ghost/apple-dev-skills \
	--skill swift-package-agents-maintainer
```

## Check out my other Skills
- [gaelic-ghost/a11y-skills](https://github.com/gaelic-ghost/a11y-skills)
- [gaelic-ghost/productivity-skills](https://github.com/gaelic-ghost/productivity-skills)
- [gaelic-ghost/python-skills](https://github.com/gaelic-ghost/python-skills)

## Update Skills

```bash
# Check for available updates to installed Skills
npx skills check
# Update installed Skills
npx skills update
```

## More resources for similar Skills

### Find Skills like these with the `skills` CLI by Vercel — [vercel-labs/skills](https://github.com/vercel-labs/skills)

```bash
npx skills find "xcode mcp"
npx skills find "xcodebuild test swiftpm"
npx skills find "dash docset apple docs"
```

### Find Skills like these with the `Find Skills` Agent Skill by Vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)

Install Vercel's skill bundle (which includes `find-skills`), then query the ecosystem:

```bash
# Install vercel-labs agent-skills bundle
npx skills add vercel-labs/agent-skills
```

Learn more:
- Skills catalog: https://skills.sh/
- `find-skills`: https://skills.sh/vercel-labs/skills/find-skills


Then ask your Agent for help finding a skill for "" or ""

## v1.0.0 Contents

Version `v1.0.0` includes the four skills above as the initial Apple-development bundle.

## v1.1.0 Highlights

Version `v1.1.0` focuses on public portability and customization:

- sanitizes user-specific path assumptions in skill content
- removes tracked Python cache artifacts
- adds per-skill customization guides for:
  - `bootstrap-swift-package`
  - `swift-package-agents-maintainer`
  - `dash-docset-search`
  - `dash-docset-install-generate`

## v1.2.0 Highlights

Version `v1.2.0` adds automation prompt support across all bundled skills:

- adds `references/automation-prompts.md` to each skill with:
  - Codex App automation prompt templates
  - Codex CLI (`codex exec`) automation prompt templates
  - placeholder-driven customization knobs and guardrails
- adds `Automation Prompting` sections to each `SKILL.md` with App/CLI fit guidance (`Strong` or `Guarded`)
- updates each `agents/openai.yaml` `default_prompt` to explicitly route users to automation template usage

## v1.3.0 Highlights

Version `v1.3.0` adds a portable Apple/Swift/Xcode hybrid workflow suite:

- `apple-xcode-hybrid-orchestrator`
  - entrypoint routing for MCP-first execution, official CLI fallback, and safety/docs handoff
- `xcode-mcp-first-executor`
  - strict Xcode MCP tool routing with workspacePath-first tab resolution and fallback handoff policy
- `apple-swift-cli-fallback`
  - automatic official-tooling fallback for `xcodebuild`, `xcrun`, SwiftPM, and toolchain checks
- `apple-dev-safety-and-docs`
  - hard mutation safety gate for Xcode-managed scope and Dash local-first docs guidance with advisory cooldown policy

## v1.4.0 Highlights

Version `v1.4.0` improves root-level discoverability and navigation:

- adds top-level workflow and skill guide sections for faster skill selection
- renames and clarifies the top summary heading for first-time readers
- improves keyword and discovery coverage in root docs

## v1.4.1 Highlights

Version `v1.4.1` improves documentation portability:

- converts Vercel repo references to inline GitHub links where appropriate
- completes `find-skills` guidance in root README usage examples

## v1.4.2 Highlights

Version `v1.4.2` applies final README cleanup before roadmap-based planning:

- cleans up README footer content and license section wording
- keeps root documentation structure consistent with latest tag metadata

## v1.5.0 Highlights

Version `v1.5.0` introduces durable, in-skill customization workflows across the full bundle:

- replaces per-skill customization `README.md` files with `Interactive Customization Flow` sections in each `SKILL.md`
- adds per-skill `customization.template.yaml` defaults and persistent user customization state at `~/.config/gaelic-ghost/apple-dev-skills/<skill-name>/customization.yaml`
- adds `scripts/customization_config.py` in each skill for `path`, `effective`, `apply`, and `reset` config operations
- adds `references/customization-flow.md` in each skill to provide a structured chat-first customization procedure
- adds a root `Customization Workflow Matrix` to improve discoverability and status tracking
- updates CI validation to enforce customization-flow contracts (`customization.template.yaml`, `scripts/customization_config.py`, and `Interactive Customization Flow` section presence)

## v1.6.0 Highlights

Version `v1.6.0` improves grouped skill-pack organization and install guidance:

- groups skills into workflow-domain folders for better repository navigation:
  - `swift-xcode-tools`
  - `dash-apple-swift-documentation`
  - `apple-swift-repo-tools`
  - `apple-swift-bootstraps`
- updates root README install examples to use repo-root source plus `--skill` flags for pack-oriented installs
- adds "install all" guidance with `--all` for one-command setup
- updates CI validation to discover `SKILL.md` recursively so nested skill directories remain supported

## v1.6.1 Highlights

Version `v1.6.1` adds Claude Code plugin manifest compatibility for grouped nested skills:

- adds `.claude-plugin/marketplace.json` at the repository root
- maps each nested skill pack to explicit plugin entries and relative skill paths
- enables `skills` CLI plugin-manifest discovery/grouping for the nested pack layout

## Repository Layout

```text
.
├── README.md
├── LICENSE
├── apple-swift-bootstraps/
│   └── bootstrap-swift-package/
├── apple-swift-repo-tools/
│   └── swift-package-agents-maintainer/
├── dash-apple-swift-documentation/
│   ├── dash-docset-search/
│   └── dash-docset-install-generate/
└── swift-xcode-tools/
    ├── apple-xcode-hybrid-orchestrator/
    ├── xcode-mcp-first-executor/
    ├── apple-swift-cli-fallback/
    └── apple-dev-safety-and-docs/
```

## Notes

- The structure is intentionally grouped by workflow domain while preserving skill-level discoverability.

## Keywords

Xcode MCP, xcodebuild, xcodebuild test, xcrun, SwiftPM, swift build, swift test, swift run, swift package, swiftly, Swift toolchain, Dash docsets, Apple developer docs, Codex skills.

## License

See [LICENSE](./LICENSE).
