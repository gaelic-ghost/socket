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
- `.claude-plugin/marketplace.json`
- `.agents/skills`
- `.claude/skills`

Codex install guidance to preserve in repo docs:

- repo-local packaged plugin surface: `plugins/<plugin-name>/`
- repo-local marketplace surface: `.agents/plugins/marketplace.json`
- personal Codex install surface lives outside the repo at `~/.codex/plugins/<plugin-name>` with `~/.agents/plugins/marketplace.json`
- repo bootstrap owns the repo-local structure; ongoing local Codex install and lifecycle workflows belong to `install-plugin-to-socket` or equivalent maintainer tooling

Claude plugin guidance to preserve in repo docs:

- local Claude development should point `claude --plugin-dir` at the tracked plugin source root
- if the repo itself should be shareable as a Claude marketplace, track a repo-root `.claude-plugin/marketplace.json`
- Claude marketplace relative paths resolve from the marketplace root and must stay inside that root

Git tracking guidance to preserve in repo docs:

- track canonical plugin source trees and shared marketplace catalogs in git
- do not track consumer-side install copies, caches, or machine-local runtime state
- include a shared `.gitignore` snippet that ignores accidental in-repo local install surfaces and Claude local-only settings

Required bootstrap outputs:

- root `skills/`
- plugin subtree under `plugins/<plugin-name>/`
- Codex plugin manifest
- Claude plugin manifest
- Claude marketplace catalog at repo root
- hooks scaffold
- maintainer docs
- `README.md`
- `AGENTS.md`
- `ROADMAP.md`
- `.gitignore` baseline with the shared local-runtime ignore snippet
- maintainer Python tooling guidance that installs `ruff` and `mypy` with `uv tool install`

This skill composes with `$skill-creator`:

- bootstrap this repo layout first
- then use `$skill-creator` to author or refine individual skills
