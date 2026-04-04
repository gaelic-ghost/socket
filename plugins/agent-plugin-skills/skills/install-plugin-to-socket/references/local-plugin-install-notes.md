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
- Codex loads installed plugins through marketplace-backed local installs
- after local plugin changes, maintainers should update the plugin directory the marketplace points at and restart Codex

Relevant docs:

- `https://developers.openai.com/codex/plugins`
- `https://developers.openai.com/codex/plugins/build`
- `https://developers.openai.com/codex/config-advanced/#project-config-files-codexconfigtoml`
