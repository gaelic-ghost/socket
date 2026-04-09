# AGENTS.md

## Repository Expectations

- For work in this repository, edit skills only under `/Users/galew/Workspace/agent-plugin-skills/skills`.
- Never modify production-installed skills under `~/.agents/skills` while working in this development repository.
- This repository is for maintainer skills that are exported for global installation.

## Standards And Guidance

Consult these resources when creating, updating, reviewing, or sharing skills in this repository:

- Agent Skills Standard: [agentskills.io/home](https://agentskills.io/home)
- Vercel KB Guidance: [vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context](https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context)
- Skill Creator workflow: [$skill-creator](/Users/galew/.codex/skills/.system/skill-creator/SKILL.md)
- OpenAI Codex Skills: [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills)
- OpenAI Codex plugin build docs: [developers.openai.com/codex/plugins/build](https://developers.openai.com/codex/plugins/build)
- Claude Code Skills: [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)
- Claude Code Plugins: [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins)
- Anthropic Agent Skills Best Practices: [platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

Applicability guidance:

- Treat the open Agent Skills standard as the repository foundation.
- Preserve OpenAI/Codex-specific and Claude-specific guidance where it materially affects workflow honesty.
- When OpenAI/Codex behavior is involved, consult official OpenAI docs before secondary sources.
- When Claude behavior is involved, consult Claude and Anthropic official docs before secondary sources.

## Repo Model

- Root `skills/` is the canonical authored and exported surface for this repository.
- `.agents/skills` and `.claude/skills` are repo-local discovery mirrors into root `skills/`.
- Claude Code's documented plugin workflow is separate from the local `.claude/skills` authoring mirror used in this repo. Keep `.claude-plugin/` packaging out of this repository unless Gale explicitly asks for that change.
- This repository intentionally does not track a nested Codex plugin copy of itself.
- This repository intentionally does not track a repo-local Codex marketplace file for itself.
- Do not recreate nested plugin directories, repo marketplaces, or installer workflows in this repository unless Gale explicitly asks for that architectural reversal.
- Do not recreate `skills/install-plugin-to-socket` or `skills/validate-plugin-install-surfaces`.

## Codex Limitation Policy

- Treat OpenAI's documented Codex plugin system as severely limited for scoping.
- The documented Codex model exposes one repo marketplace at `$REPO_ROOT/.agents/plugins/marketplace.json` and one personal marketplace at `~/.agents/plugins/marketplace.json`.
- Do not imply that Codex supports hidden repo-local plugin installs, private scoped plugin packs, or a second repo marketplace file for repo scope.
- When a skill in this repo discusses Codex plugin export boundaries, it must warn plainly that repo-visible plugins are exposed through the repo marketplace described by OpenAI's docs.
- Keep responsibility clear in docs and skill wording: this limitation comes from OpenAI's documented Codex plugin model and shipped product behavior, not from this repository.
- Do not bury this warning in optional notes. Put it in the main workflow whenever Codex plugin scoping claims are discussed.

## Repo-local Passive Standards

- Prefer `uv run` for Python command execution in examples and scripts.
- Prefer a minimal root Python tool configuration so maintainers can run `uv run --group dev pytest` without ad hoc dependency flags.
- Keep `ruff` and `mypy` available as uv-managed tools in maintainer workflows, and document that baseline with `uv tool install ruff` and `uv tool install mypy` where repo-level Python tooling guidance is described.
- Keep skill instructions deterministic, concise, and safety-forward.
- Implement all applicable YAML fields in the frontmatter.
- Keep skill runtime resources inside the skill directory: `SKILL.md`, `agents/openai.yaml`, `scripts/`, `references/`, and `assets/`.
- Do not make installed skills depend on repo-level docs under `docs/`.
- Repo-maintainer docs live under `docs/maintainers/`.
- Use the same names for the same concepts across `SKILL.md`, `agents/openai.yaml`, references, automation prompts, and scripts.
- When docs and scripts disagree on a workflow contract, fix the script or narrow the documented claim so they match.
- After completing milestone work, update `ROADMAP.md` in the same change unless explicitly told not to.

See `docs/maintainers/reality-audit.md` and `docs/maintainers/workflow-atlas.md` for the durable maintainer reference set.
