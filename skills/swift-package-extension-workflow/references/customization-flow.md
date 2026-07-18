# Swift Package Extension Workflow Customization Contract

## Purpose

Keep package-first, dual-toolchain, least-permission defaults explicit.

## Knobs

This skill does not expose ordinary user-facing customization knobs.

## Runtime Behavior

- `scripts/customization_config.py` reads, writes, resets, and reports customization state.
- `scripts/run_workflow.py` loads the state but keeps fixed routing and command-planning policy.
- Commands remain agent-executed; the runtime script does not mutate packages or invoke plugins.

## Update Flow

1. Inspect settings with `scripts/customization_config.py effective`.
2. Update the skill and affected references together.
3. Preserve the empty template until a real stable knob exists.
4. Re-run the runtime dry runs and targeted tests.
