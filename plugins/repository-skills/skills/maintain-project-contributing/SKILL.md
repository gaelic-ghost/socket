---
name: maintain-project-contributing
description: Maintain CONTRIBUTING.md as the contributor-facing member of the canonical four-document repository suite.
---

# Maintain Project Contributing

## Purpose

Keep `CONTRIBUTING.md` focused on human contributor setup, workflow,
verification, review, communication, and contribution terms while all four
canonical repository documents move together.

## Commands

The only documentation commands are:

```text
just docs-check
just docs-apply
```

Both always process README, CONTRIBUTING, AGENTS, and ROADMAP. There are no
per-file recipes and no supported direct script commands.

## Managed Contract

- `assets/document.contract.json` fixes the canonical structure and aliases.
- `assets/CONTRIBUTING.template.md` supplies deterministic bootstrap content.
- Repositories cannot customize headings, order, aliases, or fix policy.
- Healthy existing prose and allowed additional sections remain preserved.

## CONTRIBUTING Ownership

CONTRIBUTING owns who the guide serves, prerequisites, choosing work, making
changes, asking for review, runtime setup, development expectations, pull
request expectations, communication, and contribution terms. Product overview
belongs in README, durable agent policy in AGENTS, and planning in ROADMAP.

Placeholder checks ignore fenced examples, including generic DCO sign-off
examples. They apply only to prose that matches managed scaffold language.

## Deterministic Workflow

Use `just docs-check` for a no-write audit and `just docs-apply` for the atomic
four-document normalization transaction. Apply must be byte-idempotent.

## Guardrails

- Never maintain CONTRIBUTING separately from the full document suite.
- Never invent environment variables, services, commands, branch policy,
  review policy, or legal terms.
- Never expose project-local schema customization.
- Never commit, push, or open a pull request as part of documentation upkeep.

## References

- `assets/document.contract.json`
- `assets/CONTRIBUTING.template.md`
