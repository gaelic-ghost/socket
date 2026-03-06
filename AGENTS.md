# AGENTS.md

## Repository Scope

This file defines maintainer guidance for developing skills in this repository. Keep these links and rules at repo root for contributor workflows.

## Authoritative Resources (Maintainers)

- Always consult the `$skill-creator` workflow first: [/Users/galew/.codex/skills/.system/skill-creator/SKILL.md](/Users/galew/.codex/skills/.system/skill-creator/SKILL.md)
- OpenAI Codex Agent Skills documentation: [https://developers.openai.com/codex/skills/](https://developers.openai.com/codex/skills/)
- OpenAI Codex MCP documentation: [https://developers.openai.com/codex/mcp/](https://developers.openai.com/codex/mcp/)
- When OpenAI product behavior or APIs are involved, consult the built-in `openaiDeveloperDocs` MCP server and `$openai-docs` skill before using secondary sources.
- Claude Code subagents documentation (skills-equivalent): [https://docs.anthropic.com/en/docs/claude-code/sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- Claude Code integrations / plugin documentation: [https://docs.anthropic.com/en/docs/claude-code/ide-integrations](https://docs.anthropic.com/en/docs/claude-code/ide-integrations)
- Claude Code MCP documentation (plugin-style tool integration): [https://docs.anthropic.com/en/docs/claude-code/mcp](https://docs.anthropic.com/en/docs/claude-code/mcp)
- Agent Skills Standard: [https://agentskills.io/home](https://agentskills.io/home)
- Vercel KB guidance: [https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context](https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context)

## Skill Runtime Model

- A skill is an instruction and workflow-guidance layer. It teaches and structures tool use; it does not become the tool runtime.
- Skills may include local scripts for validation, policy enforcement, fallback shaping, and automation support.
- Skills in this repo must not present themselves as direct MCP clients or executors.
- When MCP is involved, the skill should guide agent-side MCP usage rather than present itself as the MCP client.
- Local scripts may enforce policy or produce plans, but they must not overclaim direct MCP execution.
- This rule applies to `SKILL.md`, workflow diagrams, customization contracts, runtime helper scripts, and maintainer-facing documentation.

## Snippet Policy

- Keep reusable end-user snippet source files in `shared/`.
- Keep per-skill internal copies of relevant snippets under `references/snippets/`.
- In each skill `SKILL.md`, reference local snippet copies and recommend adding snippets to end-user repos when the task involves baseline policy setup.
