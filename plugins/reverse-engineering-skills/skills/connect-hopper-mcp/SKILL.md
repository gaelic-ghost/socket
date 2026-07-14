---
name: connect-hopper-mcp
description: Connect an installed Hopper MCP server safely from Codex or Hermes for document navigation, assembly, pseudocode, strings, procedures, and cross-references with a private profile, read-only allowlist, approvals, and data boundaries.
metadata:
  hermes:
    category: reverse-engineering
    tags: [hopper, mcp, hermes, codex]
---

# Connect Hopper MCP

## Overview

Use Hopper's local stdio MCP server only after Hopper and the target document are ready. This workflow connects a local server to an agent client; it does not make Hopper output private to the client model or provider.

Read [references/hopper-mcp-profile.md](references/hopper-mcp-profile.md) for the data boundary and packaging decision.

## Workflow

1. Preflight the local application.
   - Start Hopper, open the intended copied artifact, and save a document checkpoint.
   - Verify the installed server command starts over stdio and the client can complete MCP initialization.

2. Configure a private client profile.
   - Point Codex or Hermes at the installed `HopperMCPServer` command; do not commit machine-local application paths or user configuration.
   - Keep the configuration outside Socket because Hopper is an operator-installed external application.

3. Enable a read/navigation allowlist first.
   - Allow document discovery, segment and procedure lookup, string and name search, address navigation, assembly, pseudocode, callers, callees, cross-references, and read-only comments or bookmarks.
   - Exclude document selection changes, comment writes, renames, bookmarks, patches, and bulk mutations until a saved checkpoint and explicit edit request exist.

4. Gate every disclosure.
   - Confirm which document, procedure, address range, strings, or pseudocode will enter the agent context before calling a tool.
   - Use per-tool approval when the client supports it. Treat the active model/provider as the data destination.

5. Calibrate the tool surface.
   - Record the exact discovered tools, Hopper version, client, server transport, document identity, and any unavailable tool behavior.
   - Prefer targeted queries over complete-document enumeration.

6. Escalate mutations deliberately.
   - Before enabling a mutation tool, save the document, state the exact proposed change, and preserve a before/after note with addresses and tool arguments.
   - Disable the mutation capability again when the edit is complete unless a maintained edit workflow requires it.

## Guardrails

- Do not add Hopper as a checked-in Socket `.mcp.json`; it is an external local application, not a Socket-distributed server.
- Do not expose an entire proprietary or sensitive document by default.
- Do not assume that a successful MCP connection proves a document is loaded, analyzed, or safe to disclose.
- Use `$use-hopper` for interactive document work and `$script-hopper-analysis` for direct Python SDK work.

## Output

Return the client profile state, Hopper and server identities, document checkpoint, enabled tool classes, approval/data destination decision, targeted calls, returned evidence, and any mutation escalation. For connection-only work, state `preflight only; no document query or mutation performed`.
