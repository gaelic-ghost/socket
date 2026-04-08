# Output Contract

Return Markdown plus JSON with:

- `run_context`
- `schema_violations`
- `workflow_drift_issues`
- `validation_drift_issues`
- `boundary_and_safety_issues`
- `fixes_applied`
- `post_fix_status`
- `errors`

Clean-run rule:

- Output exactly `No findings.` only when there are no remaining issues and no errors.
