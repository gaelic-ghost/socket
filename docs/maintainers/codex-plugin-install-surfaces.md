# Codex Plugin Install Surfaces

Use this document when maintainers need the short Socket-level map of Codex plugin install surfaces.

## Core Model

Codex plugin wiring has five separate jobs:

1. Tracked marketplace source
   - Added with `codex plugin marketplace add <owner>/<repo>`.
   - Refreshed with `codex plugin marketplace upgrade <marketplace-name>`.
2. Marketplace catalog
   - Lists discoverable plugins.
   - In Socket, this is [`.agents/plugins/marketplace.json`](../../.agents/plugins/marketplace.json).
3. Plugin root payload
   - Contains `.codex-plugin/plugin.json` and bundled surfaces such as `skills/`, `.mcp.json`, `hooks/`, or `assets/`.
   - Socket child plugin entries normally point at `./plugins/<child>`.
4. Installed plugin cache
   - Codex-owned runtime copy under `~/.codex/plugins/cache/...`.
   - Do not edit this as source.
5. Enabled-state config
   - Marketplace-scoped plugin enablement in Codex config.
   - Treat this as state, not as an install destination.

## Socket Rules

- The Socket root is a marketplace catalog, not an aggregate plugin payload.
- Child plugins stay independently listed unless a future aggregate plugin is deliberately added.
- Marketplace `source.path` points at the plugin root, not at `.codex-plugin/`.
- Git-backed marketplace add and upgrade commands are the default user-facing install and update path.
- Manual local marketplace roots and copied payload folders are for development, unpublished testing, or fallback only.
- Repo-visible plugins come from marketplace catalogs. OpenAI does not currently document a richer repo-private plugin scoping model beyond that marketplace model.

## Reading Order

When plugin state looks wrong, inspect in this order:

1. marketplace source: was the expected marketplace added or upgraded?
2. marketplace entry: does it list the plugin and point at the intended root?
3. plugin root payload: does the target contain `.codex-plugin/plugin.json` and any declared surfaces?
4. enabled state: is the expected `<plugin>@<marketplace>` identity enabled?
5. installed cache: does a fresh Codex session still see stale runtime state?

## References

- [Plugin Packaging Strategy](./plugin-packaging-strategy.md)
- [Plugin Install Testing](./plugin-install-testing.md)
- [OpenAI Codex plugin build docs](https://developers.openai.com/codex/plugins/build)
