# SwiftUI App Architecture Workflow Customization Contract

## Purpose

Preserve the repo-wide customization-file contract without pretending the first version of `swiftui-app-architecture-workflow` already has runtime-tunable behavior.

## Knobs

The first version defines no documented runtime-enforced knobs.

Keep the skill stable around its docs-first boundary and decision model before introducing persistent settings.

## Runtime Behavior

- `scripts/customization_config.py` exists so the skill participates cleanly in the shared repo customization surface.
- `swiftui-app-architecture-workflow` currently ignores persisted settings at runtime because no runtime-enforced knobs are documented yet.
- Future runtime knobs should only be added after the skill proves a stable need for deterministic configuration.

## Update Flow

1. Inspect current settings with `scripts/customization_config.py effective`.
2. If a real runtime knob is being introduced, update `SKILL.md` and the affected references first.
3. Persist the metadata change with `scripts/customization_config.py apply --input <yaml-file>`.
4. Re-run `scripts/customization_config.py effective` and confirm the stored values match the documented knob set.
5. Verify the skill text and any future runtime logic agree on the same contract.

## Validation

1. Verify the skill does not claim runtime-tunable behavior that is not actually implemented.
2. Verify future knobs are documented in both `SKILL.md` and this file before runtime behavior depends on them.
