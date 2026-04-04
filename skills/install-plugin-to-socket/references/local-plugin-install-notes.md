# Local Plugin Install Notes

This skill follows the documented OpenAI Codex local plugin flow:

- Repo scope uses:
  - `$REPO_ROOT/plugins/<plugin-name>`
  - `$REPO_ROOT/.agents/plugins/marketplace.json`
- Personal scope uses:
  - `~/.codex/plugins/<plugin-name>`
  - `~/.agents/plugins/marketplace.json`

OpenAI docs note that:

- local plugins are exposed through marketplace files
- marketplace `source.path` stays relative to the marketplace root
- marketplace `source.path` can point to any plugin path inside that marketplace root, not only the example directories
- Codex loads installed plugins through marketplace-backed local installs
- Codex installs the plugin it exposes through the marketplace into its own cache under `~/.codex/plugins/cache/...`
- after local plugin changes, maintainers should update the plugin directory the marketplace points at and restart Codex

Current repo guidance for this skill:

- Default to `copy` mode because it matches the documented OpenAI examples for local plugin installs.
- Offer `symlink` mode for adjacent or otherwise local in-development plugin repos when the maintainer wants the staged plugin path inside the chosen marketplace root to follow live source changes.
- Do not point a repo marketplace directly at a sibling repo outside the marketplace root. Stage a copy or symlink at the in-scope plugin path instead.
- Treat `install-plugin-to-socket` as the repair surface for drifted local installs:
  - rerun `install` when the staged path or marketplace entry is missing
  - rerun `refresh` when the marketplace entry is stale or the staged path needs to be rematerialized in the chosen mode
  - use `detach` then `install` when the wrong plugin tree was staged into the target path

Relevant docs:

- `https://developers.openai.com/codex/plugins`
- `https://developers.openai.com/codex/plugins/build`
- `https://developers.openai.com/codex/config-advanced/#project-config-files-codexconfigtoml`
