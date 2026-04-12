# AGENTS.md

## Repository Role

- This repository is the canonical source of truth for the shipped Python workflow skills.
- Treat `productivity-skills` as the default baseline maintainer layer for general repo docs and maintenance work; this repo is the narrower specialist layer when Python-specific behavior should change the workflow.
- Root `skills/` is the authored workflow surface.
- [`plugins/python-skills/`](./plugins/python-skills/) is the packaged plugin root used for Codex packaging and should remain a thin packaging layer rather than a second source-of-truth tree.

## Durable Skill Customization

- Global durable customization path for shipped skills: `~/.config/gaelic-ghost/python-skills/<skill-name>/customization.yaml`
- Repo-local override path: `.codex/profiles/<skill-name>/customization.yaml`
- Repo-local override files are user-local and must remain untracked.
- Built-in script defaults remain the canonical fallback when no profile exists or when bypass flags are used.

## Repo-specific Rules

- Keep direct skill-install guidance accurate alongside plugin installation. Users should be able to install one skill, several skills, or the full bundle from the shared `skills/` tree.
- Treat each skill's `SKILL.md` plus `agents/openai.yaml` as the canonical per-skill contract pair.
- Do not reintroduce maintained per-skill `README.md` files unless Gale explicitly restores that public-doc surface.
- Run repo validation with `uv run scripts/validate_repo_metadata.py` and `uv run pytest` before landing documentation or metadata changes.
