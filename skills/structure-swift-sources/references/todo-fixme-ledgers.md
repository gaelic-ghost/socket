# TODO and FIXME Ledgers

## Ledger Files

- Use `TODO.md` for TODO entries.
- Use `FIXME.md` for FIXME entries.
- Keep them separate so planned work and broken-state work stay distinct.

## Source Comment Rule

- Keep source comments in the shortened forms:
  - `// TODO: TODO-0001`
  - `// FIXME: FIXME-0001`
- Move the explanatory text into the ledger file entry instead of leaving long prose in source.

## Ticket Format

- TODO entries use IDs such as `TODO-0001`.
- FIXME entries use IDs such as `FIXME-0001`.
- IDs should be stable once assigned.

## Ledger Entry Shape

Each ledger entry should include:

- ticket ID
- current status
- source file path
- source line number at time of extraction
- short title
- full comment text that was removed from source

## Safety Rule

- When normalizing TODO or FIXME comments, update both the source file and the ledger file in the same pass.
- If line numbers change later, refresh the ledger entry rather than creating a duplicate ticket.
