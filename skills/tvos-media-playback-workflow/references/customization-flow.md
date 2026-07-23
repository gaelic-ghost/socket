# tvOS Media Playback Workflow Customization Contract

## Purpose

Preserve the standard customization-file contract without hiding media-command
or runtime decisions behind unverified persisted settings.

## Knobs

The first version defines no runtime-enforced knobs.

## Runtime Behavior

- `scripts/customization_config.py` supports the standard configuration shape.
- `tvos-media-playback-workflow` ignores persisted settings because player
  choice, commands, stream support, and device behavior require live evidence.
- Add a knob only after its deterministic runtime behavior is documented.

## Update Flow

1. Inspect with `scripts/customization_config.py effective`.
2. Document a real deterministic knob in `SKILL.md` and this file first.
3. Apply a reviewed YAML overlay and rerun `effective`.

## Validation

Do not let customization metadata imply that remote-command behavior has been
validated on hardware.
