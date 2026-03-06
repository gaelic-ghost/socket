# Implementation Audit

This document records the current claim-vs-code status for the three active skills after the runtime-truth pass.

## `apple-xcode-workflow`

### Implemented In Code

- `scripts/run_workflow.py` loads merged customization state at runtime.
- `scripts/run_workflow.py` enforces mutation-guard planning for Xcode-managed scope by calling `scripts/detect_xcode_managed_scope.sh`.
- `scripts/run_workflow.py` enforces advisory cooldown state by calling `scripts/advisory_cooldown.py`.
- `scripts/run_workflow.py` resolves docs-route order and structured CLI fallback command planning.

### Implemented By Agent/Tool Layer

- MCP execution itself remains agent-side.
- Tab resolution and actual Xcode MCP tool calls remain agent-side.

### Docs-Only And Reduced

- The skill no longer claims that local code executes MCP directly.
- The skill no longer claims inert customization metadata automatically changes runtime behavior.

## `apple-dash-docsets`

### Implemented In Code

- `scripts/run_workflow.py` is the unified runtime entrypoint for `search`, `install`, and `generate`.
- `scripts/run_workflow.py` loads merged customization state at runtime.
- `search` stage enforces configured fallback order and can probe HTTP availability through `scripts/dash_api_probe.py`.
- `install` stage enforces configured source priority and approval gating.
- `generate` stage returns structured guidance instead of freeform workflow crossing.

### Implemented By Agent/Tool Layer

- Dash MCP usage remains agent-side when `search` selects `mcp`.
- Real Dash UI launch side effects still rely on the local `open` command via helper scripts.

### Docs-Only And Reduced

- none

## `apple-swift-package-bootstrap`

### Implemented In Code

- `scripts/run_workflow.py` is the unified runtime entrypoint.
- `scripts/run_workflow.py` loads merged customization state at runtime.
- Runtime defaults for package type, platform preset, and version profile are enforced by the wrapper.
- Git initialization and `AGENTS.md` copying are now controllable through wrapper-to-shell flags.
- `scripts/bootstrap_swift_package.sh` remains the implementation core for actual scaffold creation.

### Implemented By Agent/Tool Layer

- Cross-skill recommendation to `apple-xcode-workflow` or `apple-dash-docsets` remains agent-side guidance.

### Docs-Only And Reduced

- none
- Manual fallback guidance remains documentation-level behavior unless the shell script is unavailable.

## Summary

- `apple-xcode-workflow`: pass, with MCP execution clearly separated as agent-side.
- `apple-dash-docsets`: pass, with one real runtime entrypoint and runtime-enforced search, install, and generation customization.
- `apple-swift-package-bootstrap`: pass, with one real runtime entrypoint and no remaining inert customization knobs.

No active skill should now present inert stored customization state as runtime-enforced behavior.
