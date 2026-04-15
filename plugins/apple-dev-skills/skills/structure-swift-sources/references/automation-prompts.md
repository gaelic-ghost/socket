# Structure Swift Sources Automation Contract

## Purpose

Provide one consistent automation contract for sequencing formatting and structural cleanup in Swift repositories.

## Sequencing Rule

1. Run `format-swift-sources` first.
2. Run `structure-swift-sources`.
3. Run `format-swift-sources` again.

This should stay sequential. The formatting passes and the structural pass all mutate the same files.

## Best Automation Shape

- Use a Codex GUI automation or `codex exec` wrapper for the sequence above when the task is large and repeatable.
- Keep file splitting itself agent-driven because concern detection and access-control-safe extraction still require reasoning.
- Keep deterministic follow-up work, such as running the formatting skill before and after, inside automation.
- Use `scripts/normalize_todo_fixme_ledgers.py --apply` as the deterministic helper when the structure pass includes TODO/FIXME ledger normalization.
- Use `references/file-header-inventory.template.yaml` as the starting point when the structure pass includes deterministic file-header application through `scripts/normalize_swift_file_headers.py --apply --inventory ...`.

## Codex CLI Prompt Template

```text
Use $format-swift-sources first.

Then use $structure-swift-sources for:
- cleanup_kind=<CLEANUP_KIND>
- repository_kind=<REPOSITORY_KIND>
- target_scope=<TARGET_SCOPE>
- split_mode=<SPLIT_MODE>
- todo_fixme_mode=<TODO_FIXME_MODE>
- file_header_mode=<FILE_HEADER_MODE>
- file_header_style=<FILE_HEADER_STYLE>

Execution requirements:
1) Establish or confirm the formatting baseline first.
2) Run `scripts/run_workflow.py` first so the cleanup kind, header policy, split thresholds, and handoff surface resolve into one contract.
3) Apply the structure rules from the skill references.
4) If the request becomes symbol-doc or DocC-content work, stop and hand off to $author-swift-docc-docs.
5) If splitting or moving files touches Xcode-managed membership, stop and hand off to $xcode-build-run-workflow.
6) Finish by returning to $format-swift-sources.
```
