# Xcode Workflow Compatibility Customization Contract

## Purpose

Record that `xcode-app-project-workflow` is now a compatibility-routing surface and no longer owns ordinary user-facing execution knobs.

## Knobs

| Setting | Default | Status | Meaning |
| --- | --- | --- | --- |
| _none_ | _n/a_ | `policy-only` | The compatibility router keeps a fixed routing policy and directs real runtime tuning to `xcode-build-run-workflow` and `xcode-testing-workflow`. |

## Runtime Behavior

- `scripts/customization_config.py` reads, writes, resets, and reports customization state.
- `scripts/run_workflow.py` keeps a fixed compatibility-routing policy and still preserves the direct `.pbxproj` warning boundary.
- `scripts/detect_xcode_managed_scope.sh` remains a helper script used by `scripts/run_workflow.py`.
- MCP tool execution remains agent-side and is not performed by the local runtime script.

## Update Flow

1. Inspect current settings with `scripts/customization_config.py effective`.
2. Update `SKILL.md` and the affected workflow references if the compatibility-routing behavior changes.
3. Keep `references/customization.template.yaml` empty unless the compatibility surface gains a real user-facing behavior knob again.
4. Re-run `scripts/customization_config.py effective` and confirm the stored values match the docs.
5. Verify `scripts/run_workflow.py --operation-type build --dry-run` still routes to `xcode-build-run-workflow`.

## Validation

1. Verify the docs describe this skill as a compatibility-routing surface rather than the primary Xcode execution owner.
2. Verify the direct `.pbxproj` warning path is still stated consistently across the skill and references.
3. Verify `scripts/run_workflow.py` reflects the fixed compatibility-routing behavior described above.
