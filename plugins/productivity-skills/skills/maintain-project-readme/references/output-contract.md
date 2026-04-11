# Output Contract

## Markdown Sections

1. Run Context
2. Customization State
3. Schema Contract
4. Schema Violations
5. Content Quality Issues
6. Fixes Applied
7. Post-Fix Status
8. Errors

## JSON Top-Level Keys

- `run_context`
- `customization_state`
- `schema_contract`
- `schema_violations`
- `content_quality_issues`
- `fixes_applied`
- `post_fix_status`
- `errors`

## Exit Policy

- Print exactly `No findings.` when there are no issues and no errors.
- Exit `0` for successful runs unless `--fail-on-issues` is set and unresolved issues remain.
- Exit `1` for fatal runtime errors or incompatible repo-type routing failures.
