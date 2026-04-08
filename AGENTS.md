# AGENTS.md

## Repository Expectations

- For work in this repository, edit skills only under `/Users/galew/Workspace/productivity-skills/skills`.
- Never modify production-installed skills under `~/.agents/skills` while working in this development repository.
- This file defines maintainer guidance for developing skills in this repository. Keep these links and rules at repo root for contributor workflows.
- Repository direction: keep this repo focused on broadly useful global-install skills and on the canonical general-purpose baseline versions of workflow families that may later specialize into stack- or language-specific plugins. Prefer dedicated stack- or repo-specific plugins for workflows whose best version depends on stronger project-level assumptions.

## Standards and Guidance

Consult these resources when creating, updating, reviewing, or sharing skills:

- Agent Skills Standard: [agentskills.io/home](https://agentskills.io/home)
- Vercel KB Guidance: [vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context](https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context)
- Skill Creator workflow: [$skill-creator](/Users/galew/.codex/skills/.system/skill-creator/SKILL.md)
- OpenAI Codex Skills: [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills)
- OpenAI Codex Plugins: [developers.openai.com/codex/plugins](https://developers.openai.com/codex/plugins)
- OpenAI Codex Plugin authoring: [developers.openai.com/codex/plugins/build](https://developers.openai.com/codex/plugins/build)
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
- Treat support for the open agent skills standard as the repository foundation, and prefer standard-portable structures first.
- Intend to support future open plugin or bundle standards as they emerge without sacrificing the standard-portable skill core.
- When OpenAI/Codex product behavior or APIs are involved, consult the built-in `openaiDeveloperDocs` MCP server and `$openai-docs` skill before using secondary sources.
- When packaging or distributing repo skills for Codex installation, consult the Codex plugins docs, treat `plugins/productivity-skills/` as the plugin packaging root, and keep the repo-scoped marketplace file aligned with that plugin subtree.
- When packaging or distributing repo skills for Claude marketplace sharing, keep the repo-root `.claude-plugin/marketplace.json` aligned with the tracked plugin roots and keep relative plugin paths inside that marketplace root.
- For Gale's repos, keep the source-of-truth plugin, marketplace, MCP, app, and hook manifests inside `plugins/` and `.agents/plugins/`, not mixed into root `skills/`.
- For agent-skills and agent-plugin repository maintainer workflows, prefer the dedicated sibling repo at `/Users/galew/Workspace/agent-plugin-skills` as the canonical home. Do not reintroduce local copies of those skills into this repository unless Gale explicitly asks for temporary incubation here.
- Preserve OpenAI/Codex-specific enhancements to the fullest where they materially improve packaging, install UX, invocation, routing, or metadata quality.
- Consult Claude docs when behavior is Claude skills/plugins specific.
- Preserve Claude Code and Claude plugin enhancements to the fullest where they materially improve compatibility, routing, or install UX without weakening the standard-portable core.
- Default to full coverage of applicable supported metadata fields across the Agent Skills standard, skill frontmatter, `agents/openai.yaml`, Codex plugin manifests, Claude plugin manifests, MCP surfaces, and app metadata. Leave a field out only when it is truly unsupported, inapplicable, or unverifiable.

## Plugins and Subagents

- Keep the terminology straight across ecosystems and docs:
  - a `skill` is the reusable authoring unit for workflow guidance
  - a `plugin` is a distribution bundle
  - a `subagent` is a delegated runtime worker with its own context and tool policy
- For Codex, treat skills as the primary authoring format and plugins as the installable distribution unit that can bundle skills, apps, and MCP servers.
- For Codex work in this repository, keep root `skills/` as the canonical workflow-authoring surface and treat `plugins/productivity-skills/` as the plugin packaging root.
- Philosophically, this repository is both the home for global-install productivity workflows and the superclass layer for broadly reusable workflow families. Language-, framework-, stack-, or repository-specific bundles should generally live in dedicated plugins intended for project- or repo-level install when stronger assumptions materially improve the workflow.
- Follow canonical Codex and Claude project-level discovery guidance on macOS and Linux through POSIX symlink mirrors instead of duplicate skill trees:
  - `.agents/skills -> ../skills`
  - `.claude/skills -> ../skills`
  - `plugins/productivity-skills/skills -> ../../skills`
- Treat those symlink mirrors as discovery and packaging conveniences, not as independent sources of truth.
- Track canonical plugin source trees and shared marketplace catalogs in git.
- For Claude Code, keep in mind that plugins can package more than skills alone. Claude plugins may bundle commands, hooks, MCP or LSP configuration, skills, and plugin-scoped subagents.
- For Claude Code subagents, treat them as runtime personas with their own prompts, tool access, and context windows. They are not a replacement for shared skills or repo guidance.
- For Codex subagents, treat them as explicit delegation infrastructure for bounded parallel or specialized work. They should not replace repo guidance or plugin packaging docs.
- Do not blur these layers in repo docs:
  - `AGENTS.md` defines durable behavior and project policy
  - skills define reusable workflows
  - plugins package installable distribution surfaces
  - subagents define runtime delegation behavior
- When documenting cross-platform compatibility, say explicitly whether guidance is:
  - shared between Codex and Claude
  - Codex-specific
  - Claude-specific
- This repository's source of truth remains the shipped skill assets under root `skills/`. Plugin manifests, marketplaces, and future subagent definitions are packaging or delegation layers around that canonical skill surface.
- Historical note: `maintain-skills-readme`, `bootstrap-skills-plugin-repo`, and `sync-skills-repo-guidance` were incubated here but now belong in the dedicated agent-plugin maintainer repo and should be treated as moved.

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
- Treat this as repository-maintainer tooling only, not as an installed-skill runtime requirement for end users.

### Constraints on Skills (Config/Customization/Automation)

Skills are installed by an end user for their Agent to make use of. Skill installation is typically handled by the Vercel `skills` CLI, and located in a managed directory that neither Skill, nor Agent, will have write access to. Keep this in mind when considering customizations and configuration.

Some alternatives for user customization/config include using their Agent's memory or personalization features, an end user's global or project-level `AGENTS.md` file, automation workflows such as Codex App Automations or Codex CLI exec workflows, and storing user-set custom configs within `~/.config/gaelic-ghost/<REPO>/<SKILL>/`.

## Repo-local Passive Standards

- Prefer `uv run` for Python command execution in examples and scripts.
- Prefer uv-managed tools for maintainer-only linters and type checkers such as `ruff` and `mypy`.
- Prefer a minimal root Python tool configuration when the repo contains Python-backed skills, so maintainers can run `uv run --group dev pytest ...` without ad hoc dependency flags.
- Keep skill instructions deterministic, concise, and safety-forward.
- Implement all applicable YAML fields in the Frontmatter.
- Never auto-install skills; report required commands and wait for user confirmation.
- Keep skill runtime resources inside the skill directory: `SKILL.md`, `agents/openai.yaml`, `scripts/`, `references/`, and `assets/`.
- Keep active repo-authored skills under the top-level `skills/` directory, and keep install packaging surfaces under `plugins/productivity-skills/`.
- Prefer symlinks over hardlinks for discovery mirrors in these repos. Hardlinks are not a durable repository contract.
- Treat standard-portable skill structure as the canonical core, and treat platform-specific metadata or packaging surfaces as additive overlays instead of replacements.
- Do not make installed skills depend on repo-level docs under `docs/`.
- Repo-maintainer docs live under `docs/maintainers/`.
- Use `docs/maintainers/reality-audit.md` as the maintainer operating guide for source-of-truth order, audit procedure, durable review criteria, and reusable repo-maintenance conventions.
- Use `docs/maintainers/workflow-atlas.md` for repo-maintainer workflow diagrams, branch paths, workflow inputs/outputs, and Agent+Skill UX audits.
- Prefer one clear job per skill.
- Plugins are the bundling and distribution unit; use them to group related skills instead of overloading one skill with unrelated or semi-related workflows.
- Treat standalone skills installation and bundled plugin installation as equally supported distribution paths in repo docs when both paths exist.
- Adjacent workflows may stay grouped only when they are truly one coherent job with one natural invocation surface.
- If a skill depends on mode selection to cover workflows users would naturally ask for separately, prefer splitting those workflows into separate skills and bundling them in the plugin.
- Use the same names for the same concepts across `SKILL.md`, `agents/openai.yaml`, references, automation prompts, scripts, `plugins/productivity-skills/.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, and `plugins/productivity-skills/.claude-plugin/plugin.json`.
- Keep Codex/OpenAI-specific surfaces and Claude-specific surfaces synchronized with the standard skill core instead of letting one platform become the undocumented source of truth.
- If config changes workflow decisions or output contracts, surface that in the main workflow instead of hiding it only in references.
- When docs and scripts disagree on a workflow contract, fix the script or explicitly narrow the documented contract so they match.
- When asked to report roadmap status, reconcile `ROADMAP.md` against completed repo work first or explicitly say the roadmap is stale before summarizing it.
- After completing milestone work, update `ROADMAP.md` in the same change unless the user explicitly says not to.

See `docs/maintainers/reality-audit.md` and `docs/maintainers/workflow-atlas.md` for the durable maintainer reference set.
