---
name: install-plugin-to-socket
description: Install, update, or uninstall an in-development Codex plugin in a local Codex install surface at personal or repo scope. Use when a local plugin needs marketplace wiring for Codex app or CLI discovery without hand-editing marketplace JSON.
---

# Install Plugin To Socket

Wire an in-development Codex plugin into Codex's documented local plugin surfaces.

This skill is for local Codex plugin development workflows. It does not publish plugins, does not manage the official plugin directory, and does not claim undocumented control over Codex's installed-plugin cache internals.

## Inputs

- Required: source plugin directory
  - preferred: the plugin root containing `.codex-plugin/plugin.json`
  - accepted convenience input: a repo root that contains exactly one staged plugin under `plugins/` or exactly one marketplace-resolved plugin root
- Optional: scope
  - default: `personal`
  - `repo`
  - `personal`
- Optional: config path override
  - `--config <path>`
  - when omitted, resolve defaults from:
    - `.codex/profiles/install-plugin-to-socket/customization.yaml`
    - `~/.config/gaelic-ghost/agent-plugin-skills/install-plugin-to-socket/customization.yaml`
- Optional: target repo root when `scope=repo`
  - default: current working directory when the helper is run from the target repo
- Optional: action
  - `install`
  - `update`
  - `uninstall`
  - `verify`
  - `enable`
  - `disable`
  - `promote`
- Optional: install mode
  - default: `copy`
  - `copy`
  - `symlink`
- Optional: Codex config path override
  - `--codex-config-path <path>`
- Optional: whether the request is check-only planning or real apply behavior

## Workflow

1. Confirm the task is local Codex plugin wiring, not generic plugin authoring or metadata review.
2. Resolve the effective source plugin root and read the plugin manifest at `.codex-plugin/plugin.json`.
3. Infer the plugin name, version, description, interface metadata, and optional plugin surfaces from that manifest.
3. Use `scripts/install_plugin_to_socket.py` in `check-only` mode first.
4. Resolve the effective install scope in this order:
   - explicit `--scope`
   - explicit `--config`
   - repo profile
   - global profile
   - built-in default `personal`
5. For `personal` scope, target:
   - `~/.codex/plugins/<plugin-name>`
   - `~/.agents/plugins/marketplace.json`
6. For `repo` scope, target:
   - `$REPO_ROOT/plugins/<plugin-name>`
   - `$REPO_ROOT/.agents/plugins/marketplace.json`
7. Keep marketplace `source.path` relative to the marketplace root, prefixed with `./`, and inside that root.
8. Merge one plugin entry into the marketplace without overwriting unrelated entries.
9. Default to the documented Codex local-plugin flow:
   - stage the plugin at the repo or personal plugin path
   - point the marketplace entry at that staged path
10. Use `copy` mode as the default because it matches the current OpenAI examples for local plugin installs and gives Codex a stable staged plugin tree to recache from.
11. Treat `update` as the update workflow when the source clone is ahead of the staged install copy. It should recopy the source plugin tree into the staged path and rewrite the marketplace entry if needed.
12. Treat `verify` as the audit-oriented workflow for checking whether the staged plugin tree, marketplace entry, optional plugin surfaces, and config-state expectations still match the source plugin.
13. Treat `enable` and `disable` as Codex config-state workflows backed by `~/.codex/config.toml` entries in the form `[plugins."plugin-name@marketplace-name"]`.
14. Treat `promote` as the bounded workflow that copies the source plugin into personal scope, writes the personal marketplace entry, carries forward the repo install's enabled-state if present, and then removes the repo-local install surface.
15. Treat `symlink` mode as an advanced local-dev override only when a maintainer explicitly wants a staged in-scope symlink instead of the documented copied tree.
16. For `install` and `update`, materialize the staged plugin path in the chosen mode and update the marketplace entry.
17. For `uninstall`, remove only the matching marketplace entry, staged plugin path, and matching plugin config-state entry for that install target.
18. After apply behavior, tell the maintainer to restart Codex and verify that the plugin appears in the plugin directory or reflects the intended enabled-state.

