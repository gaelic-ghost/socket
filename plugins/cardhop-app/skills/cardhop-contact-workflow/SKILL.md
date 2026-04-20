---
name: cardhop-contact-workflow
description: Add or update Cardhop.app contacts through the bundled Cardhop.app Socket MCP server. Use when a user wants to create a contact, adjust an existing contact, or validate Cardhop automation readiness on macOS.
---

# Cardhop Contact Workflow

Use the bundled Cardhop.app Socket MCP server to turn natural-language contact instructions into Cardhop actions.

## Inputs

- User intent:
  - add a new contact
  - update an existing contact
  - validate local Cardhop readiness
- Natural-language Cardhop sentence or update instruction
- Optional transport preference:
  - `auto`
  - `applescript`
  - `url_scheme`
- Optional `dry_run` request before dispatching

## Workflow

1. Check local readiness before a likely mutation path.
   - Run `healthcheck`.
2. Decide which server tool fits the request.
   - `add` for a new contact
   - `update` for an existing contact change
   - `parse` when the user gives a generic Cardhop sentence
3. Prefer `transport=auto` unless the user explicitly wants AppleScript or URL scheme routing.
4. Use `dry_run=true` when the user wants a preview or when the instruction still looks ambiguous.
5. Execute the chosen tool with the user’s natural-language instruction.
6. Report the result clearly.
   - include whether it dispatched
   - include the transport used
   - include the command preview when that helps explain what happened

## Output Contract

- Return the action taken:
  - `add`
  - `update`
  - `parse`
  - `healthcheck`
- Include the dispatch status and transport used.
- If Cardhop is unavailable or Automation permission blocks AppleScript, say that plainly and include the server’s error message.

## Guardrails

- Never invent undocumented Cardhop routes or identifiers.
- Never claim a contact mutation succeeded without tool confirmation.
- When the instruction is ambiguous, prefer `dry_run=true` or ask a narrow follow-up rather than guessing.
- Treat the bundled MCP server as the execution surface and the skill as guidance, not the other way around.

## References

- [`../../mcp/README.md`](../../mcp/README.md)
- [`../../README.md`](../../README.md)
