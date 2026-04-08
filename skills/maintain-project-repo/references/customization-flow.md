# Repo Maintenance Toolkit Customization Contract

## Purpose

Record lightweight default preferences for the maintainer toolkit without turning its managed file set into a wide runtime customization surface.

## Knobs

| Knob | Default | Status | Effect |
| --- | --- | --- | --- |
| `defaultReleaseMode` | `standard` | `policy-only` | Sets the default planning posture when the user asks for a release flow without saying whether the repo is standalone or a submodule. |

## Runtime Behavior

- `scripts/customization_config.py` reads, writes, resets, and reports customization state.
- `scripts/install_repo_maintenance_toolkit.py` and `scripts/run_workflow.py` do not currently read these customization knobs.
- The managed file set, GitHub workflow wrapper, and release script surfaces are fixed workflow behavior rather than durable runtime customization.

## Update Flow

1. Inspect current settings with `scripts/customization_config.py effective`.
2. Update `SKILL.md` and the affected references to reflect the approved default-policy change.
3. Persist the metadata change with `scripts/customization_config.py apply --input <yaml-file>`.
4. Re-run `scripts/customization_config.py effective` and confirm the stored values match the docs.
5. Verify the workflow references still describe the same install and release behavior.

## Validation

1. Verify `references/repo-maintenance-layout.md` still matches the managed asset tree.
2. Verify `references/release-modes.md` still matches `assets/repo-maintenance/release.sh`.
3. Verify every customization knob is described consistently across `SKILL.md`, this file, and `references/automation-prompts.md`.
