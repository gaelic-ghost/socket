# Xcode Workflow Customization Contract

## Purpose

Tune the documented policy defaults for MCP-first execution, fallback planning, and the remaining `.pbxproj`-edit safeguard.

## Knobs

| Setting | Default | Status | Meaning |
| --- | --- | --- | --- |
| `mcpRetryCount` | `1` | `runtime-enforced` | Controls how many retry attempts are allowed after transient MCP failures before switching to the CLI fallback path. |
| `fallbackCommandMappingProfile` | `official-default` | `runtime-enforced` | Controls which documented fallback-command profile `scripts/run_workflow.py` uses when MCP cannot complete. Supported values are `official-default` and `xcode-only`. |

## Runtime Behavior

- `scripts/customization_config.py` reads, writes, resets, and reports customization state.
- `scripts/run_workflow.py` loads the runtime-enforced knobs above and still keeps `.pbxproj` warning behavior outside ordinary customization.
- `scripts/detect_xcode_managed_scope.sh` remains a helper script used by `scripts/run_workflow.py`.
- MCP tool execution remains agent-side and is not performed by the local runtime script.

## Update Flow

1. Inspect current settings with `scripts/customization_config.py effective`.
2. Update `SKILL.md` and the affected workflow references to reflect the approved policy change.
3. Keep `references/customization.template.yaml` aligned with the runtime-enforced knobs above.
4. Re-run `scripts/customization_config.py effective` and confirm the stored values match the docs.
5. Verify `scripts/run_workflow.py --operation-type build --dry-run` still emits the configured fallback behavior.

## Validation

1. Verify the docs still describe a single MCP-first execution workflow.
2. Verify the `.pbxproj` warning path and fallback posture are still stated consistently across the skill and references.
3. Verify `scripts/run_workflow.py` reflects the runtime-enforced knobs described above.
