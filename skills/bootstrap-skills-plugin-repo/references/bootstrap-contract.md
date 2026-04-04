# Bootstrap Contract

Use this skill when the repository itself needs structural setup or alignment.

Canonical authored surfaces:

- `skills/`
- skill-local `SKILL.md`
- skill-local `agents/openai.yaml`
- skill-local `scripts/`, `references/`, and `assets/`

Packaging and discovery mirrors:

- `plugins/<plugin-name>/`
- `.agents/plugins/marketplace.json`
- `.agents/skills`
- `.claude/skills`

Codex install guidance to preserve in repo docs:

- repo-local packaged plugin surface: `plugins/<plugin-name>/`
- repo-local marketplace surface: `.agents/plugins/marketplace.json`
- personal Codex install surface lives outside the repo at `~/.codex/plugins/<plugin-name>` with `~/.agents/plugins/marketplace.json`
- repo bootstrap owns the repo-local structure; ongoing local Codex install and lifecycle workflows belong to `install-plugin-to-socket` or equivalent maintainer tooling

Required bootstrap outputs:

- root `skills/`
- plugin subtree under `plugins/<plugin-name>/`
- Codex plugin manifest
- Claude plugin manifest
- hooks scaffold
- maintainer docs
- `README.md`
- `AGENTS.md`
- `ROADMAP.md`
- maintainer Python tooling guidance that installs `ruff` and `mypy` with `uv tool install`

This skill composes with `$skill-creator`:

- bootstrap this repo layout first
- then use `$skill-creator` to author or refine individual skills
