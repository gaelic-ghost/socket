---
name: maintain-project-readme
description: Maintain README.md as the product-facing member of the canonical four-document repository suite.
---

# Maintain Project README

## Purpose

Keep `README.md` product-focused while the repository's README, CONTRIBUTING,
AGENTS, and ROADMAP documents are checked or applied as one deterministic unit.

## Commands

There are exactly two documentation commands:

```text
just docs-check
just docs-apply
```

Both commands always process all four canonical documents in this order:
README, CONTRIBUTING, AGENTS, ROADMAP. Never expose or recommend a per-file
documentation command or direct `.fsx` invocation.

## Managed Contract

- `assets/document.contract.json` is the fixed structural contract.
- `assets/README.template.md` is the bootstrap and missing-content asset.
- The contract is versioned with the skill and is not project-customizable.
- Existing prose and allowed additional sections are preserved; canonical
  headings, aliases, ordering, and fix policy cannot be overridden.

## README Ownership

README owns product identity, current status, quick start, usage, repository
shape, release-note discovery, and license discovery. Contributor workflow,
agent policy, release procedure, and roadmap tickets belong to their canonical
owners and should be linked rather than duplicated.

Preserve existing user-authored Overview prose. Missing Overview content uses
the exact managed `TBD` scaffold and is reported without inventing claims.

## Deterministic Workflow

1. Run `just docs-check` for a no-write four-document audit.
2. Run `just docs-apply` when structural normalization is requested.
3. The coordinator plans all four outputs before writing any file.
4. Apply uses atomic replacements and rolls back completed writes on failure.
5. A second apply must be byte-identical and produce no change.

## Guardrails

- Never edit or check README in isolation from the full document suite.
- Never invent product claims, commands, guarantees, or support promises.
- Never add project-local schema or fix-policy customization.
- Never commit, push, or open a pull request as part of documentation upkeep.

## References

- `assets/document.contract.json`
- `assets/README.template.md`
