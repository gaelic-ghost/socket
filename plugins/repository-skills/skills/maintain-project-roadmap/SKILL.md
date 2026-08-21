---
name: maintain-project-roadmap
description: Maintain ROADMAP.md as the planning member of the canonical four-document repository suite.
---

# Maintain Project Roadmap

## Purpose

Keep checklist-style `ROADMAP.md` milestones, tickets, progress, backlog, and
history structurally consistent while the entire canonical documentation suite
is maintained together.

## Commands

The only documentation commands are:

```text
just docs-check
just docs-apply
```

Both always process README, CONTRIBUTING, AGENTS, and ROADMAP. Ticket mutation,
source collection, and GitHub issue collection are not separate command modes;
the managed full-document pass owns deterministic roadmap normalization.

## Managed Contract

- `assets/document.contract.json` fixes sections, milestone subsections,
  allowed statuses, and a small fixed alias set.
- `assets/ROADMAP.template.md` supplies bootstrap and missing-section content.
- Repositories cannot customize status vocabulary, headings, aliases, order,
  or automatic-fix policy.

## ROADMAP Ownership

ROADMAP owns vision, product principles, milestone progress, milestone scope,
tickets, exit criteria, small tickets, backlog candidates, and notable planning
history. Setup and procedure belong to CONTRIBUTING or maintainer docs; safety
policy belongs to AGENTS.

Milestone Progress and the table of contents are regenerated from the canonical
milestone sections. Missing milestone subsections are added from the managed
template. Known status aliases normalize deterministically; unknown semantic
states remain blocking findings rather than being invented.

## Deterministic Workflow

Use `just docs-check` for the full no-write audit and `just docs-apply` for the
atomic, byte-idempotent four-document normalization transaction.

## Guardrails

- Never maintain or mutate ROADMAP independently of the full document suite.
- Never invent milestone status, scope, ticket details, or completion claims.
- Never add customization or alternate roadmap formats.
- Never commit, push, or open a pull request as part of documentation upkeep.

## References

- `assets/document.contract.json`
- `assets/ROADMAP.template.md`
