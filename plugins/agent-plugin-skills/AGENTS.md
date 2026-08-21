# AGENTS.md

This plugin owns agent-plugin repository shape and deterministic plugin
maintenance. Follow Socket root guidance for Git, release, documentation, and
repository-wide safety rules.

## Scope

- Own Codex plugin manifests, bundled skill layout, local marketplace wiring,
  fixed Socket publisher policy, and aggregate plugin validation/apply tooling.
- Keep repository documentation and releases in `repository-skills`, agent
  system behavior in `agent-engineering-skills`, cross-host transports and
  adapters in `agent-portability-skills`, and runtime hook behavior in the
  plugin that ships the hook.
- Treat authored plugin contents as source and installed plugin state as
  read-only runtime state.

## Automation Contract

- Use only managed `.fsx` scripts and `just` recipes.
- Expose exactly `just plugins-check` and `just plugins-apply` for plugin
  maintenance. Both commands always process the whole repository plugin set.
- Do not add per-plugin commands, Python or shell scripts, customization
  profiles, nested tests, compatibility wrappers, or parallel metadata paths.
- Keep Gale's publisher identity, Apache-2.0 license, marketplace policy, and
  default repository conventions fixed in the managed implementation.

## Validation

Run the essential integration path from the Socket repository root:

```text
just plugins-check
just test
```
