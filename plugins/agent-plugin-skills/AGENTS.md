# AGENTS.md

This file is the Agent Plugin Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `agent-plugin-skills` is the canonical home for maintainer skills that target skills-export and plugin-export repositories.
- Root [`skills/`](./skills/) is the canonical authored and exported surface.
- Treat [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) as plugin packaging metadata only.
- Use the Socket root maintainer docs for shared marketplace, release, and contribution workflow. Keep child maintainer notes only when they describe `agent-plugin-skills`-specific behavior.

## Local Rules

- Before changing Codex plugin, skill, MCP, hooks, or marketplace guidance, check the current OpenAI Codex docs. Keep this repo's skills focused on `socket` and skills-export repo policy rather than copying the full upstream docs.
- Keep Codex plugin structure aligned with current OpenAI docs: only `plugin.json` belongs in `.codex-plugin/`, while `skills/`, `.app.json`, `.mcp.json`, `hooks/`, and `assets/` stay at the plugin root. The manifest points to bundled skills with `"skills": "./skills/"`.
- Default user-facing install and update guidance to Git-backed marketplace sources. Do not recreate nested staged plugin directories, manual-first local install stories, `skills/install-plugin-to-socket`, or `skills/validate-plugin-install-surfaces`.
- Resolve shared project dependencies only from GitHub repository URLs, package managers, package registries, or other real remote repositories that another contributor can fetch. Machine-local dependency paths are expressly prohibited in any project that is public or intended to be shared publicly.
- When a skill contract changes, update the nearby skill docs, maintainer docs, and tests in the same pass.

## Validation

```bash
uv run pytest
uv run ruff check .
uv run mypy .
```
