# Sync Checklist

Check these surfaces:

- `README.md`
- `AGENTS.md`
- `ROADMAP.md`
- `docs/maintainers/reality-audit.md`
- `docs/maintainers/workflow-atlas.md`
- `.agents/plugins/marketplace.json`
- `.claude-plugin/marketplace.json`
- `plugins/<plugin-name>/.codex-plugin/plugin.json`
- `plugins/<plugin-name>/.claude-plugin/plugin.json`
- `.gitignore`
- `.agents/skills`
- `.claude/skills`
- `plugins/<plugin-name>/skills`

Check these policy points:

- root `skills/` is canonical
- plugin, marketplace, MCP, and app manifests live under `plugins/` and `.agents/plugins/`
- repo guidance distinguishes repo-local Codex packaging (`plugins/<plugin-name>/` plus `.agents/plugins/marketplace.json`) from personal Codex installs (`~/.codex/plugins/<plugin-name>` plus `~/.agents/plugins/marketplace.json`)
- repo guidance distinguishes direct Claude `--plugin-dir` development from Git-backed Claude marketplace sharing through repo-root `.claude-plugin/marketplace.json`
- repo guidance says which shared marketplace catalogs belong in git and which install copies and caches do not
- the shared `.gitignore` snippet for local runtime state is present or deliberately superseded by stricter ignores
- repo guidance names the workflow owner for Codex install lifecycle work instead of implying bootstrap or sync scripts perform install, update, uninstall, verify, repair, enable, disable, or promote operations themselves
- troubleshooting guidance tells users to restart Codex after marketplace changes, inspect `~/.codex/log/codex-tui.log` for skipped-marketplace warnings, and not assume `/plugins` ordering is intuitive
- POSIX discovery mirrors are explicit and documented
- bundled plugin `skills/` directories are explicit, documented, and kept in sync with root `skills/`
- maintainer Python tooling guidance keeps `ruff` and `mypy` available through `uv tool install`
- standalone skill install guidance matches `npx skills add`
- OpenAI and Claude docs links are current and accurate
- README-only or roadmap-only maintenance still routes to the narrower skills
