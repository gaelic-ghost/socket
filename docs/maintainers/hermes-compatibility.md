# Hermes Agent Compatibility

Socket's Hermes compatibility is a durable, narrow export layer: a curated
GitHub skill tap for portable maintainer workflows. It is not a second Socket
plugin bundle and does not make Codex-only runtime surfaces portable.

## Compatibility Matrix

| Socket surface | Hermes surface | Status |
| --- | --- | --- |
| Root `skills/` export | GitHub skill tap | Supported |
| Other Socket skills | Future curated export or local source | Not automatically exported |
| `.codex-plugin/plugin.json` | None | Not compatible by design |
| Socket `.mcp.json` | `mcp_servers` in Hermes config | Manual adapter path |
| Hooks, apps, and custom agents | Host-specific extension decision | Not automatically compatible |
| Runtime tools, hooks, commands, or namespaced skills | Python Hermes plugin | Separate implementation |

Socket Codex plugins are installable distribution bundles; Hermes plugins are
Python runtime extensions. Their shared portable unit is the `SKILL.md`
workflow, not either host's plugin manifest.

## Hermes Skill Tap

Hermes discovers the root `skills/` directory by default after a user adds the
Socket tap. The curated set is:

- `bootstrap-skills-plugin-repo`
- `hermes-agent-compatibility`
- `sync-skills-repo-guidance`

```bash
hermes skills tap add gaelic-ghost/socket
hermes skills search portability
hermes skills install gaelic-ghost/socket/hermes-agent-compatibility
```

Custom GitHub taps are community sources and Hermes security-scans skills at
install time. Review a finding before using `--force`; Hermes does not let that
flag override a dangerous verdict.

The source of truth is `plugins/agent-portability-skills/skills/`. Root
`skills/` is a checked-in generated export because the GitHub tap API needs real
child directories; a symlink mirror would not provide that portable discovery
surface. Root [`skills.sh.json`](../../skills.sh.json) supplies Skills Hub
grouping labels.

## Maintainer Workflow

1. Edit the canonical skill under `plugins/agent-portability-skills/skills/`.
2. Use a lowercase hyphenated directory and matching frontmatter `name`.
3. Provide a trigger-oriented `description`; add `metadata.hermes.category` and
   `metadata.hermes.tags` only when discovery benefits.
4. Add the exact name to [`skills.sh.json`](../../skills.sh.json).
5. Regenerate and validate:

   ```bash
   uv run scripts/export_hermes_skills.py
   uv run scripts/validate_hermes_compatibility.py
   ```

6. Run the root metadata validator and relevant tests before review.

The focused validator fails for malformed frontmatter, wrong names, missing
descriptions, stale generated content, grouping drift, machine-local metadata
paths, or invalid maintained MCP examples. It warns, without blocking, when a
description exceeds 240 characters.

## MCP Translation

Socket `.mcp.json` files are Codex declarations, not portable Hermes config.
Translate the chosen server into the operator's private `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  socket_example_stdio:
    command: "uv"
    args: ["run", "python", "app/server.py"]
    env:
      EXAMPLE_API_KEY: "set-this-in-your-private-config"
    tools:
      include: [read_status]
      prompts: false
      resources: false
  socket_example_http:
    url: "https://example.invalid/mcp"
    tools:
      include: [read_docs]
      prompts: false
      resources: true
```

The checked-in [example YAML](./hermes-mcp-examples.yaml) is syntax-validated.
Replace placeholders in private configuration, never in Socket. Use a narrow
tool allowlist for mutation-capable servers, configure required secrets through
the explicit `env` mapping, and run `hermes mcp test <name>` before use.

| Socket declaration | Hermes translation decision |
| --- | --- |
| Apple Dev Skills Xcode bridges | Add a stdio `command: "xcrun"` entry with matching bridge arguments only on a Mac with the required Xcode capability. |
| Cardhop and Things local servers | Use the package's actual server directory and `uv run python app/server.py`; do not infer a path from the Codex declaration. |
| Cloud Inference Runpod server | Translate the stdio command or remote docs URL separately; provide `RUNPOD_API_KEY` only when required. |
| Productivity Dice server | Use an HTTP `url` entry; do not assume an API secret for public search. |

## When a Native Hermes Plugin Is Required

Write a dedicated Python Hermes plugin only when a concrete Socket feature needs
runtime registration: a tool handler, lifecycle hook, slash command, CLI
command, or namespaced skill bundle. A real plugin has its own `plugin.yaml`
and `register(ctx)` entry point, and may call `ctx.register_tool`,
`ctx.register_hook`, `ctx.register_command`, or `ctx.register_skill`.

Do not add a generic Socket bridge or boilerplate plugin merely to mirror Codex
packaging. Instruction workflows remain skills; external tool servers remain
MCP. A native plugin is a separate implementation and distribution decision.

## Verification and Limits

This release validates the repository shape and generated tap without mutating a
user's Hermes home. It does not claim that every Socket child plugin, MCP server,
hook, app, or custom agent runs in Hermes.

- `Hermes skill tap supported`: the skill is in root `skills/` and passes the
  Hermes validator.
- `Hermes MCP configuration required`: a translation is documented, but the
  operator configures and tests it in Hermes.
- `Native Hermes plugin required`: runtime Python registration is needed.
- `Not compatible by design`: it is a Codex-only or other host-specific surface.

## Authoritative References

- [Hermes Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
  covers GitHub taps, root `skills/`, `skills.sh.json`, and frontmatter.
- [Hermes Creating Skills](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills)
  covers the skill-versus-tool decision and custom tap publishing.
- [Hermes MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)
  covers stdio and HTTP server configuration.
- [Hermes MCP Config Reference](https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference)
  defines `mcp_servers` transport, environment, filtering, and timeout fields.
- [Hermes Plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins)
  defines `plugin.yaml`, `register(ctx)`, and Python runtime extensions.
- [Agent Skills](https://agentskills.io/) is the shared progressive-disclosure
  skill format that keeps Socket's exported `SKILL.md` workflows portable.
