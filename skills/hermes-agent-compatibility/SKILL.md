---
name: hermes-agent-compatibility
description: Maintain a clear Socket-to-Hermes compatibility boundary across skills, Codex plugins, MCP configuration, and native Hermes plugins. Use when exporting Socket skills to Hermes or deciding whether an adapter is needed.
version: 1.0.0
metadata:
  hermes:
    category: agent-portability
    tags: [hermes, agent-skills, codex, mcp, portability]
---

# Hermes Agent Compatibility

Maintain Socket's deliberate compatibility boundary with Hermes Agent. Start by
classifying the requested Socket surface, then choose the narrowest Hermes
surface that preserves its real behavior.

## Surface Map

| Socket surface | Hermes equivalent | Compatibility outcome |
| --- | --- | --- |
| `SKILL.md` workflow | GitHub skill tap or direct GitHub skill install | Export when the workflow is portable instructions plus existing tools. |
| Codex plugin bundle | None | Do not present `.codex-plugin/plugin.json` as a Hermes plugin. Keep it as Codex packaging only. |
| `.mcp.json` server declaration | `mcp_servers` entry in `~/.hermes/config.yaml` | Translate the transport and required environment, then validate the server in Hermes. |
| Hook, app, or custom-agent surface | Host-specific decision | Document the limit or build a real Hermes extension only if a concrete behavior needs it. |
| Runtime integration with tools, hooks, commands, or bundled skills | Python Hermes plugin | Use `plugin.yaml` plus `register(ctx)` only when instruction-only or MCP configuration cannot express the behavior. |

## Maintain the Skill Tap

Socket's Hermes tap is the checked-in root `skills/` export. Its authored
source remains `plugins/agent-portability-skills/skills/`; do not edit the
export manually.

1. Add or revise the authored skill under `plugins/agent-portability-skills/skills/`.
2. Use a lowercase hyphenated `name` that matches the skill directory and a
   concise, trigger-oriented `description`.
3. Add `metadata.hermes.category` and `metadata.hermes.tags` when they improve
   Hermes discovery without changing the skill's meaning.
4. Add the skill name to the relevant root `skills.sh.json` grouping.
5. Run `uv run scripts/export_hermes_skills.py` and
   `uv run scripts/validate_hermes_compatibility.py`.
6. Review the generated root `skills/` diff with the authored source. The
   validator requires an exact mirror so a GitHub tap installs the reviewed
   content.

Hermes users add the Socket tap with `hermes skills tap add gaelic-ghost/socket`
and install a skill by its root export slug, for example
`hermes skills install gaelic-ghost/socket/hermes-agent-compatibility`.

## Translate MCP Deliberately

Do not copy a Socket `.mcp.json` file into Hermes configuration. Translate each
server into `mcp_servers.<name>` in `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  example_server:
    command: "uv"
    args: ["run", "python", "app/server.py"]
    env:
      EXAMPLE_API_KEY: "set-this-in-your-private-config"
    tools:
      include: [read_status]
      prompts: false
      resources: false
```

Use `url` instead of `command` and `args` for an HTTP MCP server. Keep secrets
out of Socket files and use a narrow `tools.include` list when the server has
mutation-capable tools. Validate with `hermes mcp test <name>` before asking an
agent to depend on the server.

## Decide Whether a Hermes Plugin Is Needed

Use a real Python Hermes plugin only when the integration needs a registered
tool, hook, slash command, CLI command, or namespaced bundled skill that cannot
be represented as a standalone skill or external MCP server. A plugin lives in
Hermes's plugin install surface, declares `plugin.yaml`, and exposes behavior
from `register(ctx)` such as `ctx.register_tool`, `ctx.register_hook`, or
`ctx.register_skill`.

Do not add a generic Socket-to-Hermes bridge, copy Codex manifests into a Hermes
plugin, or create an adapter template without a concrete package that needs
runtime behavior. Those would hide host differences rather than make them
maintainable.

## Report Compatibility Precisely

State each outcome as one of:

- `Hermes skill tap supported`: the exported `SKILL.md` is validated and can be
  installed through the Socket tap.
- `Hermes MCP configuration required`: a Socket server declaration has a
  documented `mcp_servers` translation but no automatic installation.
- `Native Hermes plugin required`: the requested runtime behavior needs a
  separate Python plugin and is not supplied by the Socket Codex bundle.
- `Not compatible by design`: the surface is Codex-specific and has no Hermes
  equivalent.

Link claims that depend on Hermes behavior to its official skills, MCP, or
plugin documentation. Keep the compatibility matrix and examples in Socket's
maintainer documentation rather than duplicating full upstream documentation in
this skill.
