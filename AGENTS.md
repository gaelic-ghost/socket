# AGENTS.md

## Repository Expectations

- For work in this repository, edit skills only under `/Users/galew/Workspace/productivity-skills`.
- Never modify production-installed skills under `~/.agents/skills` while working in this development repository.

## Standards and Guidance

Always consult these resources when creating, updating, reviewing, or sharing skills:

- Skill Creator workflow: [$skill-creator](/Users/galew/.codex/skills/.system/skill-creator/SKILL.md)
- OpenAI Codex Skills: [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills)
- OpenAI Codex AGENTS.md configuration: [developers.openai.com/codex/configuration/agents-md](https://developers.openai.com/codex/configuration/agents-md)
- Claude Code Features Overview: [code.claude.com/docs/en/features-overview](https://code.claude.com/docs/en/features-overview)
- Claude Code Skills: [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)
- Anthropic Agent Skills Best Practices: [platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Claude Code Plugins: [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins)
- The Complete Guide to Building Skill for Claude (PDF): [resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)
- Agent Skills Standard: [agentskills.io/home](https://agentskills.io/home)
- Vercel KB Guidance: [vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context](https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context)

Applicability guidance:

- Always consult Skill Creator workflow for skill lifecycle work.
- Consult OpenAI Codex docs when behavior is OpenAI/Codex specific.
- Consult Claude docs when behavior is Claude skills/plugins specific.
- Consult Agent Skills Standard and Vercel guidance for cross-platform standards alignment.

## Repo-local Passive Standards

- Prefer `uv run` for Python command execution in examples and scripts.
- Keep skill instructions deterministic, concise, and safety-forward.
- Never auto-commit or auto-install; report required commands and wait for user confirmation.
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

See `docs/maintainers/reality-audit.md` and `docs/maintainers/workflow-atlas.md` for the durable maintainer reference set.
