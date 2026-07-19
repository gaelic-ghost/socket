# Hermes Native Python Plugin Adapter Plan

Date checked: 2026-07-19 against Hermes Agent 0.17.0 and the current plugin
developer guide.

This is a prioritized implementation plan, not an adapter implementation.
Socket keeps its portable workflows as skills and its external tools as MCP
servers. A native Hermes Python plugin is warranted only when a real runtime
behavior cannot be represented by either surface. In particular,
`.codex-plugin/plugin.json` remains a Codex distribution bundle; it is not a
Hermes `plugin.yaml` equivalent.

Future general adapters should be independently installable Hermes plugins with
a small `plugin.yaml`, an `__init__.py` that calls `register(ctx)`, and focused
schema/handler tests. If the behavior belongs to a specialized Hermes extension
system—platform, model, memory, context, secret, media, search, browser,
desktop, or dashboard—use that subsystem's registration and packaging model
instead. Do not introduce a generic Socket-to-Hermes bridge: it would duplicate
intentionally different host models without serving a current concrete
behavior.

## Priority Order

| Priority | Socket package | Why a skill or MCP is insufficient | Adapter shape | Likely future ownership | Required configuration | Validation strategy |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `speak-swiftly` | Speech control needs session-aware local playback, queue state, and operator commands beyond a static workflow or remote MCP declaration. | General plugin: tools for status and queue control, slash command for playback state, optional post-tool hook only if a concrete accessibility flow requires it. | Standalone `SpeakSwiftlyServer` plugin source: `hermes-plugin/plugin.yaml`, `hermes-plugin/__init__.py`, `schemas.py`, `tools.py`, and tests. | Existing Speak Swiftly local endpoint or command configuration; do not embed machine paths or credentials. | Unit-test registration and handlers with a fake local client; run an opt-in local smoke test against a separately configured service. |
| 2 | `cardhop-app` | MCP already covers contact actions, but an adapter could provide a narrow slash command or local readiness tool that unifies the macOS capability check and Cardhop dispatch. | General plugin with one readiness tool and, only after a real operator need, a `/cardhop` command dispatching the documented integration route. | `plugins/cardhop-app/hermes-plugin/` with `plugin.yaml`, `__init__.py`, handler module, schemas, and tests. | macOS, Cardhop.app, `uv`, and an explicit configured MCP checkout path. | Mock AppleScript and URL-scheme execution; opt-in Mac smoke test verifies only `healthcheck` before action tools. |
| 3 | `things-app` | The MCP server carries the tools, while a native command can safely summarize a confirmed task workflow or expose explicit auth readiness without broad tool discovery. | General plugin with read-only readiness/status tool; defer task mutation tools to MCP unless a slash-command workflow proves necessary. | `plugins/things-app/hermes-plugin/` with manifest, registration, status handler, and tests. | macOS, Things.app, local MCP checkout path; `THINGS_AUTH_TOKEN` only for future update behavior. | Unit-test token-state redaction and registration; opt-in app-presence/read-only smoke test. |
| 4 | `cloud-inference-skills` | The existing Runpod MCP server is the right API surface. A Python plugin is justified only for a concrete Hermes-native provider/backend configuration or an account-safe preflight command. | Start with no adapter. If demanded, general plugin CLI command for read-only preflight; model-provider or backend plugin only when Hermes directly owns the provider integration. | `plugins/cloud-inference-skills/hermes-plugin/` only after a defined provider contract and owner. | Provider credentials such as `RUNPOD_API_KEY`, explicit account/region/cost policy. | Fake provider-client tests, redaction tests, and a separately approved no-mutation account probe. |
| 5 | `productivity-skills` | Dice's remote MCP endpoint is sufficient for job search. Static workflow guidance belongs in the skill tap. | None. Consider a slash command only if a repeatable Hermes session workflow cannot be expressed as a skill plus MCP. | No adapter files planned. | None for the documented public Dice search path. | Reassess against a concrete command request; retain MCP configuration validation. |
| 6 | `apple-dev-skills` | Xcode MCP bridges already expose runtime tools, and the skill corpus is the portable instruction surface. A plugin would duplicate Xcode's capability discovery without a defined behavior. | None. Consider a general plugin only for a verified Hermes-specific Xcode project-context command that cannot be an MCP tool. | No adapter files planned. | macOS, compatible Xcode, and Xcode MCP enablement. | Preserve MCP launch checks and require a real Xcode project smoke test before proposing an adapter. |

## Delivery Rules For A Future Adapter

1. State the missing user behavior and why the existing skill or MCP fragment cannot provide it.
2. Choose one Hermes extension point: portable skill, MCP, general plugin tool,
   plugin hook, slash command, CLI command, bundled read-only skill, gateway
   platform, model/memory/context/secret/media/search/browser provider, desktop
   plugin, dashboard plugin, config-driven extension, or none. Do not combine
   them speculatively.
3. Keep configuration in documented environment variables or private Hermes
   configuration; never commit local checkout paths, tokens, or app secrets.
4. Add `plugin.yaml` requirements such as `requires_env` only for values that
   are truly required at plugin load time. Make mutation-capable behavior
   explicit and test it separately from read-only readiness.
5. Keep the plugin opt-in through Hermes `plugins.enabled`, with a documented
   install and enable flow. Hermes treats third-party general plugins as
   disabled until the operator enables them.

## Authoritative References

- [Hermes Plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins)
  defines `plugin.yaml`, `register(ctx)`, the general plugin extension points,
  discovery locations, and opt-in enablement.
- [Build a Hermes Plugin](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins)
  is the current extension-surface router for general, specialized,
  config-driven, desktop, dashboard, and programmatic integrations.
- [Hermes MCP Config Reference](https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference)
  defines the configuration surface that remains preferable for external MCP
  servers.
