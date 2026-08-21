# Automation Prompts

Use these prompts when validating or applying the skill through automation.

## Check-only

- Audit `API.md` for the canonical section order.
- Confirm the required table of contents is present and matches the canonical top-level headings.
- Confirm sections with required subsections contain the configured `###` headings.
- Flag placeholder content and malformed or weak verification command blocks.

## Apply

- Create a missing `API.md` from the bundled template.
- Normalize `API.md` to the canonical section order.
- Preserve existing API reference guidance where it already matches the schema.
- Add missing sections or subsections from the configured templates only.
- Keep all edits bounded to `API.md`.
