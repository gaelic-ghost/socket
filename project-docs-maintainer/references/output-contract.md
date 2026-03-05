# Output Contract

## Markdown Sections

1. Run Context
2. Discovery Summary
3. Unaligned Repositories
4. Fixes Applied
5. Remaining Issues
6. Modified Files (no commit)
7. Errors/Warnings

## JSON Top-Level Keys

- `run_context`
- `repos_scanned`
- `unaligned_repos`
- `fixes_applied`
- `post_fix_status`
- `errors`

## Issue Object Keys

- `issue_id`
- `category`
- `severity`
- `language_scope`
- `doc_file`
- `evidence`
- `recommended_fix`
- `auto_fixable`
- `fixed`

## Exit Code Policy

- Exit `0` when run succeeds and unresolved issues are allowed.
- Exit `1` when fatal runtime error occurs or when `--fail-on-issues` is set and unresolved issues remain.
