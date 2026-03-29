# Section Schema

## Common Required Structure

1. `# <project-name>`
2. one-line value proposition
3. `## Table of Contents` when the README has enough H2 sections to justify it
4. `## Overview`
5. `### Motivation` directly under `## Overview`
6. `## Setup`
7. `## Usage`
8. `## Development`
9. `## Verification`
10. `## License`

## Core Rules

- `### Motivation` belongs under `## Overview`, not as a peer H2.
- `Setup`, `Usage`, `Development`, and `Verification` should all exist even when brief.
- `License` may be short, but it should still name or link the actual license.
- When a README has five or more H2 sections, prefer a compact H2-only table of contents near the top.

## Profile-Specific Additions

- `library-package`
  - canonical additional section: `## API Notes`
- `cli-tool`
  - canonical additional section: `## Command Reference`
- `app-service`
  - canonical additional section: `## Configuration`
- `monorepo-workspace`
  - canonical additional section: `## Repository Layout`

## Profile Normalization Rules

- When repo-profile detection is clear, `apply` mode should add the canonical profile-specific section if it is missing.
- When the profile-specific section already exists, keep its content and normalize its placement into the canonical order.
- When repo-profile detection is ambiguous, report that ambiguity and do not create a new profile-specific section automatically.
