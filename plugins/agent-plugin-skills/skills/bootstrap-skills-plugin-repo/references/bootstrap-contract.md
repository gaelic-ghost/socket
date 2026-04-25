# Bootstrap Contract

A bootstrapped skills-export repository should include:

- root `skills/`
- `.agents/skills -> ../skills`
- `.claude/skills -> ../skills`
- `README.md`
- `AGENTS.md`
- `ROADMAP.md`
- `docs/maintainers/reality-audit.md`
- `docs/maintainers/workflow-atlas.md`
- maintainer Python tooling guidance
- strict dependency-provenance guidance in `AGENTS.md` requiring shared dependencies to resolve from GitHub, package managers, package registries, or other real remote repositories
- an explicit `AGENTS.md` prohibition on machine-local dependency paths in public or publicly shared projects

It may include root `.codex-plugin` packaging. When it does, `.codex-plugin/plugin.json` should point at bundled skills with `"skills": "./skills/"`. It should not include a nested staged plugin directory, repo marketplace, installer skill, or install-validation skill for itself.
