# Sync Checklist

- root `skills/` is canonical
- `.codex-plugin/plugin.json` points at root `skills/` with `"skills": "./skills/"`
- `.agents/skills -> ../skills`
- `.claude/skills -> ../skills`
- README and AGENTS describe the repo as a source-first skills-export repository
- README and AGENTS keep the Codex plugin-boundary note explicit
- no nested staged plugin-directory guidance remains
- no installer or install-validation guidance remains
- maintainer tooling guidance stays explicit
