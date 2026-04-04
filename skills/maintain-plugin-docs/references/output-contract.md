# Output Contract

## Markdown Sections

1. Run Context
2. Discovery Summary
3. Profile Assignments
4. README Findings
5. ROADMAP Findings
6. Cross-Doc Findings
7. Fixes Applied
8. Post-Fix Status
9. Errors

## JSON Top-Level Keys

- `run_context`
- `repos_scanned`
- `repos_with_issues`
- `profile_assignments`
- `readme_findings`
- `roadmap_findings`
- `cross_doc_findings`
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
