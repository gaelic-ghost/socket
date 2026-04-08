---
name: install-plugin-to-socket
description: Install, update, uninstall, verify, repair, or promote an in-development Codex plugin in a local Codex install surface at personal or repo scope. Use when a local plugin needs marketplace wiring or repair without hand-editing marketplace JSON.
---

# Install Plugin To Socket

Wire an in-development Codex plugin into Codex's documented local plugin surfaces.

This skill is for local Codex plugin development workflows. It does not publish plugins, does not manage the official plugin directory, and only uses app-server plugin install or uninstall RPCs as best-effort extras when they happen to be available in the local Codex build.

## Inputs

- Required: source plugin directory
  - for mutating actions, this must be the plugin root containing `.codex-plugin/plugin.json`
  - `verify` may also accept a repo root that contains exactly one staged plugin under `plugins/` or exactly one marketplace-resolved plugin root
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
  - `repair`
  - `enable`
  - `disable`
  - `promote`
- Optional: install mode
  - default: `copy`
  - `copy`
  - `symlink`
- Optional: repo install tracking policy when `scope=repo`
  - default: `local-only`
  - `tracked`
  - `local-only`
- Optional: Codex config path override
  - `--codex-config-path <path>`
- Optional: whether the request is check-only planning or real apply behavior

## Workflow

1. Confirm the task is local Codex plugin wiring, not generic plugin authoring or metadata review.
2. Resolve the effective source plugin root and read the plugin manifest at `.codex-plugin/plugin.json`.
   - Keep repo-root source auto-detection as a `verify`-only convenience.
   - For `install`, `update`, `uninstall`, `repair`, `enable`, `disable`, and `promote`, require the canonical plugin root directly.
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
   - write the plugin enabled state into Codex's active config scope with `enabled = true` on install
10. Use `copy` mode as the default because it matches the current OpenAI examples for local plugin installs and gives Codex a stable staged plugin tree to recache from.
11. After `install`, `update`, `repair`, or `promote`, try Codex's own app-server `plugin/install` RPC against the resolved marketplace path only as a best-effort cache-sync optimization.
12. If the local Codex build does not expose a working app-server `plugin/install` path, keep the staged tree, marketplace entry, and config-state wiring anyway, and report that Codex-side installed-cache sync fell back to the documented restart-plus-plugin-browser path.
13. Treat `update` as the update workflow when the source clone is ahead of the staged install copy. It should recopy the source plugin tree into the staged path, rewrite the marketplace entry if needed, and re-run the Codex-side install step when applicable.
14. Treat `verify` as the audit-oriented workflow for checking whether the staged plugin tree, marketplace entry, optional plugin surfaces, config-state expectations, and installed-cache state still match the source plugin.
15. Treat `repair` as the bounded workflow when the intended staged plugin should keep its current scope, but the local install surface drifted. In repo scope, it should also remove any legacy repo-private `.codex/plugins/` copy or matching legacy repo-private marketplace entry left behind by older helper behavior.
16. Treat `enable` and `disable` as explicit Codex config-state workflows backed by the active scope's `config.toml` entries in the form `[plugins."plugin-name@marketplace-name"]`.
17. Treat `promote` as the bounded workflow that copies the source plugin into personal scope, writes the personal marketplace entry, carries forward the repo install's enabled-state if present in Codex's active config scope, runs the Codex-side personal install step, and then removes the repo-local staged install surface.
18. Treat `symlink` mode as an advanced local-dev override only when a maintainer explicitly wants a staged in-scope symlink instead of the documented copied tree.
19. Treat repo-scope install tracking as a maintainer policy choice, not as a second filesystem shape:
   - `tracked`: the repo-scoped staged plugin tree and marketplace change are intentional shared repo state that may be committed and synced
   - `local-only`: the repo-scoped staged plugin tree and marketplace change are local dev wiring that should stay uncommitted unless the repo explicitly chooses otherwise
20. For repo-scope installs marked as `tracked`, require `copy` mode. A symlinked repo-scope target is local-only by nature and should not be presented as shared git state.
21. For `install`, `update`, and `repair`, materialize the staged plugin path in the chosen mode and update the marketplace entry.
22. For repo-scope installs, use the documented repo-marketplace surface so the target repo can expose that local plugin install through `.agents/plugins/marketplace.json`.
23. For `uninstall`, try Codex's own app-server `plugin/uninstall` RPC as a best-effort cache cleanup before removing the matching marketplace entry, staged plugin path, and matching plugin config-state entry.
24. After apply behavior, tell the maintainer to restart Codex and verify that the plugin appears in the plugin directory or reflects the intended enabled-state.

## Usage Examples

- Personal install:
  - `uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py --source-plugin-root plugins/agent-plugin-skills --action install --run-mode apply`
  - this now enables the personal-scope plugin by default in `~/.codex/config.toml` and asks Codex's app-server to mark the plugin installed when that RPC is available locally
- Repo-local install:
  - `uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py --source-plugin-root /path/to/plugin --scope repo --repo-root /path/to/target-repo --action install --run-mode apply --repo-install-tracking local-only`
- Repo-local install intended to stay tracked in git:
  - `uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py --source-plugin-root /path/to/plugin --scope repo --repo-root /path/to/target-repo --action install --run-mode apply --repo-install-tracking tracked --install-mode copy`
