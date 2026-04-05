# Local Plugin Install Notes

This skill follows the documented OpenAI Codex local plugin flow:

- Personal scope uses:
  - `~/.codex/plugins/<plugin-name>`
  - `~/.agents/plugins/marketplace.json`
- Repo scope uses:
  - `$REPO_ROOT/plugins/<plugin-name>`
  - `$REPO_ROOT/.agents/plugins/marketplace.json`

OpenAI docs note that:

- local plugins are exposed through marketplace files
- marketplace `source.path` stays relative to the marketplace root
- marketplace `source.path` can point to any plugin path inside that marketplace root, not only the example directories
- Codex loads installed plugins through marketplace-backed local installs
- Current Codex builds may expose app-server `plugin/install` and `plugin/uninstall` RPCs that sync the marketplace-visible plugin into Codex's own cache under `~/.codex/plugins/cache/...`
- after local plugin changes, maintainers should update the plugin directory the marketplace points at and restart Codex
- Codex stores plugin enabled-state in `~/.codex/config.toml`

Current repo guidance for this skill:

- Prefer personal scope by default so one maintained local Codex plugin install can be reused across repositories.
- Personal-scope `install` should also write `enabled = true` for the plugin key by default so a new global install is immediately active after restart.
- Personal-scope `install`, `update`, `repair`, and `promote` should also prefer Codex's own app-server `plugin/install` RPC so the plugin becomes truly installed instead of merely available.
- Use repo scope only when a repository genuinely needs its own repo-local plugin catalog.
- Allow persistent default-scope preferences through:
  - `.codex/profiles/install-plugin-to-socket/customization.yaml`
  - `~/.config/gaelic-ghost/agent-plugin-skills/install-plugin-to-socket/customization.yaml`
- Default to `copy` mode because it matches the documented OpenAI examples for local plugin installs.
- Treat `update` in `copy` mode as the normal update workflow when the source clone is ahead of the staged install copy.
- Treat `verify` as the read-only audit workflow for checking staged plugin drift, marketplace drift, optional plugin-surface drift, and config-state expectations.
- Treat `verify` as the read-only audit workflow for checking staged plugin drift, marketplace drift, optional plugin-surface drift, config-state expectations, and whether Codex still reports the plugin as uninstalled.
- Treat `repair` as the bounded workflow for drifted install surfaces, including the common repo-local case where a legacy marketplace entry still points at `./` instead of `./plugins/<plugin-name>`.
- Treat personal-scope `install` as the default-enable workflow for a new global install, and use `enable` / `disable` when you need to change the config state after the install is already wired.
- Treat personal-scope `uninstall` as the matching Codex-cache removal workflow when the local build exposes app-server `plugin/uninstall`; otherwise fall back to staged-tree and marketplace removal only.
- Treat `promote` as the bounded workflow that carries a repo-local install into personal scope and then removes the repo-local install surface.
- Keep `symlink` mode as an advanced maintainer override for local development only; it is not the primary documented Codex install model.
- Do not point a repo marketplace directly at a sibling repo outside the marketplace root. Stage a copy or symlink at the in-scope plugin path instead.
- Treat `install-plugin-to-socket` as the repair surface for drifted local installs:
  - rerun `install` when the staged path or marketplace entry is missing
  - rerun `install` when a personal install is missing its default enabled-state entry
  - rerun `update` when the marketplace entry is stale, the staged path needs to be rematerialized in the chosen mode, or the copied staged tree no longer matches the source plugin tree
  - rerun `repair` when the repo-local marketplace contains an invalid `./` plugin path or a legacy repo-root plugin surface needs to be normalized to `plugins/<plugin-name>/`
  - rerun `enable` or `disable` when Codex config-state drifted
  - rerun `verify` when you need an audit-only report before changing anything
  - rerun `promote` when a repo-local install should become the personal default install surface
  - use `uninstall` then `install` when the wrong plugin tree was staged into the target path

Troubleshooting notes:

- Fully restart Codex after repo-local marketplace changes. An already-open workspace can keep the marketplace view it loaded before `install`, `update`, or `repair`.
- If the helper reports a personal-scope app-server fallback instead of a successful `plugin/install`, the plugin may still appear as available rather than installed until you install it once through Codex's plugin browser.
- When a staged repo-local plugin still does not show up, inspect `~/.codex/log/codex-tui.log` for marketplace warnings such as `skipping marketplace`.
- Repo-local scope only affects the repo that owns `.agents/plugins/marketplace.json`. Personal scope is the right path when the same plugin should be broadly available across repos.
- The Codex `/plugins` slash command list order may not be intuitive, so scan the full list before assuming a plugin is missing.

Relevant docs:

- `https://developers.openai.com/codex/plugins`
- `https://developers.openai.com/codex/plugins/build`
- `https://developers.openai.com/codex/config-advanced/#project-config-files-codexconfigtoml`

Related local references:

- `customization-schema.md`
