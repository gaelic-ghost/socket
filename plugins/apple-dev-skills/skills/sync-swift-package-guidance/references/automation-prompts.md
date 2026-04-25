# Swift Package Guidance Sync Automation Prompts

## Dry Run

```text
Run `uv run scripts/run_workflow.py --repo-root <path> --dry-run` and return the planned Swift package guidance-sync actions without writing files.
```

## Apply Sync

```text
Run `uv run scripts/run_workflow.py --repo-root <path>` and sync the bounded Swift package guidance into `AGENTS.md` for the existing SwiftPM repo at that path.
```

## Branch Protection

```text
When the managed repo-maintenance workflow is installed and branch protection is configured, require the GitHub Actions check context `validate`. Do not require `Validate Repo Maintenance / validate`.
```

## Apply Sync Without Validation

```text
Run `uv run scripts/run_workflow.py --repo-root <path> --skip-validation` when the caller explicitly wants the Swift package guidance merged without post-write validation.
```
