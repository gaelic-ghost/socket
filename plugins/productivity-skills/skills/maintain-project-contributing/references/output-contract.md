# Output Contract

Return Markdown plus JSON with:

- `run_context`
- `profile_assignment`
- `schema_violations`
- `command_integrity_issues`
- `content_quality_issues`
- `fixes_applied`
- `post_fix_status`
- `errors`

Clean-run rule:

- Output exactly `No findings.` only when there are no remaining issues and no errors.