## Usage Examples

- Personal install:
  - `uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py --source-plugin-root plugins/agent-plugin-skills --action install --run-mode apply`
- Repo-local install:
  - `uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py --source-plugin-root /path/to/plugin --scope repo --repo-root /path/to/target-repo --action install --run-mode apply`
- Update a staged copied install after source changes:
  - `uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py --source-plugin-root /path/to/plugin --action update --run-mode apply`
- Remove a local install cleanly:
  - `uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py --source-plugin-root /path/to/plugin --action uninstall --run-mode apply`
- Verify an already wired install without mutating it:
  - `uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py --source-plugin-root /path/to/plugin --action verify --run-mode check-only --print-md`
- Enable or disable a wired plugin in Codex config:
  - `uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py --source-plugin-root /path/to/plugin --action enable --run-mode apply`
  - `uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py --source-plugin-root /path/to/plugin --action disable --run-mode apply`
- Promote a repo-local install into personal scope:
  - `uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py --source-plugin-root /path/to/plugin --scope repo --repo-root /path/to/target-repo --action promote --run-mode apply`

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
  - Fix: rerun `update` in the intended mode.
- `stale-target-materialization`
  - The staged plugin path is present, but its materialization does not match the requested mode.
  - Fix: rerun `update` with the intended `copy` or `symlink` mode.
- `stale-target-copy`
  - The staged plugin tree is a copied install, but its contents no longer match the current source plugin tree.
  - Fix: rerun `update` in `copy` mode so the staged Codex install path is updated from the source clone.
- `missing-plugin-enabled-state`
  - Codex config does not include an explicit enabled-state entry for the plugin key.
  - Fix: rerun `enable` or `disable`, depending on the intended state.
- `stale-plugin-enabled-state`
  - Codex config includes a plugin entry, but the enabled-state does not match the requested workflow.
  - Fix: rerun `enable` or `disable`, depending on the intended state.
- `missing-mcp-surface`, `missing-app-surface`, `missing-hooks-config`, `missing-interface-asset`
  - The source plugin manifest or optional plugin packaging surfaces are incomplete.
  - Fix: repair the plugin packaging before trusting the staged local install.

Preferred repair flow:

1. Run the helper in `check-only` mode first.
2. Confirm the intended scope and install mode.
3. Use `update` when the staged path and marketplace entry should continue to exist but need to be rewritten.
4. Use `enable` or `disable` when marketplace wiring is correct but Codex config-state drifted.
5. Use `promote` when a repo-local install should become the personal default install surface instead.
6. Use `uninstall` and then `install` when the staged path belongs to the wrong source plugin, the wrong scope, or the wrong plugin name.
7. Restart Codex after the repair so the local marketplace view and installed cache pick up the staged plugin changes.

## Remaining Gaps

- This skill now manages Codex plugin enable or disable state through `~/.codex/config.toml`, but it does not try to manage project-scoped `.codex/config.toml` overrides.
- The current overwrite policy still uses replace-in-place semantics for staged targets; backup and fail-on-existing variants remain planned work.

## Output Contract

- Return a short summary plus JSON with:
  - `run_context`
    - include config resolution context such as `config_path` and `scope_source`
  - `scope`
  - `action`
  - `install_mode`
  - `source_plugin`
  - `target_plugin_root`
  - `marketplace_path`
  - `codex_config_path`
  - `plugin_config_key`
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
- Never delete the source plugin repo during uninstall; only remove the staged install target path.
- Never claim that updating the marketplace file alone installs a plugin into undocumented Codex internals.
- Never use this skill to publish a plugin publicly.
- Never touch Claude plugin wiring here; this skill is for Codex local plugin development surfaces.

## References

- `references/customization-schema.md`
- `references/local-plugin-install-notes.md`
