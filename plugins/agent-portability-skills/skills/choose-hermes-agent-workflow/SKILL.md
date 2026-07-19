---
name: choose-hermes-agent-workflow
description: Route Hermes Agent work to the correct operator, extension-development, messaging-gateway, Nous services, or Socket compatibility workflow. Use when a request spans surfaces or its extension boundary is unclear.
metadata:
  hermes:
    category: agent-portability
    tags: [hermes, routing, extensions, gateway, nous]
---

# Choose Hermes Agent Workflow

Classify the requested outcome before opening broad documentation or changing configuration.

## Route the Request

| Requested outcome | Use |
| --- | --- |
| Install, update, configure, run, secure, troubleshoot, or use Hermes | `operate-hermes-agent` |
| Create skills, plugins, providers, tools, hooks, desktop/dashboard extensions, or programmatic integrations | `build-hermes-agent-extensions` |
| Run a messaging gateway, API server, webhook intake, messaging platform, or long-lived remote agent | `operate-hermes-agent-gateway` |
| Use Nous Portal, Tool Gateway, Nous Chat, subscription proxy, or Hermes Cloud | `use-nous-research-services` |
| Export Socket skills, translate Socket MCP, or classify Codex-to-Hermes portability | `hermes-agent-compatibility` |

Use more than one workflow when the request genuinely crosses boundaries. Keep one workflow in charge of each write surface.

## Keep the Three Gateway Terms Separate

- `Hermes messaging gateway`: the long-running Hermes process that connects messaging platforms, webhooks, and the API server.
- `Nous Tool Gateway`: Nous-hosted backends for web, media, browser, and optional cloud terminal tools.
- `TUI gateway`: the JSON-RPC protocol used by Hermes TUI and custom host integrations.

Never use an unqualified “gateway” in a decision or implementation note when more than one meaning is possible.

## Select the Smallest Extension Surface

Prefer, in order:

1. A skill for instructions plus existing tools or commands.
2. MCP for an external tool server.
3. Config-driven backends or shell hooks when Hermes already defines that surface.
4. A standalone Python plugin for registered runtime behavior.
5. A specialized provider, platform, memory, context, browser, search, media, secret, desktop, or dashboard extension only when that exact subsystem owns the behavior.
6. A Hermes core contribution only when the behavior belongs in the upstream product rather than a user, project, or third-party extension.

## Source and State Rules

- Refresh the official Hermes docs for claims that can drift; the project moves quickly.
- Inspect the installed Hermes version and active profile before diagnosing local behavior.
- Keep `~/.hermes/` user state, project `.hermes/` state, standalone plugin source, and the upstream Hermes repository distinct.
- Do not mutate Portal accounts, gateway services, messaging accounts, cloud deployments, or user-home configuration unless the user requested that action.
- Do not describe a Codex or Claude plugin manifest as a Hermes plugin.

## Output Contract

Return:

1. `workflow`: the selected skill or combination.
2. `surface`: the concrete Hermes runtime, configuration, hosted service, or source tree involved.
3. `reason`: why that surface owns the request.
4. `state`: local, project, hosted, or upstream state that may change.
5. `verification`: the narrowest proof needed.

Read [references/workflow-map.md](references/workflow-map.md) when the request crosses multiple Hermes subsystems or uses an ambiguous “gateway,” “plugin,” “cloud,” or “provider” label.
