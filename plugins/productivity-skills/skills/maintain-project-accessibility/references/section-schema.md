# Section Schema

The canonical base `ACCESSIBILITY.md` structure is defined by:

- `../config/accessibility-customization.template.yaml`
- `../assets/ACCESSIBILITY.template.md`

Base top-level shape:

1. top-level title
2. short accessibility-facing summary
3. `## Table of Contents`
4. `## Overview`
5. `## Standards Baseline`
6. `## Accessibility Architecture`
7. `## Engineering Workflow`
8. `## Known Gaps`
9. `## User Support and Reporting`
10. `## Verification and Evidence`

Required subsection shape:

- `Overview`
  - `Status`
  - `Scope`
  - `Accessibility Goals`
- `Standards Baseline`
  - `Target Standard`
  - `Conformance Language Rules`
  - `Supported Platforms and Surfaces`
- `Accessibility Architecture`
  - `Semantic Structure`
  - `Input and Keyboard Model`
  - `Focus Management`
  - `Naming and Announcements`
  - `Color, Contrast, and Motion`
  - `Zoom, Reflow, and Responsive Behavior`
  - `Media, Captions, and Alternatives`
- `Engineering Workflow`
  - `Design and Implementation Rules`
  - `Automated Testing`
  - `Manual Testing`
  - `Assistive Technology Coverage`
  - `Definition of Done`
- `Known Gaps`
  - `Current Exceptions`
  - `Planned Remediation`
  - `Ownership`
- `User Support and Reporting`
  - `Feedback Path`
  - `Triage Expectations`
- `Verification and Evidence`
  - `CI Signals`
  - `Audit Cadence`
  - `Review History`

Schema expectations:

- Use `##` headings for top-level sections.
- Use `###` headings for required subsections.
- Always include a top-level `Table of Contents`.
- Preserve additional repo-specific sections when present, but keep canonical sections in canonical order.
- Keep `Known Gaps` and `Verification and Evidence` present even when the project is still early, because the accessibility contract still needs a truthful status surface.
