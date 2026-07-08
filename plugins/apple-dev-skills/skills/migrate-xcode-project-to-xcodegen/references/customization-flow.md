# XcodeGen Migration Customization Contract

## Purpose

Keep the standard customization file shape available for installed-skill consistency without introducing broad migration defaults. Migration behavior should come from discovered project state and explicit user intent, not durable user preference.

## Knobs

This skill currently exposes no ordinary user-facing customization knobs.

## Runtime Behavior

- `scripts/customization_config.py` reads, writes, resets, and reports customization state.
- `scripts/run_workflow.py` does not require customization state for the audit path.
- The migration audit is non-mutating by default.
- Project conversion and modernization decisions must be driven by the audit output, tracked project files, and explicit user approval for replacement or deletion.

## Update Flow

1. Inspect current settings with `scripts/customization_config.py effective` only when debugging installed-skill state.
2. Do not add persistent knobs for migration behavior unless the setting is a real user preference and cannot be inferred from the project.
3. If a real knob is added later, update this file, `references/customization.template.yaml`, and the customization consolidation review together.

## Validation

1. Run `scripts/run_workflow.py --repo-root <repo> --dry-run` on an Xcode-managed app repo.
2. Run `scripts/run_workflow.py --repo-root <repo> --dry-run` on an existing XcodeGen repo.
3. Confirm the audit output stays non-mutating and lists the files that should own migrated project state.
