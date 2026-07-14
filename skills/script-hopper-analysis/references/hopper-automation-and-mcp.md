# Hopper Automation And MCP Reference

## Python SDK Calibration

Hopper ships a Python API and extension surface with the installed application. Resolve the API from the active Hopper installation and its bundled help rather than copying an import path from another machine or release. Record the Hopper build, Python runtime, import result, document identity, selected image, and output format before relying on an automation.

Start with a read-only query or structured export. A script that writes comments, names, types, procedures, bookmarks, or patches changes analyst state and needs an explicit pre-edit document checkpoint plus a before/after record.

## MCP Boundary

Hopper's MCP server is a local stdio process, but MCP tool results become part of the connected agent's context. Treat selecting a tool and its arguments as a data-disclosure choice even when the Hopper application is local.

The default integration profile should expose only document discovery, navigation, pseudocode, assembly, cross-reference, and read-only annotation tools. Keep comment, rename, bookmark, and other mutation tools disabled until an analyst explicitly approves a checkpointed edit. Use the MCP client’s per-tool approval mode where available.

Do not publish a Socket `.mcp.json` for Hopper: Socket does not distribute Hopper or a portable launcher. The operator configures the installed `HopperMCPServer` command in their private Codex or Hermes configuration instead.

## Canonical Sources

- [Hopper product site](https://www.hopperapp.com/)
- [Hopper downloads](https://www.hopperapp.com/download.html)

Use the installed Hopper help for the active release's Python, SDK, extension, and MCP APIs.
