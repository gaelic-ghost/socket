# Automation Prompts

Use these prompts when validating or applying the skill through automation.

## Check-only

- Audit `AGENTS.md` for the canonical section order.
- Confirm the required subsection structure exists under the canonical sections.
- Flag placeholder content, weak routing guidance, malformed command blocks, and thin safety boundaries.
- Confirm setup and validation guidance uses grounded command examples with code-fence info strings when commands are present.

## Apply

- Create a missing `AGENTS.md` from the bundled template.
- Normalize `AGENTS.md` to the canonical section order.
- Preserve existing AGENTS guidance where it already matches the schema.
- Add missing sections or subsections from the configured templates only.
- Keep all edits bounded to `AGENTS.md`.
