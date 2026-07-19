# AGENTS.md

This file is the Agent Portability Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `agent-portability-skills` is the canonical home for maintainer skills that help Socket keep agent skills, Codex plugin surfaces, MCP declarations, hooks, custom agents, and host-specific adapter guidance portable without pretending every host uses the same package model.
- The shipped skills cover skills-export and plugin-export repositories, cross-host protocol selection, ACP agent operation and development, Zed native/external/terminal workflows, Socket-to-Hermes compatibility, Hermes operator and extension-development workflows, Hermes messaging gateways, and Nous Research services. Future skills should extend that foundation into explicit Socket child-plugin portability, Xcode plug-in, OpenCode, Claude Code, and MCP compatibility work.
- Root [`skills/`](./skills/) is the canonical authored and exported surface.
- Treat [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) as plugin packaging metadata only.
- Use the Socket root maintainer docs for shared marketplace, release, and contribution workflow. Keep child maintainer notes only when they describe `agent-portability-skills`-specific behavior.
- Keep repo-level planning and deterministic cross-Socket audits connected to Socket Steward under `.agents/socket-steward/`; this plugin owns reusable agent-facing workflow guidance, while Socket Steward owns repo-local audit, plan, and proposal commands.

## Local Rules

- Before changing Codex plugin, skill, MCP, hooks, marketplace, ACP, or host adapter guidance, check the current official docs for the affected host. Keep this repo's skills focused on Socket policy and agent portability decisions rather than copying full upstream docs.
- Keep Codex plugin structure aligned with current OpenAI docs: only `plugin.json` belongs in `.codex-plugin/`, while `skills/`, `.app.json`, `.mcp.json`, `hooks/`, and `assets/` stay at the plugin root. The manifest points to bundled skills with `"skills": "./skills/"`; it may point to hooks explicitly, but Codex also checks `./hooks/hooks.json` by default. Installing or enabling a plugin does not automatically trust plugin-bundled hooks.
- Keep Codex-specific marketplace, plugin manifest, hook, app, and MCP behavior distinct from host-native surfaces such as Zed skills, Xcode plug-ins, OpenCode skills, Claude Code skills, and future adapter packages.
- Default user-facing install and update guidance to Git-backed marketplace sources. Do not recreate nested staged plugin directories, manual-first local install stories, `skills/install-plugin-to-socket`, or `skills/validate-plugin-install-surfaces`.
- Resolve shared project dependencies only from GitHub repository URLs, package managers, package registries, or other real remote repositories that another contributor can fetch. Machine-local dependency paths are expressly prohibited in any project that is public or intended to be shared publicly.
- When a skill contract changes, update the nearby skill docs, maintainer docs, and tests in the same pass.
- Use the `skills-repo-guidance-sync` custom-agent role only for explicit-trigger subagent workflows: broad read-heavy skills/plugin repo guidance audits, Codex docs freshness checks, discovery mirror drift, marketplace wording checks, and review-packet planning. Keep final edits, validation, commits, pushes, PRs, and releases in the main thread.

## Validation

```bash
uv run pytest
uv run ruff check .
uv run mypy .
```
