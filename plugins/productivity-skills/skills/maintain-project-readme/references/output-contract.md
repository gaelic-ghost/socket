# Output Contract

## Markdown Sections

1. Run Context
2. Profile Assignment
3. Schema Violations
4. Command Integrity Issues
5. Content Quality Issues
6. Fixes Applied
7. Post-Fix Status
8. Errors

## JSON Top-Level Keys

- `run_context`
- `profile_assignment`
- `schema_violations`
- `command_integrity_issues`
- `content_quality_issues`
- `fixes_applied`
- `post_fix_status`
- `errors`

## Exit Policy

- Print exactly `No findings.` when there are no issues and no errors.
- Exit `0` for successful runs unless `--fail-on-issues` is set and unresolved issues remain.
- Exit `1` for fatal runtime errors or incompatible repo-type routing failures.
