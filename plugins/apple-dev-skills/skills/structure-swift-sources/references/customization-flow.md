# Structure Swift Sources Customization Contract

## Purpose

Tune the runtime-enforced header policy and split-threshold defaults for the structural-cleanup workflow without turning the skill into a repo-specific one-off.

## Knobs

| Knob | Default | Status | Effect |
| --- | --- | --- | --- |
| `fileHeaderMode` | `advisory` | `runtime-enforced` | Controls whether file-header work is recommended or required inside the workflow output. |
| `fileHeaderStyle` | `project-banner` | `runtime-enforced` | Controls the documented header shape. The current runtime supports only the project-and-file banner block-comment form. |
| `fileHeaderCopyrightOwner` | `Gale Williams` | `runtime-enforced` | Controls the copyright owner string rendered in normalized headers. |
| `splitSoftLimit` | `400` | `runtime-enforced` | Controls when the workflow starts strongly recommending a split. |
| `splitHardLimit` | `800` | `runtime-enforced` | Controls when the workflow treats a split as required. |

## Runtime Behavior

- `scripts/customization_config.py` reads, writes, resets, and reports customization state.
- `scripts/run_workflow.py` loads the effective merged customization state at runtime.
- `fileHeaderMode=advisory` keeps file headers as a strong recommendation in the output contract.
- `fileHeaderMode=required` makes missing or malformed file headers part of the required cleanup surface in the output contract.
- `fileHeaderStyle=project-banner` keeps the skill aligned with `references/file-headers.md`.
- `fileHeaderCopyrightOwner` changes the owner string rendered by `scripts/normalize_swift_file_headers.py`.
- `splitSoftLimit` and `splitHardLimit` change the thresholds reported by `scripts/run_workflow.py`, but do not turn file splitting into a deterministic script.

## Update Flow

1. Inspect current settings with `scripts/customization_config.py effective`.
2. Update `SKILL.md` and the affected references so they still describe the same runtime-enforced header policy and split-threshold boundary.
3. Persist the metadata change with `scripts/customization_config.py apply --input <yaml-file>`.
4. Re-run `scripts/customization_config.py effective` and confirm the stored values match the docs.
5. Verify `scripts/run_workflow.py --request "normalize file headers and split this large view file" --repo-path .` reflects the configured header policy and split thresholds.

## Validation

1. Verify file-header policy remains a shape-and-presence rule rather than a promise to auto-author good descriptions from code.
2. Verify DocC-shaped requests still hand off to `author-swift-docc-docs`.
3. Verify Xcode-membership-sensitive requests still hand off to `xcode-build-run-workflow`.
