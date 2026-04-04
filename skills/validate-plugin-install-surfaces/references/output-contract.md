# Output Contract

## Markdown Sections

1. Run Context
2. Canonical Skills
3. Plugin Roots
4. Metadata Findings
5. Install Surface Findings
6. Mirror Findings
7. Errors

## JSON Top-Level Keys

- `run_context`
- `canonical_skill_dirs`
- `plugin_roots`
- `metadata_findings`
- `install_surface_findings`
- `mirror_findings`
- `errors`

## Finding Object Keys

- `path`
- `issue_id`
- `message`
- `surface`

## Exit Code Policy

- Exit `0` when the audit runs successfully.
- Exit `1` when fatal runtime error occurs or when `--fail-on-findings` is set and findings remain.
