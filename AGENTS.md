# AGENTS.md

## Repository Expectations

- For work in this repository, edit skills only under `/Users/galew/Workspace/productivity-skills`.
- Never modify production-installed skills under `~/.agents/skills` while working in this development repository.
- This file defines maintainer guidance for developing skills in this repository. Keep these links and rules at repo root for contributor workflows.

## Standards and Guidance

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
- `references/`: For longer documentation, checklists, templates, etc.
- `assets/`: For static templates, output templates, sample configs, diagrams, etc.

## Repo-local Passive Standards

- Prefer `uv run` for Python command execution in examples and scripts.
- Keep skill instructions deterministic, concise, and safety-forward.
- Implement all applicable YAML fields in the Frontmatter.
- Never auto-install skills; report required commands and wait for user confirmation.
- Keep skill runtime resources inside the skill directory: `SKILL.md`, `agents/openai.yaml`, `references/`, `config/`, and `scripts/`.
- Do not make installed skills depend on repo-level docs under `docs/`.
- Repo-maintainer docs live under `docs/maintainers/`.
- Use `docs/maintainers/reality-audit.md` as the maintainer operating guide for source-of-truth order, audit procedure, durable review criteria, and reusable repo-maintenance conventions.
- Use `docs/maintainers/workflow-atlas.md` for repo-maintainer workflow diagrams, branch paths, workflow inputs/outputs, and Agent+Skill UX audits.
- Prefer logically grouped skills over splitting adjacent workflows into separate skills.
- Within a grouped skill, define one primary workflow path and keep variants subordinate to that path.
- Do not create a separate skill for an adjacent workflow unless it has materially different tools, inputs, outputs, and audience.
- Use the same names for the same concepts across `SKILL.md`, `agents/openai.yaml`, references, automation prompts, and scripts.
- If config changes workflow decisions or output contracts, surface that in the main workflow instead of hiding it only in references.
- When docs and scripts disagree on a workflow contract, fix the script or explicitly narrow the documented contract so they match.
- When asked to report roadmap status, reconcile `ROADMAP.md` against completed repo work first or explicitly say the roadmap is stale before summarizing it.
- After completing milestone work, update `ROADMAP.md` in the same change unless the user explicitly says not to.