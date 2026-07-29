# AGENTS.md

This plugin owns reusable documentation-maintenance workflows. Follow root
Socket guidance for general Git, release, dependency, and documentation rules.

## Scope

- Keep README, CONTRIBUTING, AGENTS, API, accessibility, architecture, roadmap,
  and cross-document maintenance as separate owner skills.
- Do not absorb repository release operations, agent-system design, or generic
  code exploration into this plugin.
- Root `skills/` is the authored source of truth; plugin metadata is packaging.

## Validation

```bash
uv run pytest
```
