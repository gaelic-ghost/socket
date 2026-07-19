---
name: build-hermes-agent-extensions
description: Build Hermes Agent skills, Python plugins, specialized providers, messaging adapters, memory and context engines, secret sources, desktop or dashboard extensions, MCP integrations, hooks, and programmatic hosts.
metadata:
  hermes:
    category: agent-portability
    tags: [hermes, plugins, providers, developer-guide, integrations]
---

# Build Hermes Agent Extensions

Choose the owned extension surface before creating files. Hermes uses several unrelated plugin and integration systems; do not force them into one generic package.

## Select the Surface

1. Use a skill for instructions, existing commands, and progressive disclosure.
2. Use MCP for an external tool server.
3. Use a general Python plugin for registered tools, lifecycle hooks, slash commands, CLI commands, or bundled namespaced skills.
4. Use a specialized provider/plugin surface for models, messaging platforms, memory, context engines, secrets, image/video generation, web search, or browser sessions.
5. Use configuration for TTS commands, STT commands, shell hooks, MCP, and other explicitly config-driven surfaces.
6. Use gateway hook directories for gateway event handlers.
7. Use the desktop SDK or dashboard SDK only for their respective UI host; they do not share the Python plugin API.
8. Use ACP when an editor or compatible client drives the agent; hand generic ACP implementation to `build-acp-agent` and existing client setup to `operate-acp-agent-integration`.
9. Use TUI gateway JSON-RPC or the OpenAI-compatible API server for custom programs that drive the agent without an ACP client.
10. Modify Hermes core only when the feature belongs upstream and the official contributor guide selects that path.

Read [references/extension-surface-map.md](references/extension-surface-map.md) before implementing any surface beyond a skill or MCP declaration.

## Implement a Standalone Python Plugin

For a third-party or project integration:

1. Keep it in an independently installable repository or project/user plugin directory.
2. Add `plugin.yaml` and a narrow `register(ctx)` entry point.
3. Split schemas from handlers so model-visible contracts stay reviewable.
4. Declare provided tools, hooks, commands, skills, and required environment only when they are actually registered or required.
5. Keep credentials in Hermes/private environment configuration.
6. Add unit tests for registration, schemas, handlers, redaction, and failure messages.
7. Add an opt-in smoke test for the real backend.

Do not merge third-party product integrations into the Hermes core repository merely for discoverability.

## Preserve Runtime Boundaries

- The agent loop, gateway, cron, ACP, and auxiliary calls share provider runtime resolution; a provider change must account for each consumer.
- Built-in tools and user/project plugins have different ownership and contribution paths.
- Project plugins require the explicit project-plugin enablement boundary.
- Later plugin sources can override earlier sources; test name collisions and replacement behavior.
- General Python plugins, desktop plugins, dashboard plugins, and provider subtypes have separate discovery and APIs.
- Prompt assembly separates stable, context, and volatile material; do not inject frequently changing data into stable prompt layers without measuring cache consequences.

## Validate in Layers

1. Static manifest and schema validation.
2. Unit tests with fake providers or clients.
3. Registration/discovery test in an isolated Hermes home or profile.
4. Harmless runtime invocation.
5. Failure-path and missing-secret checks.
6. Host-specific smoke test for gateway, desktop, dashboard, or provider behavior.
7. Docs and example review against the current developer guide.

## Output Contract

State:

- `classification`: durable building block, local implementation detail, or conscious stopgap;
- `surface`: exact Hermes extension system;
- `ownership`: standalone, project, user, bundled, or upstream core;
- `files`: concrete files and entry points;
- `state`: configuration, credentials, or services touched;
- `verification`: unit and runtime evidence;
- `portability`: what remains Hermes-specific versus Agent Skills or MCP portable.
