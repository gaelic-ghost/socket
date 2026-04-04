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
