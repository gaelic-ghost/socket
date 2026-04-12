# AGENTS.md

## Repository Expectations

- Never modify production-installed skills under `~/.agents/skills` while working in this development repository.
- This file defines maintainer guidance for developing skills in this repository. Keep these links and rules at repo root for contributor workflows.

## Standards and Guidance

- For any skill that governs Swift, Apple framework, Apple platform, SwiftUI, SwiftData, Observation, AppKit, UIKit, Foundation-on-Apple, or Xcode-related work, require reading the relevant Apple documentation first before proposing or permitting implementation guidance.
- Such skills must require the agent to state the documented behavior being relied on before design or code changes are proposed.
- Apple docs outrank memory, habit, and analogy. If docs and current code conflict, the skill must instruct the agent to stop and report that conflict.
- If no relevant Apple documentation can be found, the skill must instruct the agent to say that explicitly before proceeding.
- For any skill that governs Swift or Apple-platform implementation work, require an explicit simplicity-first policy: prefer the simplest correct Swift that is easiest to read and reason about.
- Such skills must treat idiomatic Swift, Cocoa conventions, and modern Swift features as tools in service of readability rather than goals by themselves.
- Such skills must strongly prefer synthesized, implicit, and framework-provided behavior over custom boilerplate.
- Such skills must instruct the agent not to add `CodingKeys`, manual `Codable`, custom initializers, helper abstractions, wrappers, protocols, coordinators, or extra layers unless they are required by a concrete constraint or make the final code clearly easier to understand.
- Such skills must treat naming consistency as a reliability feature and prefer stable source-of-truth names across layers when the data and meaning have not changed.
- Such skills must instruct the agent not to rename fields merely to match local style conventions and not to use automatic case-conversion strategies such as `.convertFromSnakeCase` or `.convertToSnakeCase` unless the project explicitly wants that behavior and it clearly improves readability.
- Such skills must prefer applicable existing framework or platform error types before inventing custom error wrappers or error hierarchies.
- Such skills must strongly discourage redundant DTO, domain, and view-model transformation layers when wire or persistence shapes and meanings have not changed.
- Such skills should explicitly encode an advanced-Swift bias toward dense but readable modern Swift rather than beginner-oriented explicitness.
- Such skills should prefer compact functional and stream-style constructs, ternary expressions, and top-down chopped formatting when they improve readability.
- Such skills should prefer Swift Logging, Swift OpenTelemetry, and Apple-native logging or telemetry facilities according to project context instead of bespoke wrappers.
- Such skills should prefer SwiftFormat by Nick Lockwood and/or SwiftLint as baseline Swift formatting or linting tools, with at least one present in any Swift project.
- Such skills should teach SwiftUI as component UI with small reusable views, small focused controller classes, straight data flow, and clear `App` / `Scene` / `View` lifecycle boundaries.
- Such skills must not teach pattern slogans like value types by default or protocols at seams as rules that outrank local simplicity and readability.
- Such skills should explicitly allow first-party and top-tier Swift ecosystem packages when they simplify the code and improve reasoning, especially packages such as `swift-configuration` and `swift-async-algorithms`.

Consult these resources when creating, updating, reviewing, or sharing skills:

