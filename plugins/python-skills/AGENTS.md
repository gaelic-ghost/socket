# AGENTS.md

This file is the Python Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `python-skills` is a monorepo-owned Socket child and the canonical source of truth for shipped Python workflow skills.
- Root [`skills/`](./skills/) is the authored workflow surface.
- The repo root is the Codex plugin root through [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).
- Treat `productivity-skills` as the default baseline maintainer layer for general repo-doc and maintenance work; use this repo when Python-specific behavior should materially change the workflow.

## Local Rules

- Match the `socket` shared semantic version exactly; use the Socket root release workflow for version inventory and bumps.
- Treat each skill directory's `SKILL.md` plus `agents/openai.yaml` as the canonical per-skill contract pair.
- Do not reintroduce a nested packaged plugin subtree for Codex.
- Do not reintroduce maintained per-skill `README.md` files unless Gale explicitly asks for that public-doc surface again.
- Keep user-facing and maintainer-facing Python command examples expressed with `uv`.
- Use [`scripts/validate_repo_metadata.py`](./scripts/validate_repo_metadata.py) and [`tests/test_validate_repo_metadata.py`](./tests/test_validate_repo_metadata.py) as the mechanical source of truth for metadata rules.

## Validation

```bash
uv run scripts/validate_repo_metadata.py
uv run pytest
uv run ruff check .
uv run mypy .
```
