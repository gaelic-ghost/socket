# Hermes Extension Surface Map

## Selection Table

| Need | Surface | Primary entry point |
| --- | --- | --- |
| Instructions using existing tools | Skill | `SKILL.md` |
| External tool server | MCP | `mcp_servers` config |
| Tools, plugin hooks, slash/CLI commands, bundled skills | General Python plugin | `plugin.yaml`, `register(ctx)` |
| Inference backend | Model-provider plugin | `register_provider(...)` |
| Messaging channel | Platform plugin | `ctx.register_platform()` |
| External memory | Memory provider | `MemoryProvider` subtype |
| Context compression | Context-engine plugin | `ctx.register_context_engine()` |
| Secret/vault lookup | Secret-source plugin | secret-source registration |
| Image generation | Image provider | `ctx.register_image_gen_provider()` |
| Video generation | Video provider | video-provider registration |
| Web search/extract | Web-search provider | web provider registration |
| Cloud browser sessions | Browser provider | browser-provider registration |
| TTS command backend | Config-driven | TTS command configuration |
| STT command backend | Config-driven | `HERMES_LOCAL_STT_COMMAND` |
| Gateway events | Gateway hook | `HOOK.yaml`, `handler.py` |
| Shell lifecycle actions | Shell hook | `hooks:` configuration |
| Native Hermes Desktop UI | Desktop Plugin SDK | `$HERMES_HOME/desktop-plugins/` |
| Hermes web dashboard UI | Dashboard extension | dashboard `manifest.json` and SDK |
| IDE integration | ACP | ACP adapter/protocol |
| Custom rich host | TUI gateway JSON-RPC | `tui_gateway` protocol |
| Generic HTTP client | API server | OpenAI-compatible HTTP API |
| Built-in core behavior | Upstream contribution | Hermes source and contributor guide |

## General Plugin Discovery

General plugins can be bundled, user-scoped, project-scoped, pip-distributed, or Nix-managed. Project plugins require explicit enablement. Specialized plugin directories use their own loaders. Later sources can override earlier sources on name collision, so tests must cover replacement and discovery order when names overlap.

Third-party product integrations should ship standalone. Keep upstream core changes for features Hermes itself owns.

## Provider Decision

Use a model-provider plugin for an OpenAI-compatible third-party provider profile that can be declared without a new core API mode. A first-class upstream provider is broader: it may require auth UI, model catalogs, runtime resolution, auxiliary-client behavior, CLI flows, native adapters, tests, and docs.

Runtime provider resolution is shared by CLI, gateway, cron, ACP, and auxiliary calls. Validate all affected consumers.

## Programmatic Host Decision

- ACP: choose when the editor already speaks ACP.
- TUI gateway JSON-RPC: choose for a custom host needing sessions, approvals, streaming, slash commands, and rich Hermes behavior.
- API server: choose for OpenAI-compatible frontends or language-agnostic HTTP clients.
- Python library: choose when embedding `AIAgent` directly in Python is the actual requirement.

## Authoritative Sources

- [Build a Hermes plugin](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins)
- [Plugins overview](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins)
- [Creating skills](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills)
- [Adding tools](https://hermes-agent.nousresearch.com/docs/developer-guide/adding-tools)
- [Adding providers](https://hermes-agent.nousresearch.com/docs/developer-guide/adding-providers)
- [Adding a platform adapter](https://hermes-agent.nousresearch.com/docs/developer-guide/adding-platform-adapters)
- [Programmatic integration](https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration)
- [Desktop Plugin SDK](https://hermes-agent.nousresearch.com/docs/developer-guide/desktop-plugin-sdk)
- [Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)
- [Agent loop](https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop)
- [Provider runtime](https://hermes-agent.nousresearch.com/docs/developer-guide/provider-runtime)
- [Plugin LLM access](https://hermes-agent.nousresearch.com/docs/developer-guide/plugin-llm-access)
