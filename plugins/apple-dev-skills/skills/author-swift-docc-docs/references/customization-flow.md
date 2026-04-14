# DocC Workflow Customization Contract

## Purpose

Tune the documented tutorial-handling posture for the DocC authoring-and-review workflow without broadening the first-release skill into a full tutorial-authoring specialist.

## Knobs

| Knob | Default | Status | Effect |
| --- | --- | --- | --- |
| `tutorialSupportLevel` | `light-review` | `runtime-enforced` | Controls whether tutorial-shaped requests get a first-pass conceptual review or an immediate defer-to-references recommendation. |

## Runtime Behavior

- `scripts/customization_config.py` reads, writes, resets, and reports customization state.
- `scripts/run_workflow.py` loads the effective merged customization state at runtime.
- `tutorialSupportLevel=light-review` keeps tutorial requests inside the workflow long enough for a high-level conceptual review before deeper directive-specific work is handed off to fuller DocC references.
- `tutorialSupportLevel=defer` recognizes tutorial-shaped requests and recommends the fuller DocC references immediately.
- The setting does not change build-run handoff rules, repo-shape detection, or the phase-one authoring-and-review boundary.

## Update Flow

1. Inspect current settings with `scripts/customization_config.py effective`.
2. Update `SKILL.md` and the affected references so they still describe the same tutorial-aware but tutorial-light boundary.
3. Persist the metadata change with `scripts/customization_config.py apply --input <yaml-file>`.
4. Re-run `scripts/customization_config.py effective` and confirm the stored values match the docs.
5. Verify `scripts/run_workflow.py --request "review this DocC tutorial draft" --repo-root . --dry-run` reflects the configured tutorial handling.

## Validation

1. Verify tutorial-shaped requests still stay within the first-release scope described in `SKILL.md`.
2. Verify build, export, and generation requests still hand off to the existing execution workflows instead of becoming local runtime behavior.
3. Verify `scripts/run_workflow.py` reflects the runtime-enforced knob above.
