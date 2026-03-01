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

## Quick Start (Vercel Skills CLI)

Use the Vercel `skills` CLI against this repository to install any skill directory you want to use. Or install them all conveniently with one command.

```bash
# Install your choice of skill(s) via the Vercel `skills` CLI
# Using `npx` fetches `skills` without installing it on your machine
npx skills add gaelic-ghost/apple-dev-skills
```

The CLI will prompt you to choose which skill(s) to install from this repo.

Notes on `skills` CLI flags (see https://www.npmjs.com/package/skills):

- `-a` targets a specific agent (for example `codex`).
- `-g` installs to the global profile.

## Install individually by Skill

```bash
# Xcode Skill Pack 1/4
npx skills add gaelic-ghost/apple-dev-skills@apple-xcode-hybrid-orchestrator
```
```bash
# Xcode Skill Pack 2/4
npx skills add gaelic-ghost/apple-dev-skills@xcode-mcp-first-executor
```
```bash
# Xcode Skill Pack 3/4
npx skills add gaelic-ghost/apple-dev-skills@apple-swift-cli-fallback
```
```bash
# Xcode Skill Pack 4/4
npx skills add gaelic-ghost/apple-dev-skills@apple-dev-safety-and-docs
```
```bash
# Dash.app Skills Pack 1/2
# Search Docsets and Cheatsheets 
npx skills add gaelic-ghost/apple-dev-skills@
```
```bash
# Dash.app Skills Pack 2/2
# Install or Generate Docsets and Cheatsheets 
npx skills add gaelic-ghost/apple-dev-skills@
```
```bash
# Bootstrap a Swift package with consistent defaults
npx skills add gaelic-ghost/apple-dev-skills@bootstrap-swift-package
```
```bash
# Automate maintaining a consistent `AGENST.md` across many Swift repos
npx skills add gaelic-ghost/apple-dev-skills@swift-package-agents-maintainer
```

## Find Skills like these with the `skills` CLI by Vercel — [vercel-labs/skills](https://github.com/vercel-labs/skills)

```bash
npx skills find "xcode mcp"
npx skills find "xcodebuild test swiftpm"
npx skills find "dash docset apple docs"
```

## Find Skills like these with `Find Skills` by Vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)

Install Vercel's skill bundle (which includes `find-skills`), then query the ecosystem:

```bash
# Install vercel-labs agent-skills bundle
npx skills add vercel-labs/agent-skills
```

```bash
# Search for relevant skills with `skills find`
npx skills find "xcode mcp swift"
npx skills find "apple docs dash docsets"
npx skills find "swift package workflow"
```

Learn more:
- Skills catalog: https://skills.sh/
- `find-skills`: https://skills.sh/vercel-labs/skills/find-skills

## v1.0.0 Contents

Version `v1.0.0` includes the four skills above as the initial Apple-development bundle.

## v1.1.0 Highlights

Version `v1.1.0` focuses on public portability and customization:

- sanitizes user-specific path assumptions in skill content
- removes tracked Python cache artifacts
- adds per-skill customization guides:
  - `bootstrap-swift-package/README.md`
  - `swift-package-agents-maintainer/README.md`
  - `dash-docset-search/README.md`
  - `dash-docset-install-generate/README.md`

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

## Repository Layout

```text
.
├── README.md
├── LICENSE
├── bootstrap-swift-package/
├── swift-package-agents-maintainer/
├── dash-docset-search/
├── dash-docset-install-generate/
├── apple-xcode-hybrid-orchestrator/
├── xcode-mcp-first-executor/
├── apple-swift-cli-fallback/
└── apple-dev-safety-and-docs/
```

## Notes

- The structure is intentionally flat at the repository root for ease of navigation and discoverability.

## Search Keywords

Xcode MCP, xcodebuild, xcodebuild test, xcrun, SwiftPM, swift build, swift test, swift run, swift package, swiftly, Swift toolchain, Dash docsets, Apple developer docs, Codex skills.

## License

See [LICENSE](./LICENSE).
