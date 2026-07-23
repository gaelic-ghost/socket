# tvOS App Experience Workflow Customization Contract

## Purpose

Preserve the repository customization-file contract without inventing persistent
behavior for a documentation-first tvOS decision workflow.

## Knobs

The first version defines no runtime-enforced knobs.

## Runtime Behavior

- `scripts/customization_config.py` can inspect, apply, and reset the standard
  customization file shape.
- `tvos-app-experience-workflow` ignores persisted settings because focus,
  device capability, beta-SDK, and migration decisions require current evidence.
- Add a knob only after its deterministic behavior and documentation are clear.

## Update Flow

1. Inspect with `scripts/customization_config.py effective`.
2. Document a real deterministic knob in `SKILL.md` and this file first.
3. Apply a reviewed YAML overlay and rerun `effective`.

## Validation

Do not claim a runtime-tunable behavior that the workflow does not implement.
