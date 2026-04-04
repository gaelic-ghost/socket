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
- Codex installs the plugin it exposes through the marketplace into its own cache under `~/.codex/plugins/cache/...`
- after local plugin changes, maintainers should update the plugin directory the marketplace points at and restart Codex

Current repo guidance for this skill:

- Prefer personal scope by default so one maintained local Codex plugin install can be reused across repositories.
- Use repo scope only when a repository genuinely needs its own repo-local plugin catalog.
- Allow persistent default-scope preferences through:
  - `.codex/profiles/install-plugin-to-socket/customization.yaml`
  - `~/.config/gaelic-ghost/agent-plugin-skills/install-plugin-to-socket/customization.yaml`
- Default to `copy` mode because it matches the documented OpenAI examples for local plugin installs.
- Treat `update` in `copy` mode as the normal update workflow when the source clone is ahead of the staged install copy.
- Keep `symlink` mode as an advanced maintainer override for local development only; it is not the primary documented Codex install model.
- Do not point a repo marketplace directly at a sibling repo outside the marketplace root. Stage a copy or symlink at the in-scope plugin path instead.
- Treat `install-plugin-to-socket` as the repair surface for drifted local installs:
  - rerun `install` when the staged path or marketplace entry is missing
  - rerun `update` when the marketplace entry is stale, the staged path needs to be rematerialized in the chosen mode, or the copied staged tree no longer matches the source plugin tree
  - use `uninstall` then `install` when the wrong plugin tree was staged into the target path

Relevant docs:

- `https://developers.openai.com/codex/plugins`
- `https://developers.openai.com/codex/plugins/build`
- `https://developers.openai.com/codex/config-advanced/#project-config-files-codexconfigtoml`

Related local references:

- `customization-schema.md`
