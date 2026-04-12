# Output Contract

`maintain-plugin-repo` returns one combined maintainer report.

Top-level keys:

- `run_context`
- `repo_root`
- `workflow`
- `owner_assignments`
- `validation_findings`
  - `repo_model`
- `fixes_applied`
- `deferred_findings`
- `post_fix_status`
- `errors`

Exact clean-run text:

- `No findings.`

Use that exact text only when there are no findings, no deferred work, no fixes applied, and no errors.
