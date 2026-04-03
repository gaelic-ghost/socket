# Output Contract

## Markdown Sections

1. Run Context
2. Discovery Summary
3. Profile Assignments
4. Schema Violations
5. Command Integrity Issues
6. Fixes Applied
7. Post-Fix Status
8. Errors

## JSON Top-Level Keys

- `run_context`
- `repos_scanned`
- `repos_with_issues`
- `profile_assignments`
- `schema_violations`
- `command_integrity_issues`
- `fixes_applied`
- `post_fix_status`
- `errors`

## Issue Object Keys

- `issue_id`
- `category`
- `severity`
- `repo`
- `doc_file`
- `evidence`
- `recommended_fix`
- `auto_fixable`
- `fixed`

## Exit Code Policy

- Exit `0` when run succeeds and unresolved issues are allowed.
- Exit `1` when fatal runtime error occurs or when `--fail-on-issues` is set and unresolved issues remain.
