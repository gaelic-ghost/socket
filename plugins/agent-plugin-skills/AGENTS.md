# AGENTS.md

This file is the Agent Plugin Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `agent-plugin-skills` is the canonical home for maintainer skills that target skills-export and plugin-export repositories.
- Root [`skills/`](./skills/) is the canonical authored and exported surface.
- Treat [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) as plugin packaging metadata only.
- Use the Socket root maintainer docs for shared marketplace, release, and contribution workflow. Keep child maintainer notes only when they describe `agent-plugin-skills`-specific behavior.

## Local Rules

- Keep Codex plugin guidance aligned with current OpenAI plugin docs: only `plugin.json` belongs in `.codex-plugin/`, while `skills/` stays at the plugin root and the manifest points to it with `"skills": "./skills/"`.
- Do not recreate `skills/install-plugin-to-socket` or `skills/validate-plugin-install-surfaces`; those retired workflows encouraged manual install-surface thinking that this repo now keeps out of the standard Codex path.
- When a skill contract changes, update the nearby skill docs, maintainer docs, and tests in the same pass.

## Validation

```bash
uv run pytest
uv run ruff check .
uv run mypy .
```
