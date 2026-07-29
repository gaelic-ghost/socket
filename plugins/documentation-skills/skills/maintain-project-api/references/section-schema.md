# Section Schema

The canonical base `API.md` structure is defined by:

- `../config/api-customization.template.yaml`
- `../assets/API.template.md`

Base top-level shape:

1. top-level title
2. short API-consumer-facing summary
3. `## Table of Contents`
4. `## Overview`
5. `## API Surface`
6. `## Authentication and Access`
7. `## Requests and Responses`
8. `## Errors`
9. `## Versioning and Compatibility`
10. `## Local Development and Verification`
11. `## Support and Ownership`

Required subsection shape:

- `Overview`
  - `Who This API Is For`
  - `Stability Status`
- `API Surface`
  - `Entry Points`
  - `Protocols and Transports`
- `Authentication and Access`
  - `Credentials`
  - `Permissions`
- `Requests and Responses`
  - `Request Shape`
  - `Response Shape`
  - `Data Models`
- `Errors`
  - `Error Shape`
  - `Common Failure Modes`
- `Versioning and Compatibility`
  - `Supported Versions`
  - `Breaking Changes`
- `Local Development and Verification`
  - `Runtime Configuration`
  - `Verification`

Schema expectations:

- Use `##` headings for top-level sections.
- Use `###` headings for required subsections.
- Always include a top-level `Table of Contents`.
- Preserve additional repo-specific sections when present, but keep canonical sections in canonical order.
