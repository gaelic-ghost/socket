# Output Contract

Return Markdown plus JSON with:

- `run_context`
- `schema_contract`
- `schema_violations`
- `claim_integrity_issues`
- `verification_evidence_issues`
- `content_quality_issues`
- `fixes_applied`
- `post_fix_status`
- `errors`

Clean-run rule:

- Output exactly `No findings.` only when there are no remaining issues and no errors.
