# AGENTS.md

## Repository Expectations

- For work in this repository, edit skills only under `/Users/galew/Workspace/agent-plugin-skills/skills`.
- Never modify production-installed skills under `~/.agents/skills` while working in this development repository.
- This repository is for stack-specific maintainer skills focused on agent-skills and agent-plugin repositories.

## Standards And Guidance

Consult these resources when creating, updating, reviewing, or sharing skills in this repository:

- Agent Skills Standard: [agentskills.io/home](https://agentskills.io/home)
- Vercel KB Guidance: [vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context](https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context)
- Skill Creator workflow: [$skill-creator](/Users/galew/.codex/skills/.system/skill-creator/SKILL.md)
- OpenAI Codex Skills: [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills)
- OpenAI Codex Plugins: [developers.openai.com/codex/plugins](https://developers.openai.com/codex/plugins)
- OpenAI Codex Plugin authoring: [developers.openai.com/codex/plugins/build](https://developers.openai.com/codex/plugins/build)
- Claude Code Skills: [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)
- Claude Code Plugins: [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins)
- Anthropic Agent Skills Best Practices: [platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

Applicability guidance:

- Treat the open Agent Skills standard as the repository foundation.
- Preserve OpenAI/Codex-specific and Claude-specific enhancements where they materially improve packaging, install UX, invocation, routing, or metadata quality.
- Default to full coverage of applicable supported metadata fields across skill frontmatter, `agents/openai.yaml`, Codex plugin manifests, Claude plugin manifests, MCP surfaces, and app metadata.
- When OpenAI/Codex behavior is involved, consult the `openaiDeveloperDocs` MCP server and official OpenAI docs before secondary sources.
- When Claude behavior is involved, consult Claude and Anthropic official docs before secondary sources.

## Repo Model

- Root `skills/` is the canonical authored skill surface. This is the canonical workflow-authoring surface.
- `plugins/agent-plugin-skills/` is the plugin packaging root for this repository.
- Keep `.agents/plugins/marketplace.json` aligned with that plugin packaging root.
- Keep source-of-truth plugin, marketplace, MCP, app, and hook manifests inside `plugins/` and `.agents/plugins/`.
- Follow canonical Codex and Claude project-level discovery guidance on macOS and Linux through POSIX symlink mirrors instead of duplicate skill trees:
  - `.agents/skills -> ../skills`
  - `.claude/skills -> ../skills`
  - `plugins/agent-plugin-skills/skills -> ../../skills`
- Treat those symlink mirrors as discovery and packaging conveniences, not as independent sources of truth.
- Prefer symlinks over hardlinks for discovery mirrors. Hardlinks are not a durable repository contract.

## Repo-local Passive Standards

- Prefer `uv run` for Python command execution in examples and scripts.
- Prefer a minimal root Python tool configuration so maintainers can run `uv run --group dev pytest` without ad hoc dependency flags.
- Keep `ruff` and `mypy` available as uv-managed tools in maintainer workflows, and document that baseline with `uv tool install ruff` and `uv tool install mypy` where repo-level Python tooling guidance is described.
- Keep skill instructions deterministic, concise, and safety-forward.
- Implement all applicable YAML fields in the frontmatter.
- Keep skill runtime resources inside the skill directory: `SKILL.md`, `agents/openai.yaml`, `scripts/`, `references/`, and `assets/`.
- Do not make installed skills depend on repo-level docs under `docs/`.
- Repo-maintainer docs live under `docs/maintainers/`.
- Use the same names for the same concepts across `SKILL.md`, `agents/openai.yaml`, references, automation prompts, scripts, plugin manifests, and marketplace metadata.
- When docs and scripts disagree on a workflow contract, fix the script or narrow the documented claim so they match.
- After completing milestone work, update `ROADMAP.md` in the same change unless explicitly told not to.

See `docs/maintainers/reality-audit.md` and `docs/maintainers/workflow-atlas.md` for the durable maintainer reference set.
