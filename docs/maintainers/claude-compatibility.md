# Claude Code and Cowork Compatibility

Date checked: 2026-07-19 against Claude Code 2.1.211 and the current Claude
Code and Cowork plugin documentation.

Socket publishes a Claude marketplace at
[`/.claude-plugin/marketplace.json`](../../.claude-plugin/marketplace.json).
It is a host adapter for the same canonical skill payloads under `plugins/`; it
does not replace the Codex marketplace or copy the skill corpus.

## Support Boundary

Claude Code is Socket's primary Claude runtime target for the components Socket
actually classifies: skills, MCP servers, selected hooks, and deliberately
designed subagents. Its marketplace entries use `strict: false` so the catalog
supplies Claude metadata while each existing Socket plugin root remains the
installed payload.

This is not a claim that every newer Claude plugin component is automatically
portable. Claude Code also documents LSP servers, monitors, channels, `bin/`,
settings, and output styles. Socket currently ships no Claude-specific
implementation of those surfaces and must classify one explicitly before using
it in a compatibility claim.

Cowork is a skills-first target. It can use the same marketplace and skill
workflows, but a connector runs from Anthropic's cloud rather than Gale's Mac.
Therefore local-process MCP servers are explicitly Code-only and must remain
disabled in Cowork:

| Plugin | Claude Code | Cowork |
| --- | --- | --- |
| `apple-dev-skills` | Xcode local MCP bridge | Skills only |
| `cardhop-app` | Local Cardhop MCP server | Skills only |
| `things-app` | Local Things MCP server | Skills only |
| `cloud-inference-skills` | Runpod remote MCP servers | Remote MCP supported |
| `productivity-skills` | Dice remote MCP server | Remote MCP supported |

All other catalog entries are portable skill workflows in both hosts. The
complete, machine-checked classification is in
[`claude-compatibility.json`](./claude-compatibility.json).

`model-lab-skills` is skills-only in Cowork and fully supported in Claude Code.
Its optional Python helpers read and write operator-selected local artifacts;
the plugin declares no MCP server or host-specific runtime extension.

The macOS platform-security workflows remain instruction-portable in Claude Code and Cowork. Apple Dev Skills owns supported app permission, sandbox file-access, and entitlement diagnosis; Reverse Engineering Skills owns exact-build private-control research; Cybersecurity Skills owns defensive host investigation. Visible permission prompts, System Settings changes, local artifact inspection, VM execution, and protection-state changes still require the corresponding approved local environment and are not supplied by the Claude marketplace adapter.

`agentdeck` is intentionally absent from the Claude marketplace: its title
hook is a Codex runtime integration, not an instruction workflow. `spotify`
is also absent because it remains a Socket placeholder. `speak-swiftly` is
excluded until its standalone source ships a Claude-native payload: Claude Code
auto-loads its current Codex-only hook, which includes a hard-coded Codex cache
path.

The `speak-swiftly` exclusion was rechecked against Socket's pinned `v11.0.0`
source on 2026-07-19. Its hook command still targets the Socket Codex cache
directly, so exposing the payload to Claude would not be a faithful adapter.

## Install and Update

In Claude Code, add the Socket Git marketplace and select individual plugins:

```bash
claude plugin marketplace add gaelic-ghost/socket
claude plugin install apple-dev-skills@socket
claude plugin marketplace update socket
```

In Cowork, open **Customize → Plugins**, add the `gaelic-ghost/socket`
marketplace, then install the desired plugin. Leave any local-process
connector disabled; its skill workflows remain usable.

## MCP Adapters

Claude marketplace installs are copied into a versioned cache. Local MCP
servers must therefore use `${CLAUDE_PLUGIN_ROOT}` rather than Codex's
`${PLUGIN_ROOT}` or a traversal outside the plugin root. Socket provides
`claude.mcp.json` adapters for Cardhop and Things. The adapters preserve each
server name and start it from the packaged `mcp/` directory.

Remote MCP configurations can use their existing standard `.mcp.json` files.
Secrets remain user or organization configuration; never commit credentials or
machine-local paths into the marketplace payload.

## Host-Specific Components

Socket's `agents/openai.yaml` files are Codex custom-agent presentation
metadata, not Claude subagent definitions. Do not mechanically convert them.
Add `agents/*.md` only when a role has an independently useful delegated job,
a Claude-specific system prompt, and a safe tool boundary. Claude plugin agents
must not be used to mimic Codex-only runtime surfaces.

Likewise, port a hook only after a Claude lifecycle event and trust boundary
have been designed and tested. A plugin may not claim a hook merely because a
Codex `hooks/hooks.json` file exists.

Treat Claude LSP servers, background monitors, MCP-backed channels, executable
`bin/` additions, settings, and output styles the same way: add them only when
Socket owns a concrete Claude behavior, then validate that component in Claude
Code and classify whether Cowork can consume it. Do not infer support from a
similarly named Codex or Xcode surface.

## Maintainer Workflow

1. Classify every changed Socket marketplace entry in
   `claude-compatibility.json` as `supported`, `local_mcp`, `remote_mcp`, or
   `not_supported` for Claude Code and as `skills_only`, `remote_mcp`, or
   `not_supported` for Cowork.
2. Add a Claude marketplace entry for every non-excluded Codex marketplace
   plugin. Keep `strict: false` unless a Claude-only package gains an
   intentionally owned manifest.
3. For each local MCP, add or update a `claude.mcp.json` adapter using
   `${CLAUDE_PLUGIN_ROOT}`. For any changed Socket `.mcp.json`, also update the
   Hermes translation and run its validation.
4. Run both compatibility validators, then run Claude marketplace validation
   and a temporary-home install smoke test.

```bash
uv run scripts/validate_socket_metadata.py
uv run scripts/validate_hermes_compatibility.py
uv run scripts/validate_claude_compatibility.py
claude plugin validate .
```

## Authoritative References

- [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
  describes `.claude-plugin/marketplace.json`, `strict`, source paths, and
  validation.
- [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference)
  describes plugin-root skills, MCP configuration, hooks, subagents, LSP
  servers, monitors, channels, executable paths, cache behavior, and
  `${CLAUDE_PLUGIN_ROOT}`.
- [Cowork plugins](https://claude.com/docs/cowork/guide/plugins) describes
  marketplace installation and component controls.
- [Custom remote connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
  explains why Cowork connectors must be reachable from Anthropic's cloud.
