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
  - default: current working directory when the helper is run from the target repo
- Optional: action
  - `install`
  - `refresh`
  - `detach`
- Optional: install mode
  - `copy`
  - `symlink`
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
8. Default to the documented Codex local-plugin flow:
   - stage the plugin at the repo or personal plugin path
   - point the marketplace entry at that staged path
9. Use `copy` mode as the default because it matches the current OpenAI examples for local plugin installs.
10. Use `symlink` mode when the source plugin lives in an adjacent in-development repo and the maintainer wants the staged plugin path to track live source changes without repeated refresh copies.
11. For `install` and `refresh`, materialize the staged plugin path in the chosen mode and update the marketplace entry.
12. For `detach`, remove only the matching marketplace entry and the matching staged plugin path for that install target.
13. After apply behavior, tell the maintainer to restart Codex and verify that the plugin appears in the plugin directory.

## Repairing Drifted Installs

Use this skill as the repair surface for bad or stale local Codex plugin installs.

Common repair cases:

- `missing-target-plugin-root`
  - The marketplace entry exists, but the staged plugin path is missing.
  - Fix: rerun `install` in the intended mode.
- `missing-marketplace-entry`
  - The staged plugin path exists, but the marketplace does not expose it.
  - Fix: rerun `install` in the intended mode.
- `stale-marketplace-entry`
  - The marketplace entry points at the wrong staged path or has stale metadata.
  - Fix: rerun `refresh` in the intended mode.
- `stale-target-materialization`
  - The staged plugin path is present, but its materialization does not match the requested mode.
  - Fix: rerun `refresh` with the intended `copy` or `symlink` mode.

Preferred repair flow:

1. Run the helper in `check-only` mode first.
2. Confirm the intended scope and install mode.
3. Use `refresh` when the staged path and marketplace entry should continue to exist but need to be rewritten.
4. Use `detach` and then `install` when the staged path belongs to the wrong source plugin, the wrong scope, or the wrong plugin name.
5. Restart Codex after the repair so the local marketplace view and installed cache pick up the staged plugin changes.

## Output Contract

- Return a short summary plus JSON with:
  - `run_context`
  - `scope`
  - `action`
  - `install_mode`
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
- Never point a repo marketplace directly at an adjacent plugin repo outside the chosen marketplace root; use a staged copy or a staged symlink path inside the scope root instead.
- Never delete the source plugin repo during detach; only remove the staged install target path.
- Never claim that updating the marketplace file alone installs a plugin into undocumented Codex internals.
- Never use this skill to publish a plugin publicly.
- Never touch Claude plugin wiring here; this skill is for Codex local plugin development surfaces.

## References

- `references/local-plugin-install-notes.md`