- Update a staged copied install after source changes:
  - `uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py --source-plugin-root /path/to/plugin --action update --run-mode apply`
- Remove a local install cleanly:
  - `uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py --source-plugin-root /path/to/plugin --action uninstall --run-mode apply`
- Verify an already wired install without mutating it:
  - `uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py --source-plugin-root /path/to/plugin --action verify --run-mode check-only --print-md`
- Repair a drifted install surface in one pass:
  - `uv run python skills/install-plugin-to-socket/scripts/install_plugin_to_socket.py --source-plugin-root /path/to/plugin --scope repo --repo-root /path/to/target-repo --action repair --run-mode apply`
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
- `invalid-marketplace-entry-empty-relative-source-path`
  - A repo-local marketplace entry points at `./`, which Codex may reject for the whole marketplace.
  - Fix: repair the repo's own product marketplace separately. This installer no longer treats repo product marketplace files as the repo-scope install surface for external plugin installs.
- `legacy-repo-private-install-surface`
  - The target repo still has old repo-private install wiring under `$REPO_ROOT/.codex/plugins/`.
  - Fix: run `repair` in repo scope so the documented repo-marketplace install stays in place and the old repo-private `.codex/plugins` surface is removed.
- `missing-plugin-enabled-state`
  - Codex config does not include an explicit enabled-state entry for the plugin key.
  - Fix: rerun `install` for a missing personal install default-enable, or rerun `enable` / `disable` when the intended state differs.
- `stale-plugin-enabled-state`
  - Codex config includes a plugin entry, but the enabled-state does not match the requested workflow.
  - Fix: rerun `enable` or `disable`, depending on the intended state.
- `missing-plugin-installed-cache`
  - Codex still sees the plugin from the marketplace, but it has not installed it into Codex's own local cache yet.
  - Fix: rerun `install`, `update`, `repair`, or `promote` with a helper version that can call app-server `plugin/install`, or install it once through the Codex plugin browser if the local build does not expose that RPC.
- `missing-mcp-surface`, `missing-app-surface`, `missing-hooks-config`, `missing-interface-asset`
  - The source plugin manifest or optional plugin packaging surfaces are incomplete.
  - Fix: repair the plugin packaging before trusting the staged local install.

Preferred repair flow:

1. Run the helper in `check-only` mode first.
2. Confirm the intended scope and install mode.
3. Use `update` when the staged path and marketplace entry should continue to exist but need to be rewritten.
4. Use `repair` when the drift includes legacy repo-private `.codex/plugins` files or a matching legacy repo-private marketplace entry from older helper behavior.
5. Use `install` when a new personal install should take the default enabled path, and use `enable` or `disable` when marketplace wiring is correct but Codex config-state needs an explicit follow-up change.
6. Use `promote` when a repo-local install should become the personal default install surface instead.
7. Use `uninstall` and then `install` when the staged path belongs to the wrong source plugin, the wrong scope, or the wrong plugin name.
8. Restart Codex after the repair so the local marketplace view and installed cache pick up the staged plugin changes.
9. For repo-scope installs, confirm whether the staged plugin tree and marketplace change are meant to be `tracked` shared repo state or `local-only` uncommitted wiring before you finalize the repair.

## Troubleshooting

- If a repo-local plugin still does not show up after `install`, `update`, or `repair`, fully restart Codex in that repo. A live workspace can continue using the installed-plugin and marketplace state it loaded before the install surface changed.
- If `/plugins` still looks wrong after restart, check `~/.codex/log/codex-tui.log` for marketplace warnings such as `skipping marketplace` or `local plugin source path must not be empty`.
- Repo-local plugin visibility now comes from the documented repo marketplace at `.agents/plugins/marketplace.json` plus the staged plugin tree under `plugins/`.
- Repo-scope tracking is a repo policy choice. `tracked` repo installs still use the same documented repo paths as `local-only` installs; the difference is whether the working-tree change is meant to be committed and shared.
- The `/plugins` slash command ordering may not be intuitive or obviously alphabetical, so scan the full list before concluding a plugin is missing.

## Remaining Gaps

- This skill now manages Codex plugin enable or disable state through Codex's active `config.toml`, and it treats app-server plugin install or uninstall RPCs as optional cache-sync helpers when the local Codex build exposes them.
- The current overwrite policy still uses replace-in-place semantics for staged targets; backup and fail-on-existing variants remain planned work.

## Output Contract

- Return a short summary plus JSON with:
  - `run_context`
    - include config resolution context such as `config_path` and `scope_source`
  - `scope`
  - `action`
  - `install_mode`
  - `repo_install_tracking`
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
- Never delete the source plugin repo during uninstall; only remove the staged install target path.
- Never claim that updating the marketplace file alone installs a plugin into undocumented Codex internals.
- Never claim that the app-server install or uninstall RPC is universally available across Codex versions; when it is missing or fails, fall back to staged install surfaces and say so plainly.
- Never use this skill to publish a plugin publicly.
- Never touch Claude plugin wiring here; this skill is for Codex local plugin development surfaces.

## References

- `references/customization-schema.md`
- `references/local-plugin-install-notes.md`
