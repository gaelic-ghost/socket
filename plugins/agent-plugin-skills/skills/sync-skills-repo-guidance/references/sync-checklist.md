# Sync Checklist

Check these surfaces:

- `README.md`
- `AGENTS.md`
- `ROADMAP.md`
- `docs/maintainers/reality-audit.md`
- `docs/maintainers/workflow-atlas.md`
- `.agents/plugins/marketplace.json`
- `plugins/<plugin-name>/.codex-plugin/plugin.json`
- `plugins/<plugin-name>/.claude-plugin/plugin.json`
- `.agents/skills`
- `.claude/skills`
- `plugins/<plugin-name>/skills`

Check these policy points:

- root `skills/` is canonical
- plugin, marketplace, MCP, and app manifests live under `plugins/` and `.agents/plugins/`
- POSIX symlink mirrors are explicit and documented
- maintainer Python tooling guidance keeps `ruff` and `mypy` available through `uv tool install`
- standalone skill install guidance matches `npx skills add`
- OpenAI and Claude docs links are current and accurate
- README-only or roadmap-only maintenance still routes to the narrower skills
