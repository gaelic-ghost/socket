---
name: install-plugin-to-socket
description: Install, refresh, or detach an in-development Codex plugin in a local Codex install surface at repo or personal scope. Use when a local plugin needs marketplace wiring for Codex app or CLI discovery without hand-editing marketplace JSON.
---

# Install Plugin To Socket

Wire an in-development Codex plugin into Codex's documented local plugin surfaces.

This skill is for local Codex plugin development workflows. It does not publish plugins, does not manage the official plugin directory, and does not claim undocumented control over Codex's installed-plugin cache internals.

## Inputs

- Required: source plugin directory containing `.codex-plugin/plugin.json`
- Required: scope
  - `repo`
  - `personal`
- Optional: target repo root when `scope=repo`
- Optional: action
  - `install`
  - `refresh`
  - `detach`
- Optional: whether the request is check-only planning or real apply behavior

## Workflow

1. Confirm the task is local Codex plugin wiring, not generic plugin authoring or metadata review.
2. Read the plugin manifest at `.codex-plugin/plugin.json` and infer the plugin name, version, description, and interface metadata.
3. Use `scripts/install_plugin_to_socket.py` in `check-only` mode first.
4. For `repo` scope, target:
   - `$REPO_ROOT/plugins/<plugin-name>`
   - `$REPO_ROOT/.agents/plugins/marketplace.json`
5. For `personal` scope, target:
   - `~/.codex/plugins/<plugin-name>`
   - `~/.agents/plugins/marketplace.json`
6. Keep marketplace `source.path` relative to the marketplace root, prefixed with `./`, and inside that root.
7. Merge one plugin entry into the marketplace without overwriting unrelated entries.
8. For `install` and `refresh`, copy the plugin into the chosen local scope and update the marketplace entry.
9. For `detach`, remove only the matching marketplace entry and the matching local plugin directory when it belongs to that install target.
10. After apply behavior, tell the maintainer to restart Codex and verify that the plugin appears in the plugin directory.

## Output Contract

- Return a short summary plus JSON with:
  - `run_context`
  - `scope`
  - `action`
  - `source_plugin`
  - `target_plugin_root`
  - `marketplace_path`
  - `findings`
  - `apply_actions`
  - `restart_required`
  - `verification_steps`
  - `errors`
- If there are no findings, no apply actions, and no errors, output exactly `No findings.`

## Guardrails

- Never overwrite an existing marketplace catalog wholesale.
- Never point `source.path` outside the marketplace root.
- Never claim that updating the marketplace file alone installs a plugin into undocumented Codex internals.
- Never use this skill to publish a plugin publicly.
- Never touch Claude plugin wiring here; this skill is for Codex local plugin development surfaces.

## References

- `references/local-plugin-install-notes.md`
