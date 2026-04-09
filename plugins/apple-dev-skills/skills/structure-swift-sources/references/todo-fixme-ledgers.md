# TODO and FIXME Ledgers

## Ledger Files

- Use `TODO.md` for TODO entries.
- Use `FIXME.md` for FIXME entries.
- Keep them separate so planned work and broken-state work stay distinct.

## Source Comment Rule

- Keep source comments in the shortened forms:
  - `// TODO: TODO-0001`
  - `// FIXME: FIXME-0001`
  - `#warning TODO: TODO-0001`
  - `#warning FIXME: FIXME-0001`
  - `#warning("TODO: TODO-0001")`
  - `#warning("FIXME: FIXME-0001")`
- Move the explanatory text into the ledger file entry instead of leaving long prose in source.
- Normalize supported comments across Swift and Objective-C sources such as `.swift`, `.h`, `.m`, and `.mm`.

## Ticket Format

- TODO entries use IDs such as `TODO-0001`.
- FIXME entries use IDs such as `FIXME-0001`.
- IDs should be stable once assigned.

## Optional Reference Tokens

- Use explicit roadmap markers in source comments when the ledger entry should link back to `ROADMAP.md`.
  - Supported forms:
    - `[M30]`
    - `[M29-T2]`
    - `[ROADMAP:M30]`
    - `[ROADMAP:M29-T2]`
- Use explicit plan-doc markers in source comments when the ledger entry should link to a saved related planning document.
  - Supported forms:
    - `[PLAN:docs/maintainers/example-plan.md]`
    - `[DOC:docs/maintainers/example-plan.md]`
- Keep those references explicit and repo-relative so the deterministic helper can resolve them without agent guesswork.

## Ledger Entry Shape

Each ledger entry should include:

- ticket ID
- current status
- source file path
- source line number at time of extraction
- source syntax kind
- short title
- full comment text that was removed from source
- optional roadmap links
- optional saved plan-doc links

## Safety Rule

- When normalizing TODO or FIXME comments, update both the source file and the ledger file in the same pass.
- If line numbers change later, refresh the ledger entry rather than creating a duplicate ticket.
- If an explicit roadmap or plan-doc marker cannot be resolved during `--apply`, stop and fix the reference instead of silently dropping it.

## Deterministic Helper

- Use `scripts/normalize_todo_fixme_ledgers.py --apply` when the task is specifically about normalizing supported Swift and Objective-C TODO/FIXME comments into the ledger format above.
- Use the script without `--apply` for a report-only preview.
- Use report mode first when you want to audit unresolved roadmap or plan-doc references before mutating source.
