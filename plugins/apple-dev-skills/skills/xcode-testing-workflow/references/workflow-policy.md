# Hybrid Workflow Policy

## Decision order

1. Resolve workspace context.
2. Attempt Xcode MCP path.
3. Retry once when the MCP failure is transient (`timeout` or `transport`).
4. If MCP remains unavailable or is unsupported, use the official CLI fallback immediately.
5. If direct `.pbxproj` mutation is being considered, apply the explicit warning path from `references/mutation-risk-policy.md`.

## MCP-first invariant

Use Xcode MCP tools first for:
- workspace/session inspection
- project discovery and read/search
- diagnostics/build/test actions
- snippet/preview operations
- structured mutation actions supported by MCP

## Automatic fallback invariant

When MCP is unavailable or insufficient:
- do not block waiting for user permission to fallback
- run official command path
