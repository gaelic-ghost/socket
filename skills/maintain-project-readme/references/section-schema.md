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
  - optional `## API Notes`
- `cli-tool`
  - optional `## Command Reference`
- `app-service`
  - optional `## Configuration`
- `monorepo-workspace`
  - optional `## Repository Layout`
