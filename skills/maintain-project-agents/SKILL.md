---
name: maintain-project-agents
description: Maintain AGENTS.md as the agent-policy member of the canonical four-document repository suite.
---

# Maintain Project Agents

## Purpose

Keep project-local `AGENTS.md` compact, durable, grounded, and specific while
README, CONTRIBUTING, AGENTS, and ROADMAP are maintained together.

## Commands

The complete documentation command surface is:

```text
just docs-check
just docs-apply
```

Both commands process all four documents. Do not create per-file recipes or
document direct `.fsx` entrypoints.

## Managed Contract

- `assets/document.contract.json` fixes structure, ordering, and aliases.
- `assets/AGENTS.template.md` supplies deterministic bootstrap scaffolding.
- No project-local structural customization is supported.
- Existing grounded policy and allowed additional sections are preserved.

## AGENTS Ownership

AGENTS owns repository scope, source-of-truth routing, change boundaries,
commands, review and delivery rules, safety boundaries, and local overrides.
Product prose belongs in README, contributor workflow in CONTRIBUTING, and
planning in ROADMAP.

## Deterministic Workflow

Use `just docs-check` for the full no-write audit and `just docs-apply` for the
atomic four-document apply. The coordinator validates every proposed document
before it writes any of them and rolls back completed replacements on failure.

## Guardrails

- Never maintain AGENTS separately from the full document suite.
- Never invent commands, toolchains, packaging surfaces, or policy.
- Never add structural customization or alternate document modes.
- Never commit, push, or open a pull request as part of documentation upkeep.

## References

- `assets/document.contract.json`
- `assets/AGENTS.template.md`