- Agent Skills Standard: [agentskills.io/home](https://agentskills.io/home)
- Vercel KB Guidance: [vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context](https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context)
- Skill Creator workflow: [$skill-creator](/Users/galew/.codex/skills/.system/skill-creator/SKILL.md)
- OpenAI Codex Skills: [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills)
- OpenAI Codex AGENTS.md configuration: [developers.openai.com/codex/configuration/agents-md](https://developers.openai.com/codex/configuration/agents-md)
- OpenAI Codex MCP documentation: [https://developers.openai.com/codex/mcp/](https://developers.openai.com/codex/mcp/)
- Claude Code Features Overview: [code.claude.com/docs/en/features-overview](https://code.claude.com/docs/en/features-overview)
- Claude Code Skills: [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)
- Anthropic Agent Skills Best Practices: [platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Claude Code Plugins: [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins)
- The Complete Guide to Building Skill for Claude (PDF): [resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)

Applicability guidance:

- Always consult the `$skill-creator` workflow for skill lifecycle work: [/Users/galew/.codex/skills/.system/skill-creator/SKILL.md](/Users/galew/.codex/skills/.system/skill-creator/SKILL.md)
- Always consult Agent Skills Standard and Vercel guidance for cross-platform standards alignment.
- When OpenAI/Codex product behavior or APIs are involved, consult the built-in `openaiDeveloperDocs` MCP server and `$openai-docs` skill before using secondary sources.
- Consult Claude docs when behavior is Claude skills/plugins specific.

## Plugins and Subagents

- Keep the terminology straight across ecosystems and docs:
  - a `skill` is the reusable authoring unit for workflow guidance
  - a `plugin` is a distribution bundle
  - a `subagent` is a delegated runtime worker with its own context and tool policy
- For Codex, treat skills as the primary authoring format and plugins as the installable distribution unit that can bundle skills, apps, and MCP servers.
- For Codex work, prefer starting with a local skill when iterating on one workflow in one repository. Escalate to plugin packaging only when the workflow should be distributed across teams, published through a marketplace, or shipped together with app integrations or MCP configuration.
- For Codex and Claude work in this repository, the canonical export surface is top-level `skills/` today. If top-level `mcps/` or `apps/` are added later, those top-level directories are the only other valid export surfaces.
- This repository must not reintroduce a nested packaged plugin tree, repo-local installer workflow, or any other second export surface under `plugins/`.
- Do not track consumer-side install copies, caches, or machine-local runtime state in this repository.
- Follow canonical Codex and Claude project-level discovery guidance on macOS and Linux through POSIX symlink mirrors for local discovery:
  - `.agents/skills -> ../skills`
  - `.claude/skills -> ../skills`
- Treat the local discovery mirrors as conveniences, not as independent sources of truth.
- For Claude Code, keep in mind that plugins can package more than skills alone. Claude plugins may bundle commands, hooks, MCP or LSP configuration, skills, and plugin-scoped subagents.
- For Claude Code subagents, treat them as Markdown-plus-frontmatter runtime personas with their own prompts, tool access, and context window. They are not a replacement for shared skills or repo guidance.
- For Codex subagents, treat them as explicit delegation infrastructure for bounded parallel or specialized work. They should not be assumed to exist unless the host supports them and the task actually benefits from delegation.
- Use subagents for noisy or separable work such as exploration, triage, tests, audits, or summarization. Be cautious with parallel write-heavy workflows because coordination cost and edit conflicts can outweigh the benefit.
- Do not blur these layers in repo docs:
  - `AGENTS.md` defines durable behavior and project policy
  - skills define reusable workflows
  - plugins package installable distribution surfaces
  - subagents define runtime delegation behavior
- When documenting cross-platform compatibility, say explicitly whether guidance is:
  - shared between Codex and Claude
  - Codex-specific
  - Claude-specific
- This repository's source of truth remains the shipped skill assets under `skills/`. If plugin manifests, marketplaces, or subagent definitions are added later, document them as packaging or delegation layers around the skills rather than as replacements for the canonical skill surface.

## Skill Runtime Model

- A skill is an instruction and workflow-guidance layer. It teaches and structured tool use; it does not become the tool runtime.
- Skills may include local scripts for validation, policy enforcement, fallback shaping, and automation support.
- Skills in this repo must not present themselves as direct MCP clients or executors.
- When MCP is involved, the skill should guide agent-side MCP usage rather than present itself as the MCP client.
- Local scripts may enforce policy or produce plans, but they must not overclaim direct MCP execution.
- This rule applies to `SKILL.md`, workflow diagrams, customization contracts, runtime helper scripts, and maintainer-facing documentation.

## Snippet Policy

- Keep reusable end-user snippet source files in `shared/`.
- Keep per-skill internal copies of relevant snippets under `references/snippets/`.
- In each skill `SKILL.md`, reference local snippet copies and recommend adding snippets to end-user repos when the task involves baseline policy setup.

## Specialization Boundaries

- Keep `xcode-build-run-workflow` focused on execution, diagnostics, mutation safety, file-membership follow-through, and fallback planning for existing Xcode-managed or Xcode-adjacent build and run work.
- Keep `xcode-testing-workflow` focused on Swift Testing, XCTest, XCUITest, `.xctestplan`, filtering, retries, and test diagnosis in existing Xcode-managed or Xcode-adjacent work.
- Keep `swift-package-build-run-workflow` focused on package build/run, manifest, dependency, plugin, resource, Metal-distribution, and Release-versus-Debug work in SwiftPM repos.
- Keep `swift-package-testing-workflow` focused on Swift Testing, XCTest holdouts, `.xctestplan`, fixtures, async test guidance, and test diagnosis in SwiftPM repos.
- Keep `xcode-app-project-workflow` and `swift-package-workflow` as legacy compatibility-routing surfaces only while migration references still exist; do not treat them as primary execution owners in new docs, prompts, or generated guidance.
- Keep `explore-apple-swift-docs` focused on Apple and Swift docs exploration across Xcode MCP docs, Dash, and official web docs.
- When an execution workflow needs documentation context, prefer entering or recommending `explore-apple-swift-docs` first rather than rebuilding docs-source selection inside the execution skills.

## Anatomy of an Agent Skill

The structure of a Skill, including purposes of each component:

### `SKILL.md`

The primary file for an Agent Skill, containing YAML Frontmatter and Markdown content.

#### YAML Frontmatter

Required fields:

- `name`: Lowercase letters/numbers with single hyphens. Must match name of parent directory. Should be clear, concise, and consistent with neighboring skills. Default to `<category>-<domain>-<purpose>` format.
- `description`: Used as trigger to activate skill. Should say what the skill does, and say when to use it.

Option, recommended fields:

- `license`: match to license in repo.
- `compatibility`: use in cases of hard environmental requirements.
- `metadata`: arbitrary k/v, good for semver and other info.
- `allowed-tools`: experimental, support varies across the ecosystem.

#### Skill Body (Markdown)

The Markdown body has no required format, but if you want reliability, use a predictable structure:

- What this skill does
- When to use it (and when not to)
- Inputs needed
- Step-by-step procedure
- Validation / “how to know we’re done”
- Common failure modes and fixes

### Additional Directories

- `scripts/`: For executable helpers. Useful in supporting deterministic, repeatable, automatable steps in workflows.
- `references/`: For longer documentation, checklists, internal templates, etc.
- `assets/`: For static/output templates, diagrams, etc.
### Python-backed Skills

- A skill may include Python helpers under `scripts/` and Python tests under a skill-local `tests/` directory when deterministic validation or local tooling is useful.
- In `*-skills` repositories that contain Python-backed skills, `pytest` and `PyYAML` should be readily available as the default maintainer/dev baseline.
- In this repository, maintain that baseline through repo-root `pyproject.toml` and `uv.lock`, and run checks with `uv run ...`.
- Treat this as repository-maintainer tooling only, not as an installed-skill runtime requirement for end users.

### Constraints on Skills (Config/Customization/Automation)

Skills are installed by an end user for their Agent to make use of. Skill installation is typically handled by the Vercel `skills` CLI, and located in a managed directory that neither Skill, nor Agent, will have write access to. Keep this in mind when considering customizations and configuration.

Some alternatives for user customization/config include using their Agent's memory or personalization features, an end user's global or project-level `AGENTS.md` file, automation workflows such as Codex App Automations or Codex CLI exec workflows, and storing user-set custom configs within `~/.config/gaelic-ghost/<REPO>/<SKILL>/`.

## Repo-local Passive Standards

- Prefer `uv run` for Python command execution in examples and scripts.
- Keep maintainer-side Python tooling available as uv-managed tools when optional repo checks need it, including guidance for `uv tool install ruff` and `uv tool install mypy`.
- Keep skill instructions deterministic, concise, and safety-forward.
- Fully implement every genuinely useful and applicable skill capability, metadata surface, resource type, and validation path. Do not skip helpful skill features for convenience just because they are optional; omit a feature only when it is truly inapplicable, empty, misleading, or harmful for that specific skill.
- Implement all applicable YAML fields in the Frontmatter.
- Never auto-install skills; report required commands and wait for user confirmation.
- Keep skill runtime resources inside the skill directory: `SKILL.md`, `agents/openai.yaml`, `scripts/`, `references/`, and `assets/`.
- Keep active repo-authored export surfaces at the repository top level: `skills/` today, plus `mcps/` or `apps/` only if those top-level directories are added later.
- Prefer symlinks over hardlinks for discovery mirrors in this repository. Hardlinks are not a durable repository contract.
- Do not make installed skills depend on repo-level docs under `docs/`.
- Repo-maintainer docs live under `docs/maintainers/`.
- Use `docs/maintainers/reality-audit.md` as the maintainer operating guide for source-of-truth order, audit procedure, durable review criteria, and reusable repo-maintenance conventions.
- Use `docs/maintainers/workflow-atlas.md` for repo-maintainer workflow diagrams, branch paths, workflow inputs/outputs, and Agent+Skill UX audits.
- Use `docs/maintainers/customization-consolidation-review.md` as the source of truth for the current customization-surface decision and its approved follow-up plan.
- Use `docs/maintainers/execution-split-and-inference-plan.md` as the source of truth for the planned execution-skill split, inference direction, guidance-preservation contract, and the current repo-maintenance toolkit ownership model.
- Use `docs/maintainers/workflow-guidance-preservation-matrix.md` as the concrete mapping from monolithic execution guidance to narrower skill or `AGENTS.md` destinations during the split.
- Prefer logically grouped skills over splitting adjacent workflows into separate skills.
- Within a grouped skill, define one primary workflow path and keep variants subordinate to that path.
- Do not create a separate skill for an adjacent workflow unless it has materially different tools, inputs, outputs, and audience.
- Use the same names for the same concepts across `SKILL.md`, `agents/openai.yaml`, references, automation prompts, and scripts.
- If config changes workflow decisions or output contracts, surface that in the main workflow instead of hiding it only in references.
- When docs and scripts disagree on a workflow contract, fix the script or explicitly narrow the documented contract so they match.
- When asked to report roadmap status, reconcile `ROADMAP.md` against completed repo work first or explicitly say the roadmap is stale before summarizing it.
- After completing milestone work, update `ROADMAP.md` in the same change unless the user explicitly says not to.
