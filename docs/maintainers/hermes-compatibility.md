# Hermes Agent Compatibility

Socket's Hermes compatibility is a durable, explicit compatibility baseline.
Every new or materially changed Socket plugin, skill, and MCP declaration must
record and validate its Hermes outcome in the same change. This does not turn
Socket into a second plugin bundle: Codex-only runtime surfaces remain
host-specific unless a concrete native Hermes implementation is designed.

## Compatibility Matrix

| Socket surface | Hermes surface | Status |
| --- | --- | --- |
| Portable `SKILL.md` | GitHub skill tap export or documented no-export decision | Required per changed skill |
| `.codex-plugin/plugin.json` | None | Not compatible by design |
| Socket `.mcp.json` | Checked-in `mcp_servers` translation fragments | Configuration required |
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

The currently exported skills are listed in `skills.sh.json`. Their canonical
sources remain in their owning child plugins; root `skills/` is a checked-in
generated export because the GitHub tap API needs real child directories, not a
symlink mirror. Root [`skills.sh.json`](../../skills.sh.json) supplies Skills
Hub grouping labels. The historical Socket inventory is not yet fully exported;
the roadmap tracks that migration. New or materially changed skills must either
join the generated tap with grouping metadata or document why their workflow is
not portable to Hermes.

## Maintainer Workflow

1. Classify each changed surface before editing: portable skill, translated MCP,
   native Hermes-plugin candidate, or Codex-only by design.
2. For each portable skill, edit the canonical child-plugin source, use a
   lowercase hyphenated directory and matching frontmatter `name`, provide a
   trigger-oriented `description`, and add it to the Hermes export inventory and
   [`skills.sh.json`](../../skills.sh.json). Add `metadata.hermes.category` and
   `metadata.hermes.tags` when discovery benefits.
3. For each changed `.mcp.json`, update its matching checked-in translation and
   `hermes-mcp/index.yaml` entry. A Codex manifest alone never satisfies this
   requirement.
4. For a runtime-only surface, record either its concrete native Hermes plugin
   design or the reason it remains host-specific; do not add a packaging shim.
5. Regenerate and validate:

   ```bash
   uv run scripts/export_hermes_skills.py
   uv run scripts/validate_hermes_compatibility.py
   ```

6. Run the root metadata validator and relevant tests before review.

The focused validator fails for malformed frontmatter, wrong names, missing
descriptions, stale generated content, grouping drift, machine-local metadata
paths, invalid maintained MCP examples, or an unaccounted Socket MCP
declaration. It warns, without blocking, when a description exceeds 240
characters.

## MCP Translation

Socket `.mcp.json` files are Codex declarations, not portable Hermes config.
Every declared Socket MCP configuration, including each new or changed one, is translated under
[`hermes-mcp/`](./hermes-mcp/), with the complete inventory and setup status in
[`hermes-mcp/index.yaml`](./hermes-mcp/index.yaml). Copy the chosen fragment's
`mcp_servers` mapping into the operator's private `~/.hermes/config.yaml` and
complete any listed setup first. The checked-in fragments never require a
machine-local path: local Cardhop and Things servers instead use documented
environment variables that the operator sets before starting Hermes.

Hermes config has this shape:

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

The checked-in [example YAML](./hermes-mcp-examples.yaml) demonstrates optional
filtering fields, while the per-plugin fragments preserve each Socket server's
actual name and transport. Replace placeholders in private configuration,
never in Socket. The translations do not add filtering where no direct
safety/namespace reason exists. Configure required secrets through the explicit
`env` mapping or Hermes process environment, then reload MCP configuration with
`/reload-mcp` and test the enabled server before use.

| Socket declaration | Checked-in Hermes translation | Status |
| --- | --- | --- |
| Apple Dev Skills Xcode bridges | [`apple-dev-skills.yaml`](./hermes-mcp/apple-dev-skills.yaml) | Manual Xcode setup required |
| Cardhop local server | [`cardhop-app.yaml`](./hermes-mcp/cardhop-app.yaml) | Local server-directory setup required |
| Cloud Inference Runpod API and docs servers | [`cloud-inference-skills.yaml`](./hermes-mcp/cloud-inference-skills.yaml) | Ready; API server needs `RUNPOD_API_KEY` |
| Productivity Dice server | [`productivity-skills.yaml`](./hermes-mcp/productivity-skills.yaml) | Ready; basic public search needs no credential |
| Things local server | [`things-app.yaml`](./hermes-mcp/things-app.yaml) | Local server-directory setup required; updates need `THINGS_AUTH_TOKEN` |

## When a Native Hermes Plugin Is Required

Write a dedicated Python Hermes plugin only when a concrete Socket feature needs
runtime registration: a tool handler, lifecycle hook, slash command, CLI
command, or namespaced skill bundle. A real plugin has its own `plugin.yaml`
and `register(ctx)` entry point, and may call `ctx.register_tool`,
`ctx.register_hook`, `ctx.register_command`, or `ctx.register_skill`.

Do not add a generic Socket bridge or boilerplate plugin merely to mirror Codex
packaging. Instruction workflows remain skills; external tool servers remain
MCP. A native plugin is a separate implementation and distribution decision.

The concrete, prioritized future work is in the
[Hermes native Python plugin adapter plan](./hermes-plugin-adapters.md). It
classifies each candidate as a tool, hook, slash command, CLI command, bundled
read-only skill, platform/backend provider, or no adapter, and names the
required configuration and test shape before any implementation begins.

## Verification and Limits

This release validates the repository shape and generated tap without mutating a
user's Hermes home. It does not claim that every Socket child plugin, MCP server,
hook, app, or custom agent runs in Hermes; the required outcome is an explicit,
validated compatibility classification, not a fictional universal runtime.

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
