# Sync Checklist

- root `skills/` is canonical
- `.codex-plugin/plugin.json` points at root `skills/` with `"skills": "./skills/"`
- `.agents/skills -> ../skills`
- README and AGENTS describe the repo as a source-first skills-export repository
- README and AGENTS keep the Codex plugin-boundary note explicit
- README or AGENTS say to refresh current OpenAI Codex docs before changing plugin, skill, MCP, hooks, marketplace, or subagent guidance
- no nested staged plugin-directory guidance remains
- user-facing install and update guidance defaults to Git-backed marketplace sources and official marketplace add/upgrade commands
- no installer or install-validation guidance remains
- maintainer tooling guidance stays explicit
