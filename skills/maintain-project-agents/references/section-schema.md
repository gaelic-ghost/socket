# Section Schema

The canonical base `AGENTS.md` structure is defined by:

- `../config/agents-customization.template.yaml`
- `../assets/AGENTS.template.md`

Base top-level shape:

1. top-level title
2. short repo-local preamble
3. `## Repository Scope`
4. `## Working Rules`
5. `## Commands`
6. `## Review and Delivery`
7. `## Safety Boundaries`
8. `## Local Overrides`

Required subsection shape:

- `Repository Scope`
  - `What This File Covers`
  - `Where To Look First`
- `Working Rules`
  - `Change Scope`
  - `Source of Truth`
  - `Communication and Escalation`
- `Commands`
  - `Setup`
  - `Validation`
  - `Optional Project Commands`
- `Review and Delivery`
  - `Review Expectations`
  - `Definition of Done`
- `Safety Boundaries`
  - `Never Do`
  - `Ask Before`

Schema expectations:

- Use `##` headings for top-level sections.
- Use `###` headings for required subsections.
- Preserve additional repo-specific sections when present, but keep canonical sections in canonical order.
- Keep the root AGENTS file compact and practical, in line with official Codex guidance.
- Treat `Local Overrides` as the place to explain whether deeper AGENTS files or fallback instruction files refine the root guidance.
