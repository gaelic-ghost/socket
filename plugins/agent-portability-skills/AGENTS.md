# AGENTS.md

This file is the Agent Portability Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `agent-portability-skills` owns cross-host protocol selection, agent host
  adapters, ACP and A2A operation, Zed agent integration, Hermes operation and
  extension development, and Nous Research service boundaries.
- Keep Codex plugin repository shape, manifests, marketplace consistency, and
  plugin-maintenance automation in `agent-plugin-skills`. Portability may
  compare a Codex plugin with another host package, but it does not author or
  maintain the Codex package.
- Root [`skills/`](./skills/) is the canonical authored and exported surface.
- Treat [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) as plugin packaging metadata only.
- Use the Socket root maintainer docs for shared marketplace, release, and contribution workflow. Keep child maintainer notes only when they describe `agent-portability-skills`-specific behavior.
- Keep reusable agent-facing portability workflows in this plugin; keep Socket-wide planning, validation, and marketplace consistency in their root-owned documents and scripts.

## Local Rules

- Before changing ACP, A2A, MCP, Zed, Hermes, or host adapter guidance, check
  the current official docs for the affected host.
- Keep transport and host compatibility decisions distinct from package
  authoring. Hand Codex manifest, marketplace, bundled asset, and plugin
  repository work to `agent-plugin-skills:maintain-agent-plugins`.
- Resolve shared project dependencies only from GitHub repository URLs, package managers, package registries, or other real remote repositories that another contributor can fetch. Machine-local dependency paths are expressly prohibited in any project that is public or intended to be shared publicly.
- When a skill contract changes, update nearby skill and maintainer docs in the same pass.

## Validation

Run the essential Socket integration path from the repository root:

```bash
just repo-validate
just test
```
