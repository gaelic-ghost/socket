# AGENTS.md

## Repository Expectations

- For work in this repository, edit skills only under `/Users/galew/Workspace/productivity-skills/skills`.
- Never modify production-installed skills under `~/.agents/skills` while working in this development repository.
- This file defines maintainer guidance for developing skills in this repository. Keep these links and rules at repo root for contributor workflows.

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
- When packaging or distributing repo skills for Codex installation, consult the Codex plugins docs, treat the repository root as the plugin root, and keep the repo-scoped marketplace file aligned with the plugin manifest.
- Preserve OpenAI/Codex-specific enhancements to the fullest where they materially improve packaging, install UX, invocation, routing, or metadata quality.
- Consult Claude docs when behavior is Claude skills/plugins specific.
- Preserve Claude Code and Claude plugin enhancements to the fullest where they materially improve compatibility, routing, or install UX without weakening the standard-portable core.

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
- Prefer a minimal root Python tool configuration when the repo contains Python-backed skills, so maintainers can run `uv run --group dev pytest ...` without ad hoc dependency flags.
- Keep skill instructions deterministic, concise, and safety-forward.
- Implement all applicable YAML fields in the Frontmatter.
- Never auto-install skills; report required commands and wait for user confirmation.
- Keep skill runtime resources inside the skill directory: `SKILL.md`, `agents/openai.yaml`, `scripts/`, `references/`, and `assets/`.
- Keep active repo-authored skills under the top-level `skills/` directory so the repository can also serve as a Codex plugin root.
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
- Use the same names for the same concepts across `SKILL.md`, `agents/openai.yaml`, references, automation prompts, scripts, `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, and future Claude plugin metadata/config.
- Keep Codex/OpenAI-specific surfaces and Claude-specific surfaces synchronized with the standard skill core instead of letting one platform become the undocumented source of truth.
- If config changes workflow decisions or output contracts, surface that in the main workflow instead of hiding it only in references.
- When docs and scripts disagree on a workflow contract, fix the script or explicitly narrow the documented contract so they match.
- When asked to report roadmap status, reconcile `ROADMAP.md` against completed repo work first or explicitly say the roadmap is stale before summarizing it.
- After completing milestone work, update `ROADMAP.md` in the same change unless the user explicitly says not to.

See `docs/maintainers/reality-audit.md` and `docs/maintainers/workflow-atlas.md` for the durable maintainer reference set.
