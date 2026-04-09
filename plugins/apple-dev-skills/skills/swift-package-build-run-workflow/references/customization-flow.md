# Swift Package Build Run Workflow Customization Contract

## Purpose

Document the fixed SwiftPM-first policy defaults for package build and run execution plus Xcode handoff behavior.

## Knobs

This skill does not expose ordinary user-facing customization knobs.

## Runtime Behavior

- `scripts/customization_config.py` reads, writes, resets, and reports customization state.
- `scripts/run_workflow.py` still loads customization state, but the current workflow uses fixed SwiftPM-first build/run defaults rather than ordinary user-facing customization knobs.
- SwiftPM command execution remains agent-side and is not performed by the local runtime script.

## Update Flow

1. Inspect current settings with `scripts/customization_config.py effective`.
2. Update `SKILL.md` and the affected workflow references to reflect the approved package build/run policy change.
3. Keep `references/customization.template.yaml` present for install-surface consistency even when `settings` is empty.
4. Re-run `scripts/customization_config.py effective` and confirm the stored values match the docs.
5. Verify `scripts/run_workflow.py --operation-type build --dry-run` still emits the fixed SwiftPM-first build/run workflow defaults.

## Validation

1. Verify the docs still describe a SwiftPM-first build/run workflow.
2. Verify the Xcode handoff boundary is stated consistently across the skill and references.
3. Verify `scripts/run_workflow.py` reflects the fixed workflow defaults described above.
