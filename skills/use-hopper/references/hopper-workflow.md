# Hopper Workflow Reference

## Capability Record

- Hopper version, edition, and host macOS build.
- Loader and CPU backend used.
- Selected image, architecture, and base address.
- Decompiler, Objective-C, Swift, debugger, Python, extension SDK, AI, and MCP availability.
- Document path, analysis options, and saved checkpoints.

## Apple Handoffs

Use `inspect-apple-artifact` for bundle and Mach-O identity, `recover-apple-runtime-metadata` for supported Swift and Objective-C reconstruction, `correlate-apple-symbols-and-crashes` for UUID and address matching, and `perform-apple-dynamic-analysis` for runtime environment evidence. Hopper owns the tool document and controls, not the underlying Apple platform facts.

## Evidence Practice

Attribute assembly, graphs, pseudocode, names, and inferred types to the specific Hopper document and version. Track original and proposed procedure names separately. Preserve a checkpoint before bulk Python or extension changes.

If an AI or MCP feature is enabled, record the server or model, transport, data selected, prompt or operation, and returned output. Do not assume an integration is local merely because Hopper is a local app.

Use `script-hopper-analysis` for the Python SDK and `connect-hopper-mcp` for local MCP configuration. Those workflows own automation and transport decisions; this skill owns the interactive Hopper document.

## Official Sources

- [Hopper product site](https://www.hopperapp.com/)
- [Hopper downloads](https://www.hopperapp.com/download.html)

Use Hopper's installed help and current product documentation for exact scripting, debugger, SDK, and integration APIs. The product site confirms broad capabilities but is not a version-specific API contract.
